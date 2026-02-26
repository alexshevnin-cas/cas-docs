# One BI Wiki — План артефактов

Единое место, где Алексей, Борис и Руслан находят всё: от бизнес-терминов до имён колонок в ClickHouse.

---

## Целевая структура Wiki

```
One BI/
│
├── Roadmap              ← этапы, решения, следующие шаги     ✅ ЕСТЬ
├── Glossary             ← архитектура, Metrics Layer          ✅ ЕСТЬ (обновить)
├── Metrics Dictionary   ← все метрики + формулы               ✅ ЕСТЬ (расширить)
├── Filters & Splits     ← все фильтры и разбивки              ✅ ЕСТЬ (расширить)
├── Data Catalog         ← техническая карта: CH-таблицы,      🔴 НЕТ
│                          колонки, типы данных, источники
├── API Contract         ← эндпоинты, запросы, ответы          🔴 НЕТ
├── DDD Conventions      ← единый язык: код = документы =      🔴 НЕТ
│                          разговоры
├── Design Spec          ← UI спецификация Quick View/Reports  ✅ ЕСТЬ
└── Decision Log         ← все решения с датами и контекстом   ✅ ЕСТЬ (в roadmap)
```

---

## Что есть и что добавить

### 1. Roadmap — ✅ готов
`onebi-roadmap.md` — этапы, команда, решения, следующие шаги.
**Ничего не меняем.**

### 2. Glossary — ✅ обновить
`onebi-glossary.md` — архитектура, Metrics Layer, фазы.

**Добавить:**
- Ссылки на новые документы (Data Catalog, API Contract, DDD)
- Убрать дублирование с Roadmap (сейчас оба описывают этапы)

### 3. Metrics Dictionary — ✅ расширить
`metrics-dictionary.md` — 100+ метрик с формулами и уровнями доступа.

**Добавить колонки:**

| Сейчас | Добавить |
|--------|----------|
| ID, Метрика, Формула, Бизнес-вопрос, L1/L2/PubC | **CH Field**, **Source Table/MV**, **Data Type**, **Aggregation** |

Пример:

| ID | Метрика | CH Field | Source MV | Type | Agg |
|----|---------|----------|-----------|------|-----|
| m13 | Ad Revenue | `ad_revenue` | `mv_daily_metrics` | DECIMAL | SUM |
| m5 | DAU | `dau` | `mv_daily_metrics` | INT | AVG |
| m20 | eCPM | `ecpm` | computed | DECIMAL | Revenue/Impr×1000 |

**Кто делает:** Борис (CH-поля) + Алексей (бизнес-проверка)

### 4. Filters & Splits — ✅ расширить
`filters.md` — все фильтры и разбивки.

**Добавить:**

| Сейчас | Добавить |
|--------|----------|
| Фильтр, Описание, Примечание | **CH Column**, **Values/Enum**, **API Param Name** |

Пример:

| Фильтр | CH Column | API Param | Values |
|--------|-----------|-----------|--------|
| Country | `country_code` | `country` | ISO 3166-1 alpha-2 |
| Platform | `platform` | `platform` | `ios`, `android` |
| Ad Type | `ad_type` | `ad_type` | `banner`, `interstitial`, `rewarded`, `mrec`, `native` |

**Кто делает:** Борис (CH-колонки) + Руслан (API param names)

### 5. Data Catalog — 🟡 плейсхолдер создан
Файл: `04-bi/data-catalog.md`

Техническая карта всего, что лежит в ClickHouse.

**Содержание:**

```markdown
## Таблицы / Materialized Views

| MV | Описание | Источник | Гранулярность | Refresh |
|----|----------|----------|--------------|---------|
| mv_daily_metrics | Основные метрики по дням | Ad Networks API | day × app × country × network × ad_type × platform | ~1.5 суток |
| mv_ilrd_hourly | ILRD-метрики | CAS Event Server | hour × app × country × ... | real-time (1h) |

## Схема mv_daily_metrics

| Column | Type | Description | Nullable |
|--------|------|-------------|----------|
| date | Date | Activity date | No |
| app_id | String | Bundle ID | No |
| country_code | String | ISO 3166-1 | No |
| ad_revenue | Decimal(18,6) | Revenue in USD | No |
| impressions | UInt64 | Total impressions | No |
| ... | ... | ... | ... |

## Data Freshness

| Источник | Задержка | Refresh |
|----------|----------|---------|
| Ad Networks API | ~1.5 суток | 1×/день |
| ILRD | секунды → MV раз в час | 1×/час |
```

