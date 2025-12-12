# Healthy Bite Backend

FastAPI backend for the Healthy Bite project.
Provides /health plus routers under /api/v1/blog, /api/v1/contact, and /api/v1/ai.

## Run locally
1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Start the server from the backend directory: `uvicorn app.main:app --reload`.





# Healthy Bite Backend

This is the backend service for the **Healthy Bite** project.  
The frontend is a static HTML/CSS/JS site in the `frontend/` folder.  
This backend provides a small REST API for the Blog, Contact forms, and AI assistant.

The backend is built with **FastAPI**, **Uvicorn**, and **SQLAlchemy**.

---

## How to run (local)

From the `backend/` directory:

1. Create and activate a virtual environment (example for Python 3):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install dependencies:

bash
Копировать код
pip install -r requirements.txt
(Optional) Create a .env file based on .env.example
Use the same variables: APP_ENV, APP_PORT, DATABASE_URL, OPENAI_API_KEY.

Run the backend:

bash
Копировать код
uvicorn app.main:app --reload
Basic checks:

Health: GET http://localhost:8000/health

Blog ping: GET http://localhost:8000/api/v1/blog/ping

Contact ping: GET http://localhost:8000/api/v1/contact/ping

AI ping: GET http://localhost:8000/api/v1/ai/ping

API Draft
This section describes the planned REST API for the Healthy Bite backend.
The frontend is a static HTML/CSS/JS site and will call these endpoints via AJAX/Fetch.

