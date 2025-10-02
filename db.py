import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        source TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        user_id BIGINT PRIMARY KEY,
        items TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_workout(text, source="manual"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO workouts (text, source) VALUES (%s, %s)", (text, source))
    conn.commit()
    conn.close()

def get_random_workout():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT text FROM workouts ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "Нет тренировок в базе."

def set_inventory(user_id, items):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventory (user_id, items)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO UPDATE SET items = EXCLUDED.items
    """, (user_id, items))
    conn.commit()
    conn.close()

def get_inventory(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT items FROM inventory WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "Инвентарь не задан."
