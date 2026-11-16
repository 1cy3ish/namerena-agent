# 名字竞技场基础概览

整理日期：2026-11-16。完整官方收录见 [official/README.md](official/README.md)，来源 ID 对应 [sources.json](sources.json)。

## 版本与收录范围

维护者确认：GitHub Pages 旧站是过时版本，其余此前讨论的入口按最新版本处理。旧资料仍需收录；现已提供 tswn-core 重写仓库，其他工具与独立史料等维护者后续提供。[维护者约定](project-context.json)

Deep Mess 的 [官方说明](https://deepmess.com/zh/namerena/) 与其链接的 [游戏本体](https://deepmess.com/namerena/) 是本轮收录对象。官方词条构成最基础的知识，不假定说明页覆盖全部机制。页面保留的旧链接作为原文证据，不据此把整个页面归为旧版本。

## 游戏与输入

名字竞技场（Namerena）是 MD5 大作战的文字对战续作。输入名字后由程序自动演算战斗；名字关联固定属性和技能，相同条件下结果可重复。每行一个名字，空行划分本局队伍。[官方说明](https://deepmess.com/zh/namerena/)

命名包括 `名字`、`名字@战队名`、`名字+装备`、`名字@战队名+装备`。战队名参与属性生成并影响徽章，与空行定义的对战队伍不是同一概念。空格后的名字部分在战斗中不显示，但仍是完整输入的一部分。[命名规则](https://deepmess.com/zh/namerena/naming.html)

## 属性、技能与特殊名字

- 官方属性页解释攻、防、速、敏、魔、抗、智七项属性。完整字段见 [属性索引](official/attributes.json)，原文个别措辞按来源保留。
- 技能页列出 14 个攻击技能、11 个辅助技能、9 个被动技能，以及技能熟练度概念。效果、伤害和触发条件见 [技能索引](official/skills.json)。34 项是页面列出的范围，不是游戏全部技能数量的断言。
- 特殊名字页列出 11 个 Boss，特殊战队名为 `!`。`seed:` 开头并处于 `!` 战队的输入是随机数种子，不参战，只改变战斗过程。完整输入和特点见 [特殊名字索引](official/special-names.json)。

以上分别来自 [属性说明](https://deepmess.com/zh/namerena/attribute.html)、[技能说明](https://deepmess.com/zh/namerena/skill.html) 和 [特殊名字](https://deepmess.com/zh/namerena/special.html)。

## 测号与评分

官方 `!test!` 同时支持名字搜索和实力评估，使用不同输入布局。搜索说明包括 `???` 替换为数字的形式；评估说明包括测试进度和评分。原始布局及数值保存在 [测号页面快照](official/pages/testing.md)，引用时明确是官方记载。[测号技巧](https://deepmess.com/zh/namerena/testing.html)

普评、强评、普单、强单及 pp、qp、pd、qd 的社区用语保留来源，现又补充了 tswn 的实际分派和 profile 布局。它们与 cqd/cqp 具体靶子集胜率、pair 头部评分分开，详见 [tswn 评分](tools/tswn-core/ratings.json)。历史变迁仍等维护者补充。[术语表](glossary.json)

## 语言包与开发入口

官方语言包原始 JSON 和 [词形索引](official/language-index.json) 继续保留。官方说明未展开的附体、自爆、隐匿等名称，现通过 [tswn 机制](tools/tswn-core/mechanics.md) 补充了有源码依据的解释，适用范围明确限定为该实现。[自定义语言](https://deepmess.com/zh/namerena/custom_lan.html)

官方嵌入方式使用 iframe、URL 的 `#n=` 参数和 `postMessage`，文档列出 `winners` 与 `all` 字段。说明页示例仍含旧站地址，但 [实际 API 示例页源码](https://deepmess.com/zh/namerena/api_test.html) 使用本站 `/namerena/index.html#n=`。原文与示例分别保留，不相互覆盖。[嵌入说明](https://deepmess.com/zh/namerena/api.html)

[关于页面](https://deepmess.com/zh/namerena/about.html) 中的作者信息、内容版权和第三方 API 使用条件已随原文归档。当前项目未实现 HTTP 对战服务或 MCP server。

tswn 已提供实际的 Rust 引擎、CLI 和 WASM 规范 BattleSession。其网页分享使用 `?input=`，与原站 `#n=` 分开；接入和已检查的部署入口见 [网页说明](tools/tswn-core/web.md)。本知识仓库尚未将这些能力封装为 MCP 工具。

## 抓取覆盖

正文快照覆盖官方目录发现的页面，另保存游戏本体、运行时发现的对战页面、脚本、CSS、图片和语言包。状态、SHA-256 与链接关系见 [抓取清单](official/crawl-manifest.json)。

天梯页面已收录，本次取得页面和前端资源，没有实时排名数据。站外广告与外链只记录地址；未公开链接的服务器文件无法据此枚举。资源归档没有改写成离线游戏，也不代表取得完整开发源码。
