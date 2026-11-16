# tswn 网页本体与开发接入

维护者提供的部署入口为 [Cloudflare 页面](https://fast-namerena.pages.dev/branch/tswn/) 和 [shenjack.top 页面](https://shenjack.top:10007/tswn)。2026-11-16 抓取时，前者显示 wrapper 0.5.12 / core 0.7.0；后者重定向到 `/static/tswn/examples/show.html`，正文可读取但版本位置为占位符，未据此指定版本。详细证据见 [deployments.json](deployments.json)。

网页本体由 WASM 包装与静态展示页组成。当前展示页专注 Fight；`demo.html` 则保留快速验证战斗和胜率的入口。已经存在引擎与 JS API，但本知识仓库还没有 MCP server，也没有据此确认一个可直接调用的远程 HTTP 对战服务。

## 会话与展示

新接入使用正式 `BattleSession`：初始快照、`next_frame()`、终局结果，最后显式 `free()`。`battle_replay` 收集同一个会话；`FightSession` 与 `WinRateSession` 属于进阶兼容入口，不能把它们的字段或停止条件直接替代规范会话。[公共契约](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/reference/public-api.md)

frame 与 round 是不同计数：空回合不产生可见帧，仍消耗推进预算。正文展示使用 rows/clips/parts 中的文本、延迟、HP/盾条与死亡特效，不从伤害数值猜测展示含义。昵称、CSS 图标与播放游标是显示层数据，不修改原始身份或构造属性。

流式页面维护源端位置、已收历史、当前播放位置，最多预取两帧。回退只读历史，追上尾部后继续同一会话。WASM 的胜率分批调用仍是同步计算，当前并没有因为使用异步 source 就自动获得多线程或后台 Worker。[网页会话设计](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/docs/design/battle-session.md)、[WASM 说明](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_wasm/README.md)

## 分享与输入

tswn 展示页使用 `?input=<UTF-8 URL-safe Base64>`，接受 `replay`、`data` 查询参数作为兼容别名。分享生成器清理旧 engine/runtime 参数并清空 hash。原站文档的 `#n=` 是另一种入口约定，不能直接把它当作本页的查询参数。[分享路由实现](https://github.com/shenjackyuanjie/tswn-core/blob/d12b462aa532f95be793c00dfed37b8fea0672bb/crates/tswn_wasm/examples/show-routing.js#L3-L93)

页面的 normal/fast/turbo、暂停、逐事件/逐帧、重播和昵称只调整显示过程。复现需要保留 raw、seed、rq、core commit 和 wrapper 版本；两个网址可打开或显示相同版本号，不证明其产物字节或所有输出已经验证一致。
