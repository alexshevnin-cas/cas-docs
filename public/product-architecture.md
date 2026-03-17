# Product Architecture: Competitive Research & Variants

> **Дата:** 2026-03-16
> **Контекст:** Исследование как устроены продуктовые портфели у ad-tech платформ с медиацией + паблишингом + своей сеткой. Три варианта архитектуры для CAS.AI.

---

## Как устроено у конкурентов: Product Family Architecture

### AppLovin (Axon) — «Вертикальная империя»

```
                        AXON (AI Engine)
                       ┌───────┴────────┐
                 DEMAND SIDE        SUPPLY SIDE         MEASUREMENT
                 ┌─────┴─────┐    ┌─────┴──────┐      ┌────┴────┐
                 AppDiscovery     MAX            ALX    Adjust
                 (DSP/UA)        (Mediation)   (Exchange) (MMP)
                      │               │            │         │
                 SparkLabs            │            │         │
                 (Creatives)          └─────┬──────┘         │
                                            │                │
                                     ◄── feedback loop ──►
```

**Ключевые решения:**
- Продали весь паблишинг (Tripledot, $900M) — чистый platform play
- Единый дашборд `dash.applovin.com`: MAX (supply) + Growth (demand) под одним логином
- ALX Exchange **не отдельный продукт** — он встроен в MAX как demand source
- Adjust сохранил отдельный бренд и дашборд (нейтральность MMP = доверие рынка)
- AI-движок Axon как бренд — позиционирование «мы не медиация, мы AI-платформа»
- **MAX = 73% топ-игр** — доминирование

**Урок для CAS:** Closed-loop (UA→Mediation→Attribution→UA) — это moat. Но для этого нужны все три стороны. CAS пока только supply side.

---

### Unity LevelPlay — «Пост-M&A Франкенштейн»

```
Unity Grow (umbrella)
├── LevelPlay (Mediation)
│   ├── LevelPlay Analytics
│   ├── LevelPlay A/B Testing
│   └── LevelPlay Ad Quality (бесплатный, даже для не-LevelPlay)
├── Unity Ads Network ─┐
│                       ├── Vector AI (общий ML-движок)
├── ironSource Ads ─────┘   (два отдельных network, так и не слили)
├── Unity Exchange ──────┐
├── ironSource Exchange ─┘ (два exchange тоже раздельно)
├── Luna (креативы + UA аналитика)
├── Tapjoy (offerwall)
├── Aura (OEM предустановки, 2B+ устройств)
└── Supersonic (паблишинг)
    ├── Self-serve тест ($200 → CPI/retention за 3 дня)
    ├── Wisdom SDK (автоконфиг обёртка)
    └── LiveOps (remote config, push, cloud save)
```

**Ключевые решения:**
- **6+ отдельных дашбордов**, не объединены после слияния — UX-катастрофа
- Два ad network НЕ слились (попытка ухудшила перформанс) — «вместе слабее, чем порознь»
- Supersonic — самый интегрированный продукт: авто-подключает LevelPlay + Analytics + LiveOps
- Ad Quality раздают бесплатно всем (даже не-LevelPlay) — land & expand
- **LevelPlay = 5.7% топ-игр** (было 30%+) — фрагментация убивает

**Урок для CAS:** НЕ фрагментировать дашборды. Unity — пример того, как M&A-сборка без unified experience теряет рынок. CAS может строить unified с нуля.

---

### Appodeal / Stack — «Ближайший аналог CAS»

```
Stack (umbrella)
├── Appodeal (SDK + Dashboard = единая точка входа)
│   ├── Mediation (60+ сетей, bidding)
│   ├── Product Analytics (retention, LTV, ARPU, revenue forecast)
│   └── Monetization Optimization
├── BidMachine (Exchange) — open source!
│   ├── 70+ DSP
│   └── Работает и вне Appodeal (с любым медиатором)
├── DataCore (BI)
│   ├── Impression-level revenue
│   ├── User segmentation (20% users → 80% revenue)
│   └── UA↔Monetization correlation
├── Accelerator
│   ├── UA-фонд $100M
│   └── Возврат soft-launch затрат (до $100×2)
└── Publishing (Strategic Partners)
    ├── UA funding + эксперты
    └── Revenue share только на прибыльных когортах
```

**Ключевые решения:**
- **Единый дашборд** — monetization + UA + analytics в одном месте. Главное конкурентное преимущество
- BidMachine **open source** — доверие, привлечение разработчиков, нет lock-in
- DataCore = «клей» между monetization и UA: не просто «что было», а «какие юзеры важны и как их получить больше»
- Tiered journey: Free SDK → Analytics → Accelerator ($) → Publishing ($$)
- Revenue share только на прибыльных когортах UA — низкий барьер входа

