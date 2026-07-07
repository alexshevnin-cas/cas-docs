# UX-паттерны и фреймворки для кабинета

Справочник дизайн-паттернов для редизайна кабинета CAS. Не привязан к конкурентам — универсальные best practices.

---

## Layout

**Рекомендация: Sidebar + Top-Rail.** Коллапсируемый sidebar (секции: Analytics, Apps, Payments, Account, Notifications) + top-rail для контекстных контролов (период, app selector, compare). Паттерн AdMob, AppLovin, Stripe, Mixpanel — паблишеры переключаются между платформами и ожидают знакомую навигацию.

---

## KPI-карточки — анатомия

```
┌─────────────────────────┐
│  Revenue          [?]   │  ← Label + Info tooltip
│  $48,234               │  ← Primary Value (24-32px)
│  ▲ +8.5% vs prev 7d    │  ← Trend Arrow + % Change
│  ╱╲╱╲╱──╱╲             │  ← Sparkline (опционально)
└─────────────────────────┘
```

- **4 карточки по умолчанию** (DAU, Revenue, ARPDAU, eCPM), "Show more" для остальных
- Цвета: blue/orange вместо green/red (8% мужчин — дальтоники)
- Trend arrow + % обязательны — без них числа лишены контекста
- Tooltip с формулой метрики по hover на [?]

---

## Фильтры — chip-based inline

```
[Period: Last 7d ▼]  [App: All ▼]  [Platform: All ▼]  [+ Add filter]  [Clear all]
```

- Активные фильтры = removable chips с "×"
- Global filters (период, приложение) — в top-rail
- Contextual filters (view by) — внутри конкретного виджета
- Sticky filter bar при скролле
- Показывать scope: "Showing data for 3 of 12 apps"

---

## Progressive disclosure (L1 vs L2)

| Уровень | Что видит | Как реализовать |
|---------|----------|-----------------|
| **L1 (базовый)** | Quick View: 4 KPI + график + таблица | Default tab |
| **L2 (продвинутый)** | Reports: все метрики, breakdowns, saved reports | Tab "Reports" |
| **Admin/BD** | Все + internal metrics, кросс-аккаунтные данные | Отдельная роль |

Паттерн GitLab Pajamas: Level 1 = 80% действий 80% пользователей → показывать по умолчанию.

---

## Онбординг — пустые состояния

**Комбинация трёх паттернов:**
1. **Checklist** — "2 из 5 шагов выполнено" (SDK integrated → первый impression → первый отчёт)
2. **Contextual empty states** — каждая пустая секция имеет свой текст и CTA
3. **Progress-driven cards** — KPI-карточки начинают как "Waiting for first data..." и оживают когда приходят данные

**НЕ использовать demo data** — в ad-tech паблишеры должны доверять числам.

---

## Уведомления — трёхуровневая архитектура

| Уровень | Канал | Пример |
|---------|-------|--------|
| **Critical** | Баннер (не закрывается) + email instant | SDK breaking change, payment failure |
| **High** | Bell icon + email instant | Revenue drop >20%, integration error |
| **Medium** | Bell icon + email digest (weekly) | New SDK version, feature update |
| **Low** | Bell icon only | Tips, product education |

Bell icon в header → dropdown 300-400px с последними 20 уведомлениями. В Settings — per-category, per-channel контроль частоты.

---

## Финансы — по модели Stripe

```
BALANCE:     Available $19,048  |  Pending $7,090
OVERVIEW:    Gross Revenue  |  Net Revenue  |  Fees  |  Payouts
HISTORY:     [Filter ▼] [Date ▼] [Type ▼] [Export CSV]
             Date | Type | Amount | Status | Comment
```

- Status indicators: цвет + label (Paid, Pending, Failed)
- Click на строку → detail panel (drawer, не новая страница)
- Export: CSV + PDF, с учётом фильтров

---

## Мобильная версия

- **Card stacking**: 4 KPI → 2×2 на tablet → 1 колонка на phone
- **Таблицы → cards**: каждая строка становится card с key-value парами
- **Sidebar → hamburger** + bottom tab bar (Analytics, Apps, Payments, Alerts, Settings)
- Touch targets: min 44×44px (Apple HIG)
- Desktop-first — корректная стратегия для ad-tech

---

## AARRR framework применительно к кабинету

| Stage | CAS аналог | Секция кабинета | Метрики |
|-------|-----------|----------------|---------|
| **Acquisition** | SDK интегрирован | Онбординг, Apps | Apps connected, SDK version |
| **Activation** | Первый impression | Quick View (progress cards) | First impression, fill rate |
| **Revenue** | Ad revenue | Quick View KPI + Финансы | Revenue, ARPDAU, payouts |
| **Retention** | Паблишер остаётся | Reports (тренды) | DAU trend, revenue trend |
| **Referral** | Рекомендации | Future | Referral count |

---

## Ссылки

- [Pencil & Paper: Dashboard UX](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards) — F-pattern, card layout
- [Pencil & Paper: Filter UX](https://www.pencilandpaper.io/articles/ux-pattern-analysis-enterprise-filtering) — chip filters
- [NNGroup: Complex Application Design](https://www.nngroup.com/articles/complex-application-design/) — навигация
- [NNGroup: Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) — показ/скрытие
- [Anatomy of KPI Card](https://nastengraph.substack.com/p/anatomy-of-the-kpi-card) — анатомия карточки
- [Carbon: Dashboard Visualization](https://carbondesignsystem.com/data-visualization/dashboards/) — IBM design system
- [PatternFly: Dashboard Pattern](https://www.patternfly.org/patterns/dashboard/design-guidelines/) — Red Hat
- [Datadog: Effective Dashboards](https://github.com/DataDog/effective-dashboards/blob/main/guidelines.md) — open-source
- [Material Design: Data Viz Accessibility](https://m3.material.io/blog/data-visualization-accessibility) — accessible colors
