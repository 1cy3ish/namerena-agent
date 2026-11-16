# tswn-core：重写引擎与开箱工具

本轮依据维护者提供的 `D:/namerena/tswn-core` 只读审阅。固定提交为 [`d12b462aa532f95be793c00dfed37b8fea0672bb`](https://github.com/shenjackyuanjie/tswn-core/tree/d12b462aa532f95be793c00dfed37b8fea0672bb)，日期为 2026-11-16。包清单中 core 为 0.7.0、Openbox 与共享后端为 0.5.2、WASM wrapper 为 0.5.12；发布记录中的旧版本表另按当时记录理解。

## 阅读范围与知识入口

重点查看 core 的名字构建、解析、Runtime、技能与状态、评分批处理，Openbox 的评分/配队/预设及共享后端，WASM 的规范会话、网页回放和分享入口。docs 共 113 份 Markdown 已通览标题与章节，重点指南、格式、机制和工具段落结合实现阅读。不是对所有源码和历史性能报告逐行审计。

- [术语及补充解释](terminology.json)：100 个新增词条、50 个已有词条的语境补充；统一进入 [总术语表](../../glossary.json)，社区词条另在对应目录维护。
- [评分体系](ratings.json)：profile 评分、靶子集评分、配队、技能榜与配置来源。
- [普通技能对照](skill-map.json)：ID、导出 key、Openbox 短名与已有术语之间的映射。
- [机制说明](mechanics.md)：rq、分身、隐匿、附体、自爆、护盾和判胜等容易误答的问题。
- [网页与接入](web.md)：部署入口、分享格式、规范会话与展示边界。
- [仓库信息与其他模块关键词](repository.json)、[阅读覆盖](review-coverage.json)：版本、标题清单、阅读深度及范围限制。

来源以 [sources.json](../../sources.json) 中的 `tswn-*` ID 引用，保留 commit、文件、行号和 SHA-256。它们是这份重写的实现证据；[官方基础说明](../../official/README.md) 仍保留自己的原文和适用范围。

## 评分需要分清的几件事

| 名称 | 这里怎样计算 | 常见误解 |
| --- | --- | --- |
| pp / pd | 普通 profile 基准，胜率乘 10000 | 与当前具体靶子集的胜率相同 |
| qp / qd | 强化 profile 基准，胜率乘 10000 | 等同于 cqp / cqd 百分比 |
| sum | 四项评分之和 | sum 高就自动获得全能资格 |
| cqd / cqp | 对配置靶子的平均胜率，可按靶子权重平均 | 命令别名强制限定单挑/组队人数 |
| pair | 每个队友组合先求靶子平均，再乘队友权重，取最高 head 项求和 | 最终分数一定不超过 100 |
| 技能榜 | 最高熟练度技能与配置阈值共同筛选 | 永久写死在引擎中的官方排行榜 |

单号 pp/qp 是“被测号加一个生成队友，对抗两个生成对手”；pd/qd 用重复单号标记进入 1v1 布局。评分 profile 每轮更新数字名字；固定阵容胜率的 profile seed 调度另有规则。多成员输入按具体 score 布局理解。依据为 [评分分派源码](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_openbox_backend/src/backend/namer_pf.rs#L287-L335) 和 [对战布局源码](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_core/src/runtime/batch.rs#L469-L558)。

“刺评、辅评、无刺评、分身评、配件评”在当前工作目录配置中都是带权队友预设，head=4。这里只确认名称、文件与计算流程，名称背后的完整社区历史等待维护者补充。根 `setting/settings.toml` 有三组靶子；内嵌默认还保留两组带 `20251102` 名称的靶子，两套配置分别记录在评分文件中，没有因日期名称而丢弃。

## 其他模块只保留关键词

| 模块 | 关键词 |
| --- | --- |
| tswn_py | Python、PyO3、绑定、类型声明 |
| tswn_capi | C ABI、FFI、动态/静态库、句柄 |
| tswn_ds4 | 模型评分、ABCP5、配对、实战筛选、增量缓存 |
| tswn_lane_ranker | lane、两两胜率、校准、排名、SQLite |
| tswn_ladder | 天梯、匹配、ELO、handicap、周期更新、PostgreSQL |
| tswn_name_ranker | 独立单号排名、专用校准资源、workspace 排除项 |
| tswn_pwp | 胜率数据集、状态采样、Parquet、校准、离线特征编码 |
| tswn_test | 共享行为测试、golden、corpus、差分 |

这些关键词来自项目地图和 Cargo 清单，未展开相应模块的独立 README 或算法实现。文档内带“提案”的设计、历史归档和版本记录有独立状态；例如 Runtime 重构评估明确写着尚未实现，不据此增加已交付能力。

## 维护方式

新增术语和补充解释以本目录 `terminology.json` 为维护入口，执行 `python scripts/merge_term_contexts.py` 合并。官方索引生成器也会调用同一合并逻辑，保留已有官方快照，并在生成后重新应用这些有来源的补充。原始官方数据的“未知机制”可以在 tswn 语境中得到解释，不意味着原文已经包含这些细节。

本轮没有修改上游仓库、构建引擎、运行 Rust 测试或比较两个部署的引擎输出；验证针对知识格式、来源定位、引用和再生成稳定性。
