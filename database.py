def get_connection():
    import sqlite3
    connection = sqlite3.connect("todos.db")
    return connection