All URLs here are relative to the backend root (e.g. http://localhost:8000 in local dev).

1. Blog API
The blog page (blog.html) needs structured content for:

hero block (title, lead, filters, search placeholder),

weekly picks,

featured story,

trending posts,

success stories,

tips & guides,

full library / all posts list.

All blog endpoints are under: /api/v1/blog.

1.1 GET /api/v1/blog/sections
Returns all content needed to render the main blog page for a given language.

Query params:

lang (string, optional)

Allowed: en, ru, am

Default: en

This should match the language in the frontend i18n system (lang.js).

Response example:

json
Копировать код
{
  "lang": "en",
  "hero": {
    "eyebrow": "Weekly picks",
    "title": "Healthy habits without crazy diets",
    "lead": "Short, practical reads about calmer eating.",
    "searchPlaceholder": "Search articles...",
    "filters": [
      { "id": "all", "label": "All" },
      { "id": "habits", "label": "Habits" },
      { "id": "psychology", "label": "Psychology" },
      { "id": "nutrition", "label": "Nutrition" }
    ]
  },
  "sections": {
    "weekly": {
      "title": "This week’s picks",
      "items": [
        {
          "id": 1,
          "slug": "small-steps-dinner",
          "eyebrow": "Week 1",
          "title": "Start with one calmer dinner",
          "summary": "How to make one evening meal less chaotic without counting calories.",
          "readingMinutes": 5,
          "tags": ["habits", "dinner"],
          "imageUrl": "/assets/images/blog/small-steps-dinner.jpg",
          "publishedAt": "2025-12-01"
        }
      ]
    },
    "featured": {
      "title": "Featured story",
      "items": [
        {
          "id": 2,
          "slug": "burnout-from-diets",
          "eyebrow": "Featured",
          "title": "Tired of starting over every Monday?",
          "summary": "Why strict plans burn you out and what to do instead.",
          "readingMinutes": 7,
          "tags": ["psychology", "motivation"],
          "imageUrl": "/assets/images/blog/burnout-monday.jpg",
          "publishedAt": "2025-11-20"
        }
      ]
    },
    "trending": {
      "title": "Trending now",
      "items": [
        {
          "id": 3,
          "slug": "snacks-that-dont-spiral",
          "eyebrow": "Trending",
          "title": "Snacks that don’t turn into a binge",
          "summary": "Simple snack ideas that keep you steady instead of triggered.",
          "readingMinutes": 4,
          "tags": ["snacks", "habits"],
          "imageUrl": null,
          "publishedAt": "2025-11-28"
        }
      ]
    },
    "success": {
      "title": "Real-life stories",
      "items": [
        {
          "id": 4,
          "slug": "anna-after-8-weeks",
          "eyebrow": "Success story",
          "title": "Anna: calmer evenings after 8 weeks",
          "summary": "How small changes in dinner routine helped Anna stop overeating at night.",
          "readingMinutes": 6,
          "tags": ["story"],
          "imageUrl": null,
          "publishedAt": "2025-10-15"
        }
      ]
    },
    "tips": {
      "title": "Tips & guides",
      "items": [
        {
          "id": 5,
          "slug": "plate-checklist",
          "eyebrow": "Guide",
          "title": "A simple checklist for a calmer plate",
          "summary": "A quick checklist you can run through before you sit down to eat.",
          "readingMinutes": 3,
          "tags": ["guide", "checklist"],
          "imageUrl": null,
          "publishedAt": "2025-09-30"
        }
      ]
    },
    "all": {
      "title": "All articles",
      "items": [
        {
          "id": 1,
          "slug": "small-steps-dinner",
          "eyebrow": "Week 1",
          "title": "Start with one calmer dinner",
          "summary": "How to make one evening meal less chaotic without counting calories.",
          "readingMinutes": 5,
          "tags": ["habits", "dinner"],
          "imageUrl": "/assets/images/blog/small-steps-dinner.jpg",
          "publishedAt": "2025-12-01"
        }
      ]
    }
  }
}
Notes:

The shape is designed to match the blog layout in blog.html:

hero block at the top,

several named sections below: weekly, featured, trending, success, tips, all.

Each items[] entry represents a single blog post in a given section.

imageUrl can be null if the post has no specific image; the frontend can fall back to a default.

The same post may appear in multiple sections (e.g., in weekly and in all).

1.2 GET /api/v1/blog/posts/{slug}
Returns full details for a single blog post.
This is for a future “single article” page or extended preview.

Path params:

slug (string, required)
Example: small-steps-dinner

Query params:

lang (string, optional, same as above)

en / ru / am

Default: en

Response example:

json
Копировать код
{
  "lang": "en",
  "id": 1,
  "slug": "small-steps-dinner",
  "eyebrow": "Week 1",
  "title": "Start with one calmer dinner",
  "summary": "How to make one evening meal less chaotic without counting calories.",
  "readingMinutes": 5,
  "tags": ["habits", "dinner"],
  "imageUrl": "/assets/images/blog/small-steps-dinner.jpg",
  "publishedAt": "2025-12-01",
  "contentBlocks": [
    {
      "type": "paragraph",
      "text": "Many people try to change everything at once and burn out in a week."
    },
    {
      "type": "paragraph",
      "text": "Instead, we start with one calmer dinner, focusing on a few simple cues."
    },
    {
      "type": "list",
      "items": [
        "Decide on dinner time in advance.",
        "Set the table before you get hungry.",
        "Keep your phone away from the table."
      ]
    }
  ]
}
Notes:

contentBlocks is intentionally simple: paragraphs and lists that the frontend can render into HTML.

More block types (quotes, images, headings) can be added later if needed.

If slug is not found, the API should return a 404 with a simple JSON error, e.g.:

json
Копировать код
{ "detail": "Post not found" }
2. Contact API
The contact page (contact.html) has several sections for help, consult, and support.
The backend will accept form submissions and (later) may forward them to email or a CRM.

All contact endpoints are under: /api/v1/contact.

2.1 POST /api/v1/contact/support
Creates a generic support/help request.

Request body (JSON):

json
Копировать код
{
  "name": "Anna",
  "email": "anna@example.com",
  "topic": "Problem with accessing the AI assistant",
  "message": "I answered the questions but the assistant did not start.",
  "lang": "en"
}
name (string, required)

email (string, required)

topic (string, optional, short subject/summary)

message (string, required, free-form text)

lang (string, optional, en / ru / am, default: en)

Response example:

json
Копировать код
{
  "status": "ok",
  "requestId": "support_12345"
}
If validation fails, return HTTP 400 with details.

2.2 POST /api/v1/contact/consult
Creates a request for a more structured consultation (e.g., 1:1 guidance).

Request body (JSON):

json
Копировать код
{
  "name": "Mariam",
  "email": "mariam@example.com",
  "preferredChannel": "email",
  "preferredTime": "evenings",
  "message": "I want to check if Healthy Bite fits my current routine.",
  "lang": "ru"
}
name (string, required)

email (string, required)

preferredChannel (string, optional, e.g. "email" or "phone")

preferredTime (string, optional, e.g. "mornings", "evenings")

message (string, required)

lang (string, optional, en / ru / am, default: en)

Response example:

json
Копировать код
{
  "status": "ok",
  "requestId": "consult_67890"
}
Later, the backend may send email notifications or push this into a CRM; for now we just store in DB and return an ID.

3. AI API
The AI page (ai.html) presents a marketing description of an assistant and a CTA to “start chat”.
The backend will expose a simple chat endpoint that talks to an AI provider (e.g., OpenAI).

All AI endpoints are under: /api/v1/ai.

3.1 POST /api/v1/ai/chat
Sends the latest user message (with optional short history) to the AI assistant and returns a reply.

Request body (JSON):

json
Копировать код
{
  "lang": "en",
  "sessionId": "user123-session-1",
  "messages": [
    { "role": "system", "content": "You are a gentle nutrition assistant for Healthy Bite." },
    { "role": "user", "content": "I always overeat in the evening, what can I change this week?" }
  ]
}
lang (string, optional, en / ru / am, default: en)

sessionId (string, optional; can be used to group messages per user/session)

messages (array, required):

Each item:

role (string, "system", "user", or "assistant")

content (string, the message text)

Response example:

json
Копировать код
{
  "reply": "Let’s start with one calmer dinner this week. Pick one evening when you can eat without screens and focus on the food. I’ll suggest a simple structure for that meal.",
  "suggestedNextQuestions": [
    "Which evening is easiest for you to choose?",
    "What usually triggers overeating at night for you?",
    "Do you prefer very detailed or very simple steps?"
  ]
}
Notes:

For now, this is a simple abstraction layer over an AI provider.

The backend will take the messages array, send it to the AI, and return the assistant’s reply plus optional suggested next questions.

If AI is temporarily unavailable, the API should return an HTTP 503 with a JSON error, e.g.:

json
Копировать код
{ "detail": "AI service temporarily unavailable" }