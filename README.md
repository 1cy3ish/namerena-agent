# namerena-agent

为名字竞技场（Namerena）整理 AI 可用的领域知识、圈内黑话，以及 skill、agent 和 MCP 接入方式。后续面向社区问答机器人和工具开发者提供可追溯的知识与能力。

## 当前状态

已归档 Deep Mess 官方基础资料，并收录 tswn-core 重写项目的引擎、Openbox 评分、WASM 网页及 docs 知识。现有 184 个词条，其中 100 个来自本轮仓库整理，50 个已有词条补充了 tswn 语境。机器人、检索服务和 MCP server 尚未实现，Python 脚本仅用于资料维护。

名字竞技场是 MD5 大作战的续作，玩家输入名字后自动推演战斗。基础资料来自 [Deep Mess 官方说明](https://deepmess.com/zh/namerena/)，实现与工具补充见 [tswn-core](knowledge/tools/tswn-core/README.md)。维护者确认 GitHub Pages 旧站过时，其他已讨论入口按最新版本处理；不同实现与历史资料保留各自语境。其他工具和独立史料等待后续提供。整理日期：2026-11-16。

## 目录

```text
.
├── AGENTS.md                      # 本仓库的协作与知识维护约定
├── knowledge/
│   ├── README.md                  # 资料与术语的数据约定
│   ├── overview.md                # 基本玩法、入口、版本差异与开发线索
│   ├── sources.json               # 来源目录、核查日期及局限
│   ├── glossary.json              # 基础术语、别名、来源与适用范围
│   ├── official/                  # 官方正文快照、结构化索引和覆盖报告
│   ├── project-context.json       # 维护者确认的版本与收录约定
│   ├── tools/tswn-core/           # 重写引擎、评分、网页、术语与阅读覆盖
│   └── history/                   # 等待维护者提供史料与口述
├── data/raw/official-namerena/     # 纳入 Git 的官方原始资源归档
├── scripts/                       # 抓取、索引生成与资料校验
├── skills/
│   └── namerena-knowledge/
│       └── SKILL.md               # 仓库内使用的领域 skill 初稿
├── agents/
│   ├── README.md
│   └── qa-assistant.md            # 问答 agent 提示词初稿
├── mcp/
│   └── README.md                  # MCP 能力规划，待实现
├── evals/
│   └── cases.json                 # 术语理解、版本辨析和未知问题的评估样例
└── docs/
    └── architecture.md            # 共享知识与各接入层的关系
```

## 从哪里开始

1. 阅读 [知识概览](knowledge/overview.md)、[官方资料](knowledge/official/README.md) 和 [tswn 知识入口](knowledge/tools/tswn-core/README.md)。
2. 在 [术语表](knowledge/glossary.json) 中补充社区黑话，并在 [来源目录](knowledge/sources.json) 中记录依据。
3. 在当前仓库中让 AI 读取 [领域 skill](skills/namerena-knowledge/SKILL.md) 或 [问答提示词](agents/qa-assistant.md)，手动试用 [评估样例](evals/cases.json)。

当前 skill 通过相对路径读取仓库内的 `knowledge/`，尚未作为可独立安装的技能包发布。`agents/` 保存通用提示词，不代表已创建或启动任何 agent；`mcp/` 目前只包含设计说明。

官方资源的 URL、状态、SHA-256 与链接关系见 [抓取清单](knowledge/official/crawl-manifest.json)，正文来源与上游声明均保留。收录及校验命令见 [脚本说明](scripts/README.md)。

## 接下来

- 优先补充玩家确认过的黑话、缩写、评分体系、工具名与真实问答。
- 依据已收录的 tswn 术语与评分规则扩充真实问答；其他仓库、史料与口述等维护者提供。
- 实现共享知识的检索与校验，再接入 MCP 和问答机器人。
- 根据真实误答扩充评估集，尤其关注同词多义与历史资料误用。
