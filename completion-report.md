# 完成报告：名字竞技场知识库补全任务

任务依据：prompt.md（名字竞技场知识库补全）。基线仓库 `1cy3ish/namerena-agent` 默认分支，基线提交 `5a176484a247100baad612836ad5b7bb98452249`（2026-11-16 每日快照）。工作于 2026-11-16 完成。

## 一、总体数字

| 指标 | 基线 | 最终 |
| --- | --- | --- |
| 词条总数（glossary.json） | 230 | 311 |
| 来源总数（sources.json） | 87 | 98 |
| 带非空 `detailed_description` 的词条 | 0 | 311（100%） |
| 评估样例（evals/cases.json） | 30 | 45 |
| 语境补充（context_notes） | 57 | 86 |

- **修改**：全部 230 个基线词条补写详细描述；其中 62 个词条追加来源引用共 294 处（`add_source_ids` 程序化并入）。
- **新增 81 个词条**，按维护入口分布：
  - `knowledge/community/qq-bots/terminology.json`：6 个（小鱼bot、名竞测试bot、shenjack的bot、鱼煲、namerena-测试中、/ladder- 前缀），含 14 条对既有词条的 bot 调用方式补充；
  - `knowledge/tools/datastructure4/terminology.json`：8 个（DataStructure4、ABCP5、增量配对、五类基础分拣、三人组流程、sieve 阈值、team_name 过滤、SP1/SP2），遵守"少量关键词"约定（≤10），含 3 条补充；
  - `knowledge/tools/pbb-new2/terminology.json`：10 个（PBB7、评分族、枚举模式、多字符集格式、续测检查点、QP 二次扣分、输出格式、autotune、计量单位、引擎结构），含 2 条补充；
  - `knowledge/community/tutorials-and-history/terminology.json`：57 个（新教程黑话/机制/工具、旧教程术语、贴吧史料、2026 天梯论坛定项阅读），含 10 条对既有词条的补充。
- **字段调整**：词条级 `scope` 栏按任务约定取消（230 个基线词条 + 维护入口源文件全部剥离），版本/年代/条件并入正文与 `context_notes`；`knowledge/README.md` 字段约定同步更新。
- **附件归档**：两份附件登记为来源并归档至 `data/raw/provided/`（SHA-256 见来源记录：qq群bot.txt `5f9be43…`、DataStructure4-Readme.md `d3e0688…`）。

## 二、过时标记（outdated）变更与依据

| 词条 | 依据 |
| --- | --- |
| historical-ladder-name（旧天梯） | 委托方确认；论坛 d/215 楼#52（2026-03-27）"旧天梯停止维护"佐证 |
| rough-evaluation（粗评）、refined-evaluation（精评） | 委托方确认；现行社区工具（tswn 评分、cqp/cqd、天梯）不再使用该称呼；官方 0%~10%/100% 语义保留在正文 |
| bot-shenjack、bot-yubao、bot-namerena-testing | 附件 qq群bot.txt 明文记载（已禁用/已弃用/已失效）；注明依据为附件，未验证当前在线状态 |
| wa-kuang（挖矿）、cangmao-dui（藏猫队）、py-slang（PY） | 2020 官方天梯时代用语，官方天梯已关（两处独立社区资料），正文保留历史语境 |
| forty-ids（四十大ID） | 2024 榜单规则，楼主 2024-07 宣布将自然停更 |
| pl-tester（pl 测号器） | 旧教程原文自标"可能已经过时"，现行测号生态已转向 pbb/PBB7 |

未因资料发表于较早年份而整体标过时的词条均经逐项核查：如团队强评（作为 `!test!` 评分类型仍现行，仅二人组评价指标被 cqp 取代）、双败赛制（天梯锦标赛 S3 起改单败，但武术大赛 2026 规程仍用）、技能榜/全能（tswn ratings.json 实现数值随提交固定）。

## 三、实际阅读范围与访问状态

各来源的结构化登记（URL、快照路径、版本状态、备注）见 `knowledge/sources.json`；逐帖证据清单见来源 `community-ladder-forum-2026-discussions` 的 notes。要点：

