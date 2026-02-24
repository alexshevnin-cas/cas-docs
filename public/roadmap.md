# CAS — Roadmap

> **Версия:** 3.0
> **Дата:** 2026-02-24
> **Статус:** Черновик — первый подход
> **Источники:** roadmap v2.1, план борды (скриншот), годовой план CTO (дек 2025), квартальный план CTO, Trello SDK backlog, диалог Капацын↔Шевнин
> **Синхронизация:** roadmap.md ↔ GitHub Issues ↔ Asana (автоматическая)

---

## Принцип

Roadmap организован по **целям** (Goals) → **контрольным точкам** (Milestones) → **инициативам** (Tasks). Каждая инициатива принадлежит треку и привязана к цели через milestone.

**Определённость убывает с горизонтом.** H1 — понятно что и как. H2 — понятно что, но не как. Beyond — стратегические ставки.

---

## Цели (Goals)

| # | Цель | Период | Key Results | Источник |
|---|------|--------|-------------|----------|
| GOAL-1 | Запустить MVP BI для L1-клиентов | H1 2026 | P1 в продакшене; ≥50% L1 заходят в BI 1×/нед; time to first insight <30 сек | roadmap v2 |
| GOAL-2 | Построить data-фундамент | H1 2026 | D1 в продакшене; latency <2 сек; D2 миграция завершена | roadmap v2 |
| GOAL-3 | Запустить маркетинговые лендинги и контент-машину | Q2 2026 | G1 live, конверсия >3%; 3 лендинга по типам; ≥4 статьи/мес | roadmap v2 |
| GOAL-4 | Обеспечить L2-аналитику | H2 2026 | P2 в продакшене; L2 используют splits сами; запросы к менеджерам −30% | roadmap v2 |
| GOAL-5 | Внедрить онбординг для новых клиентов | H2 2026 | Time to first value <24ч; completion rate >70%; нагрузка на support снижена | roadmap v2 |
| GOAL-6 | Запустить Server Bidding с основными интеграциями | H1 2026 | ≥8 сетей на s2s bidding; latency аукциона <200ms | план CTO |
| GOAL-7 | Развить CAS SSP как продукт | H1-H2 2026 | SSP CMS live; аналитика SSP; VAST 4.0 support | план борды + CTO |
| GOAL-8 | Объединённая платформа (B2B + Internal + SSP) | 2026 | Единый продукт заменяет legacy B2B + internal tools; отказ от старых версий в Q3 | план CTO (царь-платформа) |
| GOAL-9 | Сформировать команды и устранить bus factor | Q1-Q2 2026 | +4 человека; ни одна зона не на одном человеке; CI/CD настроен | план CTO итерация 1 |
| GOAL-10 | Переезд с 1С на аналитические DB | H2 2026 | BI в дашборде с данными из ClickHouse; CEO не зависит от 1С | план CTO Q3 |
| GOAL-11 | Сквозная видимость маркетинговой воронки | H2 2026 | C-level видит полную воронку канал→лид→клиент→MRR в OneBI; CAC и ROI по каналам; эффективность AM | запрос PO |

---

## Milestones

| Milestone | Срок | Goal | Зависимости | Инициативы |
|-----------|------|------|-------------|------------|
| 🏁 Org: Команды сформированы | 31.03.2026 | GOAL-9 | — | ORG-1, ORG-2, ORG-3 |
| 🏁 Core: Server Bidding Этап 1 | 30.04.2026 | GOAL-6 | — | C3a |
| 🏁 Data: Materialized Views Ready | 30.04.2026 | GOAL-2 | — | D1, D2 |
| 🏁 Growth: PubC Landing Live | 15.04.2026 | GOAL-3 | — | G1, G2, G3 |
| 🏁 Portal: MVP BI Launched (первый релиз платформы) | 30.06.2026 | GOAL-1, GOAL-8 | 🏁 Materialized Views | P1, P1a, P1b, P1c |
| 🏁 Core: Server Bidding Этап 2 | 30.06.2026 | GOAL-6 | 🏁 SB Этап 1 | C3b |
| 🏁 Core: SSP MVP | 30.09.2026 | GOAL-7 | C13 | C13, SSP-1, SSP-2, SSP-3 |
| 🏁 Data: ILRD Processing | 30.09.2026 | GOAL-4 | 🏁 Materialized Views | D3 |
| 🏁 Finance: BI заменяет 1С | 31.10.2026 | GOAL-10 | 🏁 MVP BI, D1 | F1, F2, F3, F4 |
| 🏁 Portal: L2 Features | 31.10.2026 | GOAL-4 | 🏁 ILRD Processing | P2, P6 |
| 🏁 Portal: Релиз платформы (отказ от legacy) | 30.11.2026 | GOAL-8 | 🏁 L2 Features, 🏁 BI заменяет 1С | P7 |
| 🏁 Portal: Onboarding Flow | 30.11.2026 | GOAL-5 | 🏁 MVP BI | P3 |
| 🏁 Data: Битрикс-коннектор live | 31.07.2026 | GOAL-11 | 🏁 Materialized Views | D10, G12 |
| 🏁 Portal: Marketing Funnel Dashboard | 30.11.2026 | GOAL-11 | 🏁 Битрикс-коннектор, 🏁 L2 Features | P13, P14, D11, D12, G13 |

