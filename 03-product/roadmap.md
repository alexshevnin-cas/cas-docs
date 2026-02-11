# CAS — Roadmap

> **Версия:** 1.0
> **Дата:** 2026-02-09
> **Статус:** Черновик
> **Источники:** product-strategy.md, modernization-plan.md, интервью клиентов, встреча CTO 09.02

---

## Принцип

Roadmap организован по **трекам** — параллельным потокам работы с отдельными владельцами и бэклогами. Внутри каждого трека — **инициативы** с конкретным результатом и статусом.

Треки работают параллельно. Зависимости между треками — явные (указаны в каждой инициативе).

**Определённость убывает с горизонтом.** H1 — понятно что и как. H2 — понятно что, но не как. Beyond — стратегические ставки.

---

## Треки

| Track | Суть | Владелец |
|-------|------|----------|
| **Core / Ядро** | SDK, адаптеры, bidding, сети, R&D, internal ops, trust/compliance | Denis + Vova |
| **Data / Данные** | ClickHouse, ILRD, ETL, semantic layer, коннекторы MMP | Boris + data team |
| **Portal / Кабинет** | Cabinet UI, BI аналитика, онбординг, UX | Ruslan + Product |
| **Services / Сервисы** | Predictive LTV, creative management, UA-оптимизация, бенчмарки | Product + Data |
| **Finance / Финансы** | Биллинг, reconciliation, выплаты, комиссии, 1С-миграция | Product + Backend |
| **Growth / Рост** | Сайт, воронки, контент, реклама, in-product маркетинг, community | Marketing + Product |
| **DX / Dev Experience** | SDK-документация, guides, technical onboarding, developer support | Core + Product |
| **BX / Biz Experience** | B2B-онбординг, account management, consulting, бизнес-отчётность | BD + Product |

---

## Путь клиента по трекам

```
Разработчик:  Growth → DX → Core → Portal → Services
Бизнесмен:    Growth → BX → Core (за него делают) → Portal → Services

L1:   Core + Portal (базовый)
L2:   Core + Portal + часть Services
Pub:  Core + Portal + все Services + BX (agency model)
PubC: Growth → DX → Core → Portal (минимальный)
```

---

## Core / Ядро

SDK, адаптеры, server bidding, рекламные сети, R&D эксперименты, internal ops, trust/compliance.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| C1 | Стабильность SDK, баг-фиксы | Ongoing | В работе | — |
| C2 | Новые рекламные сети | H1 | В работе | — |
| C3 | Server bidding | H1 | В работе | — |
| C4 | Monetization Management (internal tool) | H1 | Планируется | — |
| C5 | SDK Release Process (автоматизация) | H1 | Планируется | — |
| C6 | Quality Control (автоматизация) | H1 | Планируется | — |
| C7 | A/B Testing Split Engine | H2 | Планируется | Data: D3 (ILRD) |
| C8 | Experiment Registry с результатами в BI | H2 | Планируется | C7, Portal: P2 |
| C9 | Trust: ATT compliance, ad quality, fraud prevention | Ongoing | Не формализовано | — |
| C10 | Desktop/Extension SDK (новая ниша) | Beyond | Идея | Исследование (Савенков) |

**Связь:** 13 R&D-гипотез для тестирования — `03-product/rnd-hypotheses.md`

---

## Data / Данные

ClickHouse, ILRD, ETL-пайплайны, semantic layer, коннекторы MMP. Enabler для Portal и Services.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| D1 | Materialized views из существующих данных (Network Reports) | H1 | Планируется | Boris |
| D2 | Self-hosted ClickHouse (миграция с облака, 500 ГБ ILRD) | H1 | Планируется | Infra |
| D3 | ILRD processing (impression-level revenue data) | H1-H2 | Планируется | D2 |
| D4 | Semantic layer (канонические сущности: Install, DAU, Impression, Revenue) | H2 | Концепт | D3 |
| D5 | MMP-коннекторы (AppsFlyer, Adjust, Tenjin) | H2 | Концепт | D4, договорённости с клиентами |
| D6 | Data quality monitoring | H2 | Не начато | D3 |

**Архитектура:** Layered Data Platform (R2) — `03-product/product-strategy.md`, секция 3.

**Что разблокирует каждый шаг:**

| Data | Portal получает | Services получают | Core получает |
|------|----------------|-------------------|---------------|
| D1 (materialized views) | MVP BI: Revenue, DAU, eCPM, Fill Rate | — | — |
| D3 (ILRD) | Разбивка по SDK/App version, когорты | — | Анализ влияния релизов SDK |
| D5 (MMP) | Unified Report | Predictive LTV, ROAS | — |

