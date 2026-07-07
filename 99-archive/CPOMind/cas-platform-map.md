# CAS.AI Platform — Product Map

> **Дата:** 2026-03-18
> **Статус:** Черновик. Зонтичная схема всех продуктов экосистемы.
> **Источники:** product-architecture-research.md, встреча с Horyk 17.03.2026

---

```
CAS.AI PLATFORM (зонтик)
│
├── КЛИЕНТСКИЕ ПРОДУКТЫ (что видит паблишер / разработчик)
│   │
│   ├── CAS Cabinet
│   │   ├── Apps Management
│   │   ├── Payments
│   │   ├── Onboarding
│   │   ├── Notifications
│   │   ├── Help / AI Bot
│   │   └── Docs
│   │
│   ├── OneBI
│   │   ├── Quick View (5 карточек: DAU, Revenue, ARPDAU, eCPM, Impr)
│   │   ├── Reports (splits, фильтры, graph + table)
│   │   ├── Cohorts
│   │   ├── Real-time (ILRD)
│   │   └── Exports (CSV, Excel)
│   │
│   ├── CAS SDK
│   │   ├── Core Mediation (waterfall + bidding)
│   │   ├── Adapters (30+ сетей)
│   │   ├── Plugins (Unity, Unreal, Godot, RN)
│   │   └── ILRD (impression-level revenue data)
│   │
│   ├── CAS Content
│   │   ├── cas.ai site
│   │   ├── Landings
│   │   └── Community
│   │
│   └── CAS Cabinet Publishing [later]
│       ├── PubC Portal (submit game → test → status badge → CTA)
│       └── Publishing Partner (UA funding, expert setup, rev share)
│
└── ПОД КАПОТОМ (не видно клиенту)
    │
    ├── Internal products (для менеджеров CAS)
    │   │
    │   ├── CAS Configuration ★ ПРИОРИТЕТ
    │   │   │
    │   │   ├── Интерфейс монетизатора (бизнес-слой)
    │   │   │   ├── Начальная настройка приложения (дефолтный сетап)
    │   │   │   ├── Редактирование дефолтных сетапов
    │   │   │   ├── Кастомные сетапы для A/B тестов конфигов
    │   │   │   ├── SplitEngine (A/B тесты монетизации)
    │   │   │   │   ├── Self-service запуск экспериментов
    │   │   │   │   ├── Experiment Registry
    │   │   │   │   └── Auto-Significance (подвязка к OneBI)
    │   │   │   └── Drop detection / алерты
    │   │   │
    │   │   └── Техническая обвязка (под капотом)
    │   │       ├── Dispatch ботам (задачи на настройку сетей)
    │   │       ├── Синхронизация конфигов: сервер ↔ зелёный сайт ↔ SDK
    │   │       └── Network management (подключение/отключение сетей)
    │   │
    │   ├── OneBI SuperAdmin
    │   │   ├── Portfolio view by Manager/Client
    │   │   ├── Gross/Net toggle
    │   │   ├── Churn risk
    │   │   ├── Anomaly detection
    │   │   └── AM performance
    │   │
    │   ├── Growth Tools (Publishing)
    │   │   ├── Creatives Catalog
    │   │   ├── Campaign Management
    │   │   ├── Cross Promo
    │   │   └── Benchmarks
    │   │
    │   ├── 1С (legacy, остаётся пока)
    │   │   ├── Client Ops
    │   │   ├── Billing / сверка
    │   │   ├── Реферальная программа
    │   │   ├── Revenue reports
    │   │   ├── Scorecard
    │   │   └── HubSpot↔Bitrix маппинг
    │   │
    │   └── GTM Tools
    │       ├── HubSpot CRM
    │       ├── Bitrix CRM
    │       ├── Attribution
    │       └── Referral
    │
    └── Инфраструктура
        │
        ├── CAS SDK (runtime)
        │   ├── Core engine
        │   ├── ILRD tracker
        │   ├── Зелёный сайт (remote config)
        │   ├── Events Server
        │   └── Bidding Server
        │
        ├── CAS Exchange
        │   ├── SSP
        │   ├── VAST/VPAID
        │   ├── ORTB (external DSPs)
        │   ├── Cross-Promo
        │   └── PSV inventory
        │
        ├── Data Platform
        │   ├── ClickHouse
        │   ├── ILRD pipeline
        │   ├── Materialized views
        │   ├── ETL
        └── Compensation coefficients
```

---

## Элементы зонтика

| # | Элемент | Аудитория | Статус |
|---|---------|-----------|--------|
| 1 | **CAS SDK** | Разработчики | Есть, стабилизация P0 |
| 2 | **CAS Cabinet** | Клиенты | Есть, редизайн H1 |
| 3 | **OneBI** | Клиенты + Internal | В разработке, Phase 1-2 |
| 4 | **CAS Configuration** (вкл. SplitEngine) | Команда монетизации (Горик) | Бэклог, приоритет H1-H2. SplitEngine — Phase 4 |
| 5 | **Growth Tools** | Publishing команда (internal) | Частично (Creatives Catalog начат) |
| 6 | **CAS Publishing** | PubC/Pub клиенты | Деприоритизирован H1 |
| 7 | **CAS Exchange** | Невидим клиенту | Вова продвигает, отдельный трек |

---

## CAS Configuration — что это

**АРМ (автоматизированное рабочее место) команды монетизации Горика.** Это dashboard, через который монетизаторы управляют настройками рекламы для всех клиентов CAS.

Сейчас команда Горика работает через 1С — медленно, негибко, 80% тестов Горик правит за людьми вручную. CAS Configuration заменяет 1С как прокладку: монетизатор настраивает → конфиг уходит напрямую на зелёный сайт → SDK получает актуальную конфигурацию.

**Кто пользуется:** Влад Горик (Chief Monetization) и его два отдела — настройки/A/B/сети и подключение клиентов. ~10 человек.

**Зачем:** снять bottleneck Горика, дать гибкие тесты по странам (сейчас только full countries), увеличить пропускную способность команды без найма.

**Куда растёт:** интерфейс монетизатора → со временем часть функций (waterfall config, A/B) открывается крупным клиентам как self-service в CAS Cabinet.

---

## Связанные документы

- [Product Architecture Research](product-architecture-research.md) — конкурентный анализ + варианты архитектуры
- [One BI Roadmap](../03-product/onebi-roadmap.md) — фазовый план OneBI
- [SDK Release Policy](../03-product/sdk-release-policy.md) — регламент релизов SDK
- [Creatives Catalog](../03-product/creatives-catalog.md) — спека Growth Tools
