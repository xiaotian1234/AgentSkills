# 英文汇报规则

用户要求英文汇报，或汇报对象读英文时使用。结构与中文版相同，小节标题改用英文。

## 输出结构

按此顺序，每个小节用加粗的小标题；记录里没有的内容，省略该小节：

- **Status**：先写结论和进度数字。
- **Cause**：只写事实和原因。
- **Risk**：每个风险一段：是什么、影响什么、什么时候。
- **Decision needed by <date>**：每个选项写：做什么、代价、结果。最后写 "Recommendation: ..."。
- **Next steps**：每条写：谁、做什么、哪一天。

## 写作规则

按下面的英文规则写英文汇报（它们对应 ASD-STE100 的写法思路，但不等于逐条合规）。

1. Maximum 20 words in each sentence that gives an instruction or an action.
   Maximum 25 words in each descriptive sentence.
   Split a long sentence. Do not delete facts.
2. One instruction or one fact in each sentence.
3. One topic in each paragraph. Maximum 6 sentences in each paragraph.
4. Use the active voice. Put the subject first. Say who does what.
5. Use only simple present, simple past, and simple future.
   Do not use -ing forms as tenses.
   Do not use have/has/had perfect tenses.
   Do not use would, might, or could to soften a sentence.
6. One word, one meaning. Use one name for one thing in the whole report.
   Example: always write "cutover". Do not change it to "switch" or "go-live".
   Prefer simple words: use, start, stop, need, make, before, after, because.
7. Do not use idioms or phrasal verbs (touch base, roll out, circle back, follow up).
8. Do not omit words. Keep the articles (the, a, an). Do not use contractions.
   Do not stack more than 3 nouns.
9. Use numbers, units, and dates. Do not use soon, some, a few, approximately, significant.
   Write dates as "12 October".
10. If a fact is not certain, write it as its own sentence.
    Example: "The cause is not confirmed." Give the date of confirmation.
11. Do not write filler or feelings: "good progress", "basically", "overall",
    "we are happy to discuss".
12. Do not delete facts. Keep every number, date, name, cost, and deadline.
    If the notes do not have a fact, write [TO CONFIRM: ...]. Do not guess.

## 自检

把英文正文存成文本文件，运行 `python3 scripts/check_en.py <文件>`。默认句长上限是 20 词；描述性句子可加 `--limit 25`。
处理方式与中文版相同：拆句、换成数字和日期、改成主动语态。脚本只是提醒，不是判决，也不检查 ASD-STE100 核准词典。

## 输出示例

```text
**Status**
The migration of the order database is 80% complete. The project is 3 days late.

**Cause**
The index rebuild took 5 days. The plan was 2 days.

**Risk**
The sales promotion starts on 20 October. The cutover must end before this date. A late cutover puts the promotion at risk.

**Decision needed by 12 October**
- Option A: Add 2 engineers. This costs 6 person-days. The cutover date does not change.
- Option B: Move the cutover to 27 October. The promotion then runs on the old server.

Recommendation: Option A.

**Next steps**
1. Zhang Wei completes the index check on 9 October.
2. Li Na does the rollback test on 12 October.
```