**Урок для CAS:** Это template. Медиация = вход. Analytics = удержание. Exchange = доп. revenue. Publishing = premium tier.

---

### Digital Turbine — «Чего делать НЕ надо»

```
Digital Turbine
├── On Device Solutions (ODS) — $342M ← основной бизнес
│   ├── Ignite (предустановки через операторов)
│   ├── SingleTap (установка в один тап)
│   └── DT Hub (альтернативный app store)
└── App Growth Platform (AGP) — $153M
    ├── DT FairBid (Mediation) ← ex-Fyber
    ├── DT Exchange ← ex-Fyber + AdColony (слили только недавно)
    ├── DT Offer Wall ← ОТДЕЛЬНЫЙ логин (ACP platform)
    └── Reporting (dynamic reports, 15B events/day)
```

**Ключевые решения (антипаттерны):**
- 3 года после M&A — продукты всё ещё частично фрагментированы
- Offer Wall = отдельный логин от медиации — девелоперы жалуются
- Analytics = только reporting (что было), нет BI (что делать)
- Нет publishing, нет creative tools, нет UA

**Урок для CAS:** Acquisition-assembled platform без unified experience = потеря доли рынка.

---

### Yodo1 — «Managed Service для инди»

```
Yodo1
├── MAS (Managed Ad Services) ← ядро
│   ├── SDK (Unity, Unreal, Flutter, RN, Godot, Cocos, GameMaker)
│   ├── 15-17 сетей (AppLovin + AdMob обязательны)
│   ├── AI waterfall optimization (клиент НЕ настраивает)
│   └── Performance Score (AI-рекомендации: 5 категорий)
├── Growth Accelerator (managed UA + ASO + retention)
├── Publishing (mobile + PC, сильны в Китае)
│   ├── IP deals (Hasbro, Paramount, Sony)
│   └── Transformers: Earth Wars (забрали у Supercell/Space Ape)
└── IPverse (NEW, июль 2025) — AI-платформа лицензирования IP
```

**Ключевые решения:**
- **Максимальная простота:** разработчик НЕ заводит аккаунты в AdMob/AppLovin — Yodo1 использует свои. Онбординг ~2 часа
- **Zero control = trade-off:** клиент не настраивает waterfall, не видит детальную аналитику. «Мы всё сделаем за вас»
- **Нет своего exchange** — YSO network есть в коде, но выключен. Главная слабость
- **BI слабый:** дашборд = управление играми + базовые метрики. Performance Score заменяет self-service аналитику AI-рекомендациями
- **Фокус — инди/маленькие студии** без экспертизы в монетизации. ~4500 игр, 128 человек
- **Pivot к IP:** IPverse (AI matchmaking для лицензирования) — уход от прямой конкуренции с AppLovin/Unity
- **Tier 3 медиатор:** не упоминается в сравнениях с MAX/LevelPlay

**Урок для CAS:** Yodo1 — не конкурент, а **зеркало того, чем CAS НЕ хочет быть**: opaque pricing, zero self-service, нет own exchange, нет BI. Но их онбординг (2 часа, без аккаунтов в сетях) и AI Performance Score — хорошие UX-паттерны для изучения.

---

### Moloco — «ML-first, Zero-margin SDK»

```
Moloco (ML Engine)
├── Moloco Ads (DSP) ← основной бизнес, $2B+ demand
├── Moloco SDK (Publisher) ← БЕСПЛАТНЫЙ, нулевая маржа
│   └── Plugs into MAX / LevelPlay / AdMob (не своя медиация!)
├── Commerce Media (retail white-label)
└── Streaming Monetization
```

**Ключевое:** SDK с нулевой маржой = субсидируем supply, зарабатываем на demand. Обратная модель от CAS.

---

### Voodoo — «Паблишер с internal tools»

```
Voodoo
├── Publishing Pipeline (core business)
│   └── Game Testing → Soft Launch → Scale
├── Voodoo Sauce (internal SDK wrapper)
│   └── Использует AppLovin MAX для медиации (не своё)
├── Growth Platform (internal BI + creative optimization)
└── Voodoo Ads (sell inventory своих игр рекламодателям)
```

**Ключевое:** Всё internal, ничего не продаётся наружу. CAS — обратная модель.

---

## Паттерны рынка

### 1. Developer Journey — воронка продуктов

У всех, кто успешен, одинаковая воронка:

