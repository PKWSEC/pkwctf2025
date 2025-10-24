<?php
$checker1 = $_GET['PKWctf'] === "we1c%00me";
$checker2 = $_POST['PKWctf'] === "fl@g";
$checker3 = $_COOKIE['c00k13'] === "i can't eat it";
$checker4 = $_SERVER['HTTP_USER_AGENT'] === "PKWsec";
$checker5 = $_SERVER['HTTP_REFERER'] === "PKWsec";

function getIp()
{
    if ($_SERVER["HTTP_CLIENT_IP"] && strcasecmp($_SERVER["HTTP_CLIENT_IP"], "unknown")) {
        $ip = $_SERVER["HTTP_CLIENT_IP"];
    } else {
        if ($_SERVER["HTTP_X_FORWARDED_FOR"] && strcasecmp($_SERVER["HTTP_X_FORWARDED_FOR"], "unknown")) {
            $ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
        } else {
            if ($_SERVER["REMOTE_ADDR"] && strcasecmp($_SERVER["REMOTE_ADDR"], "unknown")) {
                $ip = $_SERVER["REMOTE_ADDR"];
            } else {
                if (
                    isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp(
                        $_SERVER['REMOTE_ADDR'],
                        "unknown"
                    )
                ) {
                    $ip = $_SERVER['REMOTE_ADDR'];
                } else {
                    $ip = "unknown";
                }
            }
        }
    }
    return ($ip);
}

// check if ip is local
$checker6 = getIp() === '127.0.0.1' || getIp() === 'localhost' || getIp() === '::1';

if ($checker1 && $checker2 && $checker3 && $checker4 && $checker5 && $checker6) {
    header('Location: success.php?flag=' . base64_encode(file_get_contents('/flag')));
    exit;
}

?>

<!doctype html>
<html lang="zh-cmn-Hans">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no" />
    <meta name="renderer" content="webkit" />
    <meta name="force-rendering" content="webkit" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />

    <link href="https://cdn.bootcss.com/mdui/0.4.3/css/mdui.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/mdui/0.4.3/js/mdui.min.js"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <title>看看你的 HTTP</title>
</head>

