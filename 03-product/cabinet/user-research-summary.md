# Кабинет — конспект пользовательских интервью

**Аудитория:** новый продакт-менеджер на кабинетный трек.
**Цель документа:** за 30–40 минут получить картину того, что говорят пользователи о текущем кабинете b2b.cas.ai, какие сегменты что просят и где главные боли.
**Период исследования:** январь–апрель 2026.

> Для глубокого погружения по конкретному интервью — открыть файл из колонки «Источник».

---

## 1. Карта проведённых интервью

### Внешние пользователи кабинета

| # | Дата | Респондент | Тип | Источник | Главное |
|---|------|-----------|-----|----------|---------|
| 1 | 2026-01-30 | Dima Rom (FUNBURSTGAME, 15+ apps) | L2 | `05-research/L2-dima-rom.md` | Дашборд = диагностика «всё ли загрузило сегодня». Реальная аналитика — в Excel/Firebase. Просит разбивки по SDK/App version, тёмную тему, anomaly detection, починку Payments |
| 2 | 2026-02-05 | Илья Никитин (ex-клиент, ушёл в AppLovin MAX) | Ex-client | `05-research/ex-client-nikitin.md` | Главная причина ухода — нет Reporting API и нет мультипользовательского доступа (делил логин с командой). Также: интеграция с MMP, документация, CMP |
| 3 | 2026-02-06 | Михаил Жвиков (Oktopus, Superhero) | Pub (маленький) | `05-research/pub-zhvikov-superhero.md` | Tenjin хватает, детальный BI — перебор. Хочет «индикатор здоровья проекта» и предиктивный LTV для приоритизации разработки фич |
| 4 | 2026-02-06 | Андрей Мельников (Car Crash) | Pub (микро) | `05-research/pub-melnikov-carcrash.md` | Net income после комиссии CAS, предиктивный доход за месяц, ROAS в CAS (не в Tenjin), воронки >10 шагов, тренды рынка |
| 5 | 2026-02-06 | Ярослав Савенков (ZooqVPN) | L2 | `05-research/L2-savenkov-zooqvpn.md` | Самый детальный UX-фидбэк: 10 конкретных багов, unified report Spend+Revenue+Events, CAS↔AppsFlyer интеграция, eCPM по ad type, нон-гейминг вертикаль |
| 6 | 2026-02-11 | Rinaz Khadiev (PSV studio) | Pub (маленький) | `05-research/pub-khadiev.md` | Ежедневная диагностика сетей, network health view (включая 0 impr), креативы по сетям, баг date-фильтра, ложные алерты по удалённым apps |
| 7 | 2026-04-01 | Serhii Shcherbyna (sales mediation, **внутренний**) | Internal/voice-of-customer | `05-research/cabinet-tz-shcherbyna.md` | Озвучивает боли клиентов на онбординге: empty state = отторжение за 10 секунд, app-ads.txt ложные тревоги, SDK race, отсутствие human touch |

### Внутренние сессии (контекст для PM)

| # | Дата | Тема | Источник |
|---|------|------|----------|
| 8 | 2026-03-30 | Онбординг Ruslan Novikov по кабинету — рекламная экосистема, 3 столпа (apps/credentials/waterfall), видение self-service | `05-research/internal-ruslan-cabinet-onboarding.md` |
| 9 | 2026-02-09 | Roadmap-talk: фазовый план, дизайнер на фрилансе, ClickHouse, toggle комиссии gross/net | `05-research/roadmaptalk-analysis.md` |
| 10 | 2026-03-19 | Конкурентный анализ кабинетов (AdMob, MAX, LevelPlay) | `03-product/cabinet/competitive-research.md` |
| 11 | 2026-03-19 | Deep-dive Unity LevelPlay console | `05-research/levelplay-console-research.md` |
| 12 | 2026-02-06 | UX-референсы: Voodoo, Amplitude, Appodeal | `05-research/competitive-ux-reference.md` |

---

## 2. Сегменты пользователей — кто что хочет

CAS делит клиентов на 4 типа (полное описание: `02-business-model/client-types.md`). Подытожу через линзу кабинета.

### L1 — базовый медиашный клиент
- Подключил SDK, смотрит revenue утром.
- Кабинет = «всё ли в порядке».
- Ему достаточно: KPI-карточки, тренд, top-приложения, баланс.
- **Никого из L1 в интервью пока нет** — это пробел в research.

### L2 — продвинутый медиашный клиент (Dima Rom, Savenkov)
- Делает аналитику сам, кабинет — один из источников.
- Хочет: drill-down (по сетям, версиям SDK/app, странам), сравнение периодов, экспорт, saved views, share link, тёмную тему, anomaly detection.
- **Главная боль: доверие к данным.** Сетки отваливаются молча, DAU расходится с Firebase, аджастменты дублируются.
- **L2 ≠ однородный сегмент.** ZooqVPN (non-gaming, VPN) не интересуется сетями и версиями SDK — ему нужен unified Spend+Revenue+Events. FUNBURSTGAME (gaming) живёт диагностикой сетей. Не делать «среднее по больнице».

