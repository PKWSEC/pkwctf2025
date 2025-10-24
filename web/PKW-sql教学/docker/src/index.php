<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="UTF-8">
    <title>PKWSEC-SQL教学</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/atom-one-dark.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #1e2127;
            color: #c8ccd4;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        .container {
            display: flex;
            justify-content: space-between;
            width: 80%;
            max-width: 1000px;
            margin: auto;
            animation: fadeIn 1.5s ease-in-out;
        }

        .content, .resources {
            padding: 20px;
            background-color: #282c34;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            width: 48%;
        }

        .header {
            font-size: 2.5rem;
            color: #61afef;
            margin-bottom: 20px;
        }

        .description, .resources-description {
            font-size: 1.1rem;
            margin-bottom: 30px;
        }

        .link-button, .start-button {
            display: inline-block;
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
            transition: background-color 0.3s, transform 0.2s;
        }

        .link-button {
            background-color: #56b6c2;
            color: white;
        }

        .link-button:hover {
            background-color: #3a9da5;
            transform: translateY(-2px);
        }

        .start-button {
            background-color: #98c379;
            color: white;
            font-weight: 500;
        }

        .start-button:hover {
            background-color: #89b269;
            transform: translateY(-2px);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="content">
            <div class="header">欢迎来到 PKWCTF SQL注入教学局</div>
            <div class="description">
                SQL注入是什么？我怎么没听过？别说那么多，赶紧开始速速速！！！
            </div>
            <a href="challenge.php" class="start-button">开始挑战 🚀</a>
        </div>
        <div class="resources">
            <div class="resources-description">
                如果你是初学者，不妨参考以下资源：
            </div>
            <a href="https://ctf-wiki.org/web/sqli/" class="link-button" target="_blank">CTF Wiki</a>
            <a href="https://hello-ctf.com/hc-web/sql_injection/" class="link-button" target="_blank">HelloCTF</a>
        </div>
    </div>
</body>

</html>
