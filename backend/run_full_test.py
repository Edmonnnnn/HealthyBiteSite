import requests
import sqlite3
import json
import time

API = "http://127.0.0.1:8810"
DB_PATH = "healthybite.db"

# -------------------------------------------------------
# Utility helpers
# -------------------------------------------------------

def line():
    print("-" * 60)


def check_db_table(table, limit=5):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    rows = cur.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT {limit};").fetchall()
    con.close()
    return rows


def pretty(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)


# -------------------------------------------------------
# TEST 1 — HEALTH
# -------------------------------------------------------

def test_health():
    print("\nTEST: HEALTH CHECK")
    try:
        r = requests.get(f"{API}/health")
        print("Status:", r.status_code)
        print("Response:", r.json())
        return r.status_code == 200
    except Exception as e:
        print("ERROR:", e)
        return False


# -------------------------------------------------------
# TEST 2 — BLOG
# -------------------------------------------------------

def test_blog():
    print("\nTEST: BLOG API")
    ok = True

    # Try sections
    try:
        r = requests.get(f"{API}/api/v1/blog/sections?lang=en")
        print("GET /sections:", r.status_code)
        if r.status_code != 200:
            ok = False
        else:
            print("Sections keys:", list(r.json().keys()))
    except Exception as e:
        print("ERROR:", e)
        ok = False

    # Check DB contents
    rows = check_db_table("blog_posts")
    print("Rows in blog_posts:", len(rows))
    if len(rows) == 0:
        print("WARNING: blog_posts table is empty (API still works, but frontend will show empty sections).")

    return ok


# -------------------------------------------------------
# TEST 3 — CONTACT SUPPORT & CONSULT
# -------------------------------------------------------

def test_contact():
    print("\nTEST: CONTACT API")

    ok = True

    payload_support = {
        "name": "TestUser",
        "email": "test@example.com",
        "topic": "Testing support",
        "message": "Support message test",
        "lang": "en"
    }

    payload_consult = {
        "name": "TestConsult",
        "email": "consult@example.com",
        "preferredChannel": "email",
        "preferredTime": "evening",
        "message": "Consultation message test",
        "lang": "en"
    }

    try:
        r1 = requests.post(f"{API}/api/v1/contact/support", json=payload_support)
        print("POST /support:", r1.status_code, r1.json())
        if r1.status_code != 200:
            ok = False

        r2 = requests.post(f"{API}/api/v1/contact/consult", json=payload_consult)
        print("POST /consult:", r2.status_code, r2.json())
        if r2.status_code != 200:
            ok = False

    except Exception as e:
        print("ERROR:", e)
        ok = False

    time.sleep(0.3)

    rows_support = check_db_table("contact_support_requests")
    rows_consult = check_db_table("contact_consult_requests")

    print("Rows in contact_support_requests:", len(rows_support))
    print("Rows in contact_consult_requests:", len(rows_consult))

    if len(rows_support) == 0 or len(rows_consult) == 0:
        ok = False

    return ok


# -------------------------------------------------------
# TEST 4 — AI CHAT
# -------------------------------------------------------

def test_ai():
    print("\nTEST: AI CHAT")

    ok = True

    payload = {
        "lang": "en",
        "sessionId": "sess_test_123",
        "messages": [
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Hello AI"}
        ]
    }

    try:
        r = requests.post(f"{API}/api/v1/ai/chat", json=payload)
        print("POST /ai/chat:", r.status_code)
        print("Response:", pretty(r.json()))

        if r.status_code != 200:
            ok = False

    except Exception as e:
        print("ERROR:", e)
        ok = False

    time.sleep(0.3)

    rows = check_db_table("ai_chat_logs")
    print("Rows in ai_chat_logs:", len(rows))

    if len(rows) == 0:
        ok = False

    return ok


# -------------------------------------------------------
# MAIN RUN
# -------------------------------------------------------

if __name__ == "__main__":
    print("\nRUNNING FULL HEALTH CHECK FOR HealthyBite BACKEND + DATABASE")
    line()

    results = {
        "health": test_health(),
        "blog": test_blog(),
        "contact": test_contact(),
        "ai": test_ai(),
    }

    line()
    print("\nFINAL REPORT:")
    for key, value in results.items():
        print(f"{key.upper():8} → {'OK' if value else 'FAIL'}")

    line()
    print("\nDone.")