### Pub — паблишер на договоре с CAS (Zhvikov, Melnikov, Khadiev)
- UA делегирован CAS, разработчик НЕ хочет лезть в waterfall и сети.
- **2 из 3 маленьких Pub** говорят: export/saved views/share — не нужно. Подтверждённая гипотеза **Pub-lite**.
- Хочет: net income после всех комиссий, предиктивный доход за месяц (особенно при сезонности), здоровье проекта (red/green), ROAS, креативы по сетям (self-service обучение), тренды рынка.
- Khadiev — исключение: использует кабинет ежедневно как диагностический инструмент, потому что маленькая студия и сам ведёт продакт.

### PubC — кандидат в паблишинг
- Оценивает свой потенциал, ещё не клиент.
- Никого из PubC в интервью кабинетной темы нет. Запросы на функционал идут от Pub.
- Референс — Voodoo: submit your game → автотест → метрики → решение.

### Ex-client — ушедший (Никитин)
- Причина ухода: нужно было закупать в AppLovin для Blended-кампаний, у CAS не было Reporting API.
- Дополнительно: невозможность дать доступ команде (CMO, аналитик, закупщик), отсутствие документации, отсутствие интеграции с продуктовой аналитикой (Dev2Dev).

---

## 3. Сквозные боли (повторяются у нескольких респондентов)

| Боль | Кто упоминал | Куда влияет |
|------|--------------|-------------|
| **Empty state = отторжение за 10 сек** | Shcherbyna (видит каждый день при онбординге) | Critical для retention новых |
| **Сетки отваливаются без уведомления** | Dima Rom, Khadiev | Network health view, anomaly alerts |
| **Нет разбивки по версии SDK / app** | Dima Rom, Khadiev, Savenkov | OneBI breakdowns |
| **Дата-фильтр / фильтры глючат** | Dima Rom, Khadiev, Savenkov | UX-баги |
| **eCPM агрегированный по всем ad types — обманывает** | Savenkov | Quick View, формула KPI |
| **Net income vs Gross — непонятно** | Melnikov, Dima Rom (через адж.), Savenkov | Toggle gross/net, прозрачность Payments |
| **Предиктивный доход за месяц** | Zhvikov, Melnikov, Savenkov | Prediction Revenue виджет (уже в roadmap) |
| **Аналитика разбросана по сервисам** (Tenjin, Firebase, CAS) | Melnikov, Savenkov, Никитин | Unified report, интеграции с MMP |
| **Нет мультипользовательского доступа** | Никитин (=причина ухода) | Team management (плейсхолдер в overview) |
| **Нет тёмной темы** | Dima Rom, Melnikov ("интроверты в 3 ночи") | Глобальная UX-настройка |
| **Документация только через менеджера** | Никитин, неявно Khadiev | Help center / docs |

---

## 4. Конкретные UX-баги (надо знать в лицо)

| # | Баг | Источник |
|---|-----|----------|
| 1 | Date picker сбрасывается при переключении — нужно кликать дважды | Khadiev, Dima Rom |
| 2 | Сохранённые фильтры (presets) исчезают / «не всегда работают» | Dima Rom, Savenkov |
| 3 | Лимит 15 приложений в группе — недостаточно для портфелей | Dima Rom |
| 4 | Кнопка Export скрыта — клиент не находит | Savenkov |
| 5 | Фильтры не показывают что выбрано (нет chips/tags) | Savenkov |
| 6 | Несколько приложений одним цветом на графике | Savenkov |
| 7 | Попапы без отдельных URL — нельзя поделиться ссылкой | Savenkov |
| 8 | Ложные крестики app-ads.txt на 130+ apps | Shcherbyna |
| 9 | Ложные алерты по удалённым приложениям в Applications | Khadiev |
| 10 | Незакрываемый баннер (Bigo, app-ads.txt) | Khadiev, общее |
| 11 | Bundle ID вместо имён приложений | все |
| 12 | Default бэкенд `/mediation` катастрофически медленный (до 122s) | спид-тесты, см. `05-research/dashboard-speed-results.md` |
| 13 | Аджастменты в Payments дублируются, сумма не сходится | Dima Rom |
| 14 | Иконки приложений не подтягиваются | Dima Rom |

---

## 5. Топ-запросы фич (агрегированно)

### Аналитика
- **DAU + ARPDAU в KPI-карточках** (сейчас скрыто в Table Columns) — все
- **Дельты ±% к прошлому периоду** на KPI — Savenkov, Quick View POC
- **Compare mode** (два периода рядом) — Savenkov, Pub
- **Разбивка по версии SDK и версии приложения** — Dima Rom, Khadiev, Savenkov
- **Network health view** — все сети, включая 0 impressions и неподключённые — Khadiev
- **Anomaly detection** — подсветка провалов и нулей — Dima Rom, Khadiev
- **Unified report Spend + Revenue + Events** по GEO+AdType — Savenkov (критично)
- **CAS ↔ AppsFlyer / MMP интеграция** — Savenkov, Никитин
- **Predictive revenue / LTV** за месяц — Zhvikov, Melnikov, Savenkov