---

## Portal / Кабинет

Cabinet UI, BI-аналитика, онбординг, UX. Витрина продукта для клиента.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| P1 | **MVP BI** — Quick View + Reports, тёмная тема, экспорт CSV, eCPM per ad type, сравнение периодов, chip-фильтры | H1 | Ждёт дизайн | Data: D1, дизайнер |
| P1a | Toggle gross/net (комиссия CAS) | H1 | Планируется | P1 |
| P1b | Карточка приложения (owner, portfolio, manager, commission) | H1 | Планируется | P1 |
| P1c | UX-фиксы (10 багов из интервью Савенкова) | H1 | Планируется | P1 |
| P2 | **L2 Features** — SDK/App version splits, метрики по сетям, Saved Views, Deep Linking, Export Excel | H1-H2 | Планируется | Data: D3 (ILRD) |
| P3 | **Onboarding** — welcome flow, квалификация, интеграция SDK, first data celebration | H2 | Спецификация готова | P1 |
| P4 | **PubC Portal** — self-service тест игры, status badge, креативы | H2 | Концепт | P3, Data: D5 |
| P5 | **Pub Dashboard** — profit, ROAS, health indicator, A/B comparison | H2 | Концепт | Data: D5, Services: S1 |
| P6 | **Admin Dashboard** — portfolio overview, группировка по менеджерам, anomaly detection | H1-H2 | Планируется | P1, Data: D1 |

**Дизайн-спек:** `03-product/design-spec-bi.md`
**User stories:** `03-product/user-stories.md` (78 шт.)
**Онбординг:** `03-product/onboarding-flow.md`

---

## Services / Сервисы

Надстройка над Core + Data. То, чем CAS отличается от commodity-медиации. Дифференциатор и инструмент upsell.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| S1 | Predictive LTV (вынести наружу, есть внутри) | H2 | Концепт | Data: D5 (MMP) |
| S2 | Creative management (upload + performance table) | H2 | Концепт | Portal: P4 |
| S3 | UA-оптимизация (campaign/network management) | H2 | Концепт | Data: D5 |
| S4 | Бенчмарки (средние по сети CAS, по категориям) | H2 | Концепт | Data: D3+ |
| S5 | Market trends (хайпящие жанры) | Beyond | Идея | Data |
| S6 | Unified Report (Spend + Revenue + Events) | H2 | Концепт | Data: D5 |

**Источники:** интервью Жвиков (LTV), Мельников (creatives, trends), Савенков (unified report, benchmarks)

---

## Finance / Финансы

Биллинг, reconciliation с сетями, комиссии, выплаты, 1С-миграция.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| F1 | Payments UI redesign (баланс, withdraw, adjustments) | H1 | Планируется | Portal: P1 (дизайн) |
| F2 | Commission management (per-app ставки, gross/net toggle) | H1 | Планируется | P1a |
| F3 | Revenue reconciliation (автоматизация сверки с сетями) | H2 | Не начато | Data: D1+ |
| F4 | 1С-миграция (полный уход с legacy) | H2 | Не начато | F1, F2, F3, Portal: P6 |

**User stories:** US-Pay-01..06 в `03-product/user-stories.md`
**Источник:** интервью Osyka (02.02)

---

## Growth / Рост

Привлечение и удержание клиентов. Сайт, контент, воронки, реклама, in-product маркетинг, community.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| G1 | Лендинг "Submit your game" (PubC воронка, AppQuantum стиль) | H1 | Планируется | — |
| G2 | Лендинги по типам клиентов (L1/L2/Pub) | H1 | Планируется | — |
| G3 | Контент-машина (блог, Telegram, гайды по монетизации) | H1 | Планируется | — |
| G4 | Витрина кабинета на сайте (скриншоты BI) | H1 | Ждёт | Portal: P1 (нужны макеты) |
| G5 | Email-триггеры (welcome, nudge, milestone) | H1-H2 | Планируется | Email service |
| G6 | In-app нотификации (operational, diagnostic, upsell) | H2 | Концепт | Notification service |
| G7 | Upsell-триггеры (DAU-based, retention-based) | H2 | Концепт | Portal: P2, Data: D3 |
| G8 | Community — Telegram-канал, developer community | H1 | Не начато | — |
| G9 | A/B тестирование лендингов | H1-H2 | Не начато | G1, G2 |

**Документы:** `06-marketing-site/website-plan.md`, `06-marketing-site/content-machine.md`, `06-marketing-site/content-backlog.md`