- **官方说明（17 条）**：与归档逐页比对，无内容差异、无未归档在线页面；`navigation.html` 404 为既有已知缺口。
- **新教程（tutorial-new，12 页全读）**：MkDocs 站点，作者自述"没写完/不一定对"；进阶第 5、7 章被引用但站点暂缺，已在报告中与正文标注。
- **旧教程（tutorial-old，24 个文本文件全读）**：最新提交 cfb43c7（2026-07-08）；原文多处自标过时/不确定，已逐项核查并在词条中分层标注；`docs/files/` 14 个二进制附件未读取。
- **PBB7（pbb7-repo，commit 2408dcb）**：在线读取 README、VERSION（7.0.6）、changelog.md；Releases 页为空；本地 git clone 因代理失败，故登记为 commit 固定的 community 来源（未提供 blob sha256，如实注明）。
- **天梯 10007 / 论坛 10008**：天梯公开页面全读（含 newlive API、instant 规则全文、HtmlTools 界面与脚本级 res/main.js、res/model.js）；论坛 47 个讨论帖原始快照（d/19、38、51、54、6、58、77、85、100、106、136、139、150、153、156、163、166、176、185、200、202、207、213、215、218、227、229、231、234、235、247、250、255、273、274、306、308、311、379、383、401、402、403、410、416 等）。受限项：`/forum`、`/battle`、`/team-binding` 需登录；`/cards/` 正文仅占位文案；`tianwei.txt` 已 404；负榜/遭遇战真实入口未定位；写操作未尝试。
- **贴吧（tieba-forum）**：吧主页简介可读；帖子列表/精品区不可读；全文 2 帖（Rinick 天梯上线帖、挖矿帖），部分楼层 2 帖（四十大ID、创作区），被百度安全验证拦截仅存链接 2 帖（涵虚测号器、天梯教程二），武术大赛总贴已删除；另全文转读 CSDN 教程转载（2023-05）与洛谷基本常识（2023-12）两份站外史料。

## 四、已解决的冲突

1. **官方天梯 vs 旧民间天梯 vs 新天梯**：historical-ladder-name 释义维持"按链接与年代判断"，并以 d/215 楼#52（2026-03-27）确认民间天梯自身的 1.0/2.0 交替（"旧天梯停止维护，以下更新公告默认指新天梯"）。
2. **组队加成对 namebase 还是 namebonus 取 max**：新旧教程相互印证为"简化说法 vs 精确实现"（deep-chp1：对 namebonus 取 max、扫描序列不变、不产生新识别位点），以精确版为准表述，未当版本冲突。
3. **锦标赛赛制冲突**：d/227 首帖 bo7 双败 vs 楼#31（2026-05-07）S3 起改单败——两说并存并按赛季分界写明。
4. **周赛冻结/开赛时间三说冲突**（d/227 首帖、d/215 草稿、newlive 当前页）：保留三方出处，不拼合单一时间。
5. **大豹词条证据升级**：由 unverified 升级为 source_supported（讨论 200 楼#1 原文），并新增 ming-jing-zhou-bao 词条覆盖五档豹级全貌。
6. **PBB7/pbb_new/旧 pbb 三对象区分**：分别建词条并写清关系（GoldenFish123321/Namerena-pbb_new ≠ AsunderSquall/pbb-new2）。
7. **`/namer-[pd|pd|qp|qd]` 重复 pd、官方魔/抗属性页措辞疑似笔误**：按原文保留并列待核实，未静默改写。

## 五、仍待核实的具体问题（正文均已标注）

- 两个 bot 生态的当前在线状态（依据仅附件）；附件记载为疑似笔误的命令名。
- flarum.cloud 与 10008 是否同一论坛（URL 结构一致、无同帖双域名比对）。
- 官方天梯"服务器欠费关闭"（两处独立社区资料，非官方声明）；47.109.79.252 民间天梯现状。
- PBB7 与 tswn/Openbox 的同名评分族（cp/fp/wc/fs/pj）语义异同；xp/xd 与官方四项评分的换算关系。
- Boss 的 HP/七围/熟练度数值、MP/聚气/技能倍率细节、tswn 若干实现常量——官方与 tswn 文档均未给出，逐条"待核实"标注，未编造。
- 帮测/周赛/锦标赛等活动的现行状态与额度（均为帖子规则，标注时效）。
- "偷看器"的具体用法（新教程标题提及、旧教程仅一句 SP_all 输入 8）。

## 六、执行的结构检查与验证（全部为资料级校验，非机制/模型测试）

- `python scripts/validate_knowledge.py` 通过：26 个 JSON 文件、98 条来源、311 个词条、68 条归档 URL 记录与本地链接全部校验成功；无未审阅的归档失败项。
- 程序化自检：311 个词条 ID 唯一、无未解析来源引用（含 12 条 context 补充与全部新增词条）、86 条 context_notes 的 context_id 无重复、词条级 scope 全量移除、分类枚举未扩展（修正 1 处越界分类 history→community）。
- 新增 15 条 QA 素材与既有 cases.json 结构一致（字段与既有 5 字段完全相同），全部引用合并后真实存在的词条/来源 id；未声称任何"测试通过"。
- 报告性边界：本轮没有执行测号、没有运行任何游戏/工具、没有发起任何实测验证；所有"文档用法/实现语境/社区资料/整理者推断"分层均在词条正文标注。