### Финансы / прозрачность
- **Net income после комиссии CAS** (toggle gross/net) — Melnikov, Dima Rom
- **Estimated vs finalized** revenue
- **Monthly summary** в Payments + фильтры по периоду/типу
- **Export Payments** (CSV/PDF) — Savenkov

### Self-service & команда
- **Reporting API** — Никитин (=причина ухода), L2
- **Team management** + роли — Никитин (=причина ухода)
- **Saved views + share link** — L2 (Savenkov, Dima Rom)
- **Документация / help center** — Никитин

### Pub-специфика
- **Creative performance по сетям** (self-service обучение, не управление UA) — Khadiev
- **Индикатор здоровья проекта** (red/green) — Zhvikov
- **Тренды рынка** (что хайпит в Google Play / App Store) — Melnikov
- **Воронки >10 шагов** (для игр с длинной прогрессией) — Melnikov

### Онбординг
- **Friendly empty state** вместо красной ошибки — Shcherbyna (главный bottleneck)
- **Human touch блок** (фото менеджера, ссылки на WhatsApp/Telegram) — Shcherbyna
- **Guided tour** для первой сессии
- **SDK gate** — сначала регистрация приложения, потом доступ к интеграции

---

## 6. Что важно знать про сам кабинет

> Глубоко — `03-product/cabinet/overview.md` (целевое) и `current-state.md` (as-is).

### Что есть сейчас
- 4 страницы: Mediation, Publishing, Payments, Applications + dropdown аккаунта.
- Mediation и Publishing — **два разных UX** (разные контролы, разный визуал) для одной задачи (аналитика).
- Applications — список с COPPA/app-ads.txt статусами. **Нет карточки приложения**, нет метрик рядом.
- Payments — 254 строки с 2024 без фильтров. Доминируют fraud adjustments.
- Account — минимальный dropdown. Нет team, нет 2FA, нет forgot password.
- Конфигурация waterfall — **один JSON на клиента**, правится вручную, саппорт в Telegram.

### Что в работе (Q2 2026, Phase 1 — рестайлинг)
Решено на встрече с Shcherbyna 2026-04-01:
- **4 блока вместо 4 страниц:** Analytics / Applications / Payments / Profile.
- **Баланс в хедере** (как у Appodeal).
- **Publishing → таб внутри Analytics** (единый UX с Mediation).
- **OAuth credentials → переезжают в Applications** (логически правильное место).
- **QuickView** = первый экран после логина (KPI + тренд + revenue by network).
- **Prediction Revenue** виджет (особенно для empty state новых).
- **Human touch блок** — фото менеджера + WhatsApp/Telegram, данные из 1С.
- **Имена приложений из стора** вместо bundle ID.
- **Friendly empty state**, гайд тур, починка ложных тревог app-ads.txt.
- **Дизайнер Данила Кузнецов** — первый опыт с B2B dashboards. Старт ~07.04.

### Принципы
- **Managed сейчас → self-service цель.** Сначала прозрачность (показать), потом контроль (дать рулить).
- **Один интерфейс — разные данные.** Кабинет адаптируется под тип клиента (L1/L2/Pub).
- **Three pillars** настройки приложения: Apps, Network credentials, Waterfall configs. У L1 credentials вшиты, у L2+ — свои.

---

## 7. Что не покрыто исследованием (пробелы)

- **L1 — ни одного интервью.** Базовый сегмент, ~80% клиентов, никто не опрошен с лупой кабинета.
- **Только 1 Ex-client.** Воронка ухода = большое слепое пятно.
- **PubC** на кабинете — нет.
- **Внутренние роли** (Admin, Monetisation, UA, BD) — в кабинете не интервьюировали, есть только косвенно через Shcherbyna и Osyka.
- **iOS-only клиенты** — выборка скошена в сторону Android/cross-platform.
- **Крупные L2** (>$100K MAU) — Babygamespub есть в speed-тестах, но не в интервью.

Это потенциальные первые исследования для нового PM.

---

## 8. Полезные ссылки (в порядке чтения)

| Когда | Что прочитать |
|-------|---------------|
| Старт | `01-platform/platform-overview.md` (что такое CAS) → `02-business-model/client-types.md` (сегменты) |
| Кабинет | `03-product/cabinet/overview.md` (целевое) → `current-state.md` (as-is) → `competitive-research.md` |
| Конкурент в глубине | `05-research/levelplay-console-research.md` |
| Аналитика (OneBI) | `03-product/design-spec-bi.md` + `04-bi/metrics-dictionary.md` + `04-bi/filters.md` |
| User stories | `03-product/user-stories.md` |
| Бизнес-модель | `02-business-model/cas-business-model.md` |
| Стратегия и фазы | `03-product/product-strategy-1pager.md` + `03-product/roadmap.md` |
| Скорость дашборда | `05-research/dashboard-speed-results.md` (живые данные по 4 аккаунтам) |
| Все исследования | `05-research/research-log.md` (индекс) |
