from flask import Flask, request, render_template
import sqlite3
import os
import re

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
        flag = "flag{test_flag_please_replace}"
    
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = 'Chestnut'", (flag,))
    conn.commit()
    conn.close()

# 安全过滤函数
def security_filter(input_str):
    """
    机器猫学长匆忙实现的安全过滤
    可能存在绕过方式...
    """
    if not input_str:
        return input_str
    
    # 黑名单关键词（简单替换）
    blacklist = ['union', 'select', 'and', 'where', 'or', 'from', '--', '#', '/*', '*/']
    
    filtered = input_str
    for word in blacklist:
        if word:  # 确保word不为空
            try:
                # 使用简单的字符串替换而不是正则表达式
                # 大小写不敏感替换
                filtered = filtered.replace(word, '')
                # 也替换大写版本
                filtered = filtered.replace(word.upper(), '')
            except:
                # 如果替换出错，继续处理下一个词
                pass
    
    return filtered

@app.route('/', methods=['GET', 'POST'])
def index():
    users = None
    error = None
    search_term = ""
    filtered_input = ""
    security_note = ""
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        search_term = username
        
        if username:
            try:
                # 应用安全过滤
                filtered_username = security_filter(username)
                filtered_input = f"（过滤后: {filtered_username}）"
                
                # 记录安全日志（在实际题目中可以隐藏这个提示）
                security_note = "🔒 机器猫学长的安全过滤已启用"
                
                conn = sqlite3.connect('/app/users.db')
                c = conn.cursor()
                
                # 存在SQL注入漏洞的查询 - 使用过滤后的输入
                query = f"SELECT * FROM users WHERE username = '{filtered_username}'"
                c.execute(query)
                users = c.fetchall()
                
                conn.close()
                
            except Exception as e:
                error = f"查询错误: {str(e)}"
        else:
            error = "请输入用户名"
    
    return render_template('index.html', 
                         users=users, 
                         error=error, 
                         search_term=search_term,
                         filtered_input=filtered_input,
                         security_note=security_note)

# 在模块加载时初始化数据库和flag
init_db()
setup_flag()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)