**Критический путь:**
```
🏁 Команды (ORG) ─────────────────────────────────────────────────────────────
🏁 Materialized Views (D1) → 🏁 MVP BI (P1) → 🏁 ILRD (D3) → 🏁 L2 Features (P2)
                              🏁 MVP BI (P1) → 🏁 Onboarding (P3)
                              🏁 MVP BI (P1) → 🏁 BI заменяет 1С (F) → 🏁 Релиз платформы (P7)
🏁 SB Этап 1 (C3a) → 🏁 SB Этап 2 (C3b)
                      🏁 SSP MVP (C13+SSP)
G12 (SOURCE_ID cleanup) → D10 (Битрикс-коннектор) → D12 (атрибуция) → P13 (Marketing Funnel)
```

---

## Треки

| Track | Суть | Владелец |
|-------|------|----------|
| **Org** | Формирование команд, найм, процессы, стандарты | Вова (CTO) |
| **Core** | SDK, адаптеры, bidding, сети, R&D, trust/compliance | Денис + Вова |
| **SSP** | CAS Exchange → CAS SSP: аналитика, CMS, фильтры | Денис + Вова |
| **Data** | ClickHouse, ILRD, ETL, semantic layer, CAS Event Server, коннекторы MMP | Борис + data team |
| **Portal** | Объединённая платформа (B2B + Internal), BI аналитика, онбординг | Руслан + Product |
| **Services** | Predictive LTV, creative management, UA-оптимизация, бенчмарки | Product + Data |
| **Finance** | Биллинг, reconciliation, выплаты, комиссии, 1С-миграция | Product + Backend |
| **Growth** | Сайт, воронки, контент, реклама, community | Marketing + Product |
| **DX** | SDK-документация, guides, developer support + internal onboarding tools | Core + Product |
| **Infra** | Безопасность, масштабирование, CI/CD, recovery, мониторинг | Вова + infra team |

### Путь клиента по трекам

```
Разработчик:  Growth → DX → Core → Portal → Services
Бизнесмен:    Growth → Core (за него делают) → Portal → Services

L1:   Core + Portal (базовый)
L2:   Core + Portal + часть Services
Pub:  Core + Portal + все Services
PubC: Growth → DX → Core → Portal (минимальный)
```

---

## Инициативы по трекам

### Org / Организация — НОВЫЙ ТРЕК

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| ORG-1 | Формирование команд: Infrastructure, Client Side, Core Backend, CMS Dev, Data Engineering, QA | Q1 | В работе | Бюджет CEO (+$10K/мес) | Вова | — |
| ORG-2 | Устранение bus factor — дублёры для Борис (data), Руслан (фронт), Толик (1С), Денис (SDK) | Q1-Q2 | В работе | ORG-1 | Вова | — |
| ORG-3 | Документация и аудит проектов — задокументировать что в головах | Q1-Q2 | Планируется | — | Вова + Product | — |
| ORG-4 | Внедрение процессов Захара (Asana, стандарты PSV) | Q2 | Ждёт | ORG-1, ORG-3 | Вова | — |
| ORG-5 | KPI и оценка реального результата | Q2-Q3 | Ждёт | ORG-4 | Вова | — |
| ORG-6 | Оптимизация команд, принудительные стандарты | Q3-Q4 | Ждёт | ORG-5 | Вова | — |

