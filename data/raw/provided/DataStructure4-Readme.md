# Data_Structure4.0 - all_new 数据处理主流程

本目录是 `all_new` 主流程的可分发版本，包含二人组、三人组、ABCP5
预测所需的源码、可执行程序、模型和运行库。旧主流程、训练专用程序、benchmark
以及运行产生的数据不在本包内。

## 首次使用

1. 完整解压压缩包，不要直接在压缩包预览窗口内运行。
2. 编辑 `config.json`，将 `team_name` 设置为输入数据中 `@` 后的队伍名。
3. 把待处理的 `.txt` 文件放入 `input/`。
4. 双击 `reset_and_run_all_new.bat`，清空历史运行状态并执行一次完整流程。
5. 后续需要增量处理时，把新输入放入 `input/` 后直接运行 `all_new.exe`。

发布包中的 `input/`、`file/`、`new/`、`out/`、`tmp/`、`3ren/`、
`3-out/` 都是空目录。不要删除这些目录，也不要把输入数据直接放进 `file/`。

## 输入与增量状态

`all_new.exe` 会合并 `input/` 下的普通文件，并对输入进行队伍名过滤和去重。

- `team_name` 是必填字符串。没有配置或值为空时，程序会在处理前报错退出。
- 每行最后一个 `@` 后面的队伍名必须与 `team_name` 相同。
- 队伍名比较会忽略行尾的空格、Tab 和 CR 等空白字符。
- 队伍名不同、缺少 `@` 或格式不合法的行会写入 `out/ignore_input.txt`，不参与计算。
- `file/` 保存已经处理过的数据及 old 增量状态；正常增量运行不要清空它。
- `new/` 保存本轮新增数据的分类结果，便于检查和后续使用。

同一批数据需要从头重跑时，使用 `reset_and_run_all_new.bat`。脚本会清空
`tmp/`、`out/`、`new/`、`file/`、`3ren/`、`3-out/` 和 ABCP5 的临时结果，
但保留 `input/`、配置、程序、源码和模型。

可先执行无修改检查：

```batch
reset_and_run_all_new.bat --dry-run --no-pause
```

## 主流程

`all_new.exe` 依次执行以下阶段：

1. 合并 `input/`，校验 `team_name`，过滤不属于当前队伍的行。
2. 与 `file/old.txt` 去重，得到本轮新增输入。
3. 用 SP1/SP2 计算单项与类型分数，并生成 BC、FZ、WC、FS、PJ 等分类。
4. 用新的 `two_FC_new`、`two_WC_new`、`two_RH_new` 做 old/new 增量配对。
5. `get_3=1` 时，先用 ABCP5 筛选二人组，再分类并执行八类三人组增量配对。
6. `abcp.enable=1` 时汇总二人组结果，运行 ABCP5 并输出预测结果。
7. 更新 `file/` 中的历史状态，并按配置把本轮分类复制到 `new/`。

二人组增量只计算 `new x new`、`new x old` 和 `old x new`，不会重复计算
`old x old`。完全相同的两个字符串不会组成一组。

## 主要输出

| 路径 | 内容 |
| --- | --- |
| `out/FC.txt` | FZ x BC 二人组结果 |
| `out/WC.txt` | WC 内部二人组结果 |
| `out/RH.txt` | FS x PJ 二人组结果 |
| `out/new_qp.txt` 等 | 本轮单项结果，按前置分数从大到小排序 |
| `out/qp_skill.txt` 等 | 技能筛选结果，使用追加模式 |
| `out/ignore_input.txt` | 被队伍名或格式检查忽略的输入行 |
| `abcp5/result.txt` | 带 ABCP5 分数的二人组预测结果 |
| `abcp5/result_without_score.txt` | 去除分数后的 ABCP5 结果 |
| `3ren/FFC.txt` 等 | 三人组结果 |
| `file/old*.txt` | 下次增量运行使用的历史状态 |

输出记录的顺序可能受多线程执行影响，不应将行顺序视为结果语义的一部分。

## 配置

随包提供的 `config.json`：

```json
{
    "team_name": "",
    "thread_number": 20,
    "bc": {"sieve": 4100, "ptt_sieve": 4500},
    "fz": {"sieve": 4200, "ptt_sieve": 4600},
    "wc": {"sieve": 4000, "ptt_sieve": 4400},
    "fs": {"sieve": 3900, "ptt_sieve": 4300},
    "pj": {"sieve": 4100, "ptt_sieve": 4500},
    "two_fc": {"enable": 1, "sieve": 9400},
    "two_wc": {"enable": 1, "sieve": 9200},
    "two_rh": {"enable": 1, "sieve": 9150},
    "qp": {"enable": 1, "sieve": 5700, "skill_sieve": 300},
    "qd": {"enable": 1, "sieve": 6500, "skill_sieve": 300},
    "pp": {"enable": 1, "sieve": 8000, "skill_sieve": 300},
    "pd": {"enable": 1, "sieve": 9000},
    "cqd": {"enable": 1, "sieve": 4300},
    "copy_pf_to_out": 1,
    "copy_to_new": 1,
    "run_dup": 1,
    "abcp": {"enable": 1, "sieve": 4500},
    "get_3": 1,
    "three": {
        "pair_abcp_sieve": 4400,
        "ffc": {"enable": 1, "sieve": 15000},
        "wfc": {"enable": 1, "sieve": 14950},
        "fwc": {"enable": 1, "sieve": 14950},
        "wwc": {"enable": 1, "sieve": 14750},
        "rwc": {"enable": 0, "sieve": 14850},
        "rrh": {"enable": 1, "sieve": 14700},
        "prh": {"enable": 0, "sieve": 15000},
        "wrh": {"enable": 0, "sieve": 14700}
    }
}
```

