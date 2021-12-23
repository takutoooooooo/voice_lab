import sqlite3

conn = sqlite3.connect("todo.db")

c = conn.cursor()

c.execute("select * from train")

list = c.fetchall()

print(list[0][1])

conn.close()