### Core / Ядро

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| C1 | Стабильность SDK, баг-фиксы (16 багов в Trello) | Ongoing | В работе | — | Денис | — |
| C2 | Новые рекламные сети (Amazon, Молоко, TaurusX, Verve) | H1 | В работе | — | Денис | — |
| C3a | **Server Bidding Этап 1** — Liftoff, Chartboost, inMobi, Mintegral, Pangle, Yandex, YSO, Maticoo | H1 | В работе | — | Денис | — |
| C3b | **Server Bidding Этап 2** — новые интеграции, Bigo ORTB | H2 | Планируется | C3a | Денис | — |
| C4 | Monetization Management (internal tool) | H1 | Готово | — | Денис | — |
| C5 | SDK Release Process (автоматизация) | H1 | Готово | — | Денис | — |
| C6 | Quality Control (автоматизация) | H1 | Планируется | — | Денис | — |
| C7 | A/B Testing Split Engine | H2 | Готово | Data: D3 (ILRD) | | — |
| C8 | Experiment Registry с результатами в BI | H2 | Планируется | C7, Portal: P2 | | — |
| C9 | Trust: ATT compliance, ad quality, fraud prevention | Ongoing | В работе | — | Денис | — |
| C10 | Desktop/Extension SDK (новая ниша) | Beyond | Исследование | Исследование (Савенков) | | — |
| C11 | Manager Toolkit — аналитика для менеджеров, автоматизация A/B, чеклисты онбординга | H1-H2 | Планируется | C4, регламент Осыки | | — |
| C12 | Google MCM-статус + SDK Partnership — сертификация в программе SDK Product Portfolio | H1-H2 | Планируется | C5, C9 | Денис | Q2-Q3 |
| C14 | Cross-platform SDK — Godot, Expo (React Native), Unreal на Epic Store, CI для Unreal | H1-H2 | Планируется | C5 | Денис | — |
| C15 | Crash & Background Services — crash reporting, WorkManager (Android), beginBackgroundTask (iOS) | H1 | Планируется | — | Денис | — |
| C16 | Placement ID & AdUnit фильтры — серверная конфигурация placement | H1 | Планируется | — | Денис | — |
| C17 | Tracking & Events — session event throttling, IAP/Attribution public API, splitting tracking endpoint | H1 | Планируется | — | Денис | — |
| C18 | **Publishing SDK** — объединённый SDK для паблишинг-партнёров, автоинициализация, автопрокидка ILRD | H1 | В работе | — | Юра | — |
| C19 | **Cross Promo** — обновить адаптер для CAS 4, внедрить кросс-промо между приложениями PSV | H1-H2 | Тесты | — | Денис | — |

### SSP / CAS Exchange → CAS SSP — НОВЫЙ ТРЕК

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| SSP-1 | **CASExchange развитие** — VAST 3.0/4.0+, VPAID (iOS+Android), video progress, OM SDK | H1-H2 | В работе | — | Денис | — |
| SSP-2 | **SSP новые форматы** — Native ads, AppOpen format, кастомизация кнопки закрытия/Read more | H1-H2 | Планируется | SSP-1 | Денис | — |
| SSP-3 | **SSP CMS** — управление конфигурацией SSP через CMS | H2 | Планируется | SSP-1 | | — |
| SSP-4 | **SSP аналитика** — аналитика на уровне SSP, фильтры | H2 | Планируется | SSP-3, Data: D1 | | — |

### Data / Данные

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| D1 | Materialized views из существующих данных (Network Reports) | H1 | В работе | — | Борис | — |
| D2 | Self-hosted ClickHouse (миграция с облака, 500 ГБ ILRD) | H1 | Планируется | Infra | Борис | — |
| D3 | ILRD processing (impression-level revenue data) | H1-H2 | Планируется | D2 | Борис | — |
| D4 | Semantic layer (канонические сущности: Install, DAU, Impression, Revenue) | H2 | Концепт | D3 | | — |
| D5 | MMP-коннекторы (AppsFlyer, Adjust, Tenjin) | H2 | Концепт | D4, договорённости с клиентами | | — |
| D6 | Data quality monitoring | H2 | Не начато | D3 | | — |
| D7 | **CAS Event Server** — серверная обработка событий (сессии, IAP, attribution) | H1-H2 | Планируется | D2, C17 | Борис | — |
| D8 | **Синхронизация Event Server с CMS/дашбордами** | H2 | Планируется | D7, SSP-3 | | — |
| D9 | **Переезд данных из 1С в аналитические DB** | H2 | Планируется | D1, F4 | Борис | — |
| D10 | **Битрикс-коннектор** — ETL из Битрикс CRM в ClickHouse: лиды, стадии воронки, SOURCE_ID, AM-активность, даты переходов между стадиями | H1-H2 | Не начато | D1, Битрикс API | | — |
| D11 | **Маркетинг-спенды коннектор** — импорт расходов по каналам (Google Ads, органика, реферальная, конференции) для расчёта CAC и ROI | H2 | Не начато | D10 | | — |
| D12 | **Сквозная атрибуция Lead → Client → Revenue** — связка Битрикс User ID → B2B Client ID → Revenue в ClickHouse. Мост между CRM и продуктовыми данными | H2 | Не начато | D10, D1 | | — |