<body class="mdui-theme-primary-indigo mdui-theme-accent-pink mdui-appbar-with-toolbar">
    <header class="mdui-appbar mdui-color-theme  mdui-appbar-fixed">
    </header>
    <div class="mdui-container sp-main-container mdui-center mdui-row" style="margin-top: 40px;">
        <div class="mdui-card">
            <div class="mdui-card-primary">
                <div class="mdui-card-primary-title">看看你的 HTTP</div>
            </div>
            <div class="mdui-card-content">
                <div class="mdui-table-fluid">
                    <table class="mdui-table mdui-table-hoverable">
                        <thead>
                            <tr>
                                <th>项目</th>
                                <th>你需要传入</th>
                                <th>当前传入值</th>
                                <th>是否正确</th>
                            </tr>
                        </thead>
                        <tbody class="mdui-typo">
                            <tr>
                                <td>GET 参数 <code>PKWctf</code></td>
                                <td>we1c%00me</td>
                                <td><?php echo $_GET['PKWctf']; ?></td>
                                <td><?php echo $checker1 ? '<i class="mdui-icon material-icons">check</i>' : '<i class="mdui-icon material-icons">close</i> (请注意 URL 转义)'; ?></td>
                            </tr>
                            <tr>
                                <td>POST 参数 <code>PKWctf</code></td>
                                <td>fl@g</td>
                                <td><?php echo $_POST['PKWctf']; ?></td>
                                <td><?php echo $checker2 ? '<i class="mdui-icon material-icons">check</i>' : '<i class="mdui-icon material-icons">close</i>'; ?></td>
                            </tr>
                            <tr>
                                <td>Cookie <code>c00k13</code></td>
                                <td>i can't eat it</td>
                                <td><?php echo $_COOKIE['c00k13']; ?></td>
                                <td><?php echo $checker3 ? '<i class="mdui-icon material-icons">check</i>' : '<i class="mdui-icon material-icons">close</i>'; ?></td>
                            </tr>
                            <tr>
                                <td>用户代理 (User-Agent)</td>
                                <td>PKWsec</td>
                                <td><?php echo $_SERVER['HTTP_USER_AGENT']; ?></td>
                                <td><?php echo $checker4 ? '<i class="mdui-icon material-icons">check</i>' : '<i class="mdui-icon material-icons">close</i>'; ?></td>
                            </tr>
                            <tr>
                                <td>来源 (Referer)</td>
                                <td>PKWsec</td>
                                <td><?php echo $_SERVER['HTTP_REFERER']; ?></td>
                                <td><?php echo $checker5 ? '<i class="mdui-icon material-icons">check</i>' : '<i class="mdui-icon material-icons">close</i>'; ?></td>
                            </tr>
                            <tr>
                                <td>你的 IP</td>
                                <td><code>127.0.0.1</code></td>
                                <td><?php echo getIp(); ?></td>
                                <td><?php echo $checker6 ? '<i class="mdui-icon material-icons">check</i>' : '<i class="mdui-icon material-icons">close</i>'; ?></td>
                        </tbody>
                    </table>
                </div>
                <div class="mdui-panel" mdui-panel>

                    <div class="mdui-panel-item">
                        <div class="mdui-panel-item-header">
                            <div class="mdui-panel-item-title">一点小提示</div>
                            <div class="mdui-panel-item-summary">给新手看看</div>
                            <i class="mdui-panel-item-arrow mdui-icon material-icons">keyboard_arrow_down</i>
                        </div>
                        <div class="mdui-panel-item-body mdui-typo">
                            <p>Hi~ 欢迎参加 PKWctf, 祝你玩的开心。这可能是你旅途的开始，但不要忘记，任何一个高手都是从菜鸟开始的。万事开头难，我们一起走上成为网络安全高手<!-- 黑客 -->之路吧！</p>
                            <p>HTTP 协议是网络传输的最广泛使用的协议，你可以看看 <a href='https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Messages'>MDN 文档</a> 来了解了解（当然，这篇文档可能有点长和晦涩，但是特别详细，如果觉得不太好接受就看我下面写的内容吧~）</p>
                            <p>在开始之前，你可以找一个趁手的工具。下面是我经常使用的工具, 如果你发现工具无法下载完全可以在群里面问问, 当然如果实在下载不下来也没关系:</p>
                            <h2>Hackbar</h2>
                            <ul>
                                <li>Chrome 浏览器 / Edge 浏览器: <a href='https://chrome.google.com/webstore/detail/ginpbkfigcoaokgflihfhhmglmbchinc'>下载链接</a> (可能需要科学上网, 下载不下来没关系)</li>
                                <li>FireFox 浏览器: <a href='https://addons.mozilla.org/en-US/firefox/addon/hackbar-free/'>下载链接</a></li>

                            </ul>
                            <p>这个是一个浏览器扩展，下载好后按 F12 打开开发者工具，你可以找到在开发者工具中找到他</p>
                            <p><img src="https://s2.loli.net/2024/02/22/3tEBfOKAQcXLuRY.png" referrerpolicy="no-referrer" alt="image-20240222225316478"></p>
                            <p>点击之后你可以点击 LOAD 来载入当前页面的请求</p>
                            <p><img src="https://s2.loli.net/2024/02/22/yrx8qbAv3QEMKZ9.png" referrerpolicy="no-referrer" alt="image-20240222225439213"></p>
                            <p>最上方是你的请求地址 （URL），可能会包含问号并接着一些内容，这个叫做 POST 参数</p>
                            <p>左边是你的请求内容（payload/请求载荷），右边是你的 Header （请求头）</p>
                            <p>你可以随意编辑里面的内容，当你编辑完成后，你可以点击 EXECUTE 来进行请求。</p>
                            <p>&nbsp;</p>
                            <h2>BurpSuite</h2>
                            <blockquote>
                                <p>请注意, 这个软件存在收费版, 但是他的 Community 版本目前来说够用</p>
                            </blockquote>
                            <p><a href='https://portswigger.net/burp/releases/community/latest'>下载链接</a></p>
                            <p>一般都会使用 BurpSuite 来进行 HTTP 请求的抓取和修改, 我们需要现在浏览器里面配置好代理转发</p>
                            <p>我们可以下载 <code>ProxySwitchyOmega</code> 插件, 在 Burp 的 <code>Proxy (代理)</code> 选项卡下找到 <code>代理设置 (Proxy Settings)</code></p>
                            <p><img src="https://s2.loli.net/2024/07/25/QBgfKJPd2CZyGql.png" referrerpolicy="no-referrer" alt="image-20240725233303958"></p>
                            <p>找到此处的代理端口, 我们进入到 <code>ProxySwitchyOmega</code> 插件的设置页面, 新增一个情景模式, 名称任意, 模式为代理服务器</p>
                            <p><img src="https://s2.loli.net/2024/07/25/I325eZAWpR4DuK9.png" referrerpolicy="no-referrer" alt="image-20240725233422089"></p>
                            <p>可以按照我的右边这样设置, 再点击左边的应用选项即可保存</p>
                            <p>在 Burp 的<code>代理 (Proxy)</code>页面下打开 <code>拦截 (Intercept)</code> 按钮, 即可开始抓包</p>
                            <p>之后在想要抓包的页面, 找到浏览器右上角的 <code>ProxySwitchyOmega</code> 插件</p>
                            <p><img src="https://s2.loli.net/2024/07/25/516xCRscWIjkYfP.png" referrerpolicy="no-referrer" alt="image-20240725233539240"></p>
                            <p>点击刚刚创建好的情景模式, 此时页面会刷新, 回到 Burp 中, 你会看到当前的 HTTP 请求, 右键可以选择<code>发送到 Repeater</code>, 就可以在 <code>重放器 (Repeater)</code> 选项卡中找到他了, 我们此时可以再次点击拦截按钮来放行这个包</p>
                            <h2>Yakit</h2>
                            <p><a href='https://www.yaklang.io/products/download_and_install/'>下载链接</a></p>
                            <p>你可以跟随下载链接中的步骤尝试下载和安装，之后再打开默认项目</p>
                            <p>Yakit 可以完成中间人代理，Web Fuzzer 发包等一系列功能（听不懂也没关系），从新手到专业人士都可以使用</p>
                            <p>我们可以点开 <code>MITM</code> 开启中间人代理, 可以参照 Burp 的配置方式在浏览器中配置好代理, 当然, 你也可以选择免配置启动, 此时会自动配好所有的选项, 在 Yakit 中抓到包后, 你可以通过右键一个请求, 再点击 <code>发送到 WebFuzzer</code> 来对请求进行修改</p>
                            <p>或者我们可以从头开始</p>
                            <p>我们可以打开 <code>Web Fuzzer</code></p>
                            <p><img src="https://s2.loli.net/2024/02/22/8rtdg19VlbPU3ye.png" referrerpolicy="no-referrer" alt="image-20240222230244367"></p>
                            <p>你也可以在最上面的 <code>渗透测试</code> 选项卡中找到</p>
                            <p>在这里你可以看到一个 HTTP 请求最原本的样子</p>
                            <pre><code class='language-http' lang='http'>POST / HTTP/1.1
