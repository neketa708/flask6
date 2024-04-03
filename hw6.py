from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect('online_store.db')
cursor = conn.cursor()

# Создание таблиц в базе данных
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, order_date TEXT, status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL)''')
conn.commit()

app = FastAPI()

# Модель данных для таблицы пользователей
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str

# Модель данных для таблицы заказов
class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str

# Модель данных для таблицы товаров
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

# CRUD операции для таблицы пользователей
@app.post("/users/")
async def create_user(user: User):
    cursor.execute('''INSERT INTO users (id, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)''', (user.id, user.first_name, user.last_name, user.email, user.password))
    conn.commit()
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = cursor.execute('''SELECT * FROM users WHERE id = ?''', (user_id,)).fetchone()
    if user:
        return User(id=user[0], first_name=user[1], last_name=user[2], email=user[3], password=user[4])
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    cursor.execute('''UPDATE users SET first_name = ?, last_name = ?, email = ?, password = ? WHERE id = ?''', (user.first_name, user.last_name, user.email, user.password, user_id))
    conn.commit()
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    conn.commit()
    return {"message": "User deleted successfully"}

# Аналогичные CRUD операции для таблицы заказов и таблицы товаров

# Запуск сервера FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)