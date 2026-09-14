import sqlite3

connection = sqlite3.connect("todos.db")

sqlite3.Cursor.execute(connection)