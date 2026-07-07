## Видение

OneBI — единый аналитический слой CAS. Один источник данных, одна точка доступа, без расхождений между тем, что видит клиент, менеджер и C-level с поправкой на комиссии. Любой участник может построить отчёт, поделиться ссылкой и быть уверенным, что другой видит те же цифры.

Документ для стейкхолдеров разбит фазы. Детали внутри фаз — для исполнителей.

> **Домены (актуально на 2026-06-03):** финальный хост — **platform.cas.ai** (OneBI = Live).
> Упоминания ниже `onebi-dev.cas.ai` и `onebi.cas.ai` — это планировавшиеся dev/beta-стенды, оба
> **сейчас не используются** (onebi.cas.ai потушен); `b2b.cas.ai` — legacy на период перехода.
> Канон → [`../01-platform/product-architecture.md`](../01-platform/product-architecture.md).

---

## Принцип: растущие данные, постоянная структура

Визуальная оболочка OneBI одинакова на всех этапах:

```
   Запрос                              Вывод
┌─────────────────────────┐      ┌──────────────────┐
│ Filters  (WHERE)        │      │ Table            │
│ Splits   (GROUP BY)     │─────►│ Chart            │
│ Metrics  (SELECT)       │      │ One-line cards   │
└─────────────────────────┘      └──────────────────┘
```

**Что меняется** — постоянно дополняются источники данных под капотом. Каждый новый источник и модель расширяет набор доступных метрик, фильтров и сплитов. Пользователь видит больше возможностей в той же оболочке.

```
Milestone 1   B2B New UI API ──────────► Revenue, eCPM, DAU
Milestone 2   ClickHouse + SuperAdmin View ────────► То же, но быстро и за любой период
Milestone 3   ILRD based ──────────────► Real-time based metrics
Milestone 3a  Additional Metrics ──────► FillRate, MatchRate
Milestone 4   Cohorts ─────────────────► Through Session, Cohort Analysis
Milestone 5   SplitEngine ────────────► + Experiments, Uplift, Significance
Milestone 6   MMP ────────────────────► + CPI, ROAS, UA Cost, Attribution
Milestone 7   Predictive ─────────────► + LTV Forecast, Health Score, Benchmarks
```

---

## Общая картина

| Milestone | Источник данных | Что открывается | Кому нужно |
|-------|----------------|-----------------|------------|
| **M1. Visual Shell** | Ad Networks API (текущая агр. по сетям) | Новый кабинет: Quick View + Reports на текущих данных | L1, L2 |
| **M2. ClickHouse** | Ad Networks API (текущая агр. по сетям) | Скорость работы, Портфолио | L1, CAS Team |
| **M3. ILRD** | CAS Server (device-level) | Real-time, сессии, версии SDK/App, когортный анализ | L2, CAS RnD Team |
| **M4. SplitEngine** | CAS SDK granular properties data | A/B-тесты с BI-валидацией, self-service запуск | CAS RnD Team, Pub, L3 |
| **M5. MMP** | Tenjin | Unified reports: Spend + Revenue + Events в одном месте | L2, Pub, UA Team |
| **M6. Predictive & Platform** | ML-модели | Предиктивный LTV, health score, publishing | L3, CAS Team |

**SuperAdmin** — сквозной слой поверх всех фаз. Та же структура (Filters + Splits + Metrics), но скоуп = весь портфель, все клиенты. Подключается с Milestone 2 (CH) и наращивает возможности с каждой фазой.

## Milestone 1: Visual Shell (API Данные)

Новый кабинет как отдельное SPA (Vue 3, Tailwind, тёмная тема). Расположение — текущий бэкенд b2b.cas.ai.

### Что видит пользователь

Два экрана вместо одного как сейчас:
- **Quick View** — отвечает на вопрос "всё ли ок?". Карточки с ключевыми числами, тренд, breakdown по сетям. Открыл — за 5 секунд понял ситуацию.
- **Reports** — "почему так?". Полная таблица с фильтрами, сплитами, сортировкой, экспортом. Для более подробного анализа.

#### Шаг 1а. Каркас + Quick View

**Milestone 1a: Каркас + Quick View**

