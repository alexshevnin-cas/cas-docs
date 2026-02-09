# CAS.AI Marketing Website — План

> **Дата:** 2026-02-09
> **Статус:** Черновик
> **Контекст:** Сайт cas.ai — внешняя витрина кабинета и точка входа для всех типов клиентов

---

## Зачем

Сайт cas.ai — это первое, что видит потенциальный клиент. Сейчас это общая страница про медиацию и паблишинг. По мере модернизации кабинета сайт должен стать частью воронки: от первого визита до регистрации и интеграции SDK.

Каждая фаза модернизации кабинета = обновление того, что мы можем показать и пообещать на сайте.

---

## Текущее состояние cas.ai

### Структура
- Главная (hero + статистика + отзывы)
- Mediation (описание услуги)
- Publishing (описание услуги)
- BuySellApp (отдельный продукт)
- Company (о нас)
- Blog
- Contact Us
- Login / Signup

### Языки
EN, UK, TR, AR, UR, ES, PT, RU

### Текущие CTA
- "Get started" (основная)
- "Submit your application" (форма)
- "Partner with us today"
- Login

### Текущие цифры на сайте
- 5B+ скачиваний мобильных игр
- 200+ опубликованных игр
- 5000+ приложений на медиации
- 1B показов/мес
- $1M UA spend/нед
- 650K tracked installs/день

### Что отсутствует
- Отдельные лендинги под типы клиентов (L1, L2, PubC)
- Витрина кабинета / скриншоты BI
- Self-service онбординг
- A/B тестирование лендингов
- Контентная стратегия (блог не привязан к воронке)
- Трекинг воронки (visitor → signup → integration → first revenue)

---

## Связь с фазами модернизации

| Фаза кабинета | Что появляется на сайте |
|---------------|------------------------|
| **1. BI Design** | Скриншоты нового кабинета. Лендинг "See your revenue in real-time". Обновлённый онбординг |
| **2a. ILRD** | Лендинг для L2: "SDK version analytics, cohort analysis". Кейсы стабильности |
| **2b. Сплитовалка** | Контент: "A/B test your monetization". Кейсы экспериментов |
| **3. MMP** | Лендинг для L2: "Connect AppsFlyer/Adjust — unified report". Интеграционная страница |
| **4. Publishing** | PubC лендинг: "Submit your game" (Voodoo-стиль). Self-service тест |

---

## Воронки по типам клиентов

### L1 (базовый медиационный клиент)
```
Ads / Organic / TG / Reddit
        ↓
  Лендинг Mediation (новый)
        ↓
  "Get started" → Signup
        ↓
  Онбординг: Add App → Integrate SDK
        ↓
  Aha: первая выручка в Quick View
```

### L2 (продвинутый клиент)
```
Content / SEO / Referral
        ↓
  Лендинг "Advanced Analytics"
        ↓
  Демо кабинета / скриншоты BI
        ↓
  Signup или апгрейд из L1
        ↓
  Подключение MMP → Unified Report
```

### PubC (кандидат в паблишинг)
```
Ads / Organic / Конференции
        ↓
  Лендинг "Submit your game" (AppQuantum-стиль)
        ↓
  Upload APK → автотест
        ↓
  Результаты за 3 дня (CPI, Retention, Status badge)
        ↓
  Green → переход в Pub
```

---

## Приоритеты

### P1 — Параллельно с Фазой 1 кабинета
- [ ] Лендинг Mediation (обновить под новый кабинет, скриншоты BI)
- [ ] Обновить CTA-flow: signup → онбординг (привязать к новому кабинету)
- [ ] Трекинг воронки: visitor → signup → SDK integration → first revenue
- [ ] Базовый A/B тест лендинга (заголовок, CTA)

### P2 — После Фазы 1
- [ ] Лендинг PubC "Submit your game" (Voodoo / AppQuantum референс)
- [ ] Контентная стратегия блога (привязать к воронке: SEO → статья → CTA)
- [ ] Кейсы клиентов (testimonials → развёрнутые кейсы с цифрами)
- [ ] Страница интеграций (AppsFlyer, Adjust — когда MMP будет готов)

### P3 — По мере роста
- [ ] Персонализация: разный контент для L1 / L2 / PubC по UTM или поведению
- [ ] Upsell-лендинги для существующих клиентов (L1 → L2, L2 → Pub)
- [ ] Market trends / insights как контент-магнит

---

## Инструменты и инфра

| Задача | Варианты |
|--------|----------|
| Лендинги | Текущий стек cas.ai / Webflow / Tilda (для быстрых тестов) |
| A/B тесты | Google Optimize (deprecated) → VWO / Optimizely / самописное |
| Аналитика | Google Analytics 4 + события в BI (когда будет) |
| CRM/Leads | HubSpot (есть в fin-model action items) |
| Email | Текущее решение + триггеры из product-strategy.md Stream 6 |

---

## Метрики сайта

| Метрика | Описание |
|---------|----------|
| Visitors | Уникальные посетители/мес |
| Signup Rate | Visitors → Signups |
| Integration Rate | Signups → SDK integrated |
| Time to First Revenue | Signup → первая выручка |
| Bounce Rate по лендингам | Какой лендинг работает лучше |
| Lead Source | Откуда пришёл (Ads, Organic, TG, Referral, Conference) |

---

## Связанные документы

| Документ | Что даёт |
|----------|---------|
| `02-business-model/cas-business-model.md` | Каналы привлечения (Inbound, Outbound, Referral) |
| `02-business-model/CAS Fin Model 0.4 - Acquisition.csv` | Модель привлечения по каналам и месяцам |
| `03-product/product-strategy.md` (Stream 6) | Маркетинговые нотификации, email-триггеры, upsell |
| `03-product/onboarding-flow.md` | Онбординг по типам клиентов |
| `03-product/user-stories.md` (US-PubC-07) | Self-service тестирование прототипа |
| `05-research/competitive-ux-reference.md` | Voodoo self-service, AppQuantum лендинг |
