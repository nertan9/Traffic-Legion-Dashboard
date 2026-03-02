import streamlit as st
import sqlite3
import pandas as pd
import bcrypt
from datetime import datetime, timedelta

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(page_title="Team Dashboard", layout="wide", page_icon="📊")

# =====================================================
# THEME CSS (SaaS Dark)
# =====================================================
st.markdown(
    """
<style>
:root{
  --bg:#0B1220;
  --panel:#0F172A;
  --panel2:#0B1324;
  --border:rgba(255,255,255,.08);
  --text:#E5E7EB;
  --muted:#94A3B8;
  --accent:#7C3AED;
  --good:#22C55E;
  --bad:#64748B;
  --warn:#F59E0B;
}

.block-container { padding-top: 28px; }
h1,h2,h3 { letter-spacing: -0.02em; }

.card{
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  border:1px solid var(--border);
  border-radius:16px;
  padding:18px 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,.25);
}

.cardHeader{
  display:flex; align-items:center; justify-content:space-between;
  gap:12px;
  margin-bottom: 10px;
}
.title{
  font-size: 34px; font-weight: 800; margin:0;
}
.subtitle{
  color: var(--muted);
  margin-top: 6px;
}

.kpiRow{
  display:grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}
.kpi{
  background: rgba(255,255,255,.03);
  border:1px solid var(--border);
  border-radius:14px;
  padding: 14px;
}
.kpiLabel{ color: var(--muted); font-size: 12px; }
.kpiValue{ font-size: 20px; font-weight: 800; margin-top: 6px; }

.badge{
  display:inline-flex; align-items:center; gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: 700;
  border:1px solid;
  font-size: 12px;
}
.badgeOpen{
  color: #86EFAC;
  border-color: rgba(34,197,94,.45);
  background: rgba(34,197,94,.08);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(34,197,94,.5);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(34,197,94,0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(34,197,94,0);
  }
}

.kpi{
  transition: all .25s ease;
}

.kpi:hover{
  transform: translateY(-6px);
  border-color: rgba(124,58,237,.55);
  box-shadow: 0 12px 35px rgba(0,0,0,.35);
  background: linear-gradient(180deg, rgba(124,58,237,.08), rgba(255,255,255,.02));
}

.badgePaid{ color: #CBD5E1; border-color: rgba(148,163,184,.35); background: rgba(148,163,184,.10); }

.hr{ height:1px; background: var(--border); margin: 14px 0; }

.tableRow{
  display:grid;
  grid-template-columns: 0.7fr 1.4fr 1fr 1fr 1.6fr 1.2fr 0.9fr;
  gap: 12px;
  align-items:center;
  padding: 12px 10px;
  border-bottom: 1px solid var(--border);
}
.tableHead{
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: .08em;
  padding-top: 6px;
  padding-bottom: 10px;
}
.money{ color: #86EFAC; font-weight: 800; }

.small{ color: var(--muted); font-size: 12px; }

button[kind="secondary"]{
  border-radius:12px;
  border:1px solid var(--border);
  background:rgba(255,255,255,.03);
}

button[kind="secondary"]:hover{
  border-color:rgba(124,58,237,.55);
  background:rgba(124,58,237,.10);
}

.section-title {
  font-size: 14px;
  color: var(--muted);
  margin-top: 10px;
  margin-bottom: 10px;
}

.card-small {
  background: rgba(255,255,255,.03);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 12px;
}

.card-small .label {
  font-size: 12px;
  color: var(--muted);
}

.card-small .value {
  font-size: 18px;
  font-weight: 700;
  margin-top: 6px;
}

/* =========================================
   PREMIUM FADE-IN ANIMATION
========================================= */

.card,
.kpi,
.card-small {
  opacity: 0;
  transform: translateY(16px);
  filter: blur(6px);
  animation: fadeUp .6s cubic-bezier(.22,.61,.36,1) forwards;
}

/* Каскадная задержка для KPI */
.kpi:nth-child(1) { animation-delay: .05s; }
.kpi:nth-child(2) { animation-delay: .1s; }
.kpi:nth-child(3) { animation-delay: .15s; }
.kpi:nth-child(4) { animation-delay: .2s; }
.kpi:nth-child(5) { animation-delay: .25s; }
.kpi:nth-child(6) { animation-delay: .3s; }

/* Для маленьких карточек */
.card-small:nth-child(1) { animation-delay: .08s; }
.card-small:nth-child(2) { animation-delay: .16s; }
.card-small:nth-child(3) { animation-delay: .24s; }

@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(16px);
    filter: blur(6px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

/* ===== SHOP CARD ===== */

.shop-card{
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  border:1px solid var(--border);
  border-radius:14px;
  padding:12px;
  transition: all .2s ease;
}

.shop-card:hover{
  transform: translateY(-4px);
  border-color: rgba(124,58,237,.6);
  box-shadow: 0 10px 25px rgba(0,0,0,.35);
}

.price{
  font-size:16px;
  font-weight:800;
  margin-top:6px;
  margin-bottom:6px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# DATABASE
# =====================================================
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB,
    full_name TEXT,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    year INTEGER,
    week INTEGER,
    income REAL,
    brocards REAL,
    rent REAL,
    supplies REAL,
    bonus REAL DEFAULT 0,
    percent REAL DEFAULT 30,
    usd_rate REAL DEFAULT 77,
    status TEXT DEFAULT 'Открыт',
    created_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    image_url TEXT,
    price INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS reward_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    reward_id INTEGER,
    status TEXT DEFAULT 'Ожидает',
    created_at TEXT
)
""")