**Что разблокирует каждый шаг:**

| Data | Portal получает | Services получают | Core получает |
|------|----------------|-------------------|---------------|
| D1 (materialized views) | MVP BI: Revenue, DAU, eCPM, Fill Rate | — | — |
| D3 (ILRD) | Разбивка по SDK/App version, когорты | — | Анализ влияния релизов SDK |
| D5 (MMP) | Unified Report | Predictive LTV, ROAS | — |
| D7 (Event Server) | Продвинутые метрики (session, IAP) | — | Трекинг для RND |
| D9 (из 1С) | C-level дашборд в BI | Revenue reconciliation | — |
| D10 (Битрикс) | Воронка привлечения в BI, эффективность AM | CAC по каналам | — |
| D11 (спенды) | ROI каналов, бюджетирование маркетинга | — | — |
| D12 (атрибуция) | Полная воронка Lead→Revenue, LTV по каналам | Predictive CAC | — |

### Portal / Кабинет → Объединённая платформа

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| P1 | **MVP BI** — Quick View + Reports, тёмная тема, экспорт CSV, eCPM per ad type, сравнение периодов, chip-фильтры | H1 | В работе | Data: D1 | Руслан | — |
| P1a | Toggle gross/net (комиссия CAS) | H1 | Планируется | P1 | | — |
| P1b | Карточка приложения (owner, portfolio, manager, commission) | H1 | Планируется | P1 | | — |
| P1c | UX-фиксы (10 багов из интервью Савенкова) | H1 | Планируется | P1 | | — |
| P2 | **L2 Features** — SDK/App version splits, метрики по сетям, Saved Views, Deep Linking, Export Excel | H1-H2 | Планируется | Data: D3 (ILRD) | | — |
| P3 | **Onboarding** — welcome flow, квалификация, интеграция SDK, first data celebration | H2 | Спецификация готова | P1 | | — |
| P4 | **PubC Portal** — self-service тест игры, status badge, креативы | H2 | Концепт | P3, Data: D5 | | — |
| P5 | **Pub Dashboard** — profit, ROAS, health indicator, A/B comparison | H2 | Концепт | Data: D5, Services: S1 | | — |
| P6 | **Admin Dashboard** — portfolio overview, группировка по менеджерам, anomaly detection | H1-H2 | Планируется | P1, Data: D1 | | — |
| P7 | **Релиз объединённой платформы** — отказ от legacy B2B, переключение всех клиентов | Q3 | Ждёт | P1, P2, P6, F4 | Вова + Руслан | — |
| P8 | **Internal views в платформе** — функционал internal cas.ai внутри единой платформы | H2 | Планируется | P1, P6 | | — |
| P9 | **Дашборды для паблишинг-клиентов** — отдельные views для Pub/PubC | H2 | Планируется | P5, P4 | | — |
| P10 | **Инвентарь** — доступ клиентов к своему рекламному инвентарю | H2 | Планируется | SSP-3 | | — |
| P11 | **Product Health / Единая история приложения** — health indicator, lifecycle, все данные в одном месте | H2 | Концепт | D3, D7 | | — |
| P12 | **Selfservice подключения** — автоматизация подключения клиентов (сейчас 50/50) | H1-H2 | Частично | P3 | | — |
| P13 | **C-level Marketing Funnel Dashboard** — единый экран: воронка привлечения (каналы → лиды → квалификация → онбординг → SDK → первый revenue → MRR), эффективность AM, CAC по каналам, ROI маркетинга, time to first revenue | H2 | Не начато | D10, D12, P6 | Product | — |
| P14 | **AM Performance View** — разбивка по аккаунт-менеджерам: кол-во лидов, конверсия по стадиям, время онбординга, revenue портфеля, health score клиентов | H2 | Не начато | D10, P6 | | — |