Content-Type: application/json
Host: www.example.com

{&quot;key&quot;: &quot;value&quot;}
</code></pre>
                            <p>其中 <code>POST</code> 代表<a href='https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods'>请求方法</a>, 我们还可以用 <code>GET</code>, <code>PUT</code> 等动词</p>
                            <p>&nbsp;</p>
                            <p><code>/</code> 代表请求的路径, 比如 <code>/foo/index.php</code> 表示请求站点根<code>foo</code>目录下的 <code>index.php</code>, 当然你可能在这里发现问号后面跟了一长串内容, 比如</p>
                            <pre><code>index.php?foo=bar&amp;chef=kw
</code></pre>
                            <p>问号后面的内容代表 GET 参数, 表示 GET 参数中: <code>foo</code> 为 <code>bar</code>, <code>chef</code> 为 <code>kw</code></p>
                            <p>在这里的特殊符号需要进行 URLENCODE 转义, Yakit 给了我们一个方便的 <code>fuzz 语法</code></p>
                            <pre><code>{{url(abc%def)}}
</code></pre>
                            <p>表示将 <code>abc%def</code> 转义, 请求时会变成 <code>%61%62%63%25%64%65%66</code>, 别看这变成乱码了,但是服务器会自动翻译成我们原本的内容</p>
                            <p>&nbsp;</p>
                            <p><code>HTTP/1.1</code> 表示请求的 HTTP 版本, 我们暂时忽略, 当你在以后得请求走私的时候可能会了解到他</p>
                            <p>&nbsp;</p>
                            <p>之后的内容我们称呼他为 <code>Header</code>:</p>
                            <p>&nbsp;</p>
                            <p><code>Content-Type</code>: 表示请求的载荷(payload)类型, 可以看看 <a href='https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Content-Type'>文档</a></p>
                            <p>这个值可能为 <code>application/x-www-form-urlencoded</code>, <code>multipart/form-data; boundary=something</code>, <code>application/json</code></p>
                            <p>不同的内容不一样</p>
                            <p>&nbsp;</p>
                            <p><code>Host</code>: 表示目标主机, 在 Yakit 中你需要指定这个来表示你的目标是什么, 当然, 你也可以在左边的<code>真实 Host</code> 里面设置设置</p>
                            <p>&nbsp;</p>
                            <p>当然还有一些有用的 <code>Header</code>:</p>
                            <p>比如 <code>Cookie</code>, <code>X-Forwarded-For</code>, <code>Referer</code>, <code>User-Agent</code>, 大家可以搜索一下各自是干什么的</p>
                            <p>&nbsp;</p>
                            <p>下面是一行空行, 表示 <code>Header</code> 结束, 接下来是请求载荷 (body)</p>
                            <p>&nbsp;</p>
                            <p>这个地方内容的格式和 <code>Content-Type</code> 对应</p>
                            <p>&nbsp;</p>
                            <p>如果 <code>Content-Type</code> 是 <code>application/x-www-form-urlencoded</code>, 那这个地方的格式和 <code>GET</code> 参数差不多, 比如</p>
                            <pre><code class='language-http' lang='http'>POST /somewhere HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

