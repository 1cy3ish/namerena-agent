"""Archive the linked official documentation, game and same-origin assets.

Uses only the Python standard library. Original bytes remain in data/raw/;
the tracked manifest records provenance, hashes, links and unsuccessful fetches.
This is a source archive, not an offline-compatible or modified game build.
"""

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

ORIGIN = "https://deepmess.com"
PREFIXES = ("/zh/namerena/", "/namerena/")
EXTENSIONS = r"(?:m?js|css|wasm|json|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf|mp3|ogg|wav|txt|md|html|bin|dart)"
LITERAL_FILE = re.compile(r"[\"'`]([^\"'`\s<>]+?\." + EXTENSIONS + r"(?:\?[^\"'`\s<>]*)?)[\"'`]")
CSS_URL = re.compile(r"url\(\s*[\"']?([^\"'\s)]+)")
SEEDS = [ORIGIN + "/zh/namerena/", ORIGIN + "/namerena/"] + [
    ORIGIN + "/zh/namerena/" + name + ".html"
    for name in ("index", "attribute", "skill", "naming", "special", "testing",
                 "api", "api_test", "custom_lan", "about", "ladder")
]


def normalize(value, base=ORIGIN):
    value = unescape(value.strip()).replace("\\/", "/")
    url = urllib.parse.urlsplit(urllib.parse.urljoin(base, value))
    if url.scheme not in ("http", "https") or not url.hostname:
        return None
    if url.username or url.password:
        return None
    scheme = "https" if url.hostname == "deepmess.com" else url.scheme
    path = url.path or "/"
    if url.hostname == "deepmess.com" and path in ("/namerena", "/zh/namerena"):
        path += "/"
    return urllib.parse.urlunsplit((scheme, url.netloc, path, "", ""))


def in_section(url):
    parsed = urllib.parse.urlsplit(url)
    return parsed.netloc == "deepmess.com" and parsed.path.startswith(PREFIXES)


def should_fetch(url, kind):
    same_origin = urllib.parse.urlsplit(url).netloc == "deepmess.com"
    return kind != "literal-candidate" and (in_section(url) or (
        same_origin and kind in ("resource", "module-resource", "language-resource")))


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "base" and attrs.get("href"):
            self.refs.append((attrs["href"], "base"))
        if tag in ("a", "area") and attrs.get("href"):
            self.refs.append((attrs["href"], "navigation"))
        if tag == "link" and attrs.get("href"):
            self.refs.append((attrs["href"], "resource"))
        if tag in ("script", "img", "source", "audio", "video", "iframe", "embed", "input"):
            for attr in ("src", "poster", "data-src"):
                if attrs.get(attr):
                    self.refs.append((attrs[attr], "resource"))
            for part in attrs.get("srcset", "").split(","):
                if part.strip():
                    self.refs.append((part.strip().split()[0], "resource"))
        if attrs.get("style"):
            self.refs.extend((value, "resource") for value in CSS_URL.findall(attrs["style"]))


def discover(content, content_type, url):
    text = content.decode("utf-8", errors="replace")
    refs = []
    base = url
    if "json" in content_type:
        try:
            values = json.loads(text)
            if isinstance(values, dict) and isinstance(values.get("navigationLink"), str):
                refs.append((values["navigationLink"], "navigation", ORIGIN + "/namerena/"))
        except json.JSONDecodeError:
            pass
    if "markdown" in content_type:
        for marker, value in re.findall(r"(!?)\[[^\]]*\]\(([^)]+)\)", text):
            refs.append((value, "resource" if marker else "navigation", base))
    if "html" in content_type:
        parser = References()
        parser.feed(text)
        for value, kind in parser.refs:
            if kind == "base":
                base = urllib.parse.urljoin(url, value)
        refs.extend((value, kind, base) for value, kind in parser.refs if kind != "base")
        # Language examples encode an additional resource inside the ?l= parameter.
        for value, _kind in parser.refs:
            linked = urllib.parse.urljoin(base, value)
            for language in urllib.parse.parse_qs(urllib.parse.urlsplit(linked).query).get("l", []):
                refs.append((language, "language-resource", linked))
    if "html" in content_type:
        # Do not reinterpret ordinary anchors as resource references.
        inline_scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", text, re.S | re.I)
        for script in inline_scripts:
            refs.extend((value, "literal-candidate", base) for value in LITERAL_FILE.findall(script))
            for value in re.findall(r"\.src\s*=\s*[\"']([^\"']+)[\"']", script):
                refs.append((value, "resource", base))
    elif "javascript" in content_type:
        # Build-time source names and map keys are not necessarily runtime URLs.
        refs.extend((value, "literal-candidate", base) for value in LITERAL_FILE.findall(text))
        for value in re.findall(r"(?:from\s*|import\s*\(?\s*)[\"']([^\"']+)[\"']", text):
            if value.startswith((".", "/")):
                refs.append((value, "module-resource", base))
    if any(kind in content_type for kind in ("html", "javascript", "css")):
        refs.extend((value, "resource", base) for value in CSS_URL.findall(text))
    return refs


