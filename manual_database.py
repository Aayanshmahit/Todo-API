import sqlite3

connection = sqlite3.connect("todos.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM todos")

rows = cursor.fetchall()

print(rows)

cursor.execute("""
    INSERT INTO todos(title, description , completion)
    VALUES('fastapi' , 'learn fast api' , false)
""")
connection.commit()

cursor.execute("""
    INSERT INTO todos(title, description , completion)
    VALUES('crud' , 'learned curd' , true)
""")
connection.commit()

cursor.execute("""
    INSERT INTO todos(title, description , completion)
    VALUES('sunday' , 'enjoy weekend' , true)
""")
connection.commit()

cursor.execute("""
    UPDATE todos
    set completion = true
    where id = 1""")
connection.commit()

cursor.execute("""
    DELETE from todos
    where id = 1""")
connection.commit()

cursor.execute("""SELECT * FROM todos""")
rows = cursor.fetchall()