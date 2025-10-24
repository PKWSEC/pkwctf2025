# can can need http

小明想成为一名黑客，不过太还不太会 HTTP 协议，于是拉着你一起学习。

## Writeup

使用 Yakit 发包如下

```http
POST /?dinoctf={{url(we1c%00me)}} HTTP/1.1
Host: localhost:32777
Content-Type: application/x-www-form-urlencoded
Cookie: c00k13=i can't eat it;
User-Agent: D1no
Referer: D1no
X-Forwarded-For: 127.0.0.1

D1no={{url(fl@g)}}
```

注意那个 302 重定向, 浏览器里面会跟着走, 不要跟着走, 拿到 Location 后的 `flag`, base64 解码即可