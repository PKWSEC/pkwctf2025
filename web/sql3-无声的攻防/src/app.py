from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                  username TEXT UNIQUE, 
                  password TEXT,
                  email TEXT,
                  is_admin INTEGER DEFAULT 0)''')
    
    # 插入测试数据 - 使用英文名称
    users = [
        (1, 'Doraemon', 'robotic_cat_123', 'doraemon@chef-whale.com', 1),
        (2, 'Lion', 'king_of_kitchen', 'lion@chef-whale.com', 1),
        (3, 'SillyBird', 'forgetful_bird', 'sillybird@chef-whale.com', 0),
        (4, 'Chestnut', 'FLAG_PLACEHOLDER', 'chestnut@chef-whale.com', 1),
        (5, 'LittleWhale', 'cute_mascot', 'littlewhale@chef-whale.com', 0)
    ]
    
    try:
        c.executemany('INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)', users)
        conn.commit()
    except:
        pass
    
    conn.close()

# 读取flag并插入到Chestnut用户中
def setup_flag():
    try:
        with open('/flag', 'r') as f:
            flag = f.read().strip()
    except:
        flag = "flag{test_boolean_blind_injection}"
    
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = 'Chestnut'", (flag,))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = None
    search_term = ""
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        search_term = username
        
        if username:
            try:
                conn = sqlite3.connect('/app/users.db')
                c = conn.cursor()
                
                # 存在SQL注入漏洞的查询
                query = f"SELECT * FROM users WHERE username = '{username}'"
                c.execute(query)
                user = c.fetchone()
                
                conn.close()
                
                # 布尔盲注：只返回是否存在，不返回具体数据
                if user:
                    message = "Right 用户存在"
                else:
                    message = "Wrong 用户不存在"
                
            except Exception as e:
                error = f"查询错误: {str(e)}"
        else:
            error = "请输入用户名"
    
    return render_template('index.html', 
                         message=message, 
                         error=error, 
                         search_term=search_term)

# 在模块加载时初始化数据库和flag
init_db()
setup_flag()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)