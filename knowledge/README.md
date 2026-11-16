# 共享知识

`overview.md` 保存入门概览；`glossary.json` 保存结构化术语；`sources.json` 保存引用来源，供 skill、agent、MCP 和后续检索服务共同使用。

[官方资料](official/README.md) 包含正文快照、属性、技能、特殊名字、语言包词汇索引与抓取清单。[tswn 重写与工具](tools/tswn-core/README.md) 补充实现、评分、别名和网页接入。[维护者约定](project-context.json) 记录版本及范围。[PBB7 测号器](tools/pbb-new2/terminology.json) 与 [DataStructure4](tools/datastructure4/terminology.json) 为委托方指定工具的术语入口；[教程与社区史料](community/tutorials-and-history/terminology.json) 收录新旧教程、贴吧与论坛定项阅读产出；[QQ 群 bot](community/qq-bots/terminology.json) 收录群 bot 生态。委托方附件归档于 `data/raw/provided/`。

[民间天梯与论坛](community/ladder-forum/README.md) 保存社区称呼、赛事、协作和工具关键词。观察摘要记录页面、帖子楼号和读取范围，不作为全站镜像或永久活动政策。

## 来源

每条来源使用稳定的 `id`，记录标题、URL 或本地材料路径、类型、日期、读取状态和适用范围。`read_status: retrieved` 表示读取了页面，不表示内容已经独立实测。官方原始文件保存在 `data/raw/official-namerena/`，SHA-256 与关联链接见抓取清单。

## 术语

每个术语包含：

- `id`：稳定英文标识；`term`：常用名称；`aliases`：别名或缩写。
- `definition`：结合名字竞技场语境的简短解释。
- `detailed_description`：可直接用于问答的详细中文正文；大多数实质词条必备，包含机制、数值出处、版本语境与待核实项。简单标签/纯称呼允许省略。
- `outdated`：独立布尔标记，`true` 表示历史内容、已废弃或极少使用；与是否有来源、是否待核实分开。已确认过时：旧天梯（historical-ladder-name）、粗评（rough-evaluation）、精评（refined-evaluation）；其余条目过时与否见正文依据。
- `category`：概念、玩法、输入规则或评分。
- `status`：`source_supported` 表示有来源支持这项释义；`unverified` 表示尚待核实。
- `source_ids`：指向来源目录的 ID；`checked_at`：核查日期。版本、年代与条件写在正文及 `context_notes`，不设词条级 `scope` 栏。

有来源支持不等于当前社区已达成共识。不同年代或群体的定义冲突可新增独立词条，标注语境。新旧版本都在收录范围内。问答中保留名字、战队名和输入字符，避免改写改变角色或对战条件。

`origin: official-index` 的词条由 `scripts/build_official_index.py` 从归档生成，完整字段见 `details_path` 和 `details_id`，其他词条为人工整理。语言包独有词汇与完整机制定义分开记录。

`origin: tswn-curation` 和 `origin: community-curation` 的新词与已有词条的 `context_notes` 分别由工具、社区目录中的 `terminology.json` 维护，通过 `scripts/merge_term_contexts.py` 应用。`context_refs` 指向补充解释的维护入口；官方索引再生成会再次合并，保留 tswn 实现解释和社区语境。别名允许一词多义，回答时读取 scope 与语境，不强行把所有命中合成同一机制。

仓库来源记录 `commit`、`repository_path`、行号和 `sha256`，链接指向不可变 GitHub blob。上游本地路径只是定位提示，不是本知识仓库的构建依赖。

待整理材料可暂存于被 Git 忽略的 `data/raw/` 其他子目录，官方归档子目录已纳入版本管理。维护者后续口述的信息记录为维护者来源，不伪装成已抓取的公开文档。
