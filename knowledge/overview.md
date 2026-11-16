# 名字竞技场基础概览

检索日期：2026-11-16。这是初始化时的快速资料梳理，尚未进行游戏实测或社区访谈。来源 ID 对应 [sources.json](sources.json)。

## 游戏与玩法

名字竞技场（Namerena）是一款文字对战游戏，也是 MD5 大作战的续作。玩家输入多个名字后，程序自动演算战斗。同一个名字关联相同的属性和技能；官方说明将相同输入下的战斗描述为可重复的结果。讨论复现时仍需保持游戏版本、完整输入和分组等条件一致。[官方说明 / official-guide](https://deepmess.com/zh/namerena/)

通常每行输入一个名字进行混战，名字之间加入空行可以分组进行队战。输入中的空行是有意义的，不能当作普通排版随意删除。[官方说明 / official-guide](https://deepmess.com/zh/namerena/)

官方命名文档列出 `名字`、`名字@战队名`、`名字+装备`、`名字@战队名+装备` 四种形式。名字或战队名发生变化会改变属性；战斗中的简化显示名不一定等于完整计算输入。`@战队名` 也不等于空行定义的对战分组。[名字构成 / official-naming](https://deepmess.com/zh/namerena/naming.html)

“测号”指搜索或评估名字。官方说明提供 `!test!` 入口，并区分名字搜索和实力评估两种输入布局。具体限制和评分结论需要结合目标版本核对，不直接把文档中的强号分数阈值视为当前社区标准。[测号技巧 / official-testing](https://deepmess.com/zh/namerena/testing.html)

## 入口与版本

| 入口 | 本次看到的情况 | 使用方式 |
| --- | --- | --- |
| [Deep Mess 文档](https://deepmess.com/zh/namerena/) | 官方玩法、规则与开发者文档入口 | 基础知识的优先来源 |
| [Deep Mess 游戏入口](https://deepmess.com/namerena) | 官方说明页指向此地址 | 本次未对游戏运行结果进行验证 |
| [GitHub Pages 旧站](https://namerena.github.io/) | 页面仍能读取 | 不据此假定与 Deep Mess 版本一致 |
| [社区 Wiki 教程](https://namerena.fandom.com/zh/wiki/名字竞技场教程) | 包含术语、历史与工具线索，也明确提示教程部分停用 | 作为社区语料线索，带上历史范围与待确认说明 |

Wiki 教程将 GitHub Pages 地址列为旧入口，并说明其评分及对战结果不再具有该教程所称的正式效力。这是社区页面的表述，不能替代具体赛事规则或对每个镜像版本的核验。[社区教程 / community-tutorial](https://namerena.fandom.com/zh/wiki/名字竞技场教程)

## 初始术语范围

[术语表](glossary.json) 先收录“名竞、号、测号、战队、普评、强评、普单、强单、粗评、精评”。其中评分简称按社区教程的语境记录，仅解释名称与基本用途；算法、样本、工具版本及具体分数的可比性仍待补充。[官方测号文档](https://deepmess.com/zh/namerena/testing.html)、[社区教程](https://namerena.fandom.com/zh/wiki/名字竞技场教程)

Wiki 中的历史称号、当前最强名字、榜单和强度评价暂不录为当前事实，尤其不直接采用已经被页面标为作废的旧称号阈值。

## 给工具开发者的线索

官方嵌入文档描述了网页集成方式：将名字输入编码到 iframe URL 的 `#n=` 参数，利用 `postMessage` 接收结果；文档列出 `winners` 和 `all` 两个回调字段。该页示例仍使用 GitHub Pages 旧地址，尚未验证其在目标版本上的兼容性。这些是浏览器嵌入说明，当前没有由本次检索确认的独立 HTTP 对战服务或 MCP 接口。[网页嵌入文档 / official-embedding](https://deepmess.com/zh/namerena/api.html)

后续实现工具时，应先核对目标站点和版本、完整输入的编码方式、消息来源校验与返回字段，再封装能力。

## 待核实

- 目标社区采用的游戏版本、赛事规则和评分工具版本。
- 社区黑话在当前使用中的释义、别名、歧义和例句。
- 现有测号、评分、模拟和工具项目的仓库、许可证与接入方式。
- 旧文档与现行游戏的差异，以及可重复的最小实测样例。
