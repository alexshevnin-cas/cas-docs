# CAS — Карта контекстов (Context Map)

> **Статус:** v1 · 2026-07-08 · выведена из существующих доков (канон, cabinet/, am-cabinet,
> client-types, horyk-brief, tz-consolidated-report-1c, sdk-release-policy)
> **Назначение:** границы смысла = границы данных, команд, доступа и контрактов.
> Канон слоёв (`product-architecture.md`) — вертикаль «из чего состоит продукт»;
> эта карта — горизонталь «где проходят границы и что течёт между ними».
> **Правило пользования:** фича, которая заставляет два контекста лезть в модель друг друга
> напрямую (мимо контракта), — неправильная, каким бы быстрым решение ни казалось.

---

## 1. Контексты («участки»)

| # | Контекст | Модель внутри (что это «на самом деле») | Слой | Владелец (Product / Dev) | Статус |
|---|----------|------------------------------------------|------|--------------------------|--------|
| 1 | **Identity & Access** | Организация (publisher / studio / cas_internal) × 13 ролей × role templates; impersonation, audit log | 3–4 | Cabinet team (Maksym / Evgeny); Admin Panel — Ruslan | Alpha (RBAC v1) |
| 2 | **Портфель приложений (App Registry)** | Приложение как объект регистрации: bundle ID, store, платформа, SDK key, статусы (SDK, app-ads.txt, COPPA), имена/иконки из Store | 3 | Cabinet team (Maksym / Evgeny) | Частично (`/applications`) |
| 3 | **Медиация (SDK runtime)** | Аукцион на устройстве: waterfall-исполнение, адаптеры, ILRD, server bidding (4.7+) | вне UI; питает Слой 1 | SDK team (Denys Yeshchenko) | Live (Core 4.5.x) |
| 4 | **Конфигурация монетизации** | Mediation group = сети + страны + waterfall + floors; дефолтные сетапы по сегментам; A/B (SplitEngine). North Star: ARPDAU портфолио (~2000 apps) | 4 | Горик (домен) / Alexei (продукт) / New Dev | ⚠ живёт в 1С + Excel; целевой АРМ — CAS Configuration [Project] |
| 5 | **Data Platform (конвейер)** | Источник → Data Lake → Normalization → Semantic Layer (метрики, Billing/Fees/RevShare, Prediction) → Views → API | 1 | OneBi Backend (Evgeny; Laravel DDD, ClickHouse) | In-progress; QuickView + Reports API Phase 1 — Live |
| 6 | **Аналитика (OneBI UI)** | Measure × split × filter; presets, export; QuickView + Reports | 2 | Alexei / Evgeny | Live |
| 7 | **Финансы клиента** | Баланс (available/pending), выплаты, инвойсы, fraud adjustments, комиссии, revshare | 3 | **владельца нет** (в реестре проектов нет проекта) | Частично (показ из 1С) |
| 8 | **Паблишинг / UA** | Кампания, installs, spends, ROAS, profit share; UA-бюджеты по портфелю | Growth | Maksym / Ruslan (Internal PSV) | Migrate |
| 9 | **Портфель клиентов (AM/BD)** | Клиент как управляемый объект: assignments, churn risk, MRR→ARR, AM performance, upsell L1→L2→Pub | 4 | Maksym / Ruslan (AM Cabinet) | Alpha; BD Dashboard / SuperAdmin [planned] |
| 10 | **Маркетинг-контур** | Креативы (Creatives Catalog), кампании (Campaign Interactive Dashboards) | Growth | Alexei, Borys / Ruslan | Project |
| 11 | **Коммуникации** | Алерты, нотификации, баннеры, human touch, онбординг-тур | 3 | **владельца нет** | Кандидат (2 hardcoded баннера) |

**Внешние системы** (не контексты платформы; связь только через стык):
**1С** (ERP: биллинг, контрагенты, mediation groups, данные менеджеров) · **HubSpot / Bitrix** (CRM) ·
**Ad Networks / UA Networks / MMP** (reporting API) · **Stores** (метаданные приложений) · **CAS Exchange** (OpenRTB, будущее).

---

## 2. Термины, меняющие смысл на границах

Доказательство того, что границы проведены не произвольно: одно слово — разные модели.

| Термин | В контексте… | Означает… |
|--------|--------------|-----------|
| **Приложение** | App Registry | bundle ID + store + статусы интеграции |
| | Конфигурация | юнит с waterfall-конфигом и floor prices |
| | Финансы | объект биллинга (выплаты, revshare) |
| | Паблишинг/UA | игра с экономикой закупки (CPI, ROAS, LTV) |
| | Аналитика | dimension для split/filter |
| **Revenue** | Медиация/Аналитика | gross ad revenue от сетей |
| | Финансы | net после комиссии CAS; выплата |
| | Паблишинг | RevShare / profit share |
| | Портфель клиентов | MRR/ARR, тренд для churn risk |
| **Клиент** | CRM (внешн.) | лид с воронкой (8 статусов из ТЗ реестра 1С) |
| | Identity & Access | организация с ролями и tenant-изоляцией |
| | 1С (внешн.) | контрагент с фактическими деньгами |
| | Портфель клиентов | строка портфеля AM с churn-индикаторами |
| **Платформа** | RBAC | Publishing / Monetization / Internal |
| | App Registry | iOS / Android |
| | Канон | сама CAS Platform |
| **Кампания** | Паблишинг/UA | закупочная кампания (spend, ROAS) |
| | Маркетинг-контур | маркетинговая кампания CAS |