```
FREE SDK (медиация)          ← вход, self-serve
    ↓
Analytics Dashboard           ← удержание, показать ценность сразу
    ↓
Own Exchange (доп. demand)    ← растёт revenue без усилий клиента
    ↓
UA Tools / DSP                ← клиент начинает тратить деньги
    ↓
Publishing Partnership        ← maximum value, human-touch
```

### 2. Unified Console = конкурентное преимущество

| Компания | Единый дашборд? | Доля рынка (тренд) |
|----------|----------------|---------------------|
| AppLovin MAX | Да (MAX+Growth) | 73% ↑ |
| Appodeal | Да (всё в одном) | Растёт |
| LevelPlay | Нет (6+ дашбордов) | 5.7% ↓↓ |
| Digital Turbine | Нет (разные логины) | Падает |

### 3. Exchange: Open vs Captive

| Стратегия | Пример | Плюсы | Минусы |
|-----------|--------|-------|--------|
| **Captive** (только в своей медиации) | AppLovin ALX | Lock-in, 4x revenue as host | Antitrust risk, distrust |
| **Open** (работает с любым медиатором) | BidMachine, Moloco SDK | Широкий охват, доверие | Меньше lock-in |

### 4. BI как позиционирование

| Уровень | Что делает | Пример |
|---------|-----------|--------|
| **Reporting** | «Что было» — таблицы, фильтры, экспорт | DT, базовый MAX |
| **Analytics** | «Почему» — cohorts, A/B, anomalies | LevelPlay Analytics |
| **Intelligence** | «Что делать» — user segments, LTV predict, UA↔Monetization | Appodeal DataCore |

---

## Три варианта архитектуры для CAS.AI

### Вариант A: «Stack Model» (по образцу Appodeal)

Самый прямой аналог. Медиация = вход, всё растёт вверх.

```
CAS.AI Platform
│
├── CAS SDK (Entry Point — условно бесплатная медиация)
│   ├── Core Mediation (waterfall + bidding)
│   ├── Adapters (30+ сетей)
│   └── Plugins (Unity, Unreal, Godot, RN)
│
├── CAS Cabinet (Apps & Account Management)
│   ├── App management + onboarding
│   ├── Payments + billing
│   ├── SDK integration wizard
│   └── Notifications + support
│
├── OneBI (Analytics — доступен с первого дня SDK)
│   ├── Quick View (L1: revenue, DAU, eCPM)
│   ├── Reports (L2: splits, cohorts, exports)
│   ├── Intelligence (Pub: LTV predict, anomalies, health score)
│   └── Internal BI (Admin: portfolio, AM performance, funnel)
│
├── CAS Monetization (Internal → Self-service)
│   ├── Waterfall/bidding configuration
│   ├── A/B testing конфигураций
│   ├── Network management
│   └── Drop detection + alerts
│
├── CAS Growth (UA + Creative + ASO)
│   ├── Creative catalogue + performance
│   ├── Campaign management (published apps)
│   ├── Cross Promo (published apps)
│   └── Market trends + benchmarks
│
└── CAS Publishing (Premium tier, human-touch)
    ├── Game testing ($200 → CPI/retention)
    ├── UA funding
    ├── Expert monetization setup
    └── Revenue share на прибыльных когортах
│
├── CAS Exchange (Own demand, open model)
│   ├── VAST/VPAID (programmatic video)
│   ├── ORTB (external DSPs)
│   └── Cross-Promo (PSV inventory)

```

**Плюсы:** Чёткая воронка, каждый продукт = следующий шаг клиента. Близко к Appodeal, проверенная модель.
**Минусы:** 7 продуктов — много для текущей команды. Publishing как продукт требует отдельных людей и денег.

---

### Вариант B: «Two Sides» (по образцу AppLovin)

Разделение на Supply (паблишеры) и Demand (рекламодатели) + общая платформа данных.

```
CAS.AI Platform
│
├── FOR PUBLISHERS (Supply Side)
│   │
│   ├── CAS SDK
│   │   ├── Mediation + Exchange
│   │   └── Plugins
│   │
│   ├── CAS Console (единый дашборд паблишера)
│   │   ├── Apps Management
│   │   ├── Analytics (OneBI)
│   │   ├── Monetization Config (self-service)
│   │   ├── Payments
│   │   └── Notifications
│   │
│   └── CAS Publishing (premium)
│       ├── Game testing
│       ├── Expert setup
│       └── Growth funding
│
├── FOR ADVERTISERS (Demand Side) ← будущее
│   │
│   ├── CAS Ads Manager
│   │   ├── Campaign management
│   │   ├── Creative tools
│   │   └── Reporting
│   │
│   └── CAS Exchange (programmatic buying)
│
└── SHARED PLATFORM
    ├── Data Layer (ClickHouse)
    ├── AI/ML (bid optimization, anomaly detection)
    └── GTM Stack (site, CRM, attribution)
```

