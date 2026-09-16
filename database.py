import sqlite3

class User:
    def __init__(self, id: int, city: str | None = None):
        self.id = id
        self.city = city

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db")
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def get_user(self, id: int) -> User | None:
        query = "SELECT * FROM users WHERE id = ?"
        args = (id,)
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        if row is None:
            return None
        return User(id=id, city=row[1])

    def create_user(self, id: int):
        query = "INSERT INTO users (id) VALUES (?)"
        args = (id,)
        self.cursor.execute(query, args)
        self.connection.commit()

    def set_city(self, id: int, city: str):
        query = "UPDATE users SET city = ? WHERE id = ?"
        args = (city, id)
        self.cursor.execute(query, args)
        self.connection.commit()




