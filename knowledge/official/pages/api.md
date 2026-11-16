# 在网页里嵌入名字竞技场

来源：https://deepmess.com/zh/namerena/api.html
检索日期：2026-11-16
来源 ID：official-embedding

以下为官方页面正文的抓取快照；文字、数值、链接和排版问题按来源保留。

---

## 在网页里嵌入名字竞技场

名字竞技场支持以iframe形式嵌入其他网页。

### 调用

嵌入iframe时只需要在网址后面将对战者的名字用Base64编码加在url里就可以。

```javascript
function run(names){
   var base64 = window.btoa(
      unescape(encodeURIComponent(names))
   ).replace(/\+/g,'-').replace(/\//g,'_');
   iframe.src = 'http://namerena.github.io/#n=' + base64;
}
```

### 回调

名字竞技场程序会将结果以postMessage方式发送到调用网页。

可以在网页中监听message事件得到战斗结果。

```javascript
function onMessage(e) {
   console.log(e.data.winners);
}
window.addEventListener('message', onMessage);
```

回调参数

- data.winners: 数组，获胜队伍所有成员名字
- data.all: 二维数组，以队伍划分的所有名字

### 示例

[api\_test.html](https://deepmess.com/zh/namerena/api_test.html)
