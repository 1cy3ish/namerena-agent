"""Build searchable official records from the preserved HTML and language JSON."""

import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/official-namerena/deepmess.com"
OUTPUT = ROOT / "knowledge/official"
DATE = json.loads((OUTPUT / "crawl-manifest.json").read_text(encoding="utf-8"))["captured_at"][:10]


def write(name, value):
    (OUTPUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", "", value))).strip()


def main_content(name):
    text = (RAW / "zh/namerena" / name).read_text(encoding="utf-8")
    return text.split('<section id="main-content">', 1)[1].split("</section>", 1)[0]


def rows(name):
    return [[clean(cell) for cell in re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row, re.S)]
            for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", main_content(name), re.S)]


def base_record(record_id, name, source):
    return {"id": record_id, "name": name, "source_ids": [source], "checked_at": DATE}


def main():
    attributes = []
    attr_ids = dict(zip("攻防速敏魔抗智", ("attack", "defense", "speed", "agility", "magic", "resistance", "intelligence")))
    for name, section in re.findall(r"<h3\b[^>]*>(.*?)</h3>(.*?)(?=<h3|$)", main_content("attribute.html"), re.S):
        name = clean(name)
        attributes.append({**base_record("attribute-" + attr_ids[name], name, "official-attribute"),
                           "description": [clean(line) for line in re.findall(r"<li>(.*?)</li>", section, re.S)]})
    write("attributes.json", {"schema_version": "0.1", "notes": "按官方属性页提取；魔、抗段落中关于普通/物理攻击的原文措辞保留，未静默纠错。", "attributes": attributes})

    skill_ids = dict(zip(
        "连击 会心一击 火球术 冰冻术 雷击术 地裂术 吸血攻击 狂暴术 诅咒 净化 投毒 潜行 瘟疫 生命之轮 聚气 蓄力 魅惑 加速术 减速术 铁壁 治愈术 苏生术 血祭 幻影 分身 反击 防御 伤害反弹 守护 护身符 垂死抗争 护盾 召唤亡灵 吞噬".split(),
        "combo critical fire ice thunder quake absorb berserk curse purify poison stealth plague exchange accumulate charge charm haste slow iron heal revive summon shadow clone counter defend reflect protect reraise upgrade shield zombie merge".split()))
    skills = []
    category = None
    for row in rows("skill.html"):
        if not row:
            continue
        if row[0] in ("攻击技能", "辅助技能", "被动技能"):
            category = row[0]
            continue
        if category == "攻击技能" and len(row) == 1:
            skills[-1]["description"] = row[0]
            continue
        record = {**base_record("skill-" + skill_ids[row[0]], row[0], "official-skill"), "category": category}
        if category == "攻击技能":
            record.update(attribute=row[1], damage=row[2])
        elif category == "辅助技能":
            record["description"] = row[1]
        else:
            record.update(trigger=row[1], description=row[2])
        skills.append(record)
    write("skills.json", {"schema_version": "0.1", "notes": "保留官方表格分类、属性、数值和效果原文；不假定技能列表已覆盖游戏中的全部技能。", "skills": skills})

    bosses = []
    for row in rows("special.html"):
        if not row or row[0] == "输入的名字":
            continue
        bosses.append({**base_record("boss-" + row[0].split("@")[0], row[1], "official-special"),
                       "input": row[0], "origin": row[2], "description": row[3]})
    write("special-names.json", {"schema_version": "0.1", "notes": "官方页面列出的 Boss；seed:...@! 另属于不参战的随机数种子。", "special_team": "!", "bosses": bosses})

    languages = []
    chinese = None
    for name in ("zh", "en", "zh-TW", "zh-money"):
        file = RAW / "namerena/lang" / (name + ".json")
        content = file.read_bytes()
        strings = json.loads(content)
        if name == "zh":
            chinese = strings
        languages.append({"id": name, "url": "https://deepmess.com/namerena/lang/" + name + ".json",
                          "local_path": file.relative_to(ROOT).as_posix(), "key_count": len(strings),
                          "sha256": hashlib.sha256(content).hexdigest()})
    vocabulary = {}
    for key, value in chinese.items():
        for token in re.findall(r"\[([^\[\]]+)\]", value):
            if not token.isdigit():
                vocabulary.setdefault(token, []).append(key)
    write("language-index.json", {"schema_version": "0.1", "source_ids": ["official-language-zh", "official-custom_lan"],
                                  "notes": "完整语言字符串保存在原始 JSON；词形只证明在显示文本中出现，不构成机制定义。zh-TW 与 zh 的字节是否相同可通过哈希比较。",
                                  "languages": languages,
                                  "bracketed_terms": [{"term": term, "keys": keys} for term, keys in vocabulary.items()]})

    glossary_file = ROOT / "knowledge/glossary.json"
    glossary = json.loads(glossary_file.read_text(encoding="utf-8"))
    glossary["terms"] = [term for term in glossary["terms"] if term.get("origin") != "official-index"]
    for record, category, details in [(r, "attribute", "attributes.json") for r in attributes] + [(r, "skill", "skills.json") for r in skills] + [(r, "boss", "special-names.json") for r in bosses]:
        description = record["description"]
        if isinstance(description, list):
            description = " ".join(description)
        aliases = [record["input"]] if category == "boss" else []
        if record["name"] == "治愈术":
            aliases.append("治愈魔法")
        if record["name"] == "幻影":
            aliases.append("幻术")
        glossary["terms"].append({"id": record["id"], "term": record["name"], "aliases": aliases,
                                  "definition": description, "category": category, "status": "source_supported",
                                  "scope": "当前官方说明的基础记载；原文数值和完整字段见详情，不表示已独立实测或涵盖全部机制。",
                                  "source_ids": record["source_ids"] + (["official-language-zh"] if aliases and category == "skill" else []),
                                  "checked_at": DATE, "origin": "official-index", "details_path": "official/" + details, "details_id": record["id"]})
    for term, suffix in (("附体", "possess"), ("自爆", "explode"), ("隐匿", "hide"), ("死亡笔记", "death-note"), ("属性修改器", "attribute-modifier")):
        glossary["terms"].append({"id": "language-" + suffix, "term": term, "aliases": [],
                                  "definition": "官方中文语言包中出现的名称；当前只确认名称和对应消息键，未从官方说明中取得完整机制。",
                                  "category": "language-only", "status": "source_supported", "scope": "显示词汇证据，不能据此推断触发条件、获取方式或数值。",
                                  "source_ids": ["official-language-zh"], "checked_at": DATE, "origin": "official-index"})
    glossary_file.write_text(json.dumps(glossary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"attributes": len(attributes), "skills": len(skills), "bosses": len(bosses), "languages": len(languages), "language_terms": len(vocabulary), "glossary_terms": len(glossary["terms"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
