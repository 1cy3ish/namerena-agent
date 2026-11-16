# namerena-agent

为名字竞技场（Namerena）整理 AI 可用的领域知识、圈内黑话，以及 skill、agent 和 MCP 接入方式。后续面向社区问答机器人和工具开发者提供可追溯的知识与能力。

## 当前状态

项目处于初始化阶段：已整理第一批公开资料、基础术语和领域 skill，建立问答 agent 提示词与 MCP 规划。尚未实现机器人、检索服务、MCP server 或游戏模拟器，运行语言和框架暂不选定。

名字竞技场是 MD5 大作战的续作，玩家输入名字后由程序自动推演战斗；名字关联固定属性和技能。玩法和开发者文档见 [Deep Mess 官方说明](https://deepmess.com/zh/namerena/)。社区术语及版本差异另见 [知识概览](knowledge/overview.md)。资料检索日期：2026-11-16。

## 目录

```text
.
├── AGENTS.md                      # 本仓库的协作与知识维护约定
├── knowledge/
│   ├── README.md                  # 资料与术语的数据约定
│   ├── overview.md                # 基本玩法、入口、版本差异与开发线索
│   ├── sources.json               # 来源目录、核查日期及局限
│   └── glossary.json              # 初始术语、别名、来源与适用范围
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

1. 阅读 [知识概览](knowledge/overview.md)，了解玩法、资料入口与已知局限。
2. 在 [术语表](knowledge/glossary.json) 中补充社区黑话，并在 [来源目录](knowledge/sources.json) 中记录依据。
3. 在当前仓库中让 AI 读取 [领域 skill](skills/namerena-knowledge/SKILL.md) 或 [问答提示词](agents/qa-assistant.md)，手动试用 [评估样例](evals/cases.json)。

当前 skill 通过相对路径读取仓库内的 `knowledge/`，尚未作为可独立安装的技能包发布。`agents/` 保存通用提示词，不代表已创建或启动任何 agent；`mcp/` 目前只包含设计说明。

## 接下来

- 优先补充玩家确认过的黑话、缩写、评分体系、工具名与真实问答。
- 明确目标游戏版本、社区语境和知识授权范围。
- 实现共享知识的检索与校验，再接入 MCP 和问答机器人。
- 根据真实误答扩充评估集，尤其关注同词多义与历史资料误用。