conn.commit()

# ===== ДОБАВЛЯЕМ ТЕСТОВЫЕ ТОВАРЫ (ВРЕМЕННО) =====
c.execute("SELECT COUNT(*) FROM rewards")
count = c.fetchone()[0]

if count == 0:
    c.execute("""
        INSERT INTO rewards (name, description, image_url, price)
        VALUES 
        ('AirPods Pro', 'Беспроводные наушники Apple', 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=572&hei=572&fmt=jpeg&qlt=95&.v=1660803972361', 300),
        ('MacBook Air', 'Ноутбук для работы', 'https://static.joxi.pro/1772204915999-8ecbdf94-89c6-4412-879a-744ff2c65f81.jpg', 1000)
    """)
    conn.commit()

# ===================== DB MIGRATION (debt columns) =====================
def ensure_debt_columns():
    try:
        c.execute("ALTER TABLE salaries ADD COLUMN debt_in REAL DEFAULT 0")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE salaries ADD COLUMN debt_out REAL DEFAULT 0")
    except Exception:
        pass
    conn.commit()

def recalc_all_debts():
    users_df = pd.read_sql("SELECT id FROM users WHERE role='employee'", conn)

    for _, u in users_df.iterrows():
        user_id = int(u["id"])

        reports = pd.read_sql(
            """
            SELECT * FROM salaries
            WHERE user_id=?
            ORDER BY year ASC, week ASC, id ASC
            """,
            conn,
            params=(user_id,)
        )

        running_debt = 0.0

        for _, r in reports.iterrows():
            base_profit, adj_profit, salary, total, debt_out = calc_with_debt(
                r["income"],
                r["brocards"],
                r["rent"],
                r["supplies"],
                r["bonus"],
                r["percent"],
                running_debt
            )

            c.execute(
                """
                UPDATE salaries
                SET debt_in=?, debt_out=?
                WHERE id=?
                """,
                (running_debt, debt_out, int(r["id"]))
            )

            running_debt = debt_out

    conn.commit()



# =====================================================
# CREATE ADMIN
# =====================================================
import os

def create_admin():
    try:
        admin_password = st.secrets["ADMIN_PASSWORD"]
    except Exception:
        return  # если локально нет secrets — просто не создаём

    c.execute("SELECT 1 FROM users WHERE username='admin'")
    if not c.fetchone():
        hashed = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt())
        c.execute(
            "INSERT INTO users (username,password,full_name,role) VALUES (?,?,?,?)",
            ("admin", hashed, "Администратор", "admin")
        )
        conn.commit()

create_admin()

# =====================================================
# HELPERS
# =====================================================
def get_week_range(year: int, week: int):
    first_day = datetime.strptime(f"{year}-W{week}-1", "%G-W%V-%u")
    last_day = first_day + timedelta(days=6)
    return first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")

def money(x):
    return f"{round(float(x), 2):,.2f}".replace(",", " ")

