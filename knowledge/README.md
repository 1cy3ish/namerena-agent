# 共享知识

`overview.md` 保存入门概览；`glossary.json` 保存结构化术语；`sources.json` 保存引用来源，供 skill、agent、MCP 和后续检索服务共同使用。

[官方资料](official/README.md) 包含正文快照、属性、技能、特殊名字、语言包词汇索引与抓取清单。[tswn 重写与工具](tools/tswn-core/README.md) 补充实现、评分、别名和网页接入。[维护者约定](project-context.json) 记录版本及范围，其他工具和独立史料等待后续提供。

[民间天梯与论坛](community/ladder-forum/README.md) 保存社区称呼、赛事、协作和工具关键词。观察摘要记录页面、帖子楼号和读取范围，不作为全站镜像或永久活动政策。

## 来源

每条来源使用稳定的 `id`，记录标题、URL 或本地材料路径、类型、日期、读取状态和适用范围。`read_status: retrieved` 表示读取了页面，不表示内容已经独立实测。官方原始文件保存在 `data/raw/official-namerena/`，SHA-256 与关联链接见抓取清单。

## 术语

每个术语包含：

- `id`：稳定英文标识；`term`：常用名称；`aliases`：别名或缩写。
- `definition`：结合名字竞技场语境的简短解释。
- `detailed_description`：详细描述正文，当前全部预留为空字符串；后续实质词条按根目录 [AGENTS.md](../AGENTS.md) 的类型标准补全。简单分区标签、纯别名等可不要求展开。
- `outdated`：布尔值；`true` 表示历史内容、已废弃或极少用，与待核实状态无关。首批标记旧天梯、粗评、精评；`false` 只表示尚未标记。
- `category`：概念、玩法、输入规则或评分。
- `status`：`source_supported` 表示有来源支持这项释义；`unverified` 表示尚待核实。
- `source_ids`：指向来源目录的 ID；`checked_at`：核查日期。

有来源支持不等于当前社区已达成共识。不同年代或群体的定义冲突可新增独立词条，标注语境。新旧版本都在收录范围内。问答中保留名字、战队名和输入字符，避免改写改变角色或对战条件。

词条不再设置“适用范围”字段。必要的年代、版本和条件在正文、已有语境补充与来源证据中说明；本轮只调整字段，不填详细正文，不删除旧版历史记录或原始资料。过时词条仍可阅读、检索和补全，不与当前规则混用。

`origin: official-index` 的词条由 `scripts/build_official_index.py` 从归档生成，完整字段见 `details_path` 和 `details_id`，其他词条为人工整理。语言包独有词汇与完整机制定义分开记录。

`origin: tswn-curation` 和 `origin: community-curation` 的新词与已有词条的 `context_notes` 分别由工具、社区目录中的 `terminology.json` 维护，通过 `scripts/merge_term_contexts.py` 应用。`context_refs` 指向补充解释的维护入口；已有在线历史时须先人工合并，不能直接重建覆盖。别名允许一词多义，回答时结合正文、语境补充与来源，不强行把所有命中合成同一机制。语境补充和原始证据中的历史字段保留，不等于重新引入词条级“适用范围”栏。

仓库来源记录 `commit`、`repository_path`、行号和 `sha256`，链接指向不可变 GitHub blob。上游本地路径只是定位提示，不是本知识仓库的构建依赖。

待整理材料可暂存于被 Git 忽略的 `data/raw/` 其他子目录，官方归档子目录已纳入版本管理。维护者后续口述的信息记录为维护者来源，不伪装成已抓取的公开文档。
