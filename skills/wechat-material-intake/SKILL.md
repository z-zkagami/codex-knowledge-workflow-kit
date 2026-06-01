---
name: wechat-material-intake
description: Use when the user wants to process today's tinkering notes or raw writing material into reusable article inputs, especially when they say things like “处理今天折腾素材”, “整理今天素材”, “从日记提炼 aha”, or want a cross-window default workflow for WeChat writing prep.
---

# Wechat Material Intake

把“今天折腾留下的一堆原始痕迹”整理成后续写公众号可复用的输入。

这个 skill 不负责直接写正文，主要负责把素材收口，避免每次都重讲提示词。

## When To Use

在下面这些场景直接使用：

- 用户说“处理今天折腾素材”
- 用户说“整理今天素材”
- 用户说“从今日日记提炼 aha”
- 用户贴来一段日记、命令、截图说明、AI 对话，想判断值不值得写
- 用户希望跨窗口沿用同一套素材整理默契

## Default Assumption

如果用户没有特别说明，默认素材来源优先按这个顺序找：

1. 用户刚贴进来的原始内容
2. 用户指定的某篇日记
3. 当天或最近一天的 `10_日记/YYYY/MM/YYYY-MM-DD.md`

## Workflow

1. 先把素材拆成四类：
   - 事实
   - 判断
   - 可给读者的小动作
   - 证据缺口
2. 判断素材更像哪一种：
   - 拿量型
   - 沉淀型
   - 搜索型
3. 提炼 `3` 个以内的 `aha` 点。
4. 明确哪些点还不能写，因为证据不够。
5. 给出一个最值得继续推进的方向，但停在“选题前”。

## Output Contract

输出默认按这 6 段来：

1. `素材摘要`
2. `事实 / 判断 / 小动作`
3. `Aha 点`
4. `更适合的内容类型`
5. `证据缺口`
6. `下一步最小动作`

## Guardrails

1. 不把素材硬写成文章。
2. 不替用户编造第一手经历。
3. 如果素材只够形成一个判断，不强行拔高成完整方法论。
4. 如果没有明确 `aha` 点，要明确说“先别写”。
5. 如果素材里有明显可落地的小动作，要优先指出，不要只停在抽象观点。

## Suggested Shortcuts

以后用户在任意窗口里，只要说下面任一句，默认都按本 skill 处理：

- `处理今天折腾素材`
- `整理今天素材`
- `从今日日记提炼 aha`
- `看看这段值不值得写成公众号`

## Companion Files

- `99_系统/模板/公众号素材采集速查卡.md`
- `99_系统/模板/Daily_Note.md`
- `60_内容中台/10_公众号/00_公众号工作台.md`
