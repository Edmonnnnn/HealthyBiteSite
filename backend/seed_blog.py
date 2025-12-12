import sqlite3
import json

DB = "healthybite.db"

posts = [
    # English
    {
        "slug": "healthy-snacking-for-busy-days",
        "title": "Healthy Snacking for Busy Days",
        "subtitle": "Quick and simple ideas to stay energized",
        "section": "featured",
        "hero_image": "/assets/blog/snacks.jpg",
        "summary": "Explore easy snack options that keep you fueled throughout the day.",
        "lang": "en",
        "content_blocks": [
            {"type": "paragraph", "text": "When life gets busy, we often reach for quick but unhealthy snacks. Here are better alternatives."},
            {"type": "list", "items": ["Greek yogurt + berries", "Apple slices + peanut butter", "Raw nuts", "Carrot sticks + hummus"]},
            {"type": "tip", "title": "Prep ahead", "text": "Prep snacks for 2-3 days ahead to avoid last-minute poor choices."},
        ],
    },
    {
        "slug": "evening-overeating-solutions",
        "title": "How to Reduce Evening Overeating",
        "subtitle": "Practical strategies you can apply today",
        "section": "weekly",
        "hero_image": "/assets/blog/evening.jpg",
        "summary": "Evening overeating is common. Learn how to break the cycle with simple daily habits.",
        "lang": "en",
        "content_blocks": [
            {"type": "paragraph", "text": "Most people overeat in the evening because of all-day mental fatigue or skipping meals."},
            {"type": "tip", "title": "Small win", "text": "Pick one meal today and eat it without your phone."},
            {"type": "paragraph", "text": "Focus on earlier meals, stress management, and creating relaxing routines before dinner."},
            {"type": "quote", "text": "Your evenings reflect the structure of your day."},
        ],
    },
    {
        "slug": "5-morning-habits",
        "title": "5 Morning Habits for Better Health",
        "subtitle": "Start your day with momentum",
        "section": "tips",
        "hero_image": "/assets/blog/morning.jpg",
        "summary": "Small consistent morning habits compound into long-term wellbeing.",
        "lang": "en",
        "content_blocks": [
            {"type": "list", "items": [
                "Drink water within 5 minutes after waking",
                "Stretch for 3-5 minutes",
                "Avoid phone for the first 10 minutes",
                "Eat something protein-rich",
                "Step outside for sunlight",
            ]},
            {"type": "tip", "title": "Start small", "text": "Try starting with just one habit and build up gradually."},
        ],
    },
    {
        "slug": "success-story-anna",
        "title": "Success Story: Anna's 30-Day Transformation",
        "subtitle": "Real progress from real people",
        "section": "success",
        "hero_image": "/assets/blog/success.jpg",
        "summary": "Anna improved energy, mood, and reduced overeating through simple step-based coaching.",
        "lang": "en",
        "content_blocks": [
            {"type": "paragraph", "text": "Anna started by identifying her evening triggers and introducing mindful eating."},
            {"type": "paragraph", "text": "Within 30 days, her evening cravings dropped by 60%."},
        ],
    },
    # Russian
    {
        "slug": "healthy-snacking-for-busy-days",
        "title": "Полезные перекусы в загруженные дни",
        "subtitle": "Быстрые и простые идеи для энергии",
        "section": "featured",
        "hero_image": "/assets/blog/snacks.jpg",
        "summary": "Удобные перекусы, которые помогут сохранить силы в течение дня.",
        "lang": "ru",
        "content_blocks": [
            {"type": "paragraph", "text": "Когда день расписан по минутам, мы тянемся к быстрым, но не самым полезным перекусам. Вот более здоровые варианты."},
            {"type": "list", "items": ["Греческий йогурт с ягодами", "Яблоко с арахисовой пастой", "Горсть сырых орехов", "Морковь с хумусом"]},
            {"type": "tip", "title": "Подготовьте заранее", "text": "Готовьте перекусы на 2-3 дня вперед, чтобы избежать спонтанных решений."},
        ],
    },
    {
        "slug": "evening-overeating-solutions",
        "title": "Как уменьшить переедание вечером",
        "subtitle": "Практичные шаги, которые можно сделать уже сегодня",
        "section": "weekly",
        "hero_image": "/assets/blog/evening.jpg",
        "summary": "Вечернее переедание встречается часто. Узнайте, как разорвать этот круг простыми привычками.",
        "lang": "ru",
        "content_blocks": [
            {"type": "paragraph", "text": "Чаще всего мы переедаем вечером из-за усталости и пропусков приемов пищи в течение дня."},
            {"type": "tip", "title": "Маленькая победа", "text": "Выберите один прием пищи сегодня и съешьте его без телефона."},
            {"type": "paragraph", "text": "Сосредоточьтесь на ранних приемах пищи, управлении стрессом и расслабляющих ритуалах перед ужином."},
            {"type": "quote", "text": "Твой вечер — отражение структуры дня."},
        ],
    },
    {
        "slug": "5-morning-habits",
        "title": "5 утренних привычек для лучшего самочувствия",
        "subtitle": "Начните день с правильного настроя",
        "section": "tips",
        "hero_image": "/assets/blog/morning.jpg",
        "summary": "Небольшие, но регулярные утренние действия дают долгосрочный эффект.",
        "lang": "ru",
        "content_blocks": [
            {"type": "list", "items": [
                "Выпейте воду в течение 5 минут после пробуждения",
                "Потянитесь 3-5 минут",
                "Не берите телефон первые 10 минут",
                "Съешьте что-то с белком",
                "Выйдите на улицу за утренним светом",
            ]},
            {"type": "tip", "title": "Начните с малого", "text": "Начните с одной привычки и добавляйте остальные постепенно."},
        ],
    },
    {
        "slug": "success-story-anna",
        "title": "История успеха: 30 дней Анны",
        "subtitle": "Реальный прогресс реальных людей",
        "section": "success",
        "hero_image": "/assets/blog/success.jpg",
        "summary": "Анна повысила энергию, улучшила настроение и снизила переедание благодаря простым шагам.",
        "lang": "ru",
        "content_blocks": [
            {"type": "paragraph", "text": "Анна начала с того, что определила вечерние триггеры и ввела осознанное питание."},
            {"type": "paragraph", "text": "Через 30 дней вечерние тяги снизились на 60%."},
        ],
    },
    # Armenian
    {
        "slug": "healthy-snacking-for-busy-days",
        "title": "Առողջ խորտիկներ զբաղված օրերի համար",
        "subtitle": "Արագ և պարզ գաղափարներ էներգիայի համար",
        "section": "featured",
        "hero_image": "/assets/blog/snacks.jpg",
        "summary": "Հեշտ խորտիկներ, որոնք պահում են էներգիան ամբողջ օրը։",
        "lang": "am",
        "content_blocks": [
            {"type": "paragraph", "text": "Երբ օրը լի է գործերով, սովոր ենք ընտրել արագ, բայց ոչ օգտակար խորտիկներ։ Ահա ավելի առողջ տարբերակներ։"},
            {"type": "list", "items": ["Հունական յոգուրտ հատապտուղներով", "Խնձոր կտորներ ընկույզի կարագով", "Հում ընկույզների մի բուռ", "Գազար հումուսով"]},
            {"type": "tip", "title": "Պատրաստեք նախօրոք", "text": "Պատրաստեք խորտիկները 2-3 օր առաջ, որպեսզի խուսափեք վերջին վայրկյանի վատ ընտրություններից։"},
        ],
    },
    {
        "slug": "evening-overeating-solutions",
        "title": "Ինչպես նվազեցնել երեկոյան շատ ուտելը",
        "subtitle": "Գործնական քայլեր, որոնք կարող եք անել այսօր",
        "section": "weekly",
        "hero_image": "/assets/blog/evening.jpg",
        "summary": "Երեկոյան շատ ուտելը տարածված է. սովորեք կոտրել այդ շրջանը պարզ օրակարգով։",
        "lang": "am",
        "content_blocks": [
            {"type": "paragraph", "text": "Շատերը երեկոյան շատ են ուտում օրվա հոգնածության կամ բաց թողնված ճաշերի պատճառով։"},
            {"type": "tip", "title": "Փոքր հաղթանակ", "text": "Ընտրեք մեկ ճաշ այսօր և կերեք այն առանց հեռախոսի։"},
            {"type": "paragraph", "text": "Ուշադրություն դարձրեք ավելի վաղ սնվելուն, սթրեսի վերահսկմանը և հանգստացնող սովորույթներին ընթրիքի առաջ։"},
            {"type": "quote", "text": "Քո երեկոն արտացոլում է օրվա կառուցվածքը։"},
        ],
    },
    {
        "slug": "5-morning-habits",
        "title": "5 առավոտյան սովորություն առողջության համար",
        "subtitle": "Սկսեք օրը շարժումով",
        "section": "tips",
        "hero_image": "/assets/blog/morning.jpg",
        "summary": "Փոքր, բայց շարունակական առավոտյան քայլերը երկարաժամկետ ազդեցություն ունեն։",
        "lang": "am",
        "content_blocks": [
            {"type": "list", "items": [
                "Խմեք ջուր արթնանալուց հետո առաջին 5 րոպեում",
                "Ձգվեք 3-5 րոպե",
                "Առաջին 10 րոպեում մի վերցրեք հեռախոսը",
                "Ուտեք ինչ-որ բան, որտեղ կա սպիտակուց",
                "Դուրս եկեք արևի լույս ստանալու համար",
            ]},
            {"type": "tip", "title": "Սկսեք մեկից", "text": "Սկսեք մեկ սովորությունից և աստիճանաբար ավելացրեք մնացածը։"},
        ],
    },
    {
        "slug": "success-story-anna",
        "title": "Հաջողության պատմություն․ Աննայի 30-օրյա փոփոխությունը",
        "subtitle": "Իրական առաջընթաց իրական մարդկանցից",
        "section": "success",
        "hero_image": "/assets/blog/success.jpg",
        "summary": "Աննան բարձրացրեց էներգիան, բարելավեց տրամադրությունը և նվազեցրեց երեկոյան շատ ուտելը պարզ քայլերով։",
        "lang": "am",
        "content_blocks": [
            {"type": "paragraph", "text": "Աննան սկսեց հասկանալ իր երեկոյան խթանները և ներառեց գիտակցված սնունդ։"},
            {"type": "paragraph", "text": "30 օր անց նրա երեկոյան ցանկությունները նվազեցին մոտ 60%-ով։"},
        ],
    },
]


