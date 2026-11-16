# 名竞百科静态网页

在仓库根目录运行：

```powershell
python scripts/serve_wiki.py
```

打开终端显示的本地地址，默认 [http://127.0.0.1:8765/](http://127.0.0.1:8765/)。按 `Ctrl+C` 停止服务；端口冲突时可传 `--port 8766`。修改页面或知识库后重新运行命令，会重新生成页面数据。

网页支持分类浏览、名称/别名/释义及语境补充搜索、资料语境筛选、词条详情和来源链接。搜索不区分英文大小写，支持空格分隔多个关键词，按名称与别名优先排列。可使用 `Ctrl+K`、`⌘K` 或 `/` 聚焦搜索。分类、搜索和词条状态保存在网址中，支持刷新、浏览器前进后退与链接分享。

页面采用原生 HTML、CSS、JavaScript，不需要安装 npm 依赖。源文件在本目录；[构建脚本](../scripts/build_wiki.py) 将页面及 [共享知识库](../knowledge/README.md) 的数据生成到 `dist/wiki/`，词条定义仍在 `knowledge/` 维护。生成数据不纳入 Git。

只构建静态文件时运行 `python scripts/build_wiki.py`。将 `dist/wiki/` 的完整内容放到任意静态 HTTP 服务即可访问，也支持部署在子目录。页面读取本地生成的 JSON，不请求模型或远程检索服务。

验证搜索与链接状态：

```powershell
node --test tests/wiki.test.mjs
```