def local_path(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path).lstrip("/")
    parts = Path(path).parts
    if any(part in ("..", ".") or ":" in part for part in parts):
        raise ValueError("Unsafe archive path: " + path)
    return Path("deepmess.com") / path / "index.html" if path.endswith("/") else Path("deepmess.com") / path


def fetch_once(url, timeout):
    started = time.monotonic()
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "namerena-agent-source-archive/0.1"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()
            return {
                "url": url, "final_url": response.url, "status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
                "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content),
                "content": content,
            }
    except (OSError, urllib.error.URLError) as error:
        return {"url": url, "status": getattr(error, "code", None), "error": str(error),
                "elapsed_seconds": round(time.monotonic() - started, 2)}


def fetch(url, timeout):
    for attempt in range(2):
        result = fetch_once(url, timeout)
        if "error" not in result or (result["status"] and result["status"] < 500):
            return result
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/raw/official-namerena"))
    parser.add_argument("--manifest", type=Path, default=Path("knowledge/official/crawl-manifest.json"))
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--reuse", action="store_true", help="Reuse archived bytes when their recorded SHA-256 matches")
    parser.add_argument("--runtime-log", type=Path, default=Path("knowledge/official/runtime-observation.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    pending = set(SEEDS)
    runtime_log = root / args.runtime_log
    if runtime_log.exists():
        observed = json.loads(runtime_log.read_text(encoding="utf-8"))
        for request in observed.get("requests", []):
            url = normalize(request["url"])
            if url and request.get("method") == "GET" and urllib.parse.urlsplit(url).netloc == "deepmess.com":
                pending.add(url)
    seeds = sorted(pending)
    previous = root / args.manifest
    cached = {}
    if args.reuse and previous.exists():
        cached = {item["url"]: item for item in json.loads(previous.read_text(encoding="utf-8"))["files"]}

    def read_or_fetch(url):
        old = cached.get(url)
        if old and old.get("local_path"):
            file = root / old["local_path"]
            if file.exists():
                content = file.read_bytes()
                if hashlib.sha256(content).hexdigest() == old["sha256"]:
                    return {**old, "content": content}
        return fetch(url, args.timeout)

    seen = set()
    records = []
    links = set()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        while pending and len(seen) < args.max_files:
            batch = sorted(pending)[:min(args.workers, args.max_files - len(seen))]
            pending.difference_update(batch)
            seen.update(batch)
            for record in executor.map(read_or_fetch, batch):
                content = record.pop("content", None)
                if content is not None:
                    relative = local_path(record["url"])
                    destination = (output / relative).resolve()
                    if not destination.is_relative_to(output):
                        raise ValueError("Archive escaped output directory")
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(content)
                    record["local_path"] = destination.relative_to(root).as_posix()
                    for raw, kind, base in discover(content, record["content_type"], record["final_url"]):
                        target = normalize(raw, base)
                        if not target:
                            continue
                        allowed = should_fetch(target, kind)
                        links.add((record["url"], raw, target, kind, allowed))
                        if allowed and target not in seen:
                            pending.add(target)
                records.append(record)
                print(json.dumps({key: record.get(key) for key in ("url", "status", "bytes", "error")}, ensure_ascii=False), flush=True)
    manifest = {
        "schema_version": "0.1",
        "captured_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds"),
        "seeds": seeds,
        "scope": {
            "page_prefixes": list(PREFIXES), "same_origin_referenced_assets": True,
            "external_sites": "record_links_only", "query_variants": "deduplicated; l parameter resources extracted",
            "discovery": "HTML references, CSS URLs, module imports and optional observed runtime GET requests; other JavaScript file literals are inventoried as unconfirmed candidates",
            "limits": "Does not enumerate unlinked server files or execute computed dynamic requests. Raw bytes are not rewritten for offline play.",
        },
        "summary": {
            "downloaded": sum("local_path" in item for item in records),
            "unique_files": len({item["local_path"] for item in records if "local_path" in item}),
            "unique_bytes": sum({item["local_path"]: item["bytes"] for item in records if "local_path" in item}.values()),
            "failed": sum("error" in item for item in records),
            "bytes": sum(item.get("bytes", 0) for item in records),
            "pending_due_to_limit": len(pending),
        },
        "files": sorted(records, key=lambda item: item["url"]),
        "links": [dict(zip(("from_url", "reference", "url", "kind", "in_scope"), row)) for row in sorted(links)],
        "pending": sorted(pending),
    }
    manifest_path = root / args.manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest["summary"], ensure_ascii=False))
    return 1 if pending or manifest["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
