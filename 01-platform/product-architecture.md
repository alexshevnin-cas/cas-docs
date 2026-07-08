# CAS — Продуктовая архитектура (канон)

> **Статус:** Актуально · утверждено владельцем продукта 2026-06-03 · акцент обновлён 2026-07-07
> (платформа для внешнего **и внутреннего** потребления)
> **Назначение:** единственный источник правды по слоям продукта, доменам и реестру проектов.
> Все остальные доки ссылаются сюда, а не дублируют карту.

CAS — сервисная компания с технологическим ядром: зарабатываем на комиссии от рекламного
revenue клиентов, предоставляя managed-сервис монетизации через собственный SDK.

Продукт — **платформа управления портфелем приложений**. Это не «клиентский кабинет с
внутренней надстройкой», а одна система с ролевым доступом (RBAC) и двумя равноправными
контурами потребления:

- **Внешний контур** — клиенты (паблишеры и студии): видят и управляют своим портфелем
  через кабинет и аналитику.
- **Внутренний контур** — команды CAS: аккаунт-менеджеры и BD (здоровье клиентов, churn,
  upsell), маркетинг (креативы, кампании), монетизаторы и UA — работают с теми же данными
  через ролевые АРМ и служебные инструменты.

Платформа устроена как **четыре слоя**. Главное правило: **кабинет ≠ OneBI** — OneBI это слой
аналитики, встроенный в кабинет, а кабинет шире.

---

## 1. Четыре слоя

```
СЛОЙ 4 — КАБИНЕТ AM (Account Manager)                 [Alpha] platform.cas.ai · INTERNAL
= кабинет пользователя + служебные функции; ролевые рабочие места (АРМ)
  ├─ АРМ Монетизатора · АРМ UA Manager · АРМ Account Manager
  ├─ OneBI SuperAdmin (Portfolio by Manager/Client, Gross/Net, Churn, Anomaly, AM perf)
  └─ Admin / Internal Services / Super Admin
  └── детали → 03-product/cabinet/am-cabinet.md
  │
  └─ СЛОЙ 3 — КАБИНЕТ ПОЛЬЗОВАТЕЛЯ (Customer's Cabinet)   [Beta] platform.cas.ai
     внутр. код-имя «b2b» (≠ домен). Nav: Home · Analytics · Applications ·
     Networks [SOON] · Payments · Profile
       │
       └─ СЛОЙ 2 — OneBI (Unified UI) = раздел Analytics      [Live]
          Слой аналитики (Looker/Tableau/Superset-аналог), ВСТРОЕН в кабинет.
          OneBI ⊂ кабинет. Аудитория: Customer / Producer / UA Manager / C-Level.
          ├─ Quick View (KPI-карточки + дельты + trend)       [Live]
          ├─ Reports (measures + splits + filters, Table/Chart/Line, Save preset, Export)
          │    ← Mediation + Publishing СЛИТЫ сюда (отдельных страниц в nav нет)
          └─ Cohorts · Real-time (ILRD) · Prediction Revenue  [planned]

СЛОЙ 1 — DATA PLATFORM (конвейер данных, НЕ UI)             [in-progress]
  Sources → Data Lake → Normalization → Semantic Layer → Views → API
  Sources: CMS · split tool · Vocabulary · 1С · CAS.SDK · MMP · Ad Networks · UA Networks
  Semantic Layer: Basic Metrics · Billing/Fees/RevShare · Prediction Models · Compensation coefficients
  Выходы API:  → OneBI / Analytics Framework   → Admin API (+ Raw Data)
  Реализация:  OneBi Backend (Laravel 12, DDD). QuickView API + Reports API Phase 1 [live].
               ClickHouse [live] · materialized views (лимит split=3) · RBAC · Sanctum [in-progress]
```

> **Статусы.** OneBI (Embedded Dashboards) = **Live** (трекер Platforms). Customer's Cabinet =
> **Beta** (решение владельца 2026-06-03; трекер местами помечает Alpha — зафиксирован Beta).
> AM Cabinet = **Alpha** (трекер). Статус-таксономия: `Live / Alpha / Project / Migrate / Sunset`.

---

## 2. Потребители платформы

Роль определяет scope данных, доступные метрики и функции — интерфейс один, данные разные.

| Контур | Кто | Что потребляет | Где в слоях |
|--------|-----|----------------|-------------|
| Внешний | **L1 / L2** (медиация), **Pub / PubC** (паблишинг) | Revenue, отчёты, платежи, портфель приложений | Слой 3 (кабинет) + Слой 2 (OneBI) |
| Внутренний | **Account Manager / BD** | Портфель клиентов: BD Dashboard (Revenue / DAU / Churn Risk, дерево MRR→ARR), assignments, impersonation, OneBI SuperAdmin | Слой 4 |
| Внутренний | **Монетизатор** | Разгон eCPM портфеля: CAS Configuration, SplitEngine A/B | Слой 4 |
| Внутренний | **UA Manager** | Закреплённые игры/кампании: ROAS, LTV, CPI | Слой 4 |
| Внутренний | **Маркетинг** | Creatives Catalog, Campaign Interactive Dashboards | Дата-платформа (Growth / Publishing) |
| Внутренний | **Admin / Finance / Support** | Организации, роли, аудит, биллинг | Слой 4 (RBAC: 7 internal-ролей) |

Детали внутренних АРМ и RBAC → `03-product/cabinet/am-cabinet.md`.
Полный реестр пользователей (типы × RBAC-роли × BI-коды, с расхождениями) → `01-platform/platform-users.md`.

---

## 3. Домены