foo=a&amp;bar=b
</code></pre>
                            <p>表示 <code>foo</code> 为 <code>a</code>, <code>bar</code> 为 <code>b</code></p>
                            <p>&nbsp;</p>
                            <p>如果 <code>Content-Type</code> 是 <code>multipart/form-data; boundary=--------something</code></p>
                            <pre><code class='language-http' lang='http'>POST /foo HTTP/1.1
Content-Length: 68137
Content-Type: multipart/form-data; boundary=--------something

--------something
Content-Disposition: form-data; name=&quot;description&quot;

some text
--------something
Content-Disposition: form-data; name=&quot;name&quot;

hacker

--------something
</code></pre>
                            <p>其中 <code>--------something</code> 被当做分隔符, 这个和 <code>Content-Type</code> 中一直</p>
                            <p>这表示 <code>description</code> 为 <code>some text</code>, <code>name</code> 为 <code>hacker</code></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>当你编辑好一个请求之后, 你可以 <code>发送请求</code>, 右侧会传来响应, 关于响应, 你可以看看这篇教程 <a href='https://www.runoob.com/http/http-tutorial.html'>教程</a></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>大概就是这么多, 如果还有不懂的问题欢迎在群里提问哦~</p>

                        </div>
                    </div>
                </div>
            </div>
        </div>
</body>

</html>