def seed():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Check if table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='blog_posts'")
    if not cur.fetchone():
        print("ERROR: blog_posts table does not exist. Run backend first.")
        return

    inserted = 0
    updated = 0

    for post in posts:
        cur.execute("SELECT id FROM blog_posts WHERE slug = ? AND lang = ?", (post["slug"], post["lang"]))
        exists = cur.fetchone()

        if exists:
            cur.execute(
                """
                UPDATE blog_posts
                SET title = ?, subtitle = ?, summary = ?, content_blocks = ?, section = ?, hero_image = ?
                WHERE slug = ? AND lang = ?
                """,
                (
                    post["title"],
                    post["subtitle"],
                    post["summary"],
                    json.dumps(post["content_blocks"], ensure_ascii=False),
                    post["section"],
                    post["hero_image"],
                    post["slug"],
                    post["lang"],
                ),
            )
            updated += 1
            print(f"[UPDATED] {post['slug']} ({post['lang']})")
        else:
            cur.execute(
                """
                INSERT INTO blog_posts (slug, title, subtitle, section, hero_image, summary, lang, content_blocks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post["slug"],
                    post["title"],
                    post["subtitle"],
                    post["section"],
                    post["hero_image"],
                    post["summary"],
                    post["lang"],
                    json.dumps(post["content_blocks"], ensure_ascii=False),
                ),
            )
            inserted += 1
            print(f"[ADDED] {post['slug']} ({post['lang']})")

    con.commit()
    con.close()

    print(f"\nSeeding complete. Inserted: {inserted} posts. Updated: {updated} posts.")


if __name__ == "__main__":
    seed()
