import json
import sqlite3

DB = "healthybite.db"

base_posts = {
    "healthy-snacking-for-busy-days": {"section": "featured", "hero_image": "/assets/blog/snacks.jpg"},
    "evening-overeating-solutions": {"section": "weekly", "hero_image": "/assets/blog/evening.jpg"},
    "5-morning-habits": {"section": "tips", "hero_image": "/assets/blog/morning.jpg"},
    "success-story-anna": {"section": "success", "hero_image": "/assets/blog/success.jpg"},
    "mindful-eating-basics": {"section": "mindset", "hero_image": "/assets/blog/mindful.jpg"},
    "listening-to-hunger-signals": {"section": "mindset", "hero_image": "/assets/blog/mindful.jpg"},
    "quick-balanced-meals": {"section": "routine", "hero_image": "/assets/blog/busy.jpg"},
    "busy-day-eating-plan": {"section": "routine", "hero_image": "/assets/blog/busy.jpg"},
}

localized_posts = {
    "en": {
        "healthy-snacking-for-busy-days": {
            "title": "Healthy Snacking for Busy Days",
            "subtitle": "Quick and simple ideas to stay energized",
            "summary": "Explore easy snack options that keep you fueled throughout the day.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "When life gets busy, we often reach for quick but unhealthy snacks. Here are better alternatives.",
                },
                {
                    "type": "list",
                    "items": [
                        "Greek yogurt + berries",
                        "Apple slices + peanut butter",
                        "Raw nuts",
                        "Carrot sticks + hummus",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Prep ahead",
                    "text": "Prep snacks for 2-3 days ahead to avoid last-minute poor choices.",
                },
            ],
        },
        "evening-overeating-solutions": {
            "title": "How to Reduce Evening Overeating",
            "subtitle": "Practical strategies you can apply today",
            "summary": "Evening overeating is common. Learn how to break the cycle with simple daily habits.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Most people overeat in the evening because of all-day mental fatigue or skipping meals.",
                },
                {"type": "tip", "title": "Small win", "text": "Pick one meal today and eat it without your phone."},
                {
                    "type": "paragraph",
                    "text": "Focus on earlier meals, stress management, and creating relaxing routines before dinner.",
                },
                {"type": "paragraph", "text": "Your evenings reflect the structure of your day."},
            ],
        },
        "5-morning-habits": {
            "title": "5 Morning Habits for Better Health",
            "subtitle": "Start your day with momentum",
            "summary": "Small consistent morning habits compound into long-term wellbeing.",
            "content_blocks": [
                {
                    "type": "list",
                    "items": [
                        "Drink water within 5 minutes after waking",
                        "Stretch for 3-5 minutes",
                        "Avoid phone for the first 10 minutes",
                        "Eat something protein-rich",
                        "Step outside for sunlight",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Start small",
                    "text": "Try starting with just one habit and build up gradually.",
                },
            ],
        },
        "success-story-anna": {
            "title": "Success Story: Anna's 30-Day Transformation",
            "subtitle": "Real progress from real people",
            "summary": "Anna improved energy, mood, and reduced overeating through simple step-based coaching.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Anna started by identifying her evening triggers and introducing mindful eating.",
                },
                {"type": "paragraph", "text": "Within 30 days, her evening cravings dropped by 60%."},
            ],
        },
        "mindful-eating-basics": {
            "title": "Mindful Eating Basics",
            "subtitle": "Simple steps to notice hunger and fullness",
            "summary": "Learn three quick practices to slow down, taste food, and stop at comfortable fullness.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Mindful eating is not a diet. It's a way to pay attention to food so you can feel satisfied without overeating.",
                },
                {
                    "type": "list",
                    "items": [
                        "Pause for one deep breath before the first bite",
                        "Notice textures and flavors for the first three bites",
                        "Set your utensil down between bites",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Quick reset",
                    "text": "Halfway through your meal, rate hunger from 1-10. Stop at satisfied, not stuffed.",
                },
            ],
        },
        "listening-to-hunger-signals": {
            "title": "Listening to Hunger Signals",
            "subtitle": "Practice gentle hunger and fullness checks",
            "summary": "A simple two-question check to avoid grazing and late overeating.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Hunger and fullness cues can be quiet. Checking in takes seconds and prevents autopilot snacking.",
                },
                {
                    "type": "list",
                    "items": [
                        "Ask: Am I physically hungry or just distracted?",
                        "If hungry, choose a meal or snack with protein",
                        "If not, try water, a short walk, or a pause",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Evening check",
                    "text": "Before evening snacks, rate hunger on a 1-10 scale. If under 4, add a calm activity first.",
                },
            ],
        },
        "quick-balanced-meals": {
            "title": "Quick Balanced Meals for Busy Days",
            "subtitle": "Build a plate in under 10 minutes",
            "summary": "Use a simple formula to get protein, produce, and carbs even on the busiest days.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Rushed days don't have to mean skipped meals. A simple template keeps you fueled.",
                },
                {
                    "type": "list",
                    "items": [
                        "Protein: rotisserie chicken, beans, eggs, or tofu",
                        "Produce: bagged salad, tomatoes, cucumbers, or frozen veg",
                        "Carb: whole-grain bread, rice packets, or potatoes",
                    ],
                },
                {
                    "type": "tip",
                    "title": "2-minute assemble",
                    "text": "Layer pre-washed greens, protein, and a carb; add olive oil + salt. Done.",
                },
            ],
        },
        "busy-day-eating-plan": {
            "title": "Busy Day Eating Plan",
            "subtitle": "Three anchor moments to stay fueled",
            "summary": "Set breakfast, a mid-shift snack, and a quick dinner template to avoid energy crashes.",
            "content_blocks": [
                {"type": "paragraph", "text": "Anchors prevent all-day grazing. Define three moments you will eat no matter what."},
                {
                    "type": "list",
                    "items": [
                        "Breakfast: protein + fiber (eggs + toast, yogurt + oats)",
                        "Mid-shift snack: 200-250 kcal with protein and crunch",
                        "Dinner template: protein, veg, easy carb (frozen veg + rotisserie + rice)",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Calendar cue",
                    "text": "Block 10 minutes on your calendar for each anchor to make it non-negotiable.",
                },
            ],
        },
    },
    "ru": {
        "healthy-snacking-for-busy-days": {
            "title": "Здоровые перекусы в загруженные дни",
            "subtitle": "Быстрые идеи, чтобы оставаться энергичным",
            "summary": "Простые варианты перекусов, которые поддерживают силы, когда времени мало.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Когда день расписан по минутам, рука тянется к сладостям или чипсам. Эти варианты помогут держать энергию без срывов.",
                },
                {
                    "type": "list",
                    "items": [
                        "Греческий йогурт с ягодами",
                        "Яблочные дольки с арахисовой пастой",
                        "Горсть несоленых орехов",
                        "Морковь или огурец с хумусом",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Подготовьтесь заранее",
                    "text": "Нарежьте и разложите перекусы на 2-3 дня вперед, чтобы выбирать полезное за секунды.",
                },
            ],
        },
        "evening-overeating-solutions": {
            "title": "Как уменьшить вечерние переедания",
            "subtitle": "Практичные шаги, которые можно сделать сегодня",
            "summary": "Вечером мы едим больше из-за усталости и пропущенных приемов пищи. Эти шаги помогают разорвать цикл.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Усталость и голод после дня толкают к перееданию. Нужен четкий план, который успокоит нервную систему и даст сытость.",
                },
                {
                    "type": "tip",
                    "title": "Один маленький эксперимент",
                    "text": "На сегодняшнем ужине ешьте без телефона и делайте три паузы, чтобы заметить, насколько вы сыты.",
                },
                {
                    "type": "paragraph",
                    "text": "Ставьте акцент на белок и овощи в начале дня, добавляйте перекус за 2-3 часа до ужина и создайте расслабляющий ритуал перед сном.",
                },
                {"type": "paragraph", "text": "Ваш вечер — отражение того, как вы заботились о себе весь день."},
            ],
        },
        "5-morning-habits": {
            "title": "5 утренних привычек для здоровья",
            "subtitle": "Начните день с энергии",
            "summary": "Небольшие действия утром создают основу для стабильного настроения и питания.",
            "content_blocks": [
                {
                    "type": "list",
                    "items": [
                        "Выпейте стакан воды в первые 5 минут после подъема",
                        "Сделайте 3-5 минут легкой разминки",
                        "Не берите телефон первые 10 минут",
                        "Добавьте белок в первый прием пищи",
                        "Выйдите на улицу за естественным светом",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Начните с одного пункта",
                    "text": "Выберите одну привычку на неделю и добавляйте следующие, когда она станет автоматической.",
                },
            ],
        },
        "success-story-anna": {
            "title": "История успеха: Анна за 30 дней",
            "subtitle": "Реальный прогресс на простых шагах",
            "summary": "Анна улучшила энергию и перестала переедать вечерами с помощью последовательных ритуалов.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Анна начала отслеживать триггеры вечернего голода и добавила белок утром и днём.",
                },
                {
                    "type": "paragraph",
                    "text": "Через 30 дней она заметила больше сил и снижение вечерней тяги более чем на 60%.",
                },
            ],
        },
        "mindful-eating-basics": {
            "title": "Основы осознанного питания",
            "subtitle": "Как замечать голод и сытость без диет",
            "summary": "Три практики, которые помогают замедлиться, почувствовать вкус еды и вовремя остановиться.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Осознанное питание — это внимание к ощущениям. Вы едите меньше на автомате и чувствуете удовлетворение раньше.",
                },
                {
                    "type": "list",
                    "items": [
                        "Сделайте вдох перед первым кусочком",
                        "Отложите приборы между двумя-тремя первыми кусками и замечайте текстуру",
                        "Наполовину блюда остановитесь и оцените сытость по шкале 1-10",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Быстрая проверка",
                    "text": "Когда отметка сытости достигает 7 из 10, замедлитесь и решите, нужен ли ещё один кусочек.",
                },
            ],
        },
        "listening-to-hunger-signals": {
            "title": "Как слышать сигналы голода",
            "subtitle": "Два коротких вопроса перед тем, как поесть",
            "summary": "Простая проверка помогает отличить настоящий голод от скуки и избежать вечерних перекусов.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Голод бывает физическим и эмоциональным. Откликнись на первый и заботливо обратись со вторым.",
                },
                {
                    "type": "list",
                    "items": [
                        "Спросите: это физический голод или привычка/стресс?",
                        "Если голод — выберите перекус с белком и клетчаткой.",
                        "Если нет — выпейте воду, сделайте пару вдохов или короткую прогулку.",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Вечерний стоп-сигнал",
                    "text": "Перед поздним перекусом отметьте голод по шкале 1-10; если ниже 4, добавьте воду и расслабляющее действие, затем пересмотрите решение.",
                },
            ],
        },
        "quick-balanced-meals": {
            "title": "Сбалансированная тарелка за 10 минут",
            "subtitle": "Простой шаблон для спешки",
            "summary": "Формула «белок + овощи + углеводы» помогает не пропускать питание даже в загруженный день.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Когда нет времени готовить, соберите тарелку из готовых или полуготовых продуктов и добавьте соль и масло по вкусу.",
                },
                {
                    "type": "list",
                    "items": [
                        "Белок: курица-гриль, яйца, творог, бобы или тофу",
                        "Овощи: микс-салат, помидоры, огурцы, замороженные овощи",
                        "Углеводы: цельнозерновой хлеб, варёный картофель, пакетики риса",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Сборка за 2 минуты",
                    "text": "Достаньте готовый белок, горсть овощей и быстрый углевод; полейте оливковым маслом и щепоткой соли.",
                },
            ],
        },
        "busy-day-eating-plan": {
            "title": "План питания на занятой день",
            "subtitle": "Три якоря, чтобы не голодать",
            "summary": "Заранее отметьте завтрак, перекус и ужин, чтобы избежать провалов энергии.",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Якорные приёмы пищи помогают держать ритм. Ставьте их в календарь и готовьте заранее то, что хранится долго.",
                },
                {
                    "type": "list",
                    "items": [
                        "Завтрак: белок + клетчатка (например, яйца и тост, йогурт и овсянка)",
                        "Перекус: 200–250 ккал с белком и хрустом",
                        "Ужин-шаблон: белок, овощи, быстрый углевод (замороженные овощи + готовая курица + рис)",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Напоминание в расписании",
                    "text": "Забронируйте 10 минут под каждый приём и ставьте таймер за час, чтобы успеть приготовить или взять еду с собой.",
                },
            ],
        },
    },
    "am": {
        "healthy-snacking-for-busy-days": {
            "title": "Առողջ խորտիկներ զբաղված օրերի համար",
            "subtitle": "Արագ ու պարզ մտքեր էներգիայի համար",
            "summary": "Թեթև խորտիկներ, որոնք պահում են ուժը, երբ ժամանակը քիչ է։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Երբ օրը լի է գործերով, հեշտ է ընտրել քաղցրավենիք կամ չիպսեր։ Այս տարբերակները պահում են էներգիան առանց ծանրության։",
                },
                {
                    "type": "list",
                    "items": [
                        "Յոգուրտ հատապտուղներով",
                        "Խնձորի շերտեր և գետնանուշի կարագ",
                        "Մի բուռ աղ չպարունակող ընկույզ",
                        "Գազար կամ վարունգ հումուսով",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Պատրաստեք նախօրոք",
                    "text": "Կտրատեք և բաժանեք խորտիկները 2-3 օր առաջ, որպեսզի ճիշտ ընտրությունը լինի պատրաստ րոպեների ընթացքում։",
                },
            ],
        },
        "evening-overeating-solutions": {
            "title": "Ինչպես նվազեցնել երեկոյան չափից շատ ուտելը",
            "subtitle": "Գործնական քայլեր հենց այսօր",
            "summary": "Երեկոյան հաճախ ուտում ենք հոգնածությունից և բաց թողնված սնունդներից․ այս քայլերը կօգնեն կոտրել շղթան։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Երեկոյան խուզարկությունը գալիս է հոգնածությունից ու սթրեսից։ Կարճ պլանը հանգստացնում է մարմինը և հագեցնում առանց ավելորդ կալորիաների։",
                },
                {
                    "type": "tip",
                    "title": "Փոքր փորձ",
                    "text": "Այսօրվա ընթրիքը փորձեք առանց հեռախոսի, կատարեք երեք կանգ, որպեսզի տեսնեք հագեցածությունը։",
                },
                {
                    "type": "paragraph",
                    "text": "Ավելացրեք սպիտակուց և բանջարեղեն օրվա սկզբում, հիշեք միջանկյալ խորտիկը 2-3 ժամ առաջ ընթրիքից և ստեղծեք հանգստացնող սովորություն քնելուց առաջ։",
                },
                {"type": "paragraph", "text": "Ձեր երեկոն արտացոլում է, թե ինչպես եք հոգ տարել ձեզ ամբողջ օրը։"},
            ],
        },
        "5-morning-habits": {
            "title": "Առողջ 5 առավոտյան սովորություն",
            "subtitle": "Սկսեք օրը շարժումով",
            "summary": "Փոքր գործողությունները առավոտյան ուժ և կայուն տրամադրություն են տալիս։",
            "content_blocks": [
                {
                    "type": "list",
                    "items": [
                        "Ջուր խմեք արթնանալուց հետո առաջին 5 րոպեում",
                        "Արեք 3-5 րոպե թեթև ձգումներ",
                        "Առաջին 10 րոպեն հեռախոսը մի վերցրեք",
                        "Սնունդին ավելացրեք սպիտակուց",
                        "Ելեք դուրս արևի լույսի տակ",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Սկսեք մեկ քայլից",
                    "text": "Ընտրեք մի սովորություն մեկ շաբաթով, և միայն հետո ավելացրեք երկրորդը, երբ առաջինը դառնա բնական։",
                },
            ],
        },
        "success-story-anna": {
            "title": "Հաջողության պատմություն․ Աննա՝ 30 օրում",
            "subtitle": "Իրական արդյունք պարզ քայլերով",
            "summary": "Աննան բարձրացրեց էներգիան և նվազեցրեց երեկոյան չափից շատ ուտելը հետևողական սովորություններով։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Աննան սկսեց նկատել իր երեկոյան գայթակղությունները և ավելացրեց սպիտակուց առավոտյան ու միջօրեին։",
                },
                {
                    "type": "paragraph",
                    "text": "30 օր անց նա ավելի կայուն ուժ ուներ, իսկ երեկոյան քաղցի թուլացումը ավելի քան 60% էր։",
                },
            ],
        },
        "mindful-eating-basics": {
            "title": "Գիտակցված սնվելու հիմունքներ",
            "subtitle": "Ինչպես նկատել քաղցն ու հագեցածությունը առանց դիետաների",
            "summary": "Երեք պարզ փորձ, որոնք օգնում են դանդաղել, զգալ ճաշի համը և կանգնել ժամանակին։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Գիտակցված սնվելը ուշադրություն է մարմնի ազդակներին։ Երբ դանդաղում եք, հագեցածության զգացումը գալիս է ավելի շուտ։",
                },
                {
                    "type": "list",
                    "items": [
                        "Մինչ առաջին պատառը խոր շունչ քաշեք",
                        "Առաջին երկու-երեք պատառների միջև դրեք պատառաքաղը և զգացեք հյուսվածքը",
                        "Ուտեստի կեսին կանգնեք ու գնահատեք հագեցածությունը 1-10 սանդղակով",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Արագ ստուգում",
                    "text": "Երբ հասնում եք 7/10 հագեցածության, դանդաղեք և որոշեք՝ պետք է արդյոք ևս մեկ պատառ։",
                },
            ],
        },
        "listening-to-hunger-signals": {
            "title": "Լսեք քաղցի ազդակները",
            "subtitle": "Երկու կարճ հարց մինչև ուտելը",
            "summary": "Հեշտ ստուգումը օգնում է տարբերել իրական քաղցը սովորությունից և խուսափել ուշ խորտիկներից։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Քաղցը կարող է լինել ֆիզիկական կամ էմոցիոնալ։ Առաջինը պահանջում է սնունդ, երկրորդը՝ հոգատարություն և հանգստացում։",
                },
                {
                    "type": "list",
                    "items": [
                        "Հարցրեք ձեզ՝ սա մարմնի քաղց է, թե ձանձրույթ/սթրես",
                        "Եթե քաղց եք, ընտրեք սպիտակուցով և մանրաթելով խորտիկ",
                        "Եթե ոչ, խմեք ջուր, արեք մի քանի խորը շունչ կամ կարճ քայլք",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Երեկոյան կանգ",
                    "text": "Ուշ խորտիկից առաջ գնահատեք քաղցը 1-10 սանդղակով․ եթե 4-ից ցածր է, նախ խմեք ջուր ու արեք հանգստացնող գործողություն։",
                },
            ],
        },
        "quick-balanced-meals": {
            "title": "Հավասարակշռված ուտեստ 10 րոպեում",
            "subtitle": "Պարզ ձև, երբ ժամանակ չկա",
            "summary": "«Սպիտակուց + բանջարեղեն + ածխաջուր» բանաձևը պահում է սնունդը պարզ ու արագ։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Երբ պատրաստելու ժամանակ չկա, հավաքեք ափսեն պատրաստի բաղադրիչներից և ավելացրեք քիչ աղ ու յուղ։",
                },
                {
                    "type": "list",
                    "items": [
                        "Սպիտակուց՝ խորոված հավ, ձու, լոբի կամ տոֆու",
                        "Բանջարեղեն՝ պատրաստի սալաթ, լոլիկ, վարունգ, սառեցված բանջարեղեն",
                        "Ածխաջուր՝ ամբողջական հացի կտոր, խաշած կարտոֆիլ, արագ պատրաստվող բրինձ",
                    ],
                },
                {
                    "type": "tip",
                    "title": "2 րոպե հավաքում",
                    "text": "Վերցրեք պատրաստի սպիտակուց, մի բաժին բանջարեղեն և արագ ածխաջուր, խառնեք ձիթայուղով ու աղով։",
                },
            ],
        },
        "busy-day-eating-plan": {
            "title": "Սննդակարգ զբաղված օրերի համար",
            "subtitle": "Երեք հիմք, որ չսովածանաք",
            "summary": "Նախօրոք որոշեք նախաճաշը, միջանկյալ խորտիկը և ընթրիքը, որպեսզի խուսափեք էներգիայի անկումից։",
            "content_blocks": [
                {
                    "type": "paragraph",
                    "text": "Հենարանային ընդունումները պահում են ռիթմը։ Նշեք դրանք օրացույցում և ընտրեք ուտեստներ, որոնք հեշտ է վերցնել ձեզ հետ։",
                },
                {
                    "type": "list",
                    "items": [
                        "Նախաճաշ՝ սպիտակուց + մանրաթել (ձու և տոստ, յոգուրտ և վարսակ)",
                        "Խորտիկ՝ 200-250 կկալ սպիտակուցով և խրթխրթանությամբ",
                        "Ընթրիքի ձև՝ սպիտակուց, բանջարեղեն, արագ ածխաջուր (սառեցված բանջարեղեն + պատրաստի հավ + բրինձ)",
                    ],
                },
                {
                    "type": "tip",
                    "title": "Ժամանակացույցի հիշեցում",
                    "text": "Յուրաքանչյուր ընդունման համար մեկ 10-րոպեանոց նշում դրեք օրացույցում և ազդանշան դրեք մեկ ժամ առաջ, որպեսզի չթողնեք այն։",
                },
            ],
        },
    },
}

posts = []
expected_slugs = set(base_posts.keys())
for lang, entries in localized_posts.items():
    missing = expected_slugs - set(entries.keys())
    extra = set(entries.keys()) - expected_slugs
    if missing or extra:
        raise ValueError(f"Localized posts mismatch for {lang}: missing={missing}, extra={extra}")
    for slug, data in entries.items():
        meta = base_posts[slug]
        posts.append({**meta, **data, "slug": slug, "lang": lang})


def print_section_report(cursor, section):
    cursor.execute("SELECT slug, lang FROM blog_posts WHERE section = ?", (section,))
    rows = cursor.fetchall()
    slugs = {}
    for slug, lang in rows:
        slugs.setdefault(slug, set()).add(lang)

    slug_list = sorted(slugs.keys())
    print(f"\n[REPORT] Section '{section}'")
    print(f"Distinct slugs: {len(slug_list)} -> {', '.join(slug_list) if slug_list else 'none'}")
    for slug in slug_list:
        langs = slugs[slug]
        lang_presence = {code: (1 if code in langs else 0) for code in ["en", "ru", "am"]}
        lang_counts = ", ".join([f"{code}={lang_presence[code]}" for code in ["en", "ru", "am"]])
        print(f" - {slug}: {lang_counts}")


def seed():
    con = sqlite3.connect(DB)
    cur = con.cursor()

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

    print(f"\nSeeding complete. Inserted: {inserted} posts. Updated: {updated} posts.")
    for section in ("mindset", "routine"):
        print_section_report(cur, section)

    con.close()


if __name__ == "__main__":
    seed()
