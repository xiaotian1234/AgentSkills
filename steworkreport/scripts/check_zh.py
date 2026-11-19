#!/usr/bin/env python3
"""check_zh.py - 中文汇报的"STE 思路"粗略自查脚本。

ASD-STE100 本身是英语规范。这个脚本只是借它的思路，检查中文汇报里机器容易查的几件事：
  1. 每句的字数（默认上限 30 字，这是作者自己定的，不是 STE 的规定）
  2. 模糊词 / 套话（大概、基本、尽快、取得积极进展 等）
  3. 被动句（含"被"字）
  4. 一句里的分句数（逗号、顿号分隔），分句越多，越可能一句话塞了几件事

字数的算法：不含标点和空格；连续的数字或字母串算 1 个字（如 "80%" 算 1 个）。
它不是官方检查器，词表是经验性的，会有误报和漏报，请结合自己的判断使用。

用法：
  python3 check_zh.py report.txt
  python3 check_zh.py report.txt --limit 40
  cat report.txt | python3 check_zh.py -
"""
import argparse
import re
import sys

HEDGES = [
    "大概", "大约", "左右", "约", "基本", "整体", "总体", "有所", "一定程度", "一定",
    "适当", "酌情", "尽快", "及时", "有效", "积极", "持续", "推进", "相关", "若干",
    "一些", "可能", "或许", "争取", "随时", "比较", "较", "相应", "进一步", "如有",
    "稍微", "略有", "初步", "逐步", "陆续",
]
HEDGE_RE = re.compile("|".join(sorted(map(re.escape, HEDGES), key=len, reverse=True)))
VOICE_RE = re.compile(r"被")
TOKEN_RE = re.compile(r"[一-鿿]|[A-Za-z0-9]+(?:[.%][A-Za-z0-9]+)*%?")
END_RE = re.compile(r"(?<=[。！？；])")


def count_words(sentence):
    """字数：汉字各算 1；连续数字/字母串算 1；不含标点。"""
    return len(TOKEN_RE.findall(sentence))


def count_clauses(sentence):
    parts = [p for p in re.split(r"[，、,]", sentence) if TOKEN_RE.search(p)]
    return max(len(parts), 1)


def find_issues(sentence):
    found = [("hedge", m.start(), m.end()) for m in HEDGE_RE.finditer(sentence)]
    found += [("voice", m.start(), m.end()) for m in VOICE_RE.finditer(sentence)]
    found.sort(key=lambda t: (t[1], -(t[2] - t[1])))
    result, last_end = [], -1
    for kind, s, e in found:
        if s >= last_end:
            result.append((kind, s, e))
            last_end = e
    return result


def parse(text):
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
        if not re.search(r"[。！？；]$", line) and len(line) <= 24:
            items.append({"type": "heading", "text": line})
            continue
        sentences = [s.strip() for s in END_RE.split(line) if s.strip()]
        items.append({"type": "line", "marker": marker, "sentences": sentences})
    return items


def analyze(text, limit=30):
    rows = []
    for item in parse(text):
        if item["type"] != "line":
            continue
        for s in item["sentences"]:
            issues = find_issues(s)
            n = count_words(s)
            rows.append({
                "text": s,
                "words": n,
                "clauses": count_clauses(s),
                "too_long": n > limit,
                "hedges": [s[a:b] for k, a, b in issues if k == "hedge"],
                "voice": [s[a:b] for k, a, b in issues if k == "voice"],
                "contractions": [],
            })
    return rows


def summarize(rows):
    return {
        "sentences": len(rows),
        "longest": max((r["words"] for r in rows), default=0),
        "too_long": sum(r["too_long"] for r in rows),
        "hedges": sum(len(r["hedges"]) for r in rows),
        "voice": sum(len(r["voice"]) for r in rows),
        "max_clauses": max((r["clauses"] for r in rows), default=0),
    }


def main():
    ap = argparse.ArgumentParser(description="中文汇报的 STE 思路粗略自查（非官方）")
    ap.add_argument("file", help="文本文件，或 - 表示标准输入")
    ap.add_argument("--limit", type=int, default=30, help="每句字数上限，默认 30（作者设定）")
    args = ap.parse_args()
    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    rows = analyze(text, args.limit)
    for i, r in enumerate(rows, 1):
        flags = []
        if r["too_long"]:
            flags.append(f"超过{args.limit}字")
        if r["clauses"] > 3:
            flags.append(f"{r['clauses']}个分句")
        if r["hedges"]:
            flags.append("模糊/套话：" + "、".join(r["hedges"]))
        if r["voice"]:
            flags.append("被动：" + "、".join(r["voice"]))
        mark = "!!" if flags else "ok"
        print(f"{i:>2} {mark} {r['words']:>3}字  {r['text'][:36]}")
        if flags:
            print(f"        {'；'.join(flags)}")
    s = summarize(rows)
    print("-" * 60)
    print(f"句数={s['sentences']}  最长={s['longest']}字  超限句={s['too_long']}  "
          f"模糊/套话={s['hedges']}  被动={s['voice']}  最多分句={s['max_clauses']}")
    print("提示：粗略检查，词表是经验性的，请结合自己的判断。")
    sys.exit(1 if (s["too_long"] or s["hedges"] or s["voice"]) else 0)


if __name__ == "__main__":
    main()
