import sqlite3

conn = sqlite3.connect("cases.db")
cursor = conn.cursor()

print("---- priority = 1 ----")
for row in cursor.execute("SELECT * FROM cases WHERE priority = 1"):
    print(row)

print("---- order by priority desc ----")
for row in cursor.execute("SELECT * FROM cases ORDER BY priority DESC"):
    print(row)

print("---- limit 2 offset 1 ----")
for row in cursor.execute("SELECT * FROM cases LIMIT 2 OFFSET 1"):
    print(row)

print("---- count ----")
count = cursor.execute("SELECT COUNT(*) FROM cases").fetchone()
print(count)

print("---- update ----")
cursor.execute("UPDATE cases SET priority = 2 WHERE id = 1")
conn.commit()

conn.close()