字段说明：

| 字段 | 说明 |
| --- | --- |
| `team_name` | 必填，只处理最后一个 `@` 后队伍名与此值一致的行 |
| `thread_number` | 并行线程数；应结合 CPU 核心数和可用内存设置 |
| `bc/fz/wc/fs/pj` | 五类基础分拣的保留阈值与 PTT 阈值 |
| `two_fc/two_wc/two_rh` | 二人组开关与保留阈值 |
| `qp/qd/pp` | 单人评分开关、保留阈值和技能阈值 |
| `pd/cqd` | 单人评分开关与保留阈值 |
| `copy_pf_to_out` | 是否把单人结果复制到 `out/` |
| `copy_to_new` | 是否生成 `new/` 下的本轮分类文件 |
| `run_dup` | 是否与历史输入去重 |
| `abcp.enable` | 是否运行二人组 ABCP5 预测 |
| `abcp.sieve` | ABCP5 最终输出阈值 |
| `get_3` | 是否运行三人组流程 |
| `three.pair_abcp_sieve` | 二人组进入三人配对前的 ABCP5 最低分数 |
| `three.<type>.enable` | 对应三人组类型开关 |
| `three.<type>.sieve` | 对应三人组输出阈值 |

## 三人组

三人组的详细数据结构和评分含义见 `README_3.md`。主流程支持以下接口：

```text
two_<TYPE>.exe <type> <thread_number> <sieve> <single_input> <pair_input> <output_file>
```

当前 `type` 必须为 `1`。程序将单人输入和已经由 ABCP5 筛选、再由
`classify.exe` 换算为 two 对应分数的二人组输入进行配对。

| 程序 | 单人类型 | 二人组类型 | 默认输出 |
| --- | --- | --- | --- |
| `two_FFC.exe` | FZ | FC | `3ren/FFC.txt` |
| `two_WFC.exe` | WC | FC | `3ren/WFC.txt` |
| `two_FWC.exe` | FZ | WC | `3ren/FWC.txt` |
| `two_WWC.exe` | WC | WC | `3ren/WWC.txt` |
| `two_RWC.exe` | FS | WC | `3ren/RWC.txt` |
| `two_RRH.exe` | FS | RH | `3ren/RRH.txt` |
| `two_PRH.exe` | PJ | RH | `3ren/PRH.txt` |
| `two_WRH.exe` | WC | RH | `3ren/WRH.txt` |

`all_new.exe` 负责 old/new 的增量拆分。三人组程序只负责一次
`single_input x pair_input` 计算，并以追加方式写入指定输出。

## 编译

需要已加入 `PATH` 的 64 位 MinGW-w64 `g++`，然后运行：

```batch
compile.bat
```

该脚本只编译 `all_new` 主流程所需程序。默认使用
`-Ofast -march=x86-64-v3 -funroll-all-loops -pthread -std=c++23`，因此目标电脑的
CPU 需要支持 x86-64-v3 指令集。ABCP5 如需重编译，使用
`abcp5/compile.bat`；普通用户不需要重新编译。

## ABCP5 环境诊断

ABCP5 已携带模型、ONNX Runtime 和所需的 x64 VC++ 运行库，不依赖 Python。
若双击运行后无输出、立即退出，或出现 DLL 初始化错误，请运行根目录的：

```batch
check_abcp5.bat
```

脚本会检查系统架构、CPU 指令集、DLL 加载和最小预测流程，并尝试使用兼容版
`abcp5_compatible.exe`。诊断结果保存在 `abcp5/_diagnostics/`。如普通版失败但
兼容版成功，可使用诊断程序提示的兼容配置；两者都失败时，将整个
`abcp5/_diagnostics/` 目录提供给维护者。

## 发布包目录

```text
Data_Structure4.0/
|-- all_new.exe                 主控程序
|-- config.json                 运行配置
|-- reset_and_run_all_new.bat   清理并完整重跑
|-- check_abcp5.bat             ABCP5 一键诊断入口
|-- compile.bat                 主流程源码编译脚本
|-- score_now.txt               SP1 所需评分数据
|-- src/                        主流程 C++ 源码和公共头文件
|-- abcp5/                      模型、推理程序、运行库与诊断工具
|-- input/                      用户输入，发布时为空
|-- file/                       增量历史状态，发布时为空
|-- new/                        本轮分类结果，发布时为空
|-- out/                        二人组和单人输出，发布时为空
|-- tmp/                        临时文件，发布时为空
|-- 3ren/                       三人组输出，发布时为空
`-- 3-out/                      三人组中间文件，发布时为空
```

`two_FF`、`two_RR` 仅用于训练数据收集，不属于 `all_new` 主流程，也不包含在本包中。
