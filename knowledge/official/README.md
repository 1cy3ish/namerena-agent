# 官方资料收录

收录日期：2026-11-16。起点为 [Deep Mess 官方说明](https://deepmess.com/zh/namerena/)，同时收录其指向的 [游戏本体](https://deepmess.com/namerena/)。按维护者约定，这些属于当前版本；GitHub Pages 旧站是过时版本。官方说明构成最基础的知识，但不保证覆盖全部词条和机制。

## 本轮结果

- 11 个官方文档页面的正文快照，另保留首页的 `index.html` 别名。
- 68 个成功取得的资源地址，对应 66 份原始文件，共 3,745,769 字节；首页与 `index.html` 别名共用文件。包括游戏、对战页面、计算脚本、样式、图片、图标和语言包。
- 7 项属性、34 个说明页列出的技能、11 个 Boss、4 份官方语言包、66 个中文语言包中的括号词形。
- 术语总表目前有 84 条，其中语言包独有名称只收录文本证据，未补造机制。
- 1 个已记录的不可用地址；抓取队列已遍历完毕，没有因数量上限留下的待抓地址。

## 原文入口

| 页面 | 本地快照 | 收录重点 |
| --- | --- | --- |
| 官方首页 | [index.md](pages/index.md) | 游戏、属性技能、组队与社区入口 |
| 名字构成 | [naming.md](pages/naming.md) | 战队、装备、空格、字符与长度限制 |
| 属性 | [attribute.md](pages/attribute.md) | 攻、防、速、敏、魔、抗、智 |
| 技能 | [skill.md](pages/skill.md) | 分类、熟练度、技能效果和数值 |
| 特殊名字 | [special.md](pages/special.md) | Boss 与随机数种子 |
| 测号技巧 | [testing.md](pages/testing.md) | 搜索、实力评估、显示名和徽章 |
| 嵌入说明 | [api.md](pages/api.md) | iframe、输入编码与回调字段 |
| API 示例 | [api_test.md](pages/api_test.md) | 示例界面；调用逻辑另保存在原始 HTML |
| 自定义语言 | [custom_lan.md](pages/custom_lan.md) | 语言包、链接生成与 CORS |
| 关于 | [about.md](pages/about.md) | 作者、版权和第三方 API 使用条件 |
| 天梯 | [ladder.md](pages/ladder.md) | 页面外壳及前端资源；未取得实时排名 |

`pages/` 保留抓取后的正文；[pages.json](pages.json) 记录页面、来源 ID 和抓取标识。[原始资源目录](../../data/raw/official-namerena/deepmess.com) 保留 HTML、JavaScript、CSS、JSON、图片等原始字节并纳入 Git，不以正文快照替代代码或资源。

## 结构化知识

- [attributes.json](attributes.json)：7 项属性的说明原文。
- [skills.json](skills.json)：14 个攻击技能、11 个辅助技能、9 个被动技能，保留属性、伤害表达式、效果和触发条件。
- [special-names.json](special-names.json)：11 个 Boss 的完整输入、显示名、来源与特点。
- [input-rules.json](input-rules.json)：命名形式、输入限制、测试布局、种子与嵌入参数。
- [language-index.json](language-index.json)：4 份语言包的路径、消息键数量、哈希和中文词形。
- [术语总表](../glossary.json)：汇集基础概念、官方索引及先前整理的社区评分简称。

原文和结构化记录分层保存。比如说明页称“治愈术、幻影”，中文语言文本中出现“治愈魔法、幻术”；这些对应关系保留出处。附体、自爆、隐匿、死亡笔记、属性修改器等语言包名称，没有据此生成未经说明的属性或机制。

## 覆盖证据与已知缺口

[crawl-manifest.json](crawl-manifest.json) 记录每个 URL 的状态、原始路径、大小、SHA-256 与引用关系；[runtime-observation.json](runtime-observation.json) 记录全新浏览器加载及一次触发对战页面时发现的资源。对战触发用于发现延迟加载的 `fight.html`、计算脚本和样式，没有将该次观察作为胜率或引擎兼容性测试。

[coverage.json](coverage.json) 保留以下缺口：

- 中文语言包声明的 `/namerena/navigation.html` 返回 404，未取得正文。
- 天梯文档及前端资源已归档，本次未取得实时排名，也未登录。

页面或数据差异按原文保留：属性页“魔、抗”的部分措辞、嵌入说明中的旧站示例地址，以及实际示例源码中的本站地址，都没有静默改写。各语言包分别保存并计算哈希，不因文件大小相同而合并。

范围限定为已发现的官方页面及同源关联资源。站外站点和广告只记录链接；服务器上无公开引用的文件无法由此枚举。JavaScript 字符串中的构建时路径只列为候选，不当作必然存在的网络资源。此归档保留原始文件，没有改写为离线游戏，也不代表取得完整开发源码。上游的作者信息、内容版权和 API 使用声明保存在关于页面。

更新与校验命令见 [脚本说明](../../scripts/README.md)。工具项目与史料分别等待维护者在 [tools/](../tools/README.md)、[history/](../history/README.md) 提供材料后整理。
