import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import bcrypt
from datetime import datetime

# ===============================
# БАЗА ДАННЫХ
# ===============================

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    period TEXT,
    income REAL,
    brocards REAL,
    rent REAL,
    supplies REAL,
    kpi_enabled INTEGER
)
""")
conn.commit()

# ===============================
# СОЗДАНИЕ ADMIN (если нет)
# ===============================

def create_admin():
    c.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not c.fetchone():
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  ("admin", hashed, "admin"))
        conn.commit()

create_admin()

# ===============================
# АВТОРИЗАЦИЯ
# ===============================

def login():
    st.title("🔐 Вход")

    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user and bcrypt.checkpw(password.encode(), user[2]):
            st.session_state["user"] = user
            st.success("Успешный вход")
            st.rerun()
        else:
            st.error("Неверные данные")

if "user" not in st.session_state:
    login()
    st.stop()

user = st.session_state["user"]

# ===============================
# АДМИН ПАНЕЛЬ
# ===============================

if user[3] == "admin":

    st.sidebar.title("👑 Админ панель")

    if st.sidebar.button("Добавить сотрудника"):
        new_user = st.sidebar.text_input("Логин сотрудника")
        new_pass = st.sidebar.text_input("Пароль", type="password")

        if st.sidebar.button("Создать"):
            hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                      (new_user, hashed, "employee"))
            conn.commit()
            st.success("Сотрудник создан")

    st.header("Добавить расчет")

    employees = pd.read_sql("SELECT * FROM users WHERE role='employee'", conn)
    emp_name = st.selectbox("Сотрудник", employees["username"])
    period = st.date_input("Период")
    income = st.number_input("Доход", 0.0)
    brocards = st.number_input("Brocards", 0.0)
    rent = st.number_input("Аренда", 0.0)
    supplies = st.number_input("Расходники", 0.0)
    kpi = st.checkbox("KPI включен")

    if st.button("Сохранить расчет"):
        user_id = employees[employees["username"] == emp_name]["id"].values[0]
        c.execute("""
        INSERT INTO salaries (user_id, period, income, brocards, rent, supplies, kpi_enabled)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, str(period), income, brocards, rent, supplies, int(kpi)))
        conn.commit()
        st.success("Сохранено")

# ===============================
# СТРАНИЦА СОТРУДНИКА
# ===============================

st.header("📊 Моя зарплата")

if user[3] == "employee":
    data = pd.read_sql(f"SELECT * FROM salaries WHERE user_id={user[0]}", conn)
else:
    data = pd.read_sql("SELECT * FROM salaries", conn)

if not data.empty:

    selected_period = st.selectbox("Выберите период", data["period"].unique())
    row = data[data["period"] == selected_period].iloc[0]

    total_expense = row["brocards"] + row["rent"] + row["supplies"]
    profit = row["income"] - total_expense

    if row["kpi_enabled"] == 1:
        profit = profit * 0.8

    st.metric("Чистая прибыль", f"{profit} $")

    # ===== График =====
    st.subheader("📈 Динамика прибыли")

    data["profit"] = data["income"] - (
        data["brocards"] + data["rent"] + data["supplies"]
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["period"],
        y=data["profit"],
        fill='tozeroy',
        mode='lines+markers',
        name='Чистая прибыль'
    ))

    fig.update_layout(template="simple_white")
    st.plotly_chart(fig)

else:
    st.info("Данных пока нет")