**Плюсы:** Масштабируемая модель. Когда CAS дорастёт до demand side — структура готова. Чёткое разделение аудиторий.
**Минусы:** Demand side пока не существует. Преждевременная архитектура.

---

### Вариант C: «Unified Console + Product Tiers» ⭐ рекомендуемый

Компромисс: одна консоль, продукты = функциональные модули, которые открываются по мере роста клиента.

```
┌─────────────────────────────────────────────────────────┐
│                   CAS.AI Console                        │
│               (единая точка входа)                      │
│                                                         │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  ┌────────┐ │
│  │Dashboard │  │   Apps   │  │Monetization│  │Payments│ │
│  │(OneBI)   │  │   Mgmt   │  │   Config   │  │        │ │
│  └─────────┘  └──────────┘  └───────────┘  └────────┘ │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐             │
│  │ Reports │  │ Alerts & │  │  Growth   │             │
│  │& Cohorts│  │   Health │  │  Tools    │             │
│  └─────────┘  └──────────┘  └───────────┘             │
└─────────────────────────────────────────────────────────┘
         │              │              │
    открыт всем    L2+ клиентам   Pub/PubC
    (с SDK)        (unlock)       (premium)

Под капотом (не видно клиенту):
├── CAS SDK (медиация + данные + exchange demand)
├── CAS Exchange (SSP, VAST/ORTB)
├── Data Platform (ClickHouse, ILRD, ETL)
└── GTM Stack (site, CRM, referral, attribution)
```

**Философия:** Клиент видит ОДНУ консоль. Продукты — это не отдельные приложения, а **модули**, которые постепенно открываются:

| Tier | Что видит клиент | Что под капотом |
|------|------------------|-----------------|
| **Free (L1)** | Dashboard (5 карточек), Apps, Payments, SDK docs | CAS SDK + Exchange demand (auto) |
| **Pro (L2)** | + Reports, Cohorts, Version splits, Alerts, Export | + OneBI full, + Drop detection |
| **Business (Pub)** | + Monetization Config, A/B tests, Health Score, Growth | + Self-service waterfall, + Creative tools |
| **Enterprise (PubC/Publishing)** | + Game Testing, UA Dashboard, Expert Support | + Publishing pipeline, + UA funding |

**GTM Stack** — внутренний, не клиентский продукт:

```
GTM Stack (internal)
├── Marketing Site (cas.ai — лендинги, case studies)
├── CRM Layer (HubSpot + Bitrix → единый реестр 1C)
├── Attribution (UTM → Lead → Client → Revenue)
├── Referral Program (backend 1C, frontend в Console)
└── Sales Tools (AM performance, funnel dashboard в OneBI)
```

---

## Открытый вопрос: третий слой — Internal Operations Platform

> **Статус:** мысль, не решение. Варианты A/B/C пока не выбраны.

Во всех трёх вариантах есть два слоя: **клиентская консоль** (то, что видит паблишер) и **под капотом** (SDK, Exchange, Data). Но есть ещё третий слой, который не описан — **внутренняя админка**: то, что видят менеджеры CAS, а не клиенты.

Сейчас эту роль выполняет **1С**, и с неё надо мигрировать.

```
┌─────────────────────────────────────────────────┐
│         CAS.AI Console (клиент видит)           │  ← Варианты A/B/C про это
│         Dashboard, Apps, Payments, ...          │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────┐
│         Под капотом (никто не видит)            │  ← SDK, Exchange, ClickHouse
│         SDK, Exchange, Data Platform            │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────┐
│    Internal Ops Platform (менеджеры CAS видят)  │  ← ЭТОТ СЛОЙ
│                                                 │
│    Сейчас = 1С. Что тут живёт:                 │
│                                                 │
│    ├── Network Management                       │
│    │   ├── Waterfall-конфигурации (Задача 5)    │
│    │   ├── Подключение/отключение сетей         │
│    │   └── Dispatch задач ботам                 │
│    │                                            │
│    ├── Client Operations                        │
│    │   ├── Единый реестр клиентов (Задача 1)    │
│    │   ├── HubSpot↔Bitrix↔1C маппинг           │
│    │   ├── Revenue tracking по клиентам         │
│    │   └── Реферальная программа (Задача 2)     │
│    │                                            │
│    ├── Monitoring & Alerts                      │
│    │   ├── Drop detection (Задача 3)            │
│    │   ├── АРМ менеджера монетизации            │
│    │   └── Каскадная система алертов            │
│    │                                            │
│    ├── Reporting & Accounting                   │
│    │   ├── Revenue reports по менеджерам (Задача 4) │
│    │   ├── Billing / сверка                     │
│    │   └── Scorecard для All-Hands              │
│    │                                            │
│    └── GTM Stack                                │
│        ├── CRM (HubSpot + Bitrix)               │
│        ├── Marketing site                       │
│        └── Attribution                          │
└─────────────────────────────────────────────────┘
```

