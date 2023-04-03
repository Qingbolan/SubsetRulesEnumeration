import os
# from sqlite3 import DatabaseError

import sqlite3


class Database:
    def __init__(self):
        # 指定数据库文件路径
        self.db_file = "history.db"

        # 检查数据库文件是否存在
        if os.path.isfile(self.db_file):
            # 如果文件存在，连接到数据库并读取数据
            self.conn = sqlite3.connect(self.db_file)

            #
            # # 将数据写入文件
            # with open('data.txt', 'w') as f:
            #     for row in data:
            #         f.write(f"$>id={row[0]}, m={row[1]}, n={row[2]}, k={row[3]}, j={row[4]}, s={row[5]}\n")
            #         f.write(f"  >minimum_size={row[7]}..............\n")
            #         f.write(f"  >set={row[6]}\n")
            #         # No = 1
            #         # sets= list(row[6])
            #         # for _ in sets:
            #         #     f.write(f"   {No}. {_}\n")
            #         #     No += 1
        else:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute('''CREATE TABLE  subsets
                                       (id INTEGER PRIMARY KEY,
                                       m INTEGER,
                                       n INTEGER,
                                       k INTEGER,
                                       j INTEGER,
                                       s INTEGER,
                                       reS TEXT,
                                       reL INTEGER);''')
            self.conn.commit()

            # 将数据库保存到本地
            # self.save()

            # 这里只是将新创建的数据库文件复制到当前目录下，实际应用中可以将其保存到特定位置
            # os.rename(self.db_file, 'history.db')

    def insert(self, m, n, k, j, s, reS, reL):
        self.conn.execute('''INSERT INTO subsets(m, n, k, j, s, reS, reL)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (m, n, k, j, s, str(reS), reL))
        self.conn.commit()

    def get_all(self):
        self.cursor = self.conn.execute("SELECT * FROM subsets")
        data = self.cursor.fetchall()
        return data

    def get_by_n_k_j_s(self, n, k, j, s):
        self.cursor = self.conn.execute('SELECT reS, reL FROM subsets WHERE n=? and k=? and j=? and s=?', (n, k, j, s))
        row = self.cursor.fetchone()
        if row is None:  # If no record is found
            return False, []
        print("Got it from database!")
        return True, row  # Return the row as a tuple

    # def save(self):
        # Save database to file
        # os.rename(self.db_file, 'history.db')

    def load(self):
        # Load database from file
        if os.path.isfile(self.db_file):
            with open(self.db_file, 'r') as f:
                self.conn = sqlite3.connect(':memory:')
                self.cursor = self.conn.cursor()
                self.cursor.executescript(f.read())
                self.conn.commit()

    def display(self):
        data = self.get_all()
        # 将数据写入文件
        with open('data.txt', 'w') as f:
            for row in data:
                f.write(f"$>id={row[0]}, m={row[1]}, n={row[2]}, k={row[3]}, j={row[4]}, s={row[5]}\n")
                f.write(f"  >minimum_size={row[7]}..............\n")
                # f.write(f"  >set={row[6]}\n")
                No = 1
                sets= eval(row[6])
                for _ in sets:
                    f.write(f"   {No}. {_}\n")
                    No += 1

    def close(self):
        self.conn.close()

# # Create database object and initialize table
# db = Database('history.db')
#
# # Add record to database
# db.insert(45, 8, 6, 4, 4, [[1, 2, 3, 4, 7, 8], [1, 2, 3, 5, 7, 8], [1, 2, 3, 6, 7, 8], [1, 2, 4, 5, 6, 7], [1, 3, 4, 5, 6, 8], [2, 3, 4, 5, 6, 8], [3, 4, 5, 6, 7, 8]], 7)
#
# # Query database using n, k, j, s as index
# n = 8
# k = 6
# j = 4
# s = 4
#
# results = db.get_by_n_k_j_s(n, k, j, s)
#
# if not results:
#     print("No results found.")
# else:
#     for result in results:
#         print("reS:", result[0])
#         print("reL:", result[1])
#
# # Save changes and close database
# db.save()
# db.close()
