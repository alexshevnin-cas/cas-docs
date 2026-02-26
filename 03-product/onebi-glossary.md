# One BI — Словарь

Общий язык между Alexei (CPO), Borys (Data) и Ruslan (Frontend).

---

## Как устроено

```
 Data Source             Metrics Layer              UI
┌───────────────┐      ┌───────────────┐      ┌──────────────┐
│ B2B база      │─────►│               │      │              │
│ (текущий      │      │   Metrics     │─────►│  Quick View  │
│  бэкенд)     │      │   Filters     │      │  Reports     │
│               │      │   Splits      │      │              │
│ ClickHouse    │─────►│               │      │              │
│ (Борис)       │      │  ─── контракт │      │  Руслан      │
└───────────────┘      └───────────────┘      └──────────────┘
        ▲                      ▲                      ▲
     меняется              не меняется            не меняется
     под капотом           для Руслана            для юзера
```

**Metrics Layer** — контракт между Борисом и Русланом. Набор метрик, фильтров и сплитов. Руслан строит UI по этому контракту. Когда Борис переключит источник данных — UI не меняется.

---

## Step 1–2: B2B база → новый UI

Стартуем на текущем бэкенде b2b.cas.ai. Руслан строит новое SPA (Vue 3, шаблон, тёмная тема). Данные — API рекламных сетей, задержка ~1.5 суток.

### Metrics

| Metric | Формула / описание | ID |
|--------|-------------------|----|
| **Ad Revenue** | Доход от рекламы | m13 |
| **Impressions** | Количество показов рекламы | m46 |
| **eCPM** | Revenue / Impressions x 1000 | m20 |
| **DAU** | Уникальные пользователи в день | m5 |
| **Ad ARPDAU** | Ad Revenue / DAU | m38 |
| **Impr / DAU** | Impressions / DAU | m15 |
| **Fill Rate** | Fills / Requests | m21 |
| **CTR** | Clicks / Impressions | m48 |
| **Requests** | Запросы рекламы | m49 |
| **Clicks** | Клики по рекламе | m47 |

### Filters (ограничивают выборку — WHERE)

| Filter | Значения |
|--------|----------|
| **Period** | 7d, 30d, 90d, custom range |
| **App** | Одно или несколько приложений |
| **Country** | Страна пользователя |
| **Platform** | iOS / Android |
| **Ad Type** | Banner / Interstitial / Rewarded / MREC / Native |

### Splits (группируют строки — GROUP BY)

| Split | Что делает |
|-------|-----------|
| **Application** | Строка на каждое приложение |
| **Country** | Строка на каждую страну |
| **Network** | Строка на каждую рекл. сеть (AdMob, Unity, Meta...) |
| **Ad Type** | Banner / Interstitial / Rewarded / MREC / Native |
| **Platform** | iOS / Android |

### UI

| Компонент | Что это | Step |
|-----------|---------|------|
| **Quick View** | Карточки (DAU, Revenue, ARPDAU, eCPM, Impr/DAU) + Revenue Trend chart + Revenue by Network | Step 1 |
| **Reports** | Таблица + графики с chip-фильтрами, сплитами, сортировкой, CSV export | Step 2 |
| **Metric Card** | Виджет: число + динамика ("+8.5%") | Step 1 |
| **Chart** | График (line, bar, donut) | Step 1 |
| **Table** | Данные с сортировкой, sticky header, зебра | Step 2 |
| **Chip** | Тег-кнопка для фильтра / сплита / метрики | Step 2 |

---

## Step 3: B2B база → ClickHouse (Борис)

Борис готовит данные в ClickHouse. Руслан переключает API. Те же Metrics, Filters, Splits — другой источник. UI не меняется, данные быстрее.

---

## Следующее: + ILRD → новые Metrics

После Step 3. Борис подключает данные CAS-сервера. Metrics Layer расширяется — появляются новые строки в таблицах выше.

### Что такое ILRD

Impression-Level Revenue Data — каждый показ рекламы трекается CAS SDK на устройстве и отправляется на наш сервер. Real-time (секунды). Точность ~95-98% от API.

### Новые Metrics

| Metric | Формула / описание | ID |
|--------|-------------------|----|
| **Active Users** | Уникальные пользователи по нашему трекеру | m37 |
| **Session Length** | Средняя длина сессии | s2 |
| **Sessions per User** | Сессий на пользователя | s5 |
| **Impressions per Session** | Показов на сессию | s6 |
| **Revenue by SDK Version** | Доход в разбивке по версии SDK | d1 |
| **Revenue by App Version** | Доход в разбивке по версии приложения | d2 |

### Новые Filters и Splits

| Добавляется | Тип |
|-------------|-----|
| **SDK Version** | Filter + Split |
| **App Version** | Filter + Split |

### Real-time

ILRD позволяет показывать данные за текущие сутки (закрывает gap ~1.5 суток между последними API-данными и "сейчас").

---

## Связанные документы

- Полный каталог метрик: `04-bi/metrics-dictionary.md`
- Все фильтры и сплиты: `04-bi/filters.md`
- Дизайн-спек UI: `03-product/design-spec-bi.md`
