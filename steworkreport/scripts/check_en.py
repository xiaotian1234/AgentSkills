#!/usr/bin/env python3
"""check_en.py - 一个粗略的 "STE 风格" 自查脚本。

它只检查几件机器容易查的事：
  1. 每句的词数（默认上限 20，描述性文字可用 --limit 25）
  2. 模糊词 / 软化词 / 套话（approximately, might, soon ...）
  3. 被动语态、进行时、完成时（粗略启发式）
  4. 缩写（don't, it's ...）

它【不是】官方 ASD-STE100 检查器，不检查核准词典，也不判断词义。
想做正式合规检查，请使用商业工具并对照官方文档（asd-ste100.org）。

用法：
  python3 check_en.py report.txt
  python3 check_en.py report.txt --limit 25
  cat report.txt | python3 check_en.py -
"""
import argparse
import re
import sys

HEDGES = [
    "approximately", "around", "roughly", "about", "might", "may", "could",
    "would", "possibly", "potentially", "perhaps", "basically", "overall",
    "slightly", "somewhat", "some", "various", "several", "a few", "kind of",
    "soon", "asap", "timely", "good progress", "positive", "significant",
    "additional", "at your convenience", "happy to", "due to the fact that",
    "in order to", "going forward", "touch base", "follow up", "following up",
    "circle back", "leverage", "roll out", "previously anticipated",
]

BE = r"(?:is|are|was|were|be|been|being|am)"
IRREGULAR = r"(?:done|made|taken|given|written|built|run|shown|known|set|put|kept|held|found|sent|seen|chosen|begun)"

PATTERNS = {
    "voice": [
        re.compile(rf"\b{BE}\s+(?:\w+ly\s+)?(?:\w+ed|{IRREGULAR})\b", re.I),   # passive
        re.compile(rf"\b{BE}\s+(?:\w+ly\s+)?\w+ing\b", re.I),                    # progressive
        re.compile(r"\b(?:has|have|had)\s+(?:\w+ly\s+)?(?:been|\w+ed|done|made|taken|given)\b", re.I),  # perfect
    ],
    "contraction": [
        re.compile(r"\b\w+(?:n't|'re|'ve|'ll|'d|'m)\b", re.I),
        re.compile(r"\b(?:it|that|there|he|she|what|let)'s\b", re.I),
    ],
}
HEDGE_RE = re.compile(r"\b(?:" + "|".join(re.escape(h) for h in sorted(HEDGES, key=len, reverse=True)) + r")\b", re.I)
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’%\-/.:][A-Za-z0-9]+)*%?")


def count_words(sentence):
    return len(WORD_RE.findall(sentence))


def find_issues(sentence):
    """Return a sorted, non-overlapping list of (kind, start, end)."""
    found = [("hedge", m.start(), m.end()) for m in HEDGE_RE.finditer(sentence)]
    for kind, regexes in PATTERNS.items():
        for rx in regexes:
            found += [(kind, m.start(), m.end()) for m in rx.finditer(sentence)]
    found.sort(key=lambda t: (t[1], -(t[2] - t[1])))
    result, last_end = [], -1
    for kind, s, e in found:
        if s >= last_end:
            result.append((kind, s, e))
            last_end = e
    return result


def parse(text):
    """Split text into headings and lines of sentences."""
    items = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        marker = ""
        m = re.match(r"^(?:([-*])|(\d+[.)]))\s+", line)
        if m:
            marker = m.group(1) or m.group(2)
            line = line[m.end():]
        line = line.replace("**", "").replace("`", "").strip()
        if not re.search(r"[.!?]$", line) and len(line.split()) <= 10:
            items.append({"type": "heading", "text": line})
            continue
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", line)
        items.append({"type": "line", "marker": marker, "sentences": sentences})
    return items


def analyze(text, limit=20):
    rows = []
    for item in parse(text):
        if item["type"] != "line":
            continue
        for s in item["sentences"]:
            issues = find_issues(s)
            rows.append({
                "text": s,
                "words": count_words(s),
                "too_long": count_words(s) > limit,
                "hedges": [s[a:b] for k, a, b in issues if k == "hedge"],
                "voice": [s[a:b] for k, a, b in issues if k == "voice"],
                "contractions": [s[a:b] for k, a, b in issues if k == "contraction"],
            })
    return rows


def summarize(rows):
    return {
        "sentences": len(rows),
        "longest": max((r["words"] for r in rows), default=0),
        "too_long": sum(r["too_long"] for r in rows),
        "hedges": sum(len(r["hedges"]) for r in rows),
        "voice": sum(len(r["voice"]) for r in rows),
        "contractions": sum(len(r["contractions"]) for r in rows),
    }


def main():
    ap = argparse.ArgumentParser(description="Rough STE-style self-check (not an official checker).")
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--limit", type=int, default=20, help="max words per sentence (20 for steps, 25 for descriptions)")
    args = ap.parse_args()
    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    rows = analyze(text, args.limit)
    for i, r in enumerate(rows, 1):
        flags = []
        if r["too_long"]:
            flags.append(f"LONG>{args.limit}")
        if r["hedges"]:
            flags.append("HEDGE:" + ",".join(r["hedges"]))
        if r["voice"]:
            flags.append("VOICE:" + ",".join(r["voice"]))
        if r["contractions"]:
            flags.append("CONTR:" + ",".join(r["contractions"]))
        mark = "!!" if flags else "ok"
        print(f"{i:>2} {mark} {r['words']:>3}w  {r['text'][:70]}")
        if flags:
            print(f"        {'; '.join(flags)}")
    s = summarize(rows)
    print("-" * 60)
    print(f"sentences={s['sentences']}  longest={s['longest']}w  over-limit={s['too_long']}  "
          f"hedges={s['hedges']}  voice={s['voice']}  contractions={s['contractions']}")
    print("Note: rough check only. It does not check the ASD-STE100 dictionary.")
    sys.exit(1 if (s["too_long"] or s["hedges"] or s["voice"] or s["contractions"]) else 0)


if __name__ == "__main__":
    main()