def calc_with_debt(income, brocards, rent, supplies, bonus, percent, debt_in):
    """
    debt_in: 0 или отрицательное число (например -1200).
    Минус вычитается из ПРИБЫЛИ недели:
      base_profit = income - expenses
      adj_profit  = base_profit + debt_in   (debt_in отрицательный => уменьшает прибыль)
      salary      = max(adj_profit, 0) * percent
      debt_out    = min(adj_profit, 0)      (если всё ещё минус — переносим дальше)
      total       = max(salary + bonus, 0)
    """
    income = float(income)
    brocards = float(brocards)
    rent = float(rent)
    supplies = float(supplies)
    bonus = float(bonus)
    percent = float(percent)
    debt_in = float(debt_in)

    expenses = brocards + rent + supplies
    base_profit = income - expenses
    adj_profit = base_profit + debt_in

    if adj_profit <= 0:
        salary = 0.0
    else:
        salary = adj_profit * (percent / 100.0)

    total = max(salary + bonus, 0.0)
    debt_out = min(adj_profit, 0.0)

    return base_profit, adj_profit, salary, total, debt_out

def calc_total(income, brocards, rent, supplies, bonus):
    profit = income - (brocards + rent + supplies)

    # зарплата не может быть отрицательной
    if profit <= 0:
        salary = 0
    else:
        salary = profit * 0.30

    total = salary + bonus

    return profit, salary, total

def get_user_points(user_id):
    return 350  # временно фиксированное число

ensure_debt_columns()
recalc_all_debts()



# =====================================================
# AUTH
# =====================================================
def login():
    st.markdown("<div class='card'><h1 class='title'>🔐 Вход</h1><div class='subtitle'>Team Dashboard</div></div>", unsafe_allow_html=True)
    st.write("")
    colA, colB, colC = st.columns([1.1, 1.1, 1.4])
    with colA:
        username = st.text_input("Логин", key="login_user")
    with colB:
        password = st.text_input("Пароль", type="password", key="login_pass")
    with colC:
        st.write("")
        st.write("")
        if st.button("Войти →", use_container_width=True):
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            u = c.fetchone()
            if u and bcrypt.checkpw(password.encode(), u[2]):
                st.session_state["user"] = u
                st.rerun()
            st.error("Неверный логин или пароль")

if "user" not in st.session_state:
    login()
    st.stop()