| # | Шаг | Результат | Asana |
|---|-----|----------|-------|
| 1.1 | Выбрать шаблон (Vue 3, Tailwind, тёмная тема) | ✅ Шаблон куплен | [Investigate Vue3](https://app.asana.com/0/1213554144275038/1213635002943053) |
| 1.2 | Собрать каркас: sidebar, роутинг, авторизация | ✅ Можно залогиниться | [Front Project skeleton](https://app.asana.com/0/1213554144275038/1213545671052933), [Back Project skeleton](https://app.asana.com/0/1213554144275038/1213545671052928) |
| 1.3 | Sidebar: заглушки разделов (Apps, Docs, Support) | ✅ Навигация на месте | [Front роутинги](https://app.asana.com/0/1213554144275038/1213545671052911) |
| 1.4 | Quick View: селектор приложений | ✅ Выбираешь app — данные фильтруются | [Back API фильтрация](https://app.asana.com/0/1213554144275038/1213545671052965) |
| 1.5 | Quick View: селектор дат | ✅ Пресеты 7d / 30d / 90d + custom range | [QuickView page create](https://app.asana.com/0/1213554144275038/1213641195829591) |
| 1.6 | Quick View: Metric Cards | ✅ 5 карточек: DAU, Revenue, ARPDAU, eCPM, Impr | [QuickView page create](https://app.asana.com/0/1213554144275038/1213641195829591) |
| 1.7 | Quick View: Revenue Trend chart | ✅ Line chart за выбранный период | [QuickView page create](https://app.asana.com/0/1213554144275038/1213641195829591) |
| 1.8 | Quick View: Revenue by Network | ✅ Breakdown по рекламным сетям | [QuickView page create](https://app.asana.com/0/1213554144275038/1213641195829591) |
| 1.9 | Деплой на стейдж | ⬜ Живой URL (cas.ai субдомен) | [DevOps cooperate](https://app.asana.com/0/1213554144275038/1213545671052940) |
| 1.10 | Layout: Revenue Trend на полэкрана, справа Revenue by Network таблицей | ⬜ Всё на одном экране без скролла | — |
| 1.11 | Revenue by Country: разбивка по странам на QuickView | ⬜ Breakdown по топ-странам | — |
| 1.12 | Вернуть иконки и цветовые акценты в KPI-карточки | ⬜ Синий CAS #58A6FF, фоновый градиент change % | — |
| 1.13 | График: чёткая линия с точками, без сглаживания, ось Y от нуля | ⬜ Убрать градиент под линией | — |
| 1.14 | Даты: формат с годом + день недели (Mon 10 Mar 2026) | ⬜ | — |
| 1.15 | Брендинг: шрифт из брендбука, логотип, анимация загрузки, footer, notification bell | ⬜ | — |
| 1.16 | Навигация: Quick View → Analytics, sidebar (Analytics, Reports, Payments), фикс шапка | ⬜ | — |
| 1.17 | Зона фильтров — отдельная визуальная карточка, отделить от зоны данных | ⬜ Как Firebase | — |
| 1.18 | Пресеты — кнопка-звёздочка (Favorites), сохранённые наборы фильтров | ⬜ | — |

Референсы: LevelPlay overview (компактность), Firebase Analytics (зона фильтров), Superset (визуальные элементы).

#### Milestone 1b: Reports

| Что добавляется | Описание |
|----------------|----------|
| Chip-фильтры | Period, App, Platform (iOS/Android), Country, Ad Type |
| Splits (group by) | Application, Country, Network, Ad Type, Platform |
| Таблица | Данные с сортировкой, sticky header, зебра-стайл |
| Toggle Table / Chart | Переключение между таблицей и графиком |
| CSV export | Скачать текущую выборку |

**Фидбек Reports (design review 24.03)**

- **Зона фильтров** — выделить в отдельную визуальную карточку (белый/светлый фон). Кнопки Apply, Reset, Share внизу карточки. Левую колонку убрать
- **Пресеты vs Фильтры** — разделить терминологию. Пресеты = сохранённые наборы фильтров, доступны через кнопку-звёздочку (Favorites). Фильтры = конкретные выборки
- **Chips** — плюсик добавления Splits/Measures рядом с последним чипом (не в дальнем углу). Каждая новая метрика в chart mode = отдельный chart
- **Include/Exclude** — реализовать переключение полярности как у конкурентов (на первое время только include)
- **Date picker** — убрать InstallDate, оставить только ActivityDate. Уменьшить количество пресетов периодов

### Стейджинг-план Visual Shell

#### Шаг 1 — Dev Stage (текущий)

Команда деплоит QuickView + Reports с живыми данными на onebi-dev.cas.ai. Доступ только внутренний. Смотрим, даём обратную связь по функциональности и данным. Спринты 4-5.

#### Шаг 2 — Design + правки

По фидбеку вносят пакет правок. Подключаем дизайнера — брендинг, цветовая палитра, шрифты, иконки. Результат — визуально готовый продукт, который не стыдно показать.

#### Шаг 3 — Beta

Деплой на onebi.cas.ai. 5-10 выбранных паблишеров получают доступ. Собираем фидбек по юзабилити, скорости, полноте данных. Корректируем по результатам.

#### Параллельно — рестайлинг кабинета

Обновляем b2b.cas.ai — навигация, тема, sidebar — чтобы Visual Shell не выпадал визуально из текущего кабинета. При переходе в production на b2b.cas.ai/analytics всё выглядит единым целым.

### Критерии успеха (Milestone 1)

1. **Паритет данных** — те же метрики, что на текущем дашборде (1:1)
2. **Удобство** — эргономика лучше, чем сейчас (не эстетика — именно удобство взаимодействия)
3. **Скорость** — интерфейс отзывчивый, не хуже текущего

### Что НЕ входит в Milestone 1

- Данные из ClickHouse (Milestone 2)
- SDK / App Version splits (Milestone 3)
- Retention, LTV, когорты (Milestone 3+)
- Saved Views, Deep Linking (Milestone 3)
- Excel export (Milestone 3, CSV — в Milestone 1b)
- Anomaly Detection (Milestone 3)
- Кастомный дизайн (подключаем дизайнера на шаге 2 стейджинга)

---

## Milestone 2: ClickHouse Foundation

Борис готовит materialized views в ClickHouse. Руслан переключает API. UI не меняется — меняется скорость и доступные периоды.

### Что видит пользователь

| Было | Стало |
|------|-------|
| Скорость зависит от объёма данных | Стабильно 2-5 сек на любой период |
| Ограниченные периоды (30d, 90d) | Любые периоды, включая 180d, 360d |
| Задержка данных ~1.5 суток | Та же (улучшение в Milestone 4) |

### Шаги

| # | Кто | Шаг | Результат |
|---|-----|-----|----------|
| 3.1 | Борис | Materialized views с теми же метриками | Revenue, Impressions, DAU, eCPM, Fill Rate, CTR, Requests, Clicks в разрезах App, Country, Network, Ad Type, Platform, Date |
| 3.2 | Руслан | Переключить API на данные Бориса | Те же экраны, данные из CH |
| 3.3 | Алексей | Валидация: сравнить числа CH vs B2B | Расхождение < 1% |

**Ограничения:** лимит 50K строк в ответе (UI показывает "уточните фильтры"), target latency < 2 сек.

**Результат:** бета для клиентов.

---

## Milestone 3: ILRD — Device-Level Data

Борис подключает ILRD-данные (impression-level revenue data с CAS Server). Это кардинально расширяет возможности аналитики: появляются данные, которых нет в API рекламных сетей.

### Что видит пользователь

- **Real-time** — данные за текущие сутки (закрывает gap ~1.5 суток)
- **Версии** — разбивка по SDK Version и App Version (для диагностики обновлений)
- **Сессии** — длина сессий, показы на сессию (для балансировки рекламной нагрузки)
- **Когортный анализ** — основа для retention и LTV (Milestone 6)

### Новые Metrics

| Metric | Формула | ID |
|--------|---------|-----|
| Active Users | Уникальные пользователи по трекеру CAS | m37 |
| Session Length | Средняя длина сессии | s2 |
| Sessions per User | Сессий на пользователя | s5 |
| Impressions per Session | Показов на сессию | s6 |
| Revenue by SDK Version | Revenue в разбивке по SDK | d1 |
| Revenue by App Version | Revenue в разбивке по App Version | d2 |

### Новые Filters / Splits

| Добавляется | Тип |
|-------------|-----|
| SDK Version | Filter + Split |
| App Version | Filter + Split |

### Real-time: как это работает

ILRD трекается CAS SDK на устройстве и отправляется на сервер. Задержка — секунды. Точность ~95-98% от финальных данных API.

- **Обновление:** раз в 1-6 часов (не стриминг)
- **Дискрепанси:** ~1.7% (ILRD обычно ниже, чем финальные данные сетей)
- **Компенсация:** коэффициенты коррекции по сетям (предсказываем финальные данные)
- **Ограничение:** только SDK 4.6.2+ отправляет ILRD

**UI-решение:** отдельная вкладка "Real-time" с данными за последние 1/6/12 часов (не смешиваем с финальными данными на основном графике).

### Дополнительные возможности этой фазы

| Фича | Описание |
|------|----------|
| Saved Views | Сохранение пресетов фильтров |
| Deep Linking | Состояние в URL + share link |
| Excel export | Помимо CSV |
| Anomaly Detection | Подсветка нулей и аномалий |

### Шаги

| # | Кто | Шаг |
|---|-----|-----|
| 4.1 | Борис | ILRD processing pipeline: сырые события → агрегированные метрики в CH |
| 4.2 | Борис | Compensation coefficients: модель коррекции ILRD → predicted final |
| 4.3 | Руслан | Новые метрики в UI (Active Users, Sessions, Version splits) |
| 4.4 | Руслан | Real-time вкладка |
| 4.5 | Руслан | Saved Views + Deep Linking + Excel export |

---

## Milestone 4: SplitEngine — Experiments

Детерминированная сплитовалка на уровне SDK с единым user_id. Цель — создать end-to-end контур экспериментов: от идеи до решения, без ручной аналитики.

### Что видит пользователь

- **Запуск эксперимента** — self-service: выбрал сегмент, задал конфиг, нажал "запустить"
- **Мониторинг** — real-time метрики по группам Test/Control в тех же Reports
- **Решение** — автоматический расчёт significance и uplift, рекомендация "раскатить / откатить / ждать"

### Компоненты

```
┌─────────────┐   ┌──────────────────┐   ┌─────────────────┐   ┌─────────┐
│  SDK Split  │──►│ Experiment Engine │──►│ Experiment       │──►│  BI     │
│  (hashing)  │   │ (config, launch) │   │ Registry         │   │ (auto-  │
│             │   │                  │   │ (all tests)      │   │ signif.)│
└─────────────┘   └──────────────────┘   └─────────────────┘   └─────────┘
     RND               Руслан                 Борис               Борис
```

**SDK Split — Deterministic Hashing:**
- Стабильный hashing на основе постоянного `user_id`
- Пользователь всегда попадает в одну и ту же когорту при тех же условиях
- Нет "прыжков" между сегментами при перезапусках, апдейтах SDK, изменениях конфигов
- Поддержка вложенных экспериментов (несколько одновременных тестов)
- Гарантия: равномерный сэмпл, воспроизводимость результатов

**Experiment Engine — Self-service:**
- Конфигурация через UI: аудитория, группы, параметры
- Автоматическая раскатка через SDK config
- Валидация данных при запуске (достаточно ли трафика?)
- Управление жизненным циклом: draft → running → completed → decision

**Experiment Registry — Единый реестр:**
- Все эксперименты в одном месте (включая завершённые)
- Результаты привязаны к BI-данным
- History: кто запустил, когда, что тестировали, какой результат

**BI Auto-Significance:**
- Автоматический расчёт statistical significance
- Uplift по ключевым метрикам (ARPDAU, eCPM, Fill Rate, LTV)
- DAU parity check (валиден ли эксперимент?)
- Stability over time (устойчив ли результат на D1/D3/D7?)
- Рекомендация: "раскатить" / "откатить" / "ждать данных"

### Workflow: от идеи до решения

```
Идея → Конфиг → Запуск → Валидация данных → Мониторинг → Решение
                  ▲                                         │
                  └─────── следующий тест ◄─────────────────┘
```

Критично: убрать ручные шаги между идеей и запуском. Каждый дополнительный тест почти не увеличивает операционные издержки.

### Новые Metrics

| Metric | Формула | ID |
|--------|---------|-----|
| ARPDAU Uplift % | (Test − Control) / Control | m26 |
| Revenue Uplift $ | ARPDAU uplift × DAU | m27 |
| DAU Parity | DAU_test vs DAU_control | m28 |
| Stability D1/D3/D7 | Uplift over time | m29 |
| Rollback Flag | Auto yes / no | m30 |

### Новые Filters / Splits

| Добавляется | Тип |
|-------------|-----|
| Experiment ID | Filter + Split |
| Cohort (Test / Control) | Filter + Split |

### Success Metrics

| Метрика | Описание | Цель |
|---------|----------|------|
| Time-to-first-result | От запуска до первых значимых данных | ↓ с недель до дней |
| Experiments / month | Количество тестов в месяц | ↑ 3x |
| Decision-ready % | Доля тестов с автоматическим решением | > 80% |
| ARPDAU/LTV uplift | Подтверждённый кумулятивный uplift | Измеримый |

### Бизнес-цель

Повысить доверие к аплифтам, ускорить velocity экспериментов и создать измеримое преимущество над Firebase/Adjust за счёт прозрачности и BI-валидации.

### Шаги

| # | Кто | Шаг |
|---|-----|-----|
| 5.1 | RND (Горик) | SDK: deterministic hashing, experiment assignment, config pull |
| 5.2 | Руслан | Experiment Engine UI: создание, запуск, мониторинг |
| 5.3 | Борис | Experiment views в CH: метрики по группам, significance |
| 5.4 | Руслан | Experiment Registry: список, история, результаты |
| 5.5 | Борис | Auto-significance engine: расчёт uplift, parity, stability |
| 5.6 | Алексей | Валидация: прогон 2-3 реальных экспериментов |

---

## Milestone 5: MMP — Unified Attribution

Подключение MMP (AppsFlyer, Adjust, Tenjin) как источников данных. Решает главную боль L2-клиентов: данные разбросаны по CAS, AppsFlyer/Adjust, Facebook/Google — сейчас сводят вручную в таблицах.

### Что видит пользователь

- **Unified Report** — Spend + Revenue + Events по GEO + AdType в одном экране
- **ROAS** — без переключения между сервисами
- **Attribution** — откуда пришли пользователи, сколько стоили, сколько принесли

### Новые Metrics

| Metric | Формула | ID |
|--------|---------|-----|
| UA Cost | Installs × CPI | m31 |
| Installs | New Users (attributed) | m32 |
| CPI | Cost / Installs | m33 |
| ROAS D7 / D30 | Revenue / Cost | m34 |
| ROAS To-Date | Cumulative Revenue / Spend | m43 |
| Payback Days | Day when ROAS = 100% | m35 |
| LTV | ARPDAU × Lifetime Days | m12 |
| App Profit | Ad Revenue − UA Cost | m4 |
| Profit (Calendar) | Total Revenue − UA Spend (per day) | m44 |

### Новые Filters / Splits

| Добавляется | Тип |
|-------------|-----|
| Source (Facebook, Google, TikTok...) | Filter + Split |
| Campaign | Filter + Split |
| Creative | Filter + Split |
| AdSet | Filter + Split |
| Is Organic | Filter |

### Шаги

| # | Кто | Шаг |
|---|-----|-----|
| 6.1 | Борис | Коннекторы: AppsFlyer → CH, Adjust → CH (нормализация в canonical entities) |
| 6.2 | Борис | Unified view: Join revenue (ILRD/API) + spend (MMP) + events |
| 6.3 | Руслан | Unified Report UI: Spend + Revenue + Events в одном экране |
| 6.4 | Руслан | ROAS / LTV / Payback views в Reports |

### Связь с CAS ↔ MMP Partner Integration

Параллельно с Milestone 5: CAS регистрируется как партнёр в AppsFlyer/Adjust, чтобы данные о revenue автоматически попадали в MMP без ручной передачи impression events. Это конкурентное преимущество — AppoDeal уже делает подобное.

---

## Milestone 6: Predictive & Full Platform

Горизонт. Минимум деталей — уточняется по мере приближения.

### Predictive Models

| Фича | Описание |
|------|----------|
| Predictive LTV | Прогноз LTV по ранним когортным данным (D7 → D30 → D90) |
| ARPU Forecast | Прогноз ARPU D7/D14/D30 для ранних решений по UA |
| Health Indicator | Green/yellow/red по проекту — быстрая оценка без погружения в детали |
| Benchmarks | Сравнение с категорией (средние по сети CAS) |
| Anomaly Detection (advanced) | ML-based детекция аномалий по портфелю |

### Full Platform

| Фича | Описание |
|------|----------|
| Publishing Dashboards | Pub-специфичные метрики: Profit, ROAS, Creative Performance |
| 1С Migration | Замена 1С на данные из аналитической БД |
| Legacy B2B Shutdown | Отключение текущего b2b.cas.ai, все клиенты на новой платформе |

---

## SuperAdmin: Portfolio Layer

Сквозной слой поверх всех фаз. Не отдельный продукт — тот же UI (Filters + Splits + Metrics → Table / Chart), но скоуп = весь портфель, все клиенты, все приложения.

### Концепция

Клиент видит **свои** приложения. SuperAdmin видит **все** — и может смотреть на данные на уровне портфеля: по менеджерам, по клиентам, по бандлам. Та же таблица, те же графики, те же метрики — другой масштаб.

```
Customer scope:                 SuperAdmin scope:
┌───────────────────┐           ┌───────────────────────────────────┐
│ Filters:          │           │ Filters:                          │
│   App (my apps)   │           │   Manager  → Customer → App(s)   │
│   Period          │           │   Date Created                    │
│   Country, OS...  │           │   Period, Country, OS...          │
│                   │           │                                   │
│ Splits:           │           │ Splits:                           │
│   App, Network... │           │   Client, Manager, App, Network..│
│                   │           │                                   │
│ Metrics:          │           │ Metrics:                          │
│   Revenue, DAU... │           │   Revenue, DAU... (агрегат)       │
└───────────────────┘           │   + Gross/Net toggle              │
                                └───────────────────────────────────┘
```

### SuperAdmin Filters (дополнительные)

| Filter | Описание | Логика |
|--------|----------|--------|
| **Manager** | Менеджер, закреплённый за клиентами | Фильтрует Customer → App |
| **Customer** | Клиент платформы (за ним бандлы) | Фильтрует App |
| **Date Created** | Дата подключения клиента | Диапазон, пресеты по годам |

**Каскад:** Manager → Customer → Bundle(s) → Revenue / Metrics. Выбрал Manager — список Customer сужается. Выбрал Customer — данные по его бандлам.

### SuperAdmin Splits (дополнительные)

| Split | Что делает |
|-------|-----------|
| **Client** | Строка на каждого клиента |
| **Manager** | Строка на каждого менеджера |

### SuperAdmin Features

| Feature | Описание |
|---------|----------|
| **Toggle Gross / Net** | Переключение между данными без комиссии CAS (для сравнения с конкурентами) и с комиссией (для выплат). Комиссия per app из справочника |
| **App Card** | Карточка приложения: владелец, портфолио, менеджер, комиссия. Группировка by Manager |
| **Portfolio Anomalies** | Клиенты с резким падением Revenue или DAU — проактивная реакция |
| **Churn Risk** | Клиенты с падением Revenue >20% за 30 дней — алерт для BD |
| **Client Report Export** | PDF/Excel отчёт по клиенту за период — для регулярных ревью |

### Admin Panel (управление)

Отдельный экран для управления связями Manager ↔ Customer. Через Admin API (решение #8).

```
┌────────────────────┬─────────────────────────────────────────────────┐
│ Менеджеры          │ Клиенты                                         │
│                    │                                                 │
│ Anton Smirnov (12) │ ID │ Customer      │ Manager │ Bundles │ Date  │
│ Serhii Shcherbyna  │ ───┼───────────────┼─────────┼─────────┼───────│
│   (8)              │ 42 │ FunBurst LTD  │ Serhii ▼│ 4       │ 2025  │
│ Rashid Sabirov (6) │ 51 │ ZooqVPN       │ Anton  ▼│ 2       │ 2024  │
│ Buha Maksym (5)    │ 63 │ Oktopus Games │ Rashid ▼│ 3       │ 2025  │
│ Dmytro Dubniak (4) │ ...│               │         │         │       │
└────────────────────┴─────────────────────────────────────────────────┘
```

- Переназначение менеджера — inline dropdown
- Поиск по имени, ID, Bundle ID
- Сортировка по любому столбцу

### Кому нужно

| Роль | Что смотрит | User Stories |
|------|-------------|-------------|
| **Ads Operator** | Revenue по всем клиентам, аномалии, сравнение клиентов | US-Admin-01..07 |
| **BD / Account Manager** | Свои клиенты, churn risks, upsell-кандидаты | US-BD-01..05 |
| **RND** | Impact SDK-версии на всех клиентов, adoption rate | US-RND-01..03 |
| **C-level** | Общая динамика, portfolio overview, MRR | — |

### Когда появляется

SuperAdmin не ждёт последней фазы. Он растёт вместе с платформой:

| Milestone | Что доступно SuperAdmin |
|-------|------------------------|
| **M2. ClickHouse** | Базовый portfolio view: Revenue/DAU/eCPM по всем клиентам. Фильтры Manager/Customer. Быстрые запросы по CH |
| **M3. ILRD** | + SDK Version adoption rate (кто обновил, кто нет). Session metrics по портфелю |
| **M4. SplitEngine** | + Мониторинг экспериментов по всем клиентам. Impact assessment |
| **M5. MMP** | + ROAS / LTV по published-приложениям. UA portfolio view |
| **6. Predictive** | + Churn prediction, health scores, anomaly detection (ML). Полный Admin dashboard |

### Шаги

| # | Кто | Шаг | Milestone |
|---|-----|-----|-------|
| A.1 | Руслан | Admin API: CRUD менеджеры, кастомеры, бандлы | 2 |
| A.2 | Руслан | SuperAdmin фильтры в Reports: Manager, Customer, Date Created | 2 |
| A.3 | Руслан | SuperAdmin splits: by Client, by Manager | 2 |
| A.4 | Руслан | Toggle Gross / Net (комиссия per app) | 2 |
| A.5 | Руслан | App Card (владелец, портфолио, менеджер, комиссия) | 2 |
| A.6 | Руслан | Admin Panel UI (управление Manager ↔ Customer) | 3 |
| A.7 | Борис | Portfolio-level materialized views (агрегации по Client/Manager) | 2 |
| A.8 | Борис | Anomaly detection по портфелю (правила, потом ML) | 5-6 |

---

## Команда

| Кто | Роль | Зона | Фазы |
|-----|------|------|------|
| Алексей Шевнин | Product Owner | Требования, приоритеты, клиенты | Все |
| Руслан Новиков | Full-stack dev | Frontend, backend, API | 1-6 |
| Борис Шифрин | Data lead | ClickHouse, данные, формулы метрик | 2-6 |
| Владислав Горик | RND lead | SDK, SplitEngine, эксперименты | 4 |
| Дизайнер (TBD) | UI/UX | Кастомный дизайн после обкатки шаблона | 2+ |

---

## Ключевые решения

| # | Решение | Почему | Дата |
|---|---------|--------|------|
| 1 | Отдельное SPA, не модуль старого кабинета | Своя навигация, свой URL, чистый старт | 16.02 |
| 2 | Шаблон → обкатка → дизайнер | Дизайнер приходит после, не до | 16.02 |
| 3 | Vue 3 + Tailwind + тёмная тема | Миграция с Vue 2, закрытие тех. долга. Тёмную тему просят все клиенты | 16.02 |
| 4 | Стартуем на B2B базе | Руслан не ждёт Бориса, строит UI сразу | 16.02 |
| 5 | Единый UI для B2B и Internal | Один интерфейс, разные права доступа | 16.02 |
| 6 | Мобилка на паузу | Desktop first, держим в уме | 16.02 |
| 7 | UI и API — отдельные репозитории | Замена UI без трогания API, мобилка потом, enterprise-клиенты через API | 26.02 |
| 8 | Admin API — параллельный слой | Управление менеджерами, кастомерами, портфолио — отдельно от клиентского API | 26.02 |
| 9 | DDD — единый язык в коде, API и документации | Термины в коде Руслана = термины Бориса = термины бизнеса | 26.02 |
| 10 | Не катить на прод без подтверждения PO | Баг при миграции CH — выкатили не дождавшись фидбэка клиентов | 26.02 |
| 11 | QuickView: Revenue by Network таблицей справа от графика | Всё на одном экране без скролла, видны все сетки | 17.03 |
| 12 | QuickView: вернуть иконки и цветовые акценты | Без них дашборд выглядит сухо; яркие акценты (синий CAS) оживляют UI | 17.03 |
| 13 | График: чёткая линия с точками, от нуля, без сглаживания | Сглаженный график создаёт ощущение неточности данных | 17.03 |
| 14 | Reports: зона фильтров — отдельная карточка с Apply/Reset | Визуально отделить выбор от отображения данных (как Firebase) | 24.03 |
| 15 | Разделить терминологию Пресеты vs Фильтры | Пресет = сохранённый набор. Фильтр = конкретная выборка. Разные UX-паттерны | 24.03 |
| 16 | Стейджинг: Dev → Design+правки → Beta → Production | Дизайнер подключается после обкатки, бета на 5-10 паблишерах, параллельно рестайлинг кабинета | 26.03 |

---

## Следующие шаги

| # | Действие | Кто | Статус |
|---|----------|-----|--------|
| 1 | ~~Созвон Алексей + Руслан + Борис: согласовать glossary и roadmap~~ | — | ✅ Сделано |
| 2 | Data Catalog: дополнить metrics-dictionary техническими именами полей в CH | Борис + Алексей | Ждёт |
| 3 | ~~DDD-соглашения: зафиксировать имена сущностей~~ | — | ✅ Сделано (onebi-dev/ddd-laravel-guide.md) |
| 4 | ~~Контракт API: эндпоинты, поля, форматы ответов~~ | — | ✅ Сделано (QuickView API Spec, ADRs) |
| 5 | ~~Регламент деплоя: не катить на прод без подтверждения PO~~ | — | ✅ Принято (решение #10) |
| 6 | ~~Руслан выбирает шаблон → согласование с Алексеем~~ | — | ✅ Сделано |
| 7 | Деплой на dev stage (onebi-dev.cas.ai) | Ruslan + Stas | В работе (Sprint 4) |
| 8 | Внести правки QuickView по фидбеку (решения #11-13) | Evgeniy | Ждёт |
| 9 | Внести правки Reports по фидбеку (решения #14-15) | Evgeniy + Ruslan | Ждёт |
| 10 | Подключить дизайнера (брендинг, палитра, шрифты) | Alexei | После dev stage |
| 11 | Beta: выбрать 5-10 паблишеров для бета-доступа | Alexei + Anton | После дизайна |
| 12 | Рестайлинг кабинета b2b.cas.ai (навигация, тема, sidebar) | Evgeniy + Ruslan | Параллельно с beta |

---

## Формат работы

- **Задачи:** Asana (проект CAS Platform Backlog)
- **Спринты:** двухнедельные
- **Коммуникация:** Slack-канал + еженедельные синки по прогрессу
- **Документация:** wiki.cas.ai (книга OneBI) + cas-docs (источник правды)

---

## Связанные документы

- [One BI — Glossary](onebi-glossary.md) — метрики, фильтры, сплиты
- [DDD Laravel Guide](onebi-dev/ddd-laravel-guide.md) — единый язык
- [One BI — Data Catalog](../04-bi/data-catalog.md) — техническая карта CH
- [QuickView API Spec](onebi-dev/quickview-api-spec.md) — контракт API
- [One BI — Design Spec](design-spec-bi.md) — дизайн-спецификация UI
- Полный каталог метрик: `04-bi/metrics-dictionary.md`
- Общий roadmap компании: `03-product/roadmap.md`
- R&D гипотезы: `03-product/rnd-hypotheses.md`