---

## 3. Карта связей

```
ВНЕШНИЙ КОНТУР                                ВНУТРЕННИЙ КОНТУР
L1 · L2 · Pub · PubC                          AM/BD · Монетизатор · UA · Маркетинг · Admin
     │                                              │
     └────────────┬─────────────────────────────────┘
                  ▼
   ┌─ [1] Identity & Access (кто ты → какие контексты и в каком объёме видишь) ─┐
   │                                                                            │
   │  [2] App Registry   [6] OneBI UI   [7] Финансы   [9] Портфель клиентов     │
   │        │                 │              │              │                   │
   └────────┼─────────────────┼──────────────┼──────────────┼───────────────────┘
            │        QuickView/Reports API ★ │              │
            │                 │              │              │
            ▼                 ▼              │              │
   ┌──────────────── [5] DATA PLATFORM ──────┼──────────────┼──────────┐
   │  ClickHouse · Semantic Layer · Views    │              │          │
   └───▲──────▲──────▲──────▲────────────────┼──────────────┼──────────┘
       │      │      │      │                │              │
   [3] SDK   Ad/UA  MMP   CMS             ═══╪══ 1С ════════╪═══ CRM (HubSpot/Bitrix)
   (Медиация) Networks                       ║  ERP         ║
       ▲                                     ║              ║
       └── конфиг (JSON) ── [4] Конфигурация ╝ (сейчас в 1С)║
                                 ▲                          ║
                            SplitEngine A/B         Единый реестр клиентов (ТЗ, фаза 1)
```
★ — эталонный стык: явный API-контракт между командами.

---

## 4. Стыки (здесь живут баги и ручной труд)

| Стык | Канал сейчас | Статус | Риск / боль |
|------|--------------|--------|-------------|
| Data Platform → OneBI | **QuickView + Reports API** | Live | ★ эталон; воспроизводить для остальных границ |
| SDK → Data Platform | события, ILRD | Live | контракт версионируется релизной политикой SDK |
| Ad/UA Networks, MMP → Data Platform | reporting API | Live | внешние API меняются без предупреждения |
| Конфигурация → SDK | JSON-конфиг | Live | «один JSON на всех», ручная кастомизация крупным; race condition SDK↔регистрация |
| SplitEngine → Конфигурация | ручной запуск A/B | Migrate | 80% тестов Горик правит вручную |
| **1С ↔ Конфигурация** | mediation groups ведутся в 1С | ⚠ | ERP используется как конфигуратор — смешение контекстов; лечится CAS Configuration (strangler) |
| **1С ↔ Финансы клиента** | биллинг/выплаты, кабинет показывает | ⚠ | нет ACL и владельца; «заказать выплату» упрётся в этот стык |
| 1С → Кабинет (human touch) | данные менеджера клиента | Planned (ТЗ рестайлинга) | — |
| **CRM ↔ Портфель клиентов** | вручную; поле `bitrix_deal_link`, Excel-сведение | ⚠ | «никто не может ответить, сколько клиентов пришло в марте и сколько принесли»; Единый реестр в 1С (ТЗ) = будущий ACL |
| Stores → App Registry | нет (bundle ID руками) | Planned | имена/иконки из Store — в ТЗ рестайлинга |
| App Registry ↔ остальные | ID приложения | Live | registry потребляют оба контура — строить один раз, не 4 |

---

## 5. Что карта показывает (находки v1)

1. **1С — самый нагруженный узел карты: 4 стыка** (финансы, конфигурация, реестр клиентов, human touch). Это главный кандидат на anti-corruption layer; стратегия уже движется правильно — CAS Configuration вытягивает из 1С контекст конфигурации по паттерну strangler.
2. **Два контекста без владельца:** Финансы клиента (в реестре проектов нет ни одного проекта про выплаты) и Коммуникации. Для финансов это риск: «вопрос доверия» по cabinet/overview, а хозяина нет.
3. **Эталонный стык уже есть** — QuickView/Reports API. Модель «явный контракт + владелец с двух сторон» надо воспроизводить на остальных границах (в первую очередь 1С ↔ Финансы).
4. **«Приложение» и «клиент» — термины с 4–5 значениями.** При проектировании любого API/экрана фиксировать, в каком контексте употребляется термин; не строить «универсальную сущность».
5. **App Registry потребляют оба контура** (клиент, AM, монетизатор, админ) — один контекст, четыре интерфейса; не дублировать реализацию.

---

## Связанные документы

- Канон слоёв и потребителей: [`product-architecture.md`](product-architecture.md)
- RBAC и внутренние АРМ: [`../03-product/cabinet/am-cabinet.md`](../03-product/cabinet/am-cabinet.md)
- Кабинет (Слой 3): [`../03-product/cabinet/overview.md`](../03-product/cabinet/overview.md)
- Заказ АРМ монетизатора: [`../03-product/horyk-portfolio-monetization-brief.md`](../03-product/horyk-portfolio-monetization-brief.md)
- Единый реестр клиентов (1С): [`../03-product/tz-consolidated-report-1c.md`](../03-product/tz-consolidated-report-1c.md)
- Типы клиентов: [`../02-business-model/client-types.md`](../02-business-model/client-types.md)
