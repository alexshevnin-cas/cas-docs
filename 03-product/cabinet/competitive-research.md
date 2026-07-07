# Конкурентное исследование кабинетов

**Дата:** 2026-03-19
**Источники:** AppLovin MAX, Google AdMob, Unity LevelPlay, DT FairBid, Chartboost, AppsFlyer, Adjust, Singular, Appodeal
**Структура:** по 5 секциям кабинета CAS (см. `overview.md`)

---

## Сводка: кто что умеет

| Секция CAS | AdMob | AppLovin MAX | Unity LevelPlay | **CAS сейчас** |
|-----------|-------|-------------|----------------|----------------|
| **I. Аналитика** | Home + Reports + per-app | 6 типов отчётов + compare + scheduling | Performance + Pivot + Cohorts + User Activity | 1 страница Mediation + Publishing |
| **II. Приложения** | Apps + ad units + mediation groups + app readiness | Ad Units + waterfall editor + A/B + segmentation | Management + A/B + segments + ad quality | Список (статусы, без метрик) |
| **III. Финансы** | Payments (через AdSense), ~21-е число | Tipalti, NET 15, $100 min | NET 60, invoices, advance 70% | 254 строки без фильтров |
| **IV. Аккаунт** | Users + custom roles + 2FA (Google) + Firebase | Users + granular permissions + 2FA (SMS) | 4 роли + activity logs (90d) | Personal data + OAuth |
| **V. Коммуникация** | Policy center + optimization tips + anomaly detection | Scheduled reports only. **Нет алертов** | Ad Quality rules + email | 2 hardcoded баннера |

---

## I. Аналитика

### Что делают конкуренты

**AdMob:** Home dashboard с KPI-карточками (revenue тренд, impressions/eCPM с period-over-period, user metrics через Firebase). Anomaly detection (отключена янв 2026, но архитектура есть). "My AdMob page" с optimization tips. Saved reports с sharing.

**AppLovin MAX:** 6 типов отчётов — Performance, Advanced (hourly, все dimensions), User Activity (DAU/ARPDAU), Cohorts (retention, RPI), ALX (exchange), Network Comparison (дискрепанси). Compare mode. Scheduled reports по email.

**Unity LevelPlay:** 33 метрики, 18 breakdowns, saved reports. Real-Time Pivot — OLAP с 4 data cubes, scheduling, CPM bucket analysis. Cohort reports: retention D1-D7, revenue per user. A/B Test Analyzer.

**AppsFlyer (best-in-class):** Custom widget dashboard. AI Assistant с NLP-запросами.

### Рекомендации

| Приоритет | Что | У кого | Зачем |
|-----------|-----|--------|-------|
| **P0** | DAU + ARPDAU в KPI-карточки | Все | Скрыты в Table Columns — самые нужные метрики |
| **P0** | Дельты (% к прошлому периоду) | MAX, AdMob | Без контекста числа бессмысленны |
| **P1** | Compare mode (два периода) | MAX | Один переключатель, огромная ценность |
| **P1** | Единый UX для Mediation + Publishing | — | Сейчас два разных интерфейса |
| **P1** | Saved/scheduled reports | MAX, LevelPlay | Email-доставка отчётов |
| **P2** | User Activity / Cohorts | LevelPlay, MAX | Retention и engagement |
| **P2** | Anomaly detection | AdMob (архитектура) | **Ни один медиатор не делает нативно** |

---

## II. Приложения

### Что делают конкуренты

**AdMob:** Apps → per-app dashboard (KPI, ad units, mediation groups). Добавление через поиск в сторе или manual. App readiness review (2-3 дня). app-ads.txt валидация. Firebase линковка.

**AppLovin MAX:** Waterfall editor — до 8 вариантов per ad unit, drag-and-drop. A/B testing (50/50, promote/deprecate за 24-48ч). Auto-CPM. Waterfall segmentation. Bulk CSV. Ad Unit Management API. Mediation Debugger (SDK). Ad Review suite: creative gallery, user journey, competitor monitoring. Test Mode.

**Unity LevelPlay:** Waterfall с 3-level rate hierarchy (instance/group/country). A/B testing (5% шаг, retention D1-D7 в результатах). Floor price per bidder. Ad Quality с churn tracking D1-D14, creative gallery, notification rules. Activity logs (90 дней). Dynamic segmentation (mid-session).

### Рекомендации

| Приоритет | Что | У кого | Зачем |
|-----------|-----|--------|-------|
| **P0** | Метрики рядом с приложением (revenue, DAU за 7d) | AdMob per-app | Нужно переключаться в Mediation |
| **P1** | SDK status per app | MAX Debugger | "Работает ли SDK?" — главный вопрос нового клиента |
| **P1** | Ссылки на стор | AdMob | Базовый UX |
| **P1** | Setup checklist (онбординг) | AdMob "My AdMob page" | Time-to-value, нагрузка на support |
| **P2** | Read-only waterfall | Прозрачность | Клиент видит как устроена монетизация |
| **P2** | Test mode / test devices | MAX | Для отладки |
| **P2** | app-ads.txt management | AdMob | Сейчас только статус, нет помощи |
| **P3** | A/B testing waterfalls | MAX, LevelPlay | После появления self-service |
| **Future** | Ad quality / creative review | LevelPlay, MAX | Требует Ad Review SDK |

---

## III. Финансы

### Что делают конкуренты

**AdMob:** Ежемесячно ~21-е число. EFT, wire, SEPA, PayPal Hyperwallet. Настраиваемый threshold ($100+). Payment holds (до 1 года). Tax forms (W-9/W-8). Estimated vs finalized revenue.

**AppLovin MAX:** Tipalti. NET 15 (~15-е число). ACH, wire, PayPal, check. Min $100 ($150 wire). Hold payments. PDF invoices. Платит только за свой demand — остальные сети отдельно.