### Services / Сервисы

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| S1 | Predictive LTV (вынести наружу, есть внутри) | H2 | Концепт | Data: D5 (MMP) | | — |
| S2 | Creative management (upload + performance table) | H2 | Концепт | Portal: P4 | | — |
| S3 | UA-оптимизация (campaign/network management) | H2 | Концепт | Data: D5 | | — |
| S4 | Бенчмарки (средние по сети CAS, по категориям) | H2 | Концепт | Data: D3+ | | — |
| S5 | **Big Data предсказания и аналитика событий** | Q4 | Концепт | D7, D4 | | — |

### Finance / Финансы

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| F1 | Payments UI redesign (баланс, withdraw, adjustments) | H1 | Планируется | Portal: P1 (дизайн) | | — |
| F2 | Commission management (per-app ставки, gross/net toggle) | H1 | Планируется | P1a | | — |
| F3 | Revenue reconciliation (автоматизация сверки с сетями) | H2 | Не начато | Data: D1+ | | — |
| F4 | 1С-миграция (полный уход с legacy) | H2 | Не начато | F1, F2, F3, Portal: P6, D9 | Толик | — |
| F5 | **Реферальная программа** — бэкенд в 1С (Толик), нужен фронтенд | H1 | В работе (бэк) | P1 (фронт) | Толик | — |

### Growth / Рост

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| G1 | Лендинг "Submit your game" (PubC воронка, AppQuantum стиль) | H1 | Планируется | — | Никита | — |
| G2 | Лендинги по типам клиентов (L1/L2/Pub) | H1 | Планируется | — | Никита | — |
| G3 | Контент-машина (блог, Telegram, гайды по монетизации) | H1 | Планируется | — | | — |
| G4 | Витрина кабинета на сайте (скриншоты BI) | H1 | Ждёт | Portal: P1 (нужны макеты) | Никита | — |
| G5 | Email-триггеры (welcome, nudge, milestone) | H1-H2 | Планируется | Email service | | — |
| G6 | In-app нотификации (operational, diagnostic, upsell) | H2 | Концепт | Notification service | | — |
| G7 | Upsell-триггеры (DAU-based, retention-based) | H2 | Концепт | Portal: P2, Data: D3 | | — |
| G8 | Community — Telegram-канал, developer community | H1 | Не начато | — | | — |
| G9 | A/B тестирование лендингов | H1-H2 | Не начато | G1, G2 | | — |
| G10 | PubC Retention Program — догревание после неудачного теста | H1 | Планируется | Смирнов, Publishing | | — |
| G11 | **Маркетинг 30% от прибыли** — увеличение бюджета, корреляция спендов с развитием | H1-H2 | Не начато | Решение CEO | | — |
| G12 | **Битрикс SOURCE_ID cleanup** — вычистить 79% лидов без SOURCE_ID, настроить обязательную UTM-разметку для всех каналов, автоматическое проставление источника | H1 | Не начато | Битрикс админ | | — |
| G13 | **Атрибуция каналов привлечения** — настроить сквозную разметку: utm_source/medium/campaign → Битрикс SOURCE_ID → BI. Покрыть Google Ads, органику, реферальную, конференции, контент | H1-H2 | Не начато | G12, D10 | | — |

### DX / Dev Experience

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| DX1 | Аудит текущей SDK-документации | H1 | Не начато | — | | — |
| DX2 | Integration quickstart (5-минутный guide) | H1 | Не начато | — | | — |
| DX3 | Changelog + migration guides при обновлении SDK | H1 | Не формализовано | Core: C5 | | — |
| DX4 | Sample projects (Unity, Native Android, iOS) | H1-H2 | Не начато | — | | — |
| DX5 | Developer portal (единая точка входа в документацию) | H2 | Концепт | — | | — |
| DX6 | **Docs/FAQ AI Agent** — сначала внутренний, потом для клиентов | H1 | Планируется | — | | — |

### Infra / Инфраструктура — НОВЫЙ ТРЕК

