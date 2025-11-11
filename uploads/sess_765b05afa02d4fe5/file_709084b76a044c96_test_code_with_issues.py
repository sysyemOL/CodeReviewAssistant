import os
import sqlite3

# 硬编码的敏感信息 - 安全问题
password = "admin123"
api_key = "sk-1234567890abcdef"
database_url = "mysql://root:password@localhost/mydb"

def process_user_data(username, age):
    # 缺少文档字符串
    # SQL注入漏洞
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # 未关闭数据库连接 - 资源泄漏
    return results

def calculate_total(items):
    # 性能问题：多次循环
    total = 0
    for item in items:
        total = total + item['price']
    
    tax = 0
    for item in items:
        tax = tax + item['price'] * 0.1
    
    # 魔法数字
    if total > 1000:
        discount = total * 0.15
    else:
        discount = 0
    
    return total + tax - discount

class userManager:  # 命名不符合PEP8规范
    def __init__(self, db):
        self.db = db
        self.users = []
    
    def add_user(self, name, email, pwd):  # 参数命名不清晰
        # 没有输入验证
        user = {
            'name': name,
            'email': email,
            'password': pwd  # 明文存储密码
        }
        self.users.append(user)
    
    def get_user(self, user_id):
        # 低效的查找方式
        for u in self.users:
            if u['id'] == user_id:
                return u
        return None
    
    def delete_user(self, user_id):
        # 可能的索引错误
        for i in range(len(self.users)):
            if self.users[i]['id'] == user_id:
                del self.users[i]
                break

def read_config_file(filename):
    # 缺少异常处理
    f = open(filename, 'r')
    content = f.read()
    # 未关闭文件
    return content

def process_data(data):
    # 函数过长，职责不单一
    result = []
    
    # 深度嵌套
    for item in data:
        if item is not None:
            if 'value' in item:
                if item['value'] > 0:
                    if item['value'] < 100:
                        if item['active']:
                            result.append(item)
    
    # 不必要的列表拼接
    final = []
    for r in result:
        final = final + [r]
    
    return final

def send_email(to, subject, body):
    # 使用危险的命令执行
    import subprocess
    cmd = f"echo '{body}' | mail -s '{subject}' {to}"
    subprocess.call(cmd, shell=True)  # 命令注入风险

# 全局变量使用
counter = 0

def increment():
    # 未使用global关键字
    counter = counter + 1
    return counter

# 未使用的导入
import sys
import json
import requests

# 过于宽泛的异常捕获
def risky_operation():
    try:
        result = 10 / 0
        return result
    except:  # 捕获所有异常
        pass

# 重复代码
def calculate_area_rectangle(width, height):
    return width * height

def calculate_area_square(side):
    return side * side

def calculate_area_triangle(base, height):
    return base * height / 2

# 没有主函数保护
print("Script started")
process_user_data("admin", 25)

