# tswn 机制与术语补充

范围：本轮固定的 tswn-core 提交，详见 [来源和阅读范围](README.md)。数值解释来自文档与实现，没有把静态阅读写作本轮实测。

## rq、名字系数和 seed

普通 fight/BattleSession 默认 `rq=4`，评分和胜率默认 `rq=6`。rq 在构造阶段影响 `name_factor`，后者影响七围派生，HP 不做这一缩放。普通构建还要比较名字和阵营评估值，不能只看名字长度决定最终系数。

`--keep-rq`/“不低估短号”让对应评估保留 rq=4。准备好的阵容已固定构造口径，换 rq 需要重新准备；换 seed 只改变本场初始化和随机过程。数字 profile 评分与固定阵容胜率还使用不同的轮次构造规则。[rq 机制说明](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/mechanics/name-factor-rq.md)

## 输入、身份与分组

完整输入、身份键、显示名、实体 ID 分别承担不同用途。空行决定输入队伍；`@clan` 参与名字构建，不能直接当成空行分组。玩家实体还保存运行时 team 与输入组映射。

tswn 的单个名字及有效阵营各最多 256 个 UTF-8 字节；这是本重写的解析器约束，不覆盖官方文档原先的字符限制记载。`NamerenaInput` 会提取区分大小写的 `seed:` 前缀行，不要求每行都必须带 `@!`。[输入解析源码](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_core/src/namerena/input.rs#L5-L168)

普通武器、`+diy[...]` 和 `+ol:{...}` 都会影响解释输入的方式。OL 的 skills 对象顺序是技能尝试顺序，JSON 字符串内部的 `+` 不能误拆成队友。前七围采用 +36 编码、HP 原样；带玩家级 attrs/skills 覆盖会禁用普通武器效果，仅覆盖召唤模板则不会。[DIY/OL 契约](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/reference/diy-overlay.md)

## 技能数量与别名

官方基础技能页列 34 项；tswn 的普通实际技能 ID 为 0..34，共 35 项，其中包括隐匿。35 是空技能占位，36..39 是保留槽。附体、自爆、使魔火球和武器技能另有专用槽，不能将存储容量当成普通技能总数。

Openbox 短名如命轮、护符、反弹、亡灵，与生命之轮、护身符、伤害反弹、召唤亡灵对应；导出 key 与中文短名均已加入词条别名。技能的固定槽位与 active_order 分开，不能把重新排序当作无行为变化。[普通技能对照](skill-map.json)、[技能与 hook](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/core-guide/skills-and-hooks.md)

## 附体、自爆与隐匿

- **附体**：幻影默认技能；经过免疫、回避判断后，给目标增加狂暴状态步数，并使施法实体进入死亡链。它与让目标改变友敌关系的魅惑不同。
- **自爆**：使魔专用技能，走火系魔法伤害分支，并结算施法者自身死亡；单独保存槽位，不能归入普通玩家火球。
- **隐匿**：受伤后仍活动、尚未隐匿且有效队伍存活成员多于一人时尝试触发。降低 attract，等级高于 63 时另增敏、防、抗；与主动潜行/背刺不同。

依据：[附体实现](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_core/src/runtime/combat/skills_lifecycle.rs#L437-L520)、[自爆实现](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_core/src/runtime/combat/effects.rs#L141-L205)、[隐匿触发](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_core/src/runtime/combat/passive.rs#L408-L481) 与 [有效属性](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_core/src/runtime/entity/runtime.rs#L515-L560)。

## 分身与技能衰减

分身创建新实体并重派生属性，而非复制当前面板。非蓄力本体执行相应 HP 与原始七围衰减，使用兼容浮点常量，不能精确简化为最终显示值乘 0.78。本体分身技能随机衰减，克隆体分身等级再开根号；其他技能先以当前等级截断构造基底，再重放 LastBoost 或 SlotBoost。分身条件中的 `magic` 是魔法属性，不是 MP。

不同技能有各自的衰减：命轮、苏生为整数半衰；治愈高于 8 才每次减 1；幻术按向上取整的 3/4 更新；分身有特殊流程。[分身详解](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/mechanics/clone.md)、[技能衰减](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/mechanics/skill-decay.md)

使魔、幻影、丧尸各有蓝图、实例和 owner。嵌套使魔按直接来源传导半伤；使魔克隆的相应传导直接到根主角色。手写重施策略与导出模板的默认值还可能不同。[召唤物模板与传导](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/reference/diy-overlay.md#伤害传导与分身)

## 护盾、判胜与终止

`shield` 是当前实际吸收量，`max_shield` 是当前技能熟练度这个展示尺度。一次蓄盾可能超过该尺度；铁壁的减伤资料另算，吞噬改变技能后尺度会更新。

判胜要求恰好一队仍有存活实体；全部阵亡也是无胜者。`alive_group_count` 保留旧行为的粘性计数，已有队伍复活不补回，不能用于判胜。规范会话的回合预算/无进展截断、Runtime 粘性失败、正常胜利是不同结果。[公共 API](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/reference/public-api.md)、[判胜语义](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/mechanics/winner.md)