**Вопрос:** куда это мигрирует с 1С?

Варианты (не выбрано):
- **В OneBI** — часть функций (drop detection, отчёты, scorecard) естественно ложится в BI
- **В отдельную Admin Console** — как у AppLovin (internal dash ≠ publisher dash)
- **Частично в клиентскую консоль** — self-service waterfall config = и клиенту полезно, и менеджеру
- **Гибрид** — reporting/monitoring → OneBI, network config → отдельный internal tool, client ops → 1C replacement

Факт: задачи Влада Horyk (#7-14 из xlsx) требуют данных из CAS Events Server, которых в 1С нет. Сам Влад говорит: вынести управление водопадами из 1С. А задачи Смирнова (#1-6) — классическая 1С-автоматизация, но на ClickHouse данных.

Это самый запутанный слой, потому что он обслуживает **40+ человек GTM** которые сейчас работают в Excel.

---

## Открытый вопрос: несколько точек входа в экосистему

> **Статус:** мысль, не решение.

Во всех вариантах выше предполагается одна воронка: **Free SDK (медиация) → Analytics → Exchange → ... → Publishing**. Но CAS Platform — это экосистема, и заходить в неё можно с разных сторон.

```
                    ┌─────────────────────┐
                    │   CAS.AI Platform   │
                    │    (экосистема)      │
                    └──────────┬──────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
     Entry A: SDK        Entry B: Publishing   Entry C: ...?
     (текущий)           (Voodoo-style)
            │                  │
     «У меня есть         «У меня есть
      приложение,          игра/прототип,
      хочу монетизировать»  хочу издать»
            │                  │
            ▼                  ▼
     CAS SDK integration   Publishing Pipeline
     Self-service            ├── Game test ($200 → CPI/retention)
     Dashboard, OneBI        ├── Soft launch (мини-SDK для тестов)
     Grow into tiers         ├── Scale (полноценный CAS SDK)
            │                │   └── Waterfall, Exchange, BI — всё
            │                │       уже в нашей системе
            └────────┬───────┘
                     │
              Один клиент — одна консоль
              Независимо от точки входа
```

**Ключевая мысль:** publishing-клиент не начинает с «поставь SDK и настрой сети». Он начинает с «вот моя игра, проверьте». А дальше:

1. **Тест** — минимальная интеграция или вообще без неё (CPI/retention по UA данным)
2. **Soft launch** — облегчённый SDK (как Voodoo Sauce — обёртка, авто-конфиг)
3. **Scale** — полноценный CAS SDK, все сети, self-service конфигурация

Переход 2→3 происходит внутри одной системы. Клиент не мигрирует с «publishing dashboard» на «mediation dashboard» — он просто видит больше модулей в той же консоли.

**Зачем это важно:**
- Publishing pipeline — отдельная воронка привлечения (не через сайт/SDK docs, а через BD/game scouting)
- Revenue model другой (rev share vs SaaS/take rate)
- Но data layer, BI, billing, network management — общие
- Supersonic (Unity) так и работает: publishing = вход → авто-подключает LevelPlay + Analytics

**Потенциальные Entry C:** UA-as-a-service? Creative testing? Benchmark tool? Пока не ясно, но архитектура должна допускать несколько входов.

---

## Открытый вопрос: медиация — это не один продукт, а спектр

> **Статус:** мысль, не решение.

Даже внутри «медиации» есть несколько способов зайти. Это не один продукт с одним оффером — это спектр от полного блэкбокса до полного self-service:

```
Managed (блэкбокс)                              Self-Service (свои аккаунты)
◄──────────────────────────────────────────────────────────────────────────►

┌──────────────┐    ┌──────────────────┐    ┌─────────────────────────────┐
│  ENTRY       │    │  MID             │    │  PRO                        │
│              │    │                  │    │                             │
│  Наши        │    │  Микс: часть     │    │  Свои аккаунты во всех      │
│  аккаунты    │    │  наших, часть    │    │  сетях. Свои настройки.     │
│  сетей.      │    │  своих.          │    │  CAS = медиация +           │
│  Мы          │    │  Мы помогаем     │    │  экспертиза + BI.           │
│  настраиваем │    │  настраивать.    │    │                             │
│  waterfall.  │    │                  │    │  Фишка: наша группа         │
│  Клиент не   │    │                  │    │  монетизации + актуальный   │
│  заморачива- │    │                  │    │  BI = знаем как развивать   │
│  ется.       │    │                  │    │  монетизацию лучше клиента. │
└──────────────┘    └──────────────────┘    └─────────────────────────────┘
    ↑                                               ↑
    Похоже на Yodo1,                          Можем работать поверх
    но с прозрачностью                        ЛЮБОЙ core медиации —
    и без lock-in                             фишка в нас как
                                              в настройщиках, не
                                              в SDK
```

**Конкурентное преимущество на каждом уровне:**

| Уровень | Клиент | Наш оффер | Преимущество CAS |
|---------|--------|-----------|------------------|
| **Entry** | Инди, не может/не хочет заводить аккаунты в сетях | Наши аккаунты, мы настраиваем, блэкбокс | **Финансовая гибкость:** аренда аккаунтов сетей для тех, кто не может сам (санкции, страновые ограничения, незнание). Быстрый старт |
| **Mid** | Растущий паблишер, часть сетей свои | Помогаем настраивать, микс аккаунтов | Мягкий переход без миграции. Постепенно забирает контроль |
| **Pro** | Крупный паблишер, всё своё | Self-service + экспертиза + BI | **Группа монетизации (40 чел) + актуальный BI** = всегда знаем как оптимизировать. Можем работать поверх любой core медиации |

**Ключевые мысли:**

1. **Аренда аккаунтов** — это не баг, это фича и отдельная ценность. Санкции, страновые ограничения, просто незнание — куча причин почему разработчик не может сам завести аккаунт в AdMob/AppLovin. CAS решает это.

2. **Фишка — не в SDK, а в команде.** На Pro-уровне SDK может быть вообще не наш (MAX, LevelPlay, что угодно). Ценность CAS = 40 человек монетизации, которые умеют настраивать + BI, который показывает что настраивать. Мы — настройщики, не медиатор.

3. **Это меняет позиционирование.** CAS — не «ещё один медиатор» (конкурент MAX/LevelPlay). CAS — **monetization operations platform**: от полного managed до self-service, с экспертизой на каждом уровне.

4. **Upsell-воронка натуральная:** Entry (наши аккаунты) → Mid (микс) → Pro (свои аккаунты + наша экспертиза). Клиент растёт — переход внутри платформы, без миграции.

---

## User Journeys: что причёсывать в первую очередь

> **Логика:** GTM привёл человека → он пошёл по треку → столкнулся с нашими сервисами. На каждом шаге — точка контакта, которая или работает, или теряет клиента. Что сломано/отсутствует = что чинить первым.

### Journey A: Mediation Entry (блэкбокс, наши аккаунты)

> Типичный клиент: инди из СНГ/Азии, 1-3 приложения, не может завести AdMob.

```
GTM                     ONBOARDING              РАБОТА                  РОСТ
─────────────────────── ─────────────────────── ─────────────────────── ───────────────
Google Ads /            Регистрация             Видит revenue           Хочет больше
TG Monetization /       на b2b.cas.ai           в дашборде              контроля
Реферал от клиента                              (Quick View)
        │                    │                       │                      │
        ▼                    ▼                       ▼                      ▼
   cas.ai landing  →   Добавить app      →    Dashboard (OneBI)  →   Mid-level:
   «SDK за 2 часа»     SDK integration         Payments               свои аккаунты
                        Наши аккаунты           Support chat           часть сетей
                        Мы настраиваем                                 Больше BI
                        waterfall
```

**Точки контакта и их состояние:**

| # | Шаг | Сервис | Состояние сейчас | Приоритет |
|---|-----|--------|-----------------|-----------|
| A1 | Нашёл нас | cas.ai landing | Есть, но слабый (конверсия?) | Nikita работает |
| A2 | Регистрация | b2b.cas.ai signup | Работает | Ок |
| A3 | Добавить app | Apps Management | Работает, но UX старый | H2 |
| A4 | SDK интеграция | Docs + SDK | Docs слабые, SDK нестабилен | **SDK stable = P0** |
| A5 | Настройка сетей | Internal (менеджер делает) | 1C, ручная работа | Internal Ops (Задача 5) |
| A6 | Первый revenue | Dashboard | Default mode = тормозит | **OneBI Quick View = P0** |
| A7 | Понять revenue | Quick View (5 карточек) | Нет (старый UI) | **OneBI MVP = P1** |
| A8 | Payments | Billing / payments | Работает, но UX | H2 |
| A9 | Хочет больше | Upsell → Mid | Нет процесса, нет UI | Будущее |

**Вывод Journey A:** Критические дыры = SDK стабильность (A4) и дашборд (A6-A7). Клиент приходит и видит тормозящий UI + нестабильный SDK. Остальное — ок или терпимо.

---

### Journey B: Mediation Pro (self-service, свои аккаунты)

> Типичный клиент: опытный паблишер, 10+ приложений, свои аккаунты во всех сетях, ищет лучшую медиацию или экспертизу.

```
GTM                     ONBOARDING              РАБОТА                  РОСТ
─────────────────────── ─────────────────────── ─────────────────────── ───────────────
BD outreach /           Регистрация             Self-service            Хочет
Конференция /           SDK integration         waterfall config        publishing /
Уход с MAX/LevelPlay    Свои аккаунты сетей     BI: splits, cohorts     UA funding
        │                    │                  alerts, export               │
        ▼                    ▼                       ▼                      ▼
   BD менеджер     →   Onboarding call    →    Console:              →  Publishing
   (HubSpot)           Миграция сетей          OneBI (full)             pipeline
                       Тестовый период          Monetization Config     Growth
                                                Drop Detection          Accelerator
                                                A/B tests
```

| # | Шаг | Сервис | Состояние сейчас | Приоритет |
|---|-----|--------|-----------------|-----------|
| B1 | BD нашёл | HubSpot + BD менеджер | Работает | Ок |
| B2 | Onboarding call | Ручной, нет регламента | Регламент в процессе | Osyka |
| B3 | SDK миграция | Docs + SDK + поддержка | Docs слабые, миграция болезненная | **SDK + DX = P0** |
| B4 | Свои аккаунты | Apps Mgmt + network setup | Ручная настройка через менеджера | Self-Service = H2 |
| B5 | Waterfall config | Сейчас = менеджер в 1C | **Self-Service НЕТ** | Self-Service = H2+ |
| B6 | BI: splits, cohorts | OneBI | **НЕТ** (старый default mode) | **OneBI Reports = P1** |
| B7 | Drop detection | Alerts | **НЕТ** (Excel) | **Drop Det = P1** |
| B8 | A/B тесты конфигов | — | **НЕТ** | H2+ |
| B9 | Хочет publishing | Publishing pipeline | Деприоритизирован H1 | H2+ |

**Вывод Journey B:** Этот клиент НЕ МОЖЕТ прийти сейчас — для него нет продукта. Нет self-service, нет BI, нет A/B. Всё ручное. Чтобы его обслужить, нужны: OneBI (B6), Drop Detection (B7), и хотя бы базовый self-service config (B5).

---

### Journey C: Publishing

> Типичный клиент: студия с прототипом/soft launch, ищет издателя.

```
GTM                     ТЕСТ                    SCALE                   MATURE
─────────────────────── ─────────────────────── ─────────────────────── ───────────────
BD scouting /           Game test               Soft launch             Full CAS
Конференция /           ($200 → CPI/retention)  Мини-SDK (авто-конфиг)  integration
Inbound заявка                                  UA funding              Self-service
        │                    │                       │                  BI, все модули
        ▼                    ▼                       ▼                      ▼
   Ed Hugo /           Тестовая               Полноценный           Клиент = Pro
   BD team             кампания               CAS SDK                level, всё
                       Без SDK или            Наши аккаунты          в одной консоли
                       мини-интеграция        Мы настраиваем
```

| # | Шаг | Сервис | Состояние сейчас | Приоритет |
|---|-----|--------|-----------------|-----------|
| C1 | Нашли студию | BD / Ed Hugo канал | Ed Hugo = $200-300K потенциал | GTM |
| C2 | Game test | Тестовая UA кампания | Ручной процесс, нет платформы | Будущее |
| C3 | Решение: берём | Оценка + контракт | Ручной | Ок для объёмов |
| C4 | Мини-SDK | Облегчённая интеграция | **НЕТ** (сразу полный SDK) | Идея |
| C5 | UA funding | Бюджет на scale | Есть у PSV | Бизнес-решение |
| C6 | Полный SDK | CAS SDK + все сети | = Journey A, шаг A4 | **SDK stable = P0** |
| C7 | Зрелый клиент | Все модули консоли | = Journey B | Зависит от B |

**Вывод Journey C:** Publishing деприоритизирован в H1, и это правильно — он зависит от Journey A/B инфраструктуры. Но Ed Hugo канал ($200-300K) работает и без платформы.

---

### Сводка: что причёсывать в первую очередь

```
                        СЕЙЧАС            H1 2026           H2 2026          2027
                        ──────            ───────           ───────          ────

Все journeys:
  SDK stable            ███ P0 ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  SDK docs / DX         ███ P0 ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Journey A (Entry):
  OneBI Quick View      ░░░░░░ ███ P1 ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  cas.ai landing        ░░░░░░ ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Journey B (Pro):
  OneBI Reports+Splits  ░░░░░░░░░░░░░░░░ ███ P1 ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░
  Drop Detection        ░░░░░░░░░░░░░░░░ ███ P1 ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░
  Self-Service Config   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ███ ▓▓▓▓▓▓▓▓▓▓▓▓▓
  A/B тесты             ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ███ ▓▓▓▓▓▓

Journey C (Publishing):
  Мини-SDK              ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ▓▓▓▓▓▓
  Publishing platform   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ▓▓▓▓▓▓

Internal Ops:
  Internal Ops (от 1C)  ░░░░░░░░░░░░░░░░ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

███ = начало    ▓ = активная работа    ░ = ещё не началось
```

**Приоритет в одном абзаце:** Сначала SDK stable + docs (без этого все три journey ломаются). Потом OneBI Quick View (Entry-клиенты видят хоть что-то). Потом OneBI Reports + Drop Detection (Pro-клиенты получают ценность). Self-Service и Publishing — H2+, потому что зависят от предыдущих слоёв. Internal Ops (миграция с 1C) — параллельный трек, потому что обслуживает менеджеров, а не клиентов.

---

## Почему Вариант C

1. **Appodeal доказал**, что единый дашборд = главное конкурентное преимущество. Unity доказал, что фрагментация = смерть.

2. **Клиент не должен думать в терминах «продуктов»** — он думает в терминах задач: «посмотреть revenue», «настроить сети», «понять почему просело». Модули в одной консоли это обеспечивают.

3. **Тиерная модель** создаёт upsell-воронку без friction: клиент не переходит в другой продукт, а просто видит больше модулей.

4. **SDK + Exchange = невидимы** для паблишера. Он ставит CAS SDK и автоматически получает demand из CASExchange. Ему не нужно знать, что это отдельный продукт.

5. **GTM Stack — internal**, не клиентский. Это инструменты команды CAS для привлечения и удержания, не продукт для рынка.

6. **Масштабируемо:** когда/если CAS выйдет на demand side — добавляется ещё один раздел в Console (Ads Manager), а не отдельный продукт.

---

## Мета: какую задачу это решает

Лестница абстракции — от бытового до стратегического:

0. **Операционка** → "как мигрируем в Asana, как ведём документацию, как общаемся с командой" (процессы, ритуалы, инструменты)
1. **Тактика** → "какие задачи в SDK бэклоге" (50 задач, Asana)
2. **Структура** → "как сгруппировать задачи в Areas/Buckets" (5 направлений)
3. **Портфель** → "какие продукты есть у CAS кроме SDK" (7 семейств)
4. **Позиционирование** → "как это устроено у AppLovin/Appodeal/Unity" (конкурентный анализ)
5. **Мета** → "а зачем я вообще это делаю?"

Уровень 0 — это то, на чём всё держится: Захар настраивает Asana, cas-docs — source of truth, wiki.cas.ai — публичная версия для команды, OneNote — черновики на ходу, Claude — обработка и синтез. Без этого слоя верхние уровни остаются слайдами.

**Program Management** — это и есть клей между уровнями 0-1 (операционка/тактика) и 3-5 (портфель/стратегия). Суть: управление не одним проектом, а **группой связанных проектов** ради стратегической цели, которую ни один проект по отдельности не достигает. Три вещи, которые PM делает, а project management — нет:
- **Зависимости между проектами:** SDK 4.7 блокирует ILRD → блокирует OneBI → блокирует Drop Detection. Задержка в SDK = задержка везде.
- **Ресурсный арбитраж:** Denys, Borys, Женя — по одному на трек. Кого куда кинуть, когда всё горит одновременно?
- **Stakeholder alignment:** Oleg хочет publishing, Osyka — инструменты для AM, Smirnov — drop detection. Кому сказать «подожди» и как объяснить почему?

Применительно к портфелю CAS: все 7 продуктовых семейств зависят от SDK и Data Platform. Это не 7 параллельных проектов — это одна программа с критическим путём: `SDK → ILRD → OneBI → Self-Service`. CPO = program manager этой цепочки.

> **Одним предложением:** Я строю **Product Portfolio Map** — документ, который связывает стратегию (куда идём), архитектуру (из чего состоим), roadmap (в каком порядке) и ownership (кто делает) в единую картину, которую можно показать Осыке на следующем 1:1 и команде на следующем All-Hands.
