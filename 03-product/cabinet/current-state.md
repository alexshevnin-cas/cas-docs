# Кабинет (legacy b2b) — текущее состояние на 2026-03-19

> Снимок legacy-кабинета b2b на 2026-03-19. Целевое состояние — platform.cas.ai (см. [overview.md](overview.md)).
> Детальная FE-спека legacy → [legacy-fe-spec.md](legacy-fe-spec.md). Канон → [`../../01-platform/product-architecture.md`](../../01-platform/product-architecture.md).

Описание текущего кабинета CAS на 2026-03-19, организованное по 5 целевым секциям.
Документ фиксирует **что есть сейчас** — от чего отталкиваться при редизайне.

Скриншоты: `assets/audit-*.png` | Данные: `assets/audit-results.json`
Скрипт сбора: `scripts/cas_cabinet_audit_v2.py`

---

## Навигация и layout

### Текущее меню

```
[CAS.AI лого]   Mediation   Publishing   Payments   Applications   |   [👤 Khadiev Publishing ▾]
```

- Лого слева, 4 пункта навигации по центру, аккаунт-меню справа
- Активный пункт подсвечивается цветом (оранжевый для Mediation, синий для остальных)
- Ранее (до марта 2026) были ещё **Creatives**, **Cross Promo Campaigns**, **$ USD** — убраны

### Маппинг текущих страниц → целевые секции

| Текущая страница | URL | Целевая секция |
|-----------------|-----|---------------|
| Mediation | `/mediation` | **I. Аналитика** → Quick View + Reports (mediation) |
| Publishing | `/publishing` | **I. Аналитика** → Reports (publishing) |
| Payments | `/mypayments` | **III. Финансы** |
| Applications | `/applications` | **II. Приложения** → Список |
| Account menu | dropdown | **IV. Аккаунт** |
| Баннеры (Bigo, app-ads.txt) | встроены в `/mediation` | **V. Коммуникация** |

### Страница логина (`/login`)

- Поля: Email, Password. Кнопка: **Log In**. Ссылка: **Sign Up**
- После входа → редирект на `/mediation`
- Нет: forgot password, OAuth, 2FA

---

## I. Аналитика

Текущая реализация: две отдельные страницы (Mediation и Publishing) с разным UX. В целевой структуре — это один блок с табами.

### Mediation (`/mediation`) — основной экран

**KPI-карточки (3 шт.):**

| Карточка | Формат | Пример |
|----------|--------|--------|
| **Est. Revenue** | Зелёный фон, крупный шрифт | $ 13,848.472 |
| **Impressions** | Обычный текст | 7,775,232 |
| **eCPM** | Обычный текст | $ 1.781 |

Справа: блок **Presets** — "No presets found".

Нет: DAU, ARPDAU, дельты (% к прошлому периоду), тултипы с формулами.

**Панель управления (toolbar):**

| Контрол | Тип | Значения |
|---------|-----|----------|
| **Период** | Кнопки-табы | `LAST ACTUAL DAY` · `7 DAYS` · `30 DAYS` · `CUSTOM` |
| **Show graph** | Чекбокс | Вкл/выкл |
| **View by** | Кастомный dropdown | `Total` · `Application` · `Country` · `Network` |
| **Compared to** | Кастомный dropdown | `None` · `Last week to prior week` · `Last weekend to prior weekend` · `Custom date range` |
| **Table Columns** | Dropdown с чекбоксами | `Application`, `Date`, `Week`, `Month`, `Network`, `Model`, `Platform`, `Country`, `DAU`, `ARPDAU` |
| **Filters** | Кнопка → модальное окно | Applications, Countries, Networks, Ad Type, Platform |

**Фильтры (модальное окно):**
Applications (мультиселект), Countries, Networks, Ad Type (radio + мультиселект), Platform (iOS / Android). Кнопки: SAVE FILTER · CLEAR ALL · APPLY.

**График:** линейный (canvas), ось Y — доллары, ось X — даты. Легенда: Total + Active users. Кнопка HIDE ALL.

**Таблица:** 4 дефолтные колонки (App, Impressions, eCPM, Est. Earnings). Строка Totals. Пагинация 10 строк. Кнопка DOWNLOAD REPORT. Приложения показываются как bundle ID, не как имена.

**Режимы бэкенда:** Default (старый, 2.5–122s), Chart ClickHouse `?mode=ch` (1.5–5.5s), Table `?mode=tb` (1.5–5.5s). Визуально идентичны.