**Не зависит от Data/Portal:** G1, G2, G3, G8 — можно начинать сейчас.

---

## DX / Dev Experience

Как разработчик интегрирует CAS SDK. Документация, guides, technical onboarding, support.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| DX1 | Аудит текущей SDK-документации | H1 | Не начато | — |
| DX2 | Integration quickstart (5-минутный guide) | H1 | Не начато | — |
| DX3 | Changelog + migration guides при обновлении SDK | H1 | Не формализовано | Core: C5 |
| DX4 | Sample projects (Unity, Native Android, iOS) | H1-H2 | Не начато | — |
| DX5 | Developer portal (единая точка входа в документацию) | H2 | Концепт | — |

---

## BX / Biz Experience

Как бизнесмен работает с CAS как с агентством. B2B-онбординг, account management, consulting.

### Инициативы

| # | Инициатива | Горизонт | Статус | Зависимости |
|---|-----------|----------|--------|-------------|
| BX1 | Формализация B2B-онбординга (бриф, договор, настройка) | H1 | Не формализовано | — |
| BX2 | Шаблон клиентского отчёта (monthly review) | H1 | Не начато | — |
| BX3 | VIP Monetization Setup (процесс + measurement) | H1 | Существует неформально | — |
| BX4 | Client health dashboard (churn risk, upsell candidates) | H2 | Концепт | Portal: P6, Data: D1 |
| BX5 | ROI-калькулятор для sales pitch | H1 | Не начато | — |

**User stories:** US-BD-01..05 в `03-product/user-stories.md`

---

## Зависимости между треками

```
         Core ◄──────────────────────────────────────┐
          │                                           │
          ▼                                           │
        Data ──────────────────┐                      │
          │                    │                      │
          ▼                    ▼                      │
       Portal ◄──────────── Finance                   │
          │                                           │
          ├──────────► Services (надстройка над Data + Portal)
          │
          ▼
       Growth (витрина Portal + контент)
          │
          ├──► DX (техническая воронка)
          └──► BX (бизнес-воронка)
```

**Критический путь для Portal:**
```
Data: D1 (materialized views) → Portal: P1 (MVP BI) → всё остальное
```

**Параллельно и без зависимостей (можно начинать сейчас):**
- Growth: G1, G2, G3, G8
- DX: DX1, DX2
- BX: BX1, BX2, BX3, BX5
- Core: C1, C2, C3, C4, C5, C6
- Finance: F1 (дизайн)

---

## H1 2026 — фокус

| Track | Ключевые инициативы |
|-------|-------------------|
| Core | Стабильность, новые сети, server bidding, internal tools |
| Data | Materialized views, self-hosted ClickHouse, начать ILRD |
| Portal | **MVP BI** (Quick View + Reports), Payments UI, Admin dashboard |
| Finance | Payments redesign, commission management |
| Growth | Лендинги (PubC, по типам), контент-машина, community |
| DX | Аудит доков, quickstart guide |
| BX | Формализация онбординга, шаблон отчёта, ROI-калькулятор |

## H2 2026 — фокус

| Track | Ключевые инициативы |
|-------|-------------------|
| Core | A/B split engine, experiment registry |
| Data | ILRD полностью, MMP-коннекторы, semantic layer |
| Portal | L2 features, onboarding, PubC portal, Pub dashboard |
| Services | Predictive LTV, creative management, unified report, бенчмарки |
| Finance | Reconciliation, 1С-миграция |
| Growth | In-app нотификации, email-триггеры, upsell |
| DX | Developer portal, sample projects |
| BX | Client health dashboard |

---

## Решения (встреча CTO 09.02)

Ключевые решения, влияющие на roadmap — `03-product/modernization-plan.md`, секция "Решения".

---

## Связанные документы

| Документ | Что даёт |
|----------|---------|
| `03-product/product-strategy.md` | Полная стратегия (6 стримов, архитектура, роли) |
| `03-product/modernization-plan.md` | Фазы модернизации BI, решения CTO |
| `03-product/design-spec-bi.md` | UI-спецификация (Quick View, Reports) |
| `03-product/user-stories.md` | 78 user stories по ролям |
| `03-product/onboarding-flow.md` | Flow онбординга |
| `04-bi/metrics-dictionary.md` | 100+ метрик |
| `04-bi/filters.md` | Фильтры и сплиты |
| `03-product/rnd-hypotheses.md` | 13 R&D-гипотез |
| `06-marketing-site/website-plan.md` | План маркетингового сайта |
| `06-marketing-site/content-machine.md` | Контент-стратегия |