| Домен | Статус | Роль |
|-------|--------|------|
| **platform.cas.ai** | Живой, основной | Целевой хост кабинета + OneBI + AM-сборки (футер «CAS.AI Analytics platform») |
| **b2b.cas.ai** | Legacy, жив на период перехода | Старый кабинет (`/mediation`, `/publishing`, `/mypayments`). «b2b» = внутр. код-имя кабинета, **не** домен |
| **onebi.cas.ai** | **Мёртв (потушен)** | Не использовать |
| onebi-dev.cas.ai | Устарел | dev-stage, не использовать |

---

## 4. Смежные продукты на дата-платформе (вне кабинета)

- **Mediation Platform / CAS.AI SDK** — основной продукт-двигатель: Core 4.5.x [live]; треки
  Stable + Feature [in-progress]; adapters, plugins, ILRD, R&D Toolkit, Core Waterfall (5.0, Q1 2027).
  → `03-product/sdk-release-policy.md`, `03-product/job-tech-pm-mediation.md`
- **Growth / Publishing** — Publishing (Profit Share) [live, UX слит в Analytics]; маркетинговый
  контур внутреннего потребления: Creatives Catalog на Superset [Project] + Campaign Interactive
  Dashboards [Project]; сюда же относится старый набор сервисов **Internal/PSV** (паблишинг игр).
- **CAS Configuration** — АРМ монетизатора (заказ из `horyk-portfolio-monetization-brief.md`); часть Слоя 4.

---

## 5. Вне платформенной карты (граница системы)

Эти системы взаимодействуют с платформой, но **не являются её частью**:

- **CAS Exchange** — отдельная компания холдинга.
- **1С** — ERP. На карту продукта не выносится, **но остаётся источником данных Слоя 1**.
- **HubSpot / Bitrix** — внешние CRM (GTM).
- **Студийные тулзы CAS Games** (Shops, Price Management, ASO, Admob/CMS Admin, …) — операции студии PSV.

---

## 6. Реестр проектов (снимок трекера Platforms, 2026-06-03)

Оперативный борд живёт в `Operations/cas-projects.md`; здесь — стабильный канон-срез с привязкой к слою.

| Проект | Слой / ветка | Статус | Product | Dev |
|--------|--------------|--------|---------|-----|
| Embeded Dashboards (One BI) | Слой 2 — OneBI | **Live** | Alexei Shevnin | Evgeny Chuyko |
| Customer's Cabinet (код «b2b») | Слой 3 — Кабинет юзера | **Beta** | Maksym Balatskyi | Evgeny Chuyko |
| AM Cabinet | Слой 4 — Кабинет AM | **Alpha** | Maksym Balatskyi | Ruslan Novikov |
| Admin Panel («Kontora») | Слой 4 | Project | Ruslan Novikov | Ruslan Novikov |
| CAS Configuration. JSON Builder | Слой 4 / CAS Configuration | Project | Alexei Shevnin | New Developer |
| Internal A/B Tests (SplitEngine) | Слой 4 / монетизация | Migrate | Vladyslav Horyk | Ruslan Novikov |
| Bot Managent | Слой 4 (on hold) | Project | Alexei Shevnin | New Developer |
| Internal (PSV) | Growth / Publishing | Migrate | Maksym Balatskyi | Ruslan Novikov |
| Creatives Catalog | Growth / Publishing | Project | Alexei Shevnin | Ruslan Novikov |
| Campaign Interactive Dashboards | Growth / Publishing | Project | Borys Shyfrin | Ruslan Novikov |
| Shops · Price Management · ASO · Admob/CMS Admin | Вне платформы (CAS Games ops) | Migrate | Yuriy Vityuk | Bohdan Pryidun |
| Creating Request · Reports · TENJIN · SuperSet · BigQuery · … | Вне платформы (CAS Games ops) | **Sunset** | Yuriy Vityuk | Ruslan Novikov |

---

## 7. Привязка к стратегии (3 уровня роста)

Связь слоёв с тремя уровнями роста из `03-product/product-strategy-1pager.md` (без дублирования текста):

- **Уровень 1 «Quantity»** (СЕЙЧАС) — customer-facing: Слой 3 (Кабинет) + Слой 2 (OneBI). По факту
  уже в проде/Beta на platform.cas.ai — ближе к завершению, чем рисовала старая стратегия.
- **Уровень 2 «Quality»** (СЛЕДУЮЩИЙ) — качество монетизации: Слой 4 (АРМ Монетизатора + CAS Configuration),
  SplitEngine A/B, алерты, OneBI SuperAdmin (portfolio view).
- **Уровень 3 «Engine»** — технология аукциона: внутри Mediation Platform / SDK (Server Bidding,
  Core Waterfall 5.0). Фундамент под все три уровня — Слой 1 (Data Platform).

---

## Связанные документы

- Карта контекстов (границы, стыки, владельцы): `01-platform/context-map.md`
- Стратегия: `03-product/product-strategy-1pager.md`
- Roadmap: `03-product/roadmap.md`
- Кабинет (Слой 3): `03-product/cabinet/overview.md`
- Кабинет AM / ролевые АРМ (Слой 4): `03-product/cabinet/am-cabinet.md`
- OneBI (Слой 2): `03-product/onebi-glossary.md`, `03-product/design-spec-bi.md`, `04-bi/metrics-dictionary.md`
- Data Platform (Слой 1): `03-product/onebi-dev/` (ADR, API spec, DDD guide)
- Legacy b2b-фронт (референс для рефакторинга): `03-product/cabinet/legacy-fe-spec.md`