**Ограничения для редизайна:**
- Нет DAU/ARPDAU в KPI-карточках
- Нет дельт (% к прошлому периоду)
- Нет тултипов на метриках
- Выбор приложения спрятан в модальном окне Filters (2 клика)
- Нет периодов Today, This month, 90d, 180d
- Нет compare mode (два периода side-by-side)
- Нет saved/scheduled reports
- Bundle ID вместо имён приложений
- Default бэкенд катастрофически медленный
- **Empty state:** новый пользователь видит красную ошибку, прочерки и пустой график. Время до отторжения — ~10 секунд (по данным Serhii Shcherbyna, sales mediation). Нет friendly empty state, нет обучения, нет prediction

### Publishing (`/publishing`) — UA-экономика

**Контролы:** период (`7 DAYS` · `30 DAYS` · `CUSTOM`), Group By (`Application`), Filter + «+».

**Таблица:** Application, Tracked installs, Spends, Ad Revs, InApp Revs, Total Revs, RevShare. Строка Totals.

**Ограничения для редизайна:**
- Нет KPI-карточек, нет графика, нет экспорта
- Нет Compared to, Table Columns, Show graph — значительно беднее Mediation
- Group By только Application — нет страны/сети
- Другой паттерн фильтрации (кнопка + «+» vs модальное окно)

### Проблема: два разных UX для одного блока

Mediation и Publishing — два интерфейса аналитики с разным набором контролов, разным визуалом, разной глубиной. Клиент-паблишер (Pub) вынужден переключаться между двумя страницами, чтобы видеть полную картину: monetization + UA. В целевой структуре это должны быть табы одного блока с единым UX.

---

## II. Приложения

Текущая реализация: одна страница-список. Из 5 подблоков целевой структуры (список, карточка, монетизация, качество, онбординг) реализован только список.

### Список приложений (`/applications`)

**Шапка:** заголовок "Applications", кнопка **ADD APPLICATION**, поле **"Search app"**.

**Таблица:**

| Колонка | Тип | Описание |
|---------|-----|----------|
| **App** | Текст | Название (human-readable) |
| **Bundle** | Текст | Bundle ID |
| **Store** | Текст | Google Play / Apple App Store |
| **Orientation** | Текст | Landscape / Portrait |
| **Ads** | ✓/✗ | Монетизация |
| **Coppa** | ✓/✗ | COPPA compliance |
| **Cross promo** | ✓/✗ | Кросс-промо |
| **Status app-ads.txt** | 🟢/🔴 | Валидность |
| **Admob Policy** | иконка | Статус политики |

~30 приложений, без пагинации.

### Чего нет

- **Карточка приложения** — нет per-app dashboard с метриками
- **Монетизация** — клиент не видит waterfall, сети, floor prices
- **Качество рекламы** — нет ad review, нет creative gallery
- **Онбординг** — нет чеклиста, нет прогресса интеграции, нет SDK status
- **Метрики рядом с приложениями** — revenue, impressions, DAU не видны (надо идти в Mediation)
- **Ссылки на стор**, batch-операции, фильтрация по статусу

### Известные проблемы

**app-ads.txt ложные тревоги.** Бот индексирует файл очень медленно или вообще не индексирует. Красный крест (🔴) появляется сразу после добавления приложения и висит неопределённо долго. У клиентов с 130+ приложениями все строки помечены красным. Эффект «волки-волки» — клиент перестаёт доверять статусам. Новые пользователи видят красный крест до того, как начали интеграцию, что вызывает отторжение.

**SDK race condition.** Клиенты начинают интеграцию SDK до того, как CAS зарегистрировал их приложение в системе. Результат: алерты, некорректный config-файл, ощущение что "что-то сломано". Пока процесс managed — это решается через саппорт, но при переходе на self-service нужен гейт (регистрация → подтверждение → доступ к SDK).

---

## III. Финансы

Текущая реализация: одна страница с длинной таблицей. Из 4 подблоков целевой структуры (обзор, история, действия, аналитика) реализована только история — и та без фильтров.

### Payments (`/mypayments`)

**Шапка:** "Payments info" + иконка **?**, справа **Current balance: $ 19,048.1**.

**Таблица (254 строки, с Jun 2024):**

| Колонка | Описание |
|---------|----------|
| **Period** | Месяц (`2026-Mar`) |
| **Accrual sum** | Начисления |
| **Commission** | Корректировки (обычно −) |
| **Payment date** | Дата выплаты |
| **Payment sum** | Сумма выплаты |
| **Current balance** | Баланс после операции |
| **Comment** | Описание транзакции |
| *(иконка)* | Скачать акт/инвойс |

**Типы транзакций:** fraud adjustments (GoogleAds, Facebook, DSP Exchange, AppLovin, IronSource, Unity, Pangle, Mintegral, Bigo, CASExchange), выплаты (PMNT), bank/crypto fees, crediting, balance adjustments, in-apps, compensations.

