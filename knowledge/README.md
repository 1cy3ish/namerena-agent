# 共享知识

`overview.md` 保存入门概览；`glossary.json` 保存结构化术语；`sources.json` 保存引用来源，供 skill、agent、MCP 和后续检索服务共同使用。

[官方资料](official/README.md) 包含正文快照、属性、技能、特殊名字、语言包词汇索引与抓取清单。[维护者约定](project-context.json) 记录版本及收录范围；工具项目和历史资料分别留在 `tools/`、`history/`，等待后续提供材料。

## 来源

每条来源使用稳定的 `id`，记录标题、URL 或本地材料路径、类型、日期、读取状态和适用范围。`read_status: retrieved` 表示读取了页面，不表示内容已经独立实测。官方原始文件保存在 `data/raw/official-namerena/`，SHA-256 与关联链接见抓取清单。

## 术语

每个术语包含：

- `id`：稳定英文标识；`term`：常用名称；`aliases`：别名或缩写。
- `definition`：结合名字竞技场语境的简短解释。
- `category`：概念、玩法、输入规则或评分。
- `status`：`source_supported` 表示有来源支持这项释义；`unverified` 表示尚待核实。
- `scope`：来源语境和版本局限，不能省略为“适用于所有版本”。
- `source_ids`：指向来源目录的 ID；`checked_at`：核查日期。

有来源支持不等于当前社区已达成共识。不同年代或群体的定义冲突可新增独立词条，标注语境。新旧版本都在收录范围内。问答中保留名字、战队名和输入字符，避免改写改变角色或对战条件。

`origin: official-index` 的词条由 `scripts/build_official_index.py` 从归档生成，完整字段见 `details_path` 和 `details_id`，其他词条为人工整理。语言包独有词汇与完整机制定义分开记录。

待整理材料可暂存于被 Git 忽略的 `data/raw/` 其他子目录，官方归档子目录已纳入版本管理。维护者后续口述的信息记录为维护者来源，不伪装成已抓取的公开文档。
