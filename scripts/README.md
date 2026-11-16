# 资料维护脚本

这些脚本只用于收录和校验资料，不决定未来机器人或 MCP 的运行语言。使用 Python 3.9 以上版本及系统可用的 `Asia/Shanghai` 时区数据，无第三方 Python 库依赖。

```powershell
python scripts/archive_official.py
python scripts/build_official_index.py
python scripts/merge_term_contexts.py
python scripts/validate_knowledge.py
```

抓取器会读取官方文档、游戏入口、链接的同源资源，以及已有运行时观察记录中发现的 GET 地址。它保留原始字节，记录 SHA-256、失败项及链接关系；不会扩展抓取站外站点或无关游戏页面。资源没有为离线运行改写。

`archive_official.py --reuse` 会在 SHA-256 一致时复用本地已归档文件，只补抓新发现或尚未成功取得的地址。默认命令重新请求资源。抓取失败或触及数量上限时退出码为 1，仍会保存报告；当前已记录语言包声明的 `navigation.html` 返回 404。

构建脚本从原始官方 HTML 和语言 JSON 提取属性、技能、Boss 与词形，更新 `origin: official-index` 的词条，保留人工词条。日期取自抓取清单。手工维护输入规则、来源与页面快照时，应同步检查对应原文。

工具知识以 `knowledge/tools/*/terminology.json` 维护新增词条及已有词条的语境解释。`merge_term_contexts.py` 可单独合并；官方构建脚本也会在末尾执行同一合并，避免重新生成时丢失重写项目的解释或重复叠加别名/注释。

校验器验证 JSON、稳定 ID、来源引用、本地路径、归档哈希、抓取队列闭合和已审阅的上游缺口。运行时观察记录来自一次独立的全新浏览器加载及本地对战页面触发，保留资源请求证据，不作为评分或引擎兼容性测试。

若本机仍有提供的 tswn 仓库，可运行 `python scripts/validate_knowledge.py --source-checkout D:/namerena/tswn-core`，按记录的 commit 从 Git 对象核对源码哈希与行号；默认校验不依赖该外部路径。