Выплаты: ежемесячно ~27-го числа, $5,000–$15,000, несколько траншей (wire + crypto).

### Чего нет

- **Обзор** — нет available vs pending, нет прогноза следующей выплаты
- **Фильтрация** — нет фильтра по периоду, типу, поиска
- **Действия** — нет «заказать выплату», нет настройки реквизитов из кабинета
- **Аналитика** — нет monthly summary, нет графика баланса, нет estimated vs finalized
- **Export** — нет CSV/PDF
- 254 строки в одном скролле без пагинации — fraud adjustments доминируют визуально

---

## IV. Аккаунт

Текущая реализация: dropdown-меню из шапки. Из 3 подблоков целевой структуры (профиль, команда, безопасность) реализован только минимальный профиль.

### Аккаунт-меню (dropdown)

| Пункт | Что делает |
|-------|------------|
| Personal data | Персональные данные |
| Payment details | Реквизиты для выплат |
| Authorize Admob | OAuth-привязка Google AdMob |
| Authorize DTExchange | OAuth-привязка Digital Turbine |
| Api documentation | Ссылка на API-документацию |
| Logout | Выход |

### Чего нет

- **Команда** — нет team management, 1 аккаунт = 1 логин, нет ролей
- **Безопасность** — нет 2FA, нет forgot password, нет audit log
- **API keys** — нет управления ключами в кабинете
- **Баланс/статус** — нет quick info о балансе или проблемах в аккаунт-меню

---

## V. Коммуникация

Текущая реализация: два hardcoded баннера внутри страницы Mediation. Нет notification center, нет email-алертов, нет upsell, нет маркетинга.

### Баннеры

**1. Инцидент Bigo Network (оранжевый фон)**
- "Dear partners! Due to technical limitations, we are temporarily unable to provide accurate statistics for the Bigo advertising network..."
- Не закрывается, нет таймстампа

**2. Проблема app-ads.txt (розово-красный фон)**
- "A problem with app-ads.txt has been detected..."
- Кликабелен → `/applications`. Не закрывается.

~120px высоты, сдвигают рабочую область.

### Чего нет

- **Notification center** — нет bell icon, нет списка уведомлений
- **Технические алерты** — revenue drop, SDK problems, network outage — не существуют
- **Email** — нет дайджестов, нет алертов на email
- **Upsell** — нет точек входа в publishing из кабинета
- **Маркетинг** — нет анонсов фич, SDK updates, best practices
- Баннеры привязаны к Mediation, а не к кабинету в целом
- Нет приоритизации: инцидент и action required визуально одинаковы

---

## Как работает конфигурация сейчас

Конфигурация монетизации (waterfall, bid floors, сети) не управляется через кабинет.

| Аспект | Текущее состояние |
|--------|-------------------|
| **Формат** | Один JSON-файл на клиента |
| **Кастомизация** | Ручная правка JSON для крупных клиентов (L2+). Для L1 — дефолтный JSON |
| **Канал саппорта** | Телеграм-чатики (не кабинет, не тикет-система) |
| **Credentials сетей** | У L1 — вшиты ключи CAS. У L2+ — свои, передаются вручную |

Для мелких паблишеров текущий процесс работает. Крупные клиенты ожидают профессиональный инструмент, а не переписку в мессенджере.

---

## Техническое приложение

### Скрытые разделы

- `/creatives` — отдаёт сырой JSON `{"allCreatives":[],"campaignCreatives":[]}`. Фронтенд отсутствует.
- Cross Promo Campaigns — убрана из навигации, URL не найден.
- Все нераспознанные пути → тихий редирект на `/mediation`. Нет 404.

### Мобильная версия (375×812)

| Элемент | Поведение |
|---------|-----------|
| Навигация | Иконка ≡ справа |
| KPI-карточки | 2 в ряд |
| Таблицы | Горизонтальный скролл |
| График | Масштабируется |

`user-scalable=no` — зум отключён.

### Тех. стек

| Параметр | Значение |
|----------|----------|
| Фреймворк | Предположительно Laravel Blade + vanilla JS |
| JS | Один бандл `app.js` |
| CSS | 11 файлов (не bundled) |
| Иконки | Material Design Icons + Fontastic |
| Title | `CleverAdsSolutions` — один на все страницы |

---

## Связанные документы

- Целевая структура кабинета: `03-product/cabinet/overview.md`
- Конкурентное исследование: `03-product/cabinet/competitive-research.md`
- UX-паттерны: `03-product/cabinet/ux-patterns.md`
- ТЗ для дизайнера (OneBI): `03-product/design-spec-bi.md`
- Сравнение с QuickView POC: `99-archive/03-product/current-vs-quickview.md`
