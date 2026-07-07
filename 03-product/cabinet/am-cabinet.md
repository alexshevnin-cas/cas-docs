# Кабинет AM — ролевые рабочие места (Слой 4)

> **Статус:** Alpha · хост platform.cas.ai (INTERNAL-сборка)
> **Что это:** тот же кабинет, что видит клиент, **плюс служебные функции**. Канон слоёв → [product-architecture.md](../../01-platform/product-architecture.md).
> **Источник RBAC:** прототип `/git-project/onebi/docs/research/rbac-overview.md` (v1 Alpha).

AM-кабинет — это не отдельный продукт, а **role-based workspace** поверх единого кабинета.
Менеджер, владеющий клиентами, видит ту же систему + служебные зоны. INTERNAL-бейдж, пункты
Internal Services / Admin / Super Admin — это и есть AM-сборка на platform.cas.ai.

---

## 1. Ролевые рабочие места (АРМ)

### АРМ Монетизатора (zone monetisation)
Разгон eCPM портфеля (Уровень 2 «Quality»). North Star — ARPDAU портфолио.
- Метрики: Ad Revenue, ARPDAU, eCPM, Fill Rate, Share of Voice by Network, Impr/Session (Banner/Inter/Reward).
- Заказ инструмента: **CAS Configuration** (настройка + раскатка waterfall-конфигов, эксперименты) — см. [horyk-portfolio-monetization-brief.md](../horyk-portfolio-monetization-brief.md).

### АРМ UA Manager (zone ua)
Закреплённые игры/кампании. **Нет доступа к финансам, нет impersonation.**
- Метрики: New Users, Retention, LTV, ROAS, CPI.

### АРМ Account Manager
Ведёт закреплённый пул студий и паблишеров.
- **Organization Assignments** — видит только назначенные организации (кто назначил / когда / комментарий).
- **Impersonation «Войти как»** — работа в интерфейсе клиента, 30-мин idle-timeout, всё в audit log.
- BD Dashboard: Client / Manager / Revenue / DAU / Trend / Churn Risk; дерево MRR → ARR → по AM → по приложениям.

---

## 2. Admin / Internal / Super Admin

- **Super Admin** (`super_admin`) — полный доступ ко всем организациям, биллинг, управление ролями, impersonate кого угодно.
- **Platform Admin** (`platform_admin`) — администратор одной платформы (publishing / monetization / internal): все орги своей платформы, управление ролями, аудит-лог.
- **Internal Services** — служебные инструменты (zone tools).
- **OneBI SuperAdmin** разрезы в Reports: Manager / Customer / Date Created (кросс-клиентские фильтры, вне клиентской версии). Фичи Portfolio view / Gross-Net toggle / Churn risk / Anomaly detection / AM performance — **[planned]**, каркас Internal/Admin в Alpha.

---

## 3. RBAC — модель доступа

**Три уровня проверки** (независимы): 1) Аутентификация (JWT/сессия) → 2) Авторизация (Роль + Права + Платформа) → 3) Данные (фильтрация по организации/tenant).
**Три измерения:** `Роль × Организация × Платформа`. Принцип изоляции: каждый запрос к БД автоматически фильтруется по текущей организации — чужой tenant физически недоступен.

**Платформы и типы организаций:**

| Платформа | Тип орг. | Что включает |
|-----------|----------|--------------|
| Publishing | `studio` | Игры, UA-кампании, ROAS, revenue sharing, выплаты |
| Monetization | `publisher` | Приложения, SDK, waterfall, bidding, eCPM, инвойсы |
| Internal | `cas_internal` | Единственная орг. этого типа; доступ ко всем платформам, управление пользователями/ролями, аудит |

**13 ролей:**
- Internal (CAS): `super_admin`, `platform_admin`, `account_manager`, `ua_manager`, `analyst`, `finance`, `support`
- Studio (Publishing): `studio_owner`, `studio_member`, `studio_viewer`
- Publisher (Monetization): `publisher_owner`, `publisher_developer`, `publisher_finance`

**Impersonation:** только `super_admin` (любого) и `account_manager` (назначенных). `analyst` / `ua_manager` / `finance` / `support` — никогда. Логируется: кто → кого → когда → что изменил; клиент видит лог действий от своего имени.

**Role Templates (тарифы поверх роли):** Publisher — `client.standard` / `client.analytics` / `client.full`; Studio — `studio.standard` / `studio.full`. Админ назначает шаблон при онбординге; самостоятельное переключение — v2.

**Обязательный аудит:** финансовые операции (выплаты, инвойсы, revenue-share), управление доступом (роли, инвайты, организации), безопасность (регенерация SDK-ключей, impersonation, system permissions).

**Не входит в v1 (→ v2):** кастомные роли, API-токены с гранулярными scope, SSO/SAML, временные доступы, делегирование прав, политика 2FA по организации, UI-панель управления ролями.

---

## 4. Реальные роли (для наполнения — *illustrative / mock из прототипа, подтвердить состав*)

- super_admin: Alex Shevnin · platform_admin: Roman Petrov / Iryna Volkova · finance: Igor Belov
- AM (5): Anton Smirnov, Serhii Shcherbyna, Rashid Sabirov, Maksym Buha, Dmytro Dubniak

---

## Связанные документы

- Канон слоёв: [../../01-platform/product-architecture.md](../../01-platform/product-architecture.md)
- Кабинет пользователя (Слой 3): [overview.md](overview.md)
- АРМ Монетизатора (бриф): [../horyk-portfolio-monetization-brief.md](../horyk-portfolio-monetization-brief.md)
- RBAC (источник): прототип `/git-project/onebi/docs/research/rbac-overview.md`
