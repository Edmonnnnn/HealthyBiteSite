import requests
import sqlite3
from datetime import datetime

BASE = "http://127.0.0.1:8810/api/v1"


def line():
    print("-" * 60)


def check_db():
    con = sqlite3.connect("healthybite.db")
    cur = con.cursor()

    tables = {
        "blog_posts": 0,
        "contact_support_requests": 0,
        "contact_consult_requests": 0,
        "ai_chat_logs": 0,
    }

    for table in tables.keys():
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        tables[table] = cur.fetchone()[0]

    con.close()
    return tables


print("\nRUNNING SUPER TEST FOR HealthyBite BACKEND + DB")
line()

# ---------------------------
# 1. INITIAL DB COUNTS
# ---------------------------

db_before = check_db()
print("DB before:", db_before)
line()

# ---------------------------
# 2. TEST BLOG SECTIONS
# ---------------------------

print("TEST: BLOG SECTIONS")
sec = requests.get(f"{BASE}/blog/sections?lang=en")

print("Status:", sec.status_code)

if sec.status_code != 200:
    print("FAIL: blog sections endpoint")
    exit()

data = sec.json()
print("Keys:", list(data.keys()))

try:
    first_slug = data["sections"]["weekly"]["items"][0]["slug"]
except:
    print("FAIL: Cannot extract slug from weekly section")
    exit()

print("Extracted slug:", first_slug)
line()

# ---------------------------
# 3. TEST BLOG POST BY SLUG
# ---------------------------

print("TEST: BLOG POST PAGE")
post = requests.get(f"{BASE}/blog/posts/{first_slug}")

print("Status:", post.status_code)

if post.status_code != 200:
    print("FAIL: blog post endpoint")
    exit()

post_data = post.json()
print("Post title:", post_data["title"])
line()

# ---------------------------
# 4. TEST CONTACT (SUPPORT + CONSULT)
# ---------------------------

print("TEST: CONTACT FORMS")

# SUPPORT
support = requests.post(
    f"{BASE}/contact/support",
    json={
        "name": "SuperTest User",
        "email": "test@example.com",
        "topic": "AI assistant",
        "message": "SuperTest support message",
        "lang": "en"
    }
)

print("Support:", support.status_code, support.json())

# CONSULT
consult = requests.post(
    f"{BASE}/contact/consult",
    json={
        "name": "TestUser",
        "email": "test@example.com",
        "preferredChannel": "email",
        "preferredTime": "Morning",
        "topic": "First consultation",
        "message": "SuperTest consult message",
        "lang": "en"
    }
)

print("Consult:", consult.status_code, consult.json())
line()

# ---------------------------
# 5. TEST AI CHAT
# ---------------------------

print("TEST: AI CHAT")

chat = requests.post(
    f"{BASE}/ai/chat",
    json={
        "lang": "en",
        "sessionId": "test_session_" + datetime.now().strftime("%H%M%S"),
        "messages": [
            {"role": "user", "content": "Hello from super test"}
        ]
    }
)

print("AI Status:", chat.status_code)
print("AI Response:", chat.json())
line()

# ---------------------------
# 6. FINAL DB CHECK
# ---------------------------

db_after = check_db()
print("DB after:", db_after)
line()

# Compare before/after
print("VALIDATING DB...")

errors = []

if db_after["contact_support_requests"] <= db_before["contact_support_requests"]:
    errors.append("Support request NOT logged.")

if db_after["contact_consult_requests"] <= db_before["contact_consult_requests"]:
    errors.append("Consult request NOT logged.")

if db_after["ai_chat_logs"] <= db_before["ai_chat_logs"]:
    errors.append("AI chat NOT logged.")

if errors:
    print("TEST FAILED:")
    for e in errors:
        print(" -", e)
else:
    print("ALL TESTS PASSED!")

line()
print("SUPER TEST COMPLETED.")
