import os
import sqlite3

# 指定数据库文件路径
db_file = 'example_new.db'

# 检查数据库文件是否存在
if os.path.isfile(db_file):
    # 如果文件存在，连接到数据库并读取数据
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT * FROM users")
    data = cursor.fetchall()

    # 将数据写入文件
    with open('data.txt', 'w') as f:
        for row in data:
            f.write(f"id={row[0]}, name={row[1]}, email={row[2]}, age={row[3]}\n")

    # 关闭数据库连接
    conn.close()
else:
    # 如果文件不存在，创建新的数据库文件并插入一条数据
    conn = sqlite3.connect(db_file)
    conn.execute('''CREATE TABLE users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     email TEXT NOT NULL,
                     age INTEGER NOT NULL);''')
    conn.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ('Alice', 'alice@example.com', 25))
    conn.commit()

    # 将数据库保存到本地
    conn.close()

    # 这里只是将新创建的数据库文件复制到当前目录下，实际应用中可以将其保存到特定位置
    os.rename(db_file, 'example_new_new.db')
