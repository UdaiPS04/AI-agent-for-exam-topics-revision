import sqlite3
from datetime import datetime, timedelta

DB = "srs_agent.db"
DEFAULT_EASINESS = 2.5
MIN_EASINESS = 1.3

# Database Setup
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY,
        topic TEXT UNIQUE,
        content TEXT,
        easiness REAL,
        interval INTEGER,
        repetitions INTEGER,
        next_review TEXT
    )
    """)
    conn.commit()
    conn.close()

# Core Functions
def add_card(topic, content):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute("""
        INSERT OR REPLACE INTO cards (topic, content, easiness, interval, repetitions, next_review)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (topic, content, DEFAULT_EASINESS, 0, 0, now))
    conn.commit()
    conn.close()
    print(f"✅ Added topic: {topic}")

def get_due_cards():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, topic, content, easiness, interval, repetitions, next_review FROM cards")
    rows = cur.fetchall()
    conn.close()
    now = datetime.now()
    return [r for r in rows if datetime.fromisoformat(r[6]) <= now]

def update_card(card_id, quality):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT easiness, interval, repetitions FROM cards WHERE id=?", (card_id,))
    easiness, interval, reps = cur.fetchone()

    # SM-2 algorithm
    easiness = max(MIN_EASINESS, easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    if quality < 3:
        reps, interval = 0, 1
    else:
        reps += 1
        interval = 1 if reps == 1 else 6 if reps == 2 else int(interval * easiness)

    next_review = (datetime.now() + timedelta(days=interval)).isoformat()
    cur.execute("UPDATE cards SET easiness=?, interval=?, repetitions=?, next_review=? WHERE id=?",
                (easiness, interval, reps, next_review, card_id))
    conn.commit()
    conn.close()

def review_session():
    due = get_due_cards()
    if not due:
        print("🎉 No topics due!")
        return
    for c in due:
        print(f"\n📘 {c[1]}:\n{c[2]}")
        try:
            q = int(input("👉 Rate recall (0–5): "))
        except:
            q = 2
        update_card(c[0], q)
        print("✅ Progress saved.")

def review_all():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, topic, content FROM cards")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("⚠️ No topics available.")
        return

    for r in rows:
        print(f"\n📘 {r[1]}:\n{r[2]}")
        try:
            q = int(input("👉 Rate recall (0–5): "))
        except:
            q = 2
        update_card(r[0], q)
        print("✅ Progress saved.")

def list_cards():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT topic, next_review FROM cards")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("⚠️ No topics found.")
    else:
        print("\n📖 Topics in Database:")
        for t, nr in rows:
            print(f"- {t} (Next review: {nr.split('T')[0]})")
# Menu System
def menu():
    init_db()
    while True:
        print("\n===== Revision Agent =====")
        print("1. Add topic")
        print("2. Review due topics")
        print("3. List topics")
        print("4. Exit")
        print("5. Revise all topics")   # NEW OPTION
        ch = input("Choice: ").strip()

        if ch == "1":
            t = input("Topic: "); c = input("Notes: ")
            add_card(t, c)
        elif ch == "2":
            review_session()
        elif ch == "3":
            list_cards()
        elif ch == "4":
            print("👋 Bye! See you tomorrow.")
            break
        elif ch == "5":
            review_all()
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()