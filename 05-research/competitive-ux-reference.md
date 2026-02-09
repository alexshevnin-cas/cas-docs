# Конкурентный UX-анализ: референсы из интервью

**Дата:** 2026-02-06
**Источники:** интервью Мельников (Pub), Савенков/ZooqVPN (L2), скриншоты

---

## Voodoo — Self-service тестирование прототипов

**Скриншоты:** `assets/competitive/voodoo-*.png`
**Источник:** интервью Мельников — _"Проще с людьми не говорить, а закинуть на этот сайт"_

### Что делает Voodoo
Платформа для тестирования прототипов гиперказуальных игр. Разработчик загружает APK + простой SDK (TinySource), Voodoo запускает рекламную кампанию (~$200), через 3 дня — результат.

### UX-паттерны для CAS

| Паттерн | Что видим | Связь с CAS |
|---------|----------|-------------|
| **Status badge** | "Low potential" (оранжевый) на каждой игре | US-Pub-08 (индикатор здоровья проекта) — прямой референс |
| **Card-based metrics** | CPI, Retention D1, D7 — крупные карточки вверху | Инициатива 1 (Quick View виджеты) |
| **Secondary metrics row** | CPNU, Gender split, Install rate, Daily playtime, Retention D14 | Расширенный набор метрик для PubC |
| **Creative performance table** | Spend / Impressions / Clicks / Installs / CPI per creative | Возможная фича для Pub (UA-прозрачность) |
| **Totals row** | Сумма по всем креативам внизу таблицы | US-L2-19 |
| **"Create a Game test" CTA** | Большая кнопка в header | PubC self-service онбординг, HYP-10 |
| **Voodoo Academy** | Образовательный раздел в навигации | US-L2-24 (metric education) |
| **Iteration-based testing** | "#1 iteration, Sep 5-9, 2020" с датами | A/B-тест flow для PubC |
| **Minimal clean design** | Белый фон, много воздуха, фокус на цифрах | Общий UX-стандарт |

### Что взять для CAS PubC
1. Status badge (green/yellow/red) на каждом приложении в списке
2. Card layout для ключевых метрик: CPI, Retention D1/D7, Daily Playtime
3. Self-service CTA "Submit your game" на главной
4. Education section (Academy / Help center) в навигации

---

## Amplitude — Report + Table

**Скриншот:** `assets/competitive/amplitude-report-grouped.png`
**Источник:** интервью Савенков/ZooqVPN — показывал свой дашборд Amplitude

### Что делает Amplitude
Продуктовая аналитика с гибкими отчётами. Клиент ZooqVPN использует для анализа событий.

### UX-паттерны для CAS

| Паттерн | Что видим | Связь с CAS |
|---------|----------|-------------|
| **Graph + Table below** | Линейный график сверху, таблица с числами снизу | Инициатива 1 (Reports) — референс для layout |
| **Group by dimension** | Группировка по языку с цветовой маркировкой | Фильтры/Splits — разбивка по Country, AdType |
| **% toggle** | Переключение абсолют ↔ процент | UX-фича для Reports |
| **Top N filter** | "Top 12 (Default)" — ограничение видимых сегментов | Полезно при большом количестве стран/сетей |
| **Share link** | Кнопка share — _"как в Amplitude, кнопочка share link"_ | US-L2-15 |
| **Event selection panel** | Левая панель: выбор events, measured as, formula | Прототип для выбора метрик в CAS Reports |

### Что взять для CAS Reports
1. Layout: график сверху + data table снизу (не один без другого)
2. Группировка с цветовой маркировкой сегментов
3. % toggle для переключения абсолют/процент
4. "Top N" лимит для читаемости
5. Share link с сохранением состояния фильтров

---

## Appodeal — Позиционирование предиктивного LTV

**Скриншот:** `assets/competitive/appodeal-linkedin-ad.png`
**Источник:** упомянут Алексеем в интервью с Мельниковым — _"баннеры наших конкурентов, они прямо пишут, что у нас ваш предиктивный LTV"_

### Что делает Appodeal
Конкурент CAS (медиация + паблишинг). Позиционирует BI и предиктивную аналитику как ключевое преимущество.

### Ключевые маркетинговые сообщения

| Элемент | Текст | Импликация для CAS |
|---------|-------|-------------------|
| **Headline** | "Hard to predict ROI or LTV?" | Predictive LTV — маркетинговый крючок, не только продуктовая фича |
| **Value prop** | "We provide BI forecasts and analytics" | CAS должен иметь аналогичное (US-Pub-06, US-Pub-07) |
| **Accelerator** | "Appodeal Accelerator funds your UA tests — you keep all the revenue" | Конкурентная модель: финансирование тестов. CAS может противопоставить свою модель |
| **CTA** | "Plan your growth →" | Growth-oriented messaging |

### Что это значит для CAS
1. **Predictive LTV — уже не дифференциатор, а table stakes** — конкуренты активно продвигают. Нужно ускорить вывод наружу (US-Pub-06, US-Pub-07).
2. **Appodeal уже имеет MMP-интеграцию** — подтверждает HYP-13 (CAS ↔ AppsFlyer).
3. **Маркетинговое позиционирование** — CAS может делать контент вокруг BI/forecasts, как Appodeal.
4. **"You keep all the revenue"** — Appodeal подчёркивает отсутствие комиссии на тестах. CAS нужно сформулировать свой value prop.

---

## Связанные документы
- Интервью Мельников: `05-research/pub-melnikov-carcrash.md`
- Интервью Савенков: `05-research/L2-savenkov-zooqvpn.md`
- User stories: `03-product/user-stories.md`
- Гипотезы R&D: `03-product/rnd-hypotheses.md`