user = st.session_state["user"]

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown(f"### 👤 {user[3]}")
if st.sidebar.button("🚪 Выйти", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# =====================================================
# ADMIN
# =====================================================

if user[4] == "admin":

    menu = st.sidebar.radio("Навигация", [
    "Создать сотрудника",
    "Создать отчет",
    "Все отчеты",
    "Магазин"
    ])

    # =====================================================
    #  МАГАЗИН
    # =====================================================

    if menu == "Магазин":

        st.markdown("<h1 class='title'>🎁 Магазин наград</h1><div class='subtitle'>Обмен очков на подарки</div>", unsafe_allow_html=True)

        rewards = pd.read_sql("SELECT * FROM rewards", conn)

        if rewards.empty:
            st.info("Пока нет товаров")
            st.stop()

        user_points = get_user_points(user[0])

        st.markdown(f"<div class='card'><b>Ваши очки:</b> {user_points}</div>", unsafe_allow_html=True)
        st.write("")

        cols = st.columns(4)

        for i, (_, r) in enumerate(rewards.iterrows()):
            with cols[i % 3]:

                enough = user_points >= r["price"]

                st.markdown("<div class='shop-card'>", unsafe_allow_html=True)

                st.image(r["image_url"], width=140)

                st.markdown(f"<div style='font-weight:700; font-size:14px'>{r['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='small'>{r['description']}</div>", unsafe_allow_html=True)

                price_color = "#22C55E" if enough else "#EF4444"

                st.markdown(
                    f"<div class='price' style='color:{price_color}'>{r['price']} очков</div>",
                    unsafe_allow_html=True
                )

                if st.button(
                    "Обменять",
                    key=f"buy_{r['id']}",
                    disabled=not enough,
                    use_container_width=True
                ):
                    c.execute(
                        "INSERT INTO reward_orders (user_id, reward_id, created_at) VALUES (?, ?, ?)",
                        (user[0], r["id"], datetime.now().strftime("%Y-%m-%d %H:%M"))
                    )
                    conn.commit()
                    st.success("Запрос на получение подарка отправлен")

                st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # СОЗДАТЬ СОТРУДНИКА
    # =====================================================
    if menu == "Создать сотрудника":
        st.markdown("<h1 class='title'>👥 Сотрудники</h1><div class='subtitle'>Создание аккаунта сотрудника</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        full_name = st.text_input("Имя сотрудника (для отображения)")
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")

        if st.button("Создать", use_container_width=True):
            if not full_name or not username or not password:
                st.warning("Заполни все поля")
            else:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                try:
                    c.execute(
                        "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                        (username, hashed, full_name, "employee"),
                    )
                    conn.commit()
                    st.success("Сотрудник создан")
                except:
                    st.error("Логин уже существует")
        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # СОЗДАТЬ ОТЧЕТ  (перенос долга тут работает)
    # =====================================================
    if menu == "Создать отчет":
        st.markdown("<h1 class='title'>➕ Новый отчет</h1><div class='subtitle'>Создание отчёта за неделю</div>", unsafe_allow_html=True)

        employees = pd.read_sql("SELECT id, full_name FROM users WHERE role='employee'", conn)
        if employees.empty:
            st.info("Сначала создай сотрудника")
            st.stop()

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        emp_name = st.selectbox("Сотрудник", employees["full_name"])
        user_id = int(employees.loc[employees["full_name"] == emp_name, "id"].values[0])

        colA, colB, colC = st.columns(3)
        year = int(colA.number_input("Год", value=datetime.now().year))
        week = int(colB.number_input("Неделя (ISO)", min_value=1, max_value=53, value=int(datetime.now().isocalendar().week)))
        usd_rate = float(colC.number_input("Курс USD (₽)", value=77.0, step=1.0))

        start, end = get_week_range(year, week)
        st.caption(f"Период: {start} — {end}")

        col1, col2, col3 = st.columns(3)
        income = float(col1.number_input("Доход ($)", 0.0))
        bonus = float(col2.number_input("Премия ($)", 0.0))
        percent = float(col3.number_input("Процент сотрудника (%)", value=30.0, min_value=0.0, max_value=100.0))

        col4, col5, col6 = st.columns(3)
        brocards = float(col4.number_input("Brocards ($)", 0.0))
        rent = float(col5.number_input("Аренда ($)", 0.0))
        supplies = float(col6.number_input("Расходники ($)", 0.0))

        # долг из прошлого отчета
        c.execute("""
            SELECT debt_out
            FROM salaries
            WHERE user_id = ?
            ORDER BY year DESC, week DESC, id DESC
            LIMIT 1
        """, (user_id,))
        prev = c.fetchone()
        debt_in = float(prev[0]) if prev and prev[0] is not None else 0.0

        base_profit, adj_profit, salary, total, debt_out = calc_with_debt(
            income, brocards, rent, supplies, bonus, percent, debt_in
        )

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="kpiRow">
  <div class="kpi"><div class="kpiLabel">Долг из прошлого</div><div class="kpiValue">{money(debt_in)} $</div></div>
  <div class="kpi"><div class="kpiLabel">Прибыль недели</div><div class="kpiValue">{money(base_profit)} $</div></div>
  <div class="kpi"><div class="kpiLabel">Прибыль с долгом</div><div class="kpiValue">{money(adj_profit)} $</div></div>
  <div class="kpi"><div class="kpiLabel">Долг дальше</div><div class="kpiValue">{money(debt_out)} $</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

        status = st.selectbox("Статус", ["Открыт", "Выплачен"], index=0)

        if st.button("Сохранить отчет", use_container_width=True):
            c.execute(
                """
                INSERT INTO salaries
                (user_id, year, week, income, brocards, rent, supplies, bonus, percent, usd_rate, status, created_at, debt_in, debt_out)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id, year, week,
                    income, brocards, rent, supplies,
                    bonus, percent, usd_rate,
                    status, datetime.now().strftime("%Y-%m-%d %H:%M"),
                    debt_in, debt_out
                ),
            )
            conn.commit()
            st.success("Отчет создан")

        st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # ВСЕ ОТЧЕТЫ (РЕДАКТИРОВАНИЕ)
    # =====================================================
    if menu == "Все отчеты":

        st.markdown("<h1 class='title'>📚 Все отчеты</h1><div class='subtitle'>Редактирование и пересчёт задолженности</div>", unsafe_allow_html=True)

        reports = pd.read_sql(
            """
            SELECT s.*, u.full_name
            FROM salaries s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.year DESC, s.week DESC, s.id DESC
            """,
            conn,
        )

        if reports.empty:
            st.info("Нет отчетов")
            st.stop()

        # удобный список выбора (как ты хотел: сотрудник + период + статус)
        options = []
        for _, r in reports.iterrows():
            start, end = get_week_range(int(r["year"]), int(r["week"]))
            label = f"#{int(r['id'])} — {r['full_name']} — {start} - {end} — {r['status']}"
            options.append((label, int(r["id"])))

        picked = st.selectbox("Выберите отчет", options, format_func=lambda x: x[0])
        selected_id = picked[1]

        report = reports[reports["id"] == selected_id].iloc[0]
        start, end = get_week_range(int(report["year"]), int(report["week"]))

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(
            f"### ✏️ Отчет #{selected_id}  \n<span class='small'>{report['full_name']} • {start} — {end}</span>",
            unsafe_allow_html=True
        )

        # поля редактирования
        col1, col2 = st.columns(2)
        income = col1.number_input("Доход ($)", value=float(report["income"]))
        bonus = col2.number_input("Премия ($)", value=float(report["bonus"]))

        col3, col4, col5 = st.columns(3)
        brocards = col3.number_input("Brocards ($)", value=float(report["brocards"]))
        rent = col4.number_input("Аренда ($)", value=float(report["rent"]))
        supplies = col5.number_input("Расходники ($)", value=float(report["supplies"]))

        colA, colB = st.columns(2)
        usd_rate = colA.number_input("Курс USD (₽)", value=float(report["usd_rate"]))
        percent = colA.number_input("Процент сотрудника (%)", value=float(report["percent"]), min_value=0.0, max_value=100.0)
        status = colB.selectbox("Статус", ["Открыт", "Выплачен"], index=0 if report["status"] == "Открыт" else 1)

        # debt_in НЕ редактируем руками: он приходит из прошлого отчёта
        debt_in = float(report["debt_in"]) if "debt_in" in report and report["debt_in"] is not None else 0.0

        # ✅ пересчёт по новой логике (долг вычитается из прибыли, а не из дохода)
        base_profit, adj_profit, salary, total, debt_out = calc_with_debt(
            income, brocards, rent, supplies, bonus, percent, debt_in
        )

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
    <div class="kpiRow">
      <div class="kpi"><div class="kpiLabel">Задолженность (в отчёт)</div><div class="kpiValue">{money(debt_in)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Прибыль недели</div><div class="kpiValue">{money(base_profit)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Прибыль с учетом долга</div><div class="kpiValue">{money(adj_profit)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Долг дальше</div><div class="kpiValue">{money(debt_out)} $</div></div>
    </div>
    <div class="hr"></div>
    <div class="kpiRow">
      <div class="kpi"><div class="kpiLabel">Зарплата</div><div class="kpiValue money">{money(salary)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Премия</div><div class="kpiValue">{money(bonus)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Итого ($)</div><div class="kpiValue money">{money(total)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Итого (₽)</div><div class="kpiValue">{money(total * usd_rate)} ₽</div></div>
    </div>
    """,
            unsafe_allow_html=True,
        )

        if st.button("💾 Сохранить изменения", use_container_width=True):
            c.execute(
                """
                UPDATE salaries SET
                  income=?,
                  brocards=?,
                  rent=?,
                  supplies=?,
                  bonus=?,
                  usd_rate=?,
                  percent=?,
                  status=?,
                  debt_out=?
                WHERE id=?
                """,
                (
                    income, brocards, rent, supplies,
                    bonus, usd_rate, percent, status,
                    debt_out, selected_id
                ),
            )
            conn.commit()
            recalc_all_debts()
            st.success("Сохранено")
            st.rerun()

        st.write("")

        if st.button("🗑 Удалить отчет", use_container_width=True):
            c.execute("DELETE FROM salaries WHERE id=?", (selected_id,))
            conn.commit()
            recalc_all_debts()
            st.success("Отчет удален")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# EMPLOYEE
# =====================================================
if user[4] == "employee":

    st.markdown("<h1 class='title'>📄 Мои отчеты</h1>", unsafe_allow_html=True)

    user_id = int(user[0])
    full_name = user[3]

    data = pd.read_sql(
        "SELECT * FROM salaries WHERE user_id=? ORDER BY id DESC",
        conn,
        params=(user_id,)
    )

    if data.empty:
        st.info("Пока нет отчетов")
        st.stop()

    if "selected_report" not in st.session_state:
        st.session_state["selected_report"] = None

    # =========================
    # LIST
    # =========================
    if st.session_state["selected_report"] is None:

        header_cols = st.columns([0.6, 1.5, 1, 1, 1.6, 1.3])
        header_cols[0].markdown("<span class='small'>ID</span>", unsafe_allow_html=True)
        header_cols[1].markdown("<span class='small'>Сотрудник</span>", unsafe_allow_html=True)
        header_cols[2].markdown("<span class='small'>Выплата</span>", unsafe_allow_html=True)
        header_cols[3].markdown("<span class='small'>Статус</span>", unsafe_allow_html=True)
        header_cols[4].markdown("<span class='small'>Период</span>", unsafe_allow_html=True)
        header_cols[5].markdown("<span class='small'>Создан</span>", unsafe_allow_html=True)

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        for _, row in data.iterrows():

            start, end = get_week_range(int(row["year"]), int(row["week"]))

            income = float(row["income"])
            brocards = float(row["brocards"])
            rent = float(row["rent"])
            supplies = float(row["supplies"])
            bonus = float(row["bonus"])
            percent = float(row["percent"])

            # ✅ долг из прошлого отчёта (0 или отрицательный)
            debt_in = float(row["debt_in"]) if "debt_in" in row and row["debt_in"] is not None else 0.0

            # ✅ расчёт с учётом долга (минус вычитается из ПРИБЫЛИ)
            base_profit, adj_profit, salary, total_payment, debt_out = calc_with_debt(
                income, brocards, rent, supplies, bonus, percent, debt_in
            )

            badge = (
                "<span class='badge badgeOpen'>Открыт</span>"
                if row["status"] == "Открыт"
                else "<span class='badge badgePaid'>Выплачен</span>"
            )

            cols = st.columns([0.6, 1.5, 1, 1, 1.6, 1.3])

            with cols[0]:
                if st.button(str(int(row["id"])), key=f"row_{int(row['id'])}"):
                    st.session_state["selected_report"] = int(row["id"])
                    st.rerun()

            cols[1].markdown(full_name)
            cols[2].markdown(f"<span class='money'>{money(total_payment)} $</span>", unsafe_allow_html=True)
            cols[3].markdown(badge, unsafe_allow_html=True)
            cols[4].markdown(f"{start} - {end}")
            cols[5].markdown(row["created_at"] or "-")

            st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # =========================
    # DETAIL
    # =========================
    else:

        report_id = int(st.session_state["selected_report"])
        report = data[data["id"] == report_id].iloc[0]
        start, end = get_week_range(int(report["year"]), int(report["week"]))

        income = float(report["income"])
        brocards = float(report["brocards"])
        rent = float(report["rent"])
        supplies = float(report["supplies"])
        bonus = float(report["bonus"])
        usd_rate = float(report["usd_rate"])
        percent = float(report["percent"])

        # ✅ долг из прошлого отчёта (0 или отрицательный)
        debt_in = float(report["debt_in"]) if "debt_in" in report and report["debt_in"] is not None else 0.0

        # ✅ единый расчёт: минус вычитается из ПРИБЫЛИ недели
        base_profit, adj_profit, salary, total_payment, debt_out = calc_with_debt(
            income, brocards, rent, supplies, bonus, percent, debt_in
        )

        total_expense = brocards + rent + supplies
        rub_total = total_payment * usd_rate

        badge = (
            "<span class='badge badgeOpen'>Открыт</span>"
            if report["status"] == "Открыт"
            else "<span class='badge badgePaid'>Выплачен</span>"
        )

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        # HEADER
        st.markdown(
            f"""
    <div class="cardHeader">
      <div>
        <div style="font-size:18px; font-weight:800;">
          Отчет • {start} — {end}
        </div>
        <div class="small">{full_name}</div>
      </div>
      <div>{badge}</div>
    </div>
    <div class="hr"></div>
    """,
            unsafe_allow_html=True,
        )

        # KPI BLOCK 1
        st.markdown(
            f"""
    <div class="kpiRow">
      <div class="kpi"><div class="kpiLabel">Курс USD</div><div class="kpiValue">{money(usd_rate)} ₽</div></div>
      <div class="kpi"><div class="kpiLabel">Доход</div><div class="kpiValue">{money(income)} $</div></div>
      <div class="kpi"><div class="kpiLabel">Расход</div><div class="kpiValue">{money(total_expense)} $</div></div>
      <div class="kpi">
        <div class="kpiLabel">Прибыль недели</div>
        <div class="kpiValue" style="color:{'#EF4444' if base_profit < 0 else '#E5E7EB'};">
          {money(base_profit)} $
        </div>
      </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

        if brocards > 0 or rent > 0 or supplies > 0:

            st.markdown("<div class='section-title'>Структура расходов</div>", unsafe_allow_html=True)

            exp_cols = st.columns(3)

            with exp_cols[0]:
                if brocards > 0:
                    st.markdown(f"""
                        <div class='card-small'>
                            <div class='label'>Brocards</div>
                            <div class='value'>{money(brocards)} $</div>
                        </div>
                    """, unsafe_allow_html=True)

            with exp_cols[1]:
                if rent > 0:
                    st.markdown(f"""
                        <div class='card-small'>
                            <div class='label'>Аренда</div>
                            <div class='value'>{money(rent)} $</div>
                        </div>
                    """, unsafe_allow_html=True)

            with exp_cols[2]:
                if supplies > 0:
                    st.markdown(f"""
                        <div class='card-small'>
                            <div class='label'>Расходники</div>
                            <div class='value'>{money(supplies)} $</div>
                        </div>
                    """, unsafe_allow_html=True)

        if debt_in < 0 or debt_out < 0:
            # вывод блока долга
            st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        # KPI BLOCK 2 (долг + прибыль с учетом долга)
        

        # =========================
        # БЛОК С ДОЛГОМ (ТОЛЬКО ЕСЛИ ОН ЕСТЬ)
        # =========================
        if debt_in < 0 or debt_out < 0:

            st.markdown(
                f"""
        <div class="kpiRow">
          <div class="kpi">
            <div class="kpiLabel">Задолженность с прошлого отчёта</div>
            <div class="kpiValue" style="color:{'#EF4444' if debt_in < 0 else '#E5E7EB'};">
              {money(debt_in)} $
            </div>
          </div>

          <div class="kpi">
            <div class="kpiLabel">Прибыль с учетом долга</div>
            <div class="kpiValue" style="color:{'#EF4444' if adj_profit < 0 else '#E5E7EB'};">
              {money(adj_profit)} $
            </div>
          </div>

          <div class="kpi">
            <div class="kpiLabel">Долг, который уйдет дальше</div>
            <div class="kpiValue" style="color:{'#EF4444' if debt_out < 0 else '#E5E7EB'};">
              {money(debt_out)} $
            </div>
          </div>

          
        </div>
        """,
                unsafe_allow_html=True,
            )

        # =========================
        # ЗАРПЛАТА + ПРЕМИЯ (ВСЕГДА)
        # =========================
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        if bonus > 0:
            st.markdown(
                f"""
        <div class="kpiRow">
          <div class="kpi">
            <div class="kpiLabel">Зарплата ({percent}%)</div>
            <div class="kpiValue money">{money(salary)} $</div>
          </div>

          <div class="kpi">
            <div class="kpiLabel">💰 Премия</div>
            <div class="kpiValue" style="color:#FBBF24;">
              {money(bonus)} $
            </div>
          </div>
        </div>
        """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
        <div class="kpiRow">
          <div class="kpi">
            <div class="kpiLabel">Зарплата ({percent}%)</div>
            <div class="kpiValue money">{money(salary)} $</div>
          </div>
        </div>
        """,
                unsafe_allow_html=True,
            )
        

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        st.markdown(
            f"""
        <div class="kpiRow">
          <div class="kpi">
            <div class="kpiLabel">Итого ($)</div>
            <div class="kpiValue money">{money(total_payment)} $</div>
          </div>
          <div class="kpi">
            <div class="kpiLabel">Итого (₽)</div>
            <div class="kpiValue">{money(rub_total)} ₽</div>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")
        if st.button("← Назад к списку", use_container_width=True):
            st.session_state["selected_report"] = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)