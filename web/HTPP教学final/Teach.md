Hi~ 欢迎参加 PKWCTF, 祝你玩的开心。这可能是你旅途的开始，但不要忘记，任何一个高手都是从菜鸟开始的。万事开头难，我们一起走上成为网络安全高手<!-- 黑客 -->之路吧！

HTTP 协议是网络传输的最广泛使用的协议，你可以看看 [MDN 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Messages) 来了解了解（当然，这篇文档可能有点长和晦涩，但是特别详细，如果觉得不太好接受就看我下面写的内容吧~）

在开始之前，你可以找一个趁手的工具。下面是我经常使用的工具, 如果你发现工具无法下载完全可以在群里面问问, 当然如果实在下载不下来也没关系:

## Hackbar

* Chrome 浏览器 / Edge 浏览器: [下载链接](https://chrome.google.com/webstore/detail/ginpbkfigcoaokgflihfhhmglmbchinc) (可能需要科学上网, 下载不下来没关系)
* FireFox 浏览器: [下载链接](https://addons.mozilla.org/en-US/firefox/addon/hackbar-free/)

这个是一个浏览器扩展，下载好后按 F12 打开开发者工具，你可以找到在开发者工具中找到他

![image-20240222225316478](https://s2.loli.net/2024/02/22/3tEBfOKAQcXLuRY.png)

点击之后你可以点击 LOAD 来载入当前页面的请求

![image-20240222225439213](https://s2.loli.net/2024/02/22/yrx8qbAv3QEMKZ9.png)

最上方是你的请求地址 （URL），可能会包含问号并接着一些内容，这个叫做 POST 参数

左边是你的请求内容（payload/请求载荷），右边是你的 Header （请求头）

你可以随意编辑里面的内容，当你编辑完成后，你可以点击 EXECUTE 来进行请求。



## BurpSuite

> 请注意, 这个软件存在收费版, 但是他的 Community 版本目前来说够用

[下载链接](https://portswigger.net/burp/releases/community/latest)

一般都会使用 BurpSuite 来进行 HTTP 请求的抓取和修改, 我们需要现在浏览器里面配置好代理转发

我们可以下载 `ProxySwitchyOmega` 插件, 在 Burp 的 `Proxy (代理)` 选项卡下找到 `代理设置 (Proxy Settings)`

![image-20240725233303958](https://s2.loli.net/2024/07/25/QBgfKJPd2CZyGql.png)

找到此处的代理端口, 我们进入到 `ProxySwitchyOmega` 插件的设置页面, 新增一个情景模式, 名称任意, 模式为代理服务器

![image-20240725233422089](https://s2.loli.net/2024/07/25/I325eZAWpR4DuK9.png)

可以按照我的右边这样设置, 再点击左边的应用选项即可保存

在 Burp 的`代理 (Proxy)`页面下打开 `拦截 (Intercept)` 按钮, 即可开始抓包

之后在想要抓包的页面, 找到浏览器右上角的 `ProxySwitchyOmega` 插件

![image-20240725233539240](https://s2.loli.net/2024/07/25/516xCRscWIjkYfP.png)

点击刚刚创建好的情景模式, 此时页面会刷新, 回到 Burp 中, 你会看到当前的 HTTP 请求, 右键可以选择`发送到 Repeater`, 就可以在 `重放器 (Repeater)` 选项卡中找到他了, 我们此时可以再次点击拦截按钮来放行这个包

## Yakit

[下载链接](https://www.yaklang.io/products/download_and_install/)

你可以跟随下载链接中的步骤尝试下载和安装，之后再打开默认项目

Yakit 可以完成中间人代理，Web Fuzzer 发包等一系列功能（听不懂也没关系），从新手到专业人士都可以使用

我们可以点开 `MITM` 开启中间人代理, 可以参照 Burp 的配置方式在浏览器中配置好代理, 当然, 你也可以选择免配置启动, 此时会自动配好所有的选项, 在 Yakit 中抓到包后, 你可以通过右键一个请求, 再点击 `发送到 WebFuzzer` 来对请求进行修改

或者我们可以从头开始

我们可以打开 `Web Fuzzer`

![image-20240222230244367](https://s2.loli.net/2024/02/22/8rtdg19VlbPU3ye.png)

你也可以在最上面的 `渗透测试` 选项卡中找到

在这里你可以看到一个 HTTP 请求最原本的样子

```http
POST / HTTP/1.1
Content-Type: application/json
Host: www.example.com

{"key": "value"}
```

其中 `POST` 代表[请求方法](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods), 我们还可以用 `GET`, `PUT` 等动词



`/` 代表请求的路径, 比如 `/foo/index.php` 表示请求站点根`foo`目录下的 `index.php`, 当然你可能在这里发现问号后面跟了一长串内容, 比如

```
index.php?foo=bar&chef=kw
```

问号后面的内容代表 GET 参数, 表示 GET 参数中: `foo` 为 `bar`, `chef` 为 `kw`

在这里的特殊符号需要进行 URLENCODE 转义, Yakit 给了我们一个方便的 `fuzz 语法`

```
{{url(abc%def)}}
```

表示将 `abc%def` 转义, 请求时会变成 `%61%62%63%25%64%65%66`, 别看这变成乱码了,但是服务器会自动翻译成我们原本的内容



`HTTP/1.1` 表示请求的 HTTP 版本, 我们暂时忽略, 当你在以后得请求走私的时候可能会了解到他



之后的内容我们称呼他为 `Header`:



`Content-Type`: 表示请求的载荷(payload)类型, 可以看看 [文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Content-Type)

这个值可能为 `application/x-www-form-urlencoded`, `multipart/form-data; boundary=something`, `application/json`

不同的内容不一样



`Host`: 表示目标主机, 在 Yakit 中你需要指定这个来表示你的目标是什么, 当然, 你也可以在左边的`真实 Host` 里面设置设置



当然还有一些有用的 `Header`:

比如 `Cookie`, `X-Forwarded-For`, `Referer`, `User-Agent`, 大家可以搜索一下各自是干什么的



下面是一行空行, 表示 `Header` 结束, 接下来是请求载荷 (body)



这个地方内容的格式和 `Content-Type` 对应



如果 `Content-Type` 是 `application/x-www-form-urlencoded`, 那这个地方的格式和 `GET` 参数差不多, 比如

```http
POST /somewhere HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

foo=a&bar=b
```

表示 `foo` 为 `a`, `bar` 为 `b`



如果 `Content-Type` 是 `multipart/form-data; boundary=--------something`

```http
POST /foo HTTP/1.1
Content-Length: 68137
Content-Type: multipart/form-data; boundary=--------something

--------something
Content-Disposition: form-data; name="description"

some text
--------something
Content-Disposition: form-data; name="name"

hacker

--------something
```

其中 `--------something` 被当做分隔符, 这个和 `Content-Type` 中一直

这表示 `description` 为 `some text`,  `name` 为 `hacker`





当你编辑好一个请求之后, 你可以 `发送请求`, 右侧会传来响应, 关于响应, 你可以看看这篇教程 [教程](https://www.runoob.com/http/http-tutorial.html)

响应中也有 Header, 有些关键信息比如 `Location` 表示要进行跳转到的地址

大概就是这么多, 如果还有不懂的问题欢迎在群里提问哦~