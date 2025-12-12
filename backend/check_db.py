import sqlite3

con = sqlite3.connect("healthybite.db")
cur = con.cursor()

print("Tables in DB:")
rows = cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
for (name,) in rows:
    print(" -", name)

con.close()