**Unity LevelPlay:** NET 60. Wire, PayPal, eCheck (Tipalti). Invoices + payment history + per-app revenue breakdown. Advance payments ~70% к 15-му числу текущего месяца.

### Рекомендации

| Приоритет | Что | У кого | Зачем |
|-----------|-----|--------|-------|
| **P0** | Фильтр по периоду + тип транзакции | Базовый UX | 254 строки невозможно сканировать |
| **P0** | Monthly summary | **Никто не делает хорошо** | Шанс дифференцироваться |
| **P1** | Estimated vs finalized revenue | AdMob | "Это прогноз или начислено?" |
| **P1** | Export CSV/PDF | Базовый UX | Для бухгалтерии |
| **P2** | Заказ выплаты из кабинета | — | Self-service |
| **P2** | Graph of balance over time | — | Визуальная история |

**Ключевой инсайт:** финансовая прозрачность — самое слабое место **всех** конкурентов.

---

## IV. Аккаунт

### Что делают конкуренты

**AdMob:** Google Account (SSO, 2FA). Built-in roles: Administrator, Manager. Custom roles с granular permissions (5 категорий). Per-app доступ. Linked services (Firebase, AdSense). Test devices.

**AppLovin MAX:** Users с granular permissions (reporting, ad management, payments). Per-app restrictions. 5 типов API-ключей (SDK, Report, Management, Event, Ad Review). 2FA (SMS).

**Unity LevelPlay:** 4 роли (Owner, Manager, User, Guest). Activity logs: кто что менял за 90 дней. User management из profile dropdown.

### Рекомендации

| Приоритет | Что | У кого | Зачем |
|-----------|-----|--------|-------|
| **P1** | Team management (invite + roles) | AdMob, MAX | Крупные паблишеры = несколько человек |
| **P1** | API keys в кабинете | MAX | Для интеграций |
| **P2** | Activity logs | LevelPlay | "Кто менял настройки" |
| **P2** | Forgot password + 2FA | AdMob | Базовый security |

---

## V. Коммуникация

### Что делают конкуренты

**AdMob:** Policy center (нарушения + апелляции). Optimization tips ("My AdMob page"). Anomaly detection (отключена, но архитектура была). Ad review alerts (email). Announcements.

**AppLovin MAX:** **Нет алертов.** Только scheduled email reports. Нет revenue drop notifications. Нет notification center.

**Unity LevelPlay:** Ad Quality notifications (custom rules + email daily). A/B test results notifications. Cross-promotion tools.

**Никто:** Revenue anomaly alerts нативно. Рынок покрывается 3rd-party (Aditude, Segwise).

### Рекомендации

| Приоритет | Что | Модель | Зачем |
|-----------|-----|--------|-------|
| **P0** | Dismissable баннеры | Базовый UX | Текущие не закрываются |
| **P1** | Revenue drop alerts (email) | Aditude/Segwise | **Уникальная дифференциация** |
| **P1** | Notification center (bell icon) | — | Централизованное место для уведомлений |
| **P2** | SDK update notifications | — | Retention |
| **P2** | Upsell точки (publishing) | — | Cross-sell из mediation |
| **P3** | Weekly email digest | — | Engagement |

---

## Что убрать из текущего кабинета

| Элемент | Действие |
|---------|----------|
| Незакрываемые баннеры | Крестик или → notification center |
| `/creatives` → JSON | Удалить роут или реализовать страницу |
| Bundle ID вместо имён в Mediation | Использовать имена из Applications |
| Presets "No presets found" | Сделать UX создания или убрать блок |
| Default backend (медленный) | Перевести всех на ClickHouse |
| `user-scalable=no` | Убрать |

---

## Возможности для дифференциации

Области, где **ни один конкурент не силён**:

1. **Revenue anomaly alerts** — ни один медиатор нативно. 3rd-party стоят денег.
2. **Payments transparency** — самое слабое место всех. Monthly summary, graph, фильтрация.
3. **In-dashboard benchmarking** — "ваш eCPM vs рынок". Никто не встраивает.
4. **Publishing + Mediation = один кабинет** — конкуренты разделяют. CAS может связать (ROAS).
5. **Mobile revenue glance** — ни у кого нет хорошего мобильного UX.
6. **Auto-generated app-ads.txt** — все делают руками.
7. **Transparency-first** — fill rate, latency, eCPM distribution. MAX годами не показывает.
8. **Native alerting** — Slack/email/Telegram. Никто не предлагает.

---

## Боли паблишеров (из форумов и обзоров)

| Боль | Кто страдает | Вывод для CAS |
|------|-------------|---------------|
| **Bias** — платформа приоритизирует свою сеть | MAX, LevelPlay | CAS без своей ad network → «честный медиатор» |
| **Forced migration** — ломают фичи без обратной связи | MAX | Коммуницировать изменения заранее |
| **Missing metrics** — fill rate, latency годами нет | MAX | Показать то, что конкуренты прячут |
| **SDK bloat** — 10+ адаптеров, glitches | Все | CAS SDK объединяет — подчеркнуть |
| **Poor support** — месяцами нет ответа | AdMob, MAX | Managed model = speed of response |
| **Lock-in** — уйти = потерять UA | MAX | Export/API с первого дня |
| **Dashboard stagnation** — годами без улучшений | MAX | Регулярные улучшения = retention |
| **NET 60** — 2 месяца ждать денег | LevelPlay | NET terms = конкурентный аргумент |

---

## Связанные документы

- Целевая структура: `overview.md`
- Текущее состояние: `current-state.md`
- UX-паттерны: `ux-patterns.md`
- Deep dive LevelPlay: `05-research/levelplay-console-research.md`