| # | Инициатива | Горизонт | Статус | Зависимости | Владелец | H1 2026 |
|---|-----------|----------|--------|-------------|----------|---------|
| INF-1 | **Безопасность** — аудит, hardening | H1-H2 | Не начато | ORG-1 | Вова | — |
| INF-2 | **Масштабирование** — инфраструктура под рост | H1-H2 | Не начато | ORG-1 | Вова | — |
| INF-3 | **CI/CD** — пайплайны для всех продуктов | H1-H2 | Частично (SDK done) | ORG-1 | Вова | — |
| INF-4 | **Recovery system** — бэкапы, disaster recovery | H2 | Не начато | INF-1 | | — |
| INF-5 | **Мониторинг и алертификация** — observability для всех сервисов | H1-H2 | Не начато | INF-2 | | — |

---

## Зависимости между треками

```
       Org ──────────────────────────────────────────────────────┐
        │                                                        │
        ▼                                                        ▼
      Core ◄────────────────────────────────────────┐          Infra
        │                                           │
        ├───► SSP (CASExchange → SSP)               │
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
        └──► DX (техническая воронка)
```

**Параллельно и без зависимостей (можно начинать сейчас):**
- Org: ORG-1, ORG-2, ORG-3
- Growth: G1, G2, G3, G8
- DX: DX1, DX2, DX6
- Core: C1, C2, C3a, C17, C18, C19
- SSP: SSP-1
- Infra: INF-1, INF-3, INF-5
- Finance: F1 (дизайн), F5

---

## Поквартальный план CTO (ориентир)

| Q1 (янв–мар) | Q2 (апр–июн) | Q3 (июл–сен) | Q4 (окт–дек) |
|--------------|-------------|-------------|-------------|
| Формирование команд | Первый релиз платформы | BI с переездом из 1С | Полноценное использование платформы |
| Погружение, поддержка текущего | Server bidding основные интеграции | Релиз платформы (отказ от legacy) | Big Data для предсказаний и аналитики |
| Старт проектирования платформы | | | |
| Запуск Server bidding | | | |

---

## Сводка: всего инициатив

| Трек | Кол-во | H1 активных | Новые в v3.0 |
|------|--------|-------------|-------------|
| Org | 6 | 3 | все новые |
| Core | 17 | 10 | C3a/C3b (разбивка), C18, C19 |
| SSP | 4 | 1 | все новые (выделены из C13) |
| Data | 12 | 3 | D7, D8, D9, D10, D11, D12 |
| Portal | 14 | 5 | P7, P8, P9, P10, P11, P12, P13, P14 |
| Services | 5 | 0 | S5 |
| Finance | 5 | 3 | F5 |
| Growth | 13 | 8 | G11, G12, G13 |
| DX | 6 | 4 | DX6 |
| Infra | 5 | 3 | все новые |
| **Итого** | **87** | **40** | **34 новых** |

---

## Решения

### Встреча CTO 09.02
Ключевые решения — `03-product/modernization-plan.md`, секция "Решения".

### Обзор с Осыкой 12.02
| Решение | Детали |
|---------|--------|
| Self-service own ad accounts — отложен на H2+ | Реализация кривая (потерян клиент из Португалии). H1: ручной онбординг для VIP. Из коробки — не раньше H2. |
| C4 → C11: расширение internal tools | C4 (Monetization Management) готов, но менеджеры работают без аналитических инструментов. Добавлен C11 — Manager Toolkit. |
| PubC retention program (G10) | Из 60 лидов → 2 клиента. Новая программа «догревания»: платная закупка → аудит → повторный тест. |
| DX = двусторонний | Наружу: документация, quickstart. Внутрь: инструменты для менеджеров, чеклисты. |

### Новое в v3.0 (план борды + CTO, февраль 2026)
| Решение | Детали |
|---------|--------|
| Царь-платформа = единый продукт | B2B + Internal + PSV Promo + Инвентарь + BI в одном SPA. Отказ от legacy в Q3. |
| Server Bidding в 2 этапа | Этап 1: 8 сетей (H1). Этап 2: новые (H2). |
| CAS SSP как продукт | Exchange эволюционирует в SSP с CMS и аналитикой. |
| Cross Promo — внедрить | Тесты идут, борда хочет полноценный запуск. |
| MCM-статус Google | Отдельно от SDK Partnership. Управление AdMob-аккаунтами клиентов. |
| +4 человека, +$10K/мес | Бюджет на найм утверждён CEO. |
| BI заменяет 1С к Q3 | C-level дашборд в OneBI, CEO не зависит от 1С. |
| Big Data в Q4 | Предсказания и аналитика событий после полного запуска платформы. |

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
