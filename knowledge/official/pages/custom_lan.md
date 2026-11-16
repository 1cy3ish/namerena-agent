# 自定义语言

来源：https://deepmess.com/zh/namerena/custom_lan.html
检索日期：2026-11-16
来源 ID：official-custom_lan

以下为官方页面正文的抓取快照；文字、数值、链接和排版问题按来源保留。

---

## 自定义语言

名字竞技场默认语言是中文。但是可以自己设定文字，使用其他语言，甚至可以完全改变游戏显示的内容。

#### 改变语言：

- 英文版： [/?l=lang%2Fen.json](https://deepmess.com/namerena/?l=lang%2Fen.json)
- 繁体中文： [/?l=lang%2Fzh-TW.json](https://deepmess.com/namerena/?l=lang%2Fzh-TW.json)

#### 改变内容：

- 大富翁： [/#l=lang%2zh-money.json](https://deepmess.com/namerena/?l=lang%2Fzh-money.json)


用金币代替生命值，如果不喜欢打打杀杀，推荐试一下大富翁语言包。

##### 大富翁语言包 战斗过程示例

![](https://deepmess.com/zh/namerena/images/lan_demo_money.png)

##### 对比普通版

![](https://deepmess.com/zh/namerena/images/lan_demo_zh.png)

### 创建自己的语言包

- 首先下载默认的语言文件： [/lang/zh.json](https://deepmess.com/namerena/lang/zh.json)
- 用UTF8编码打开语言文件，编辑语言，再以UTF8保存。
- 上传语言文件到某个网站，请确保该网站返回正确的 [CORS头文件](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)
  - 如果没有自己网站，可以到 [Github Page](https://pages.github.com/) 免费建站
- 把json文件的网址输入下面的输入框，点击 生成链接