**Кто делает:** Борис (он знает схему) + Алексей (ревью)

### 6. API Contract — 🟡 плейсхолдер создан
Файл: `03-product/api-contract.md`

Контракт между бэкендом (Руслан) и фронтендом / внешними клиентами.

**Содержание:**

```markdown
## Quick View

GET /api/v1/quick-view?app_id=123&period=30d

Response:
{
  "cards": [
    {"metric": "ad_revenue", "value": 48200, "trend": 0.085, "unit": "USD"},
    {"metric": "dau", "value": 890000, "trend": 0.12},
    ...
  ],
  "revenue_trend": [
    {"date": "2026-02-20", "value": 6800},
    ...
  ],
  "revenue_by_network": [
    {"network": "admob", "revenue": 22000, "share": 0.45},
    ...
  ]
}

## Reports

POST /api/v1/reports
{
  "filters": {"period": "30d", "platform": "ios", "country": ["US", "DE"]},
  "splits": ["country", "network"],
  "metrics": ["ad_revenue", "impressions", "ecpm"]
}

## Admin API

GET /api/v1/admin/managers
GET /api/v1/admin/customers?manager_id=m1
```

**Кто делает:** Руслан (он проектирует API) + Алексей (ревью бизнес-полей)

### 7. DDD Conventions — 🟡 плейсхолдер создан
Файл: `03-product/ddd-conventions.md`

Единый язык: как называть вещи в коде, в документах, в разговорах.

**Содержание:**

```markdown
## Сущности

| Бизнес-термин | Код (Ruslan) | CH (Boris) | API | UI |
|--------------|-------------|-----------|-----|-----|
| Приложение | App | app_id (bundle) | app_id | App Selector |
| Метрика | Metric | column name | metric param | Metric Card / Chip |
| Фильтр | Filter | WHERE clause | filter param | Filter Chip |
| Разбивка | Split | GROUP BY | split param | Split Chip |
| Рекл. сеть | Network | network_id | network | Network name |
| Тип рекламы | AdType | ad_type | ad_type | enum |
| Период | Period | date range | period | Period Selector |
| Клиент (наш) | Customer | customer_id | — | — |
| Менеджер | Manager | manager_id | — | Admin filter |

## Правила именования

- **CH колонки:** snake_case (`ad_revenue`, `country_code`)
- **API параметры:** snake_case (`app_id`, `ad_type`)
- **Код (Vue):** camelCase (`adRevenue`, `countryCode`)
- **UI лейблы:** Title Case (`Ad Revenue`, `Country`)
- **Документация:** как в UI (`Ad Revenue`, не `ad_revenue`)
```

**Кто делает:** Руслан (код) + Борис (CH) + Алексей (бизнес-термины). На общем созвоне.

### 8. Design Spec — ✅ готов
`design-spec-bi.md` — Quick View и Reports wireframes.
**Ничего не меняем пока.** Обновим после выбора шаблона.

---

## Порядок создания

```
Сейчас (можно сразу)
────────────────────
① DDD Conventions        ← фиксируем имена сущностей (созвон втроём)
② Data Catalog           ← Борис описывает свои MV и колонки

После ①②
────────────────────
③ Metrics Dictionary     ← добавляем CH Field и Source MV (Борис заполняет)
④ Filters & Splits       ← добавляем CH Column и API Param (Борис + Руслан)

После ③④
────────────────────
⑤ API Contract           ← Руслан проектирует эндпоинты на базе ③④
⑥ Glossary               ← обновляем ссылки, убираем дублирование
```

---

## Sidebar после всех артефактов

```
One BI
  Roadmap
  Glossary
  DDD Conventions
  Metrics Dictionary
  Filters & Splits
  Data Catalog
  API Contract
  Design Spec
```

---

## Первый шаг: созвон

Алексей организует созвон с Русланом и Борисом. Повестка:

1. Показать Roadmap и Glossary — синхронизация
2. Пройтись по DDD Conventions — согласовать имена сущностей
3. Борис рассказывает, какие MV у него уже есть — заполняем Data Catalog
4. Договориться кто что заполняет и к когда
