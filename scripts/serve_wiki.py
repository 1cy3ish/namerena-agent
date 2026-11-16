"""Build and serve the static wiki on loopback, using only the standard library."""

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from build_wiki import build


class PreviewHandler(SimpleHTTPRequestHandler):
    # Windows registry MIME mappings can otherwise serve ES modules as text/plain.
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".mjs": "text/javascript",
                      ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, "Not found")
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765, help="Local port (default: 8765)")
    args = parser.parse_args()
    output = build()
    handler = functools.partial(PreviewHandler, directory=str(output))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        parser.exit(1, f"Cannot start local wiki: {error}. Try --port 8766.\n")
    print(f"Namerena Wiki: http://127.0.0.1:{server.server_port}/", flush=True)
    print("Press Ctrl+C to stop. After changing knowledge or web files, restart to rebuild.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
