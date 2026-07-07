# ТЗ для дизайнера: Кабинет (platform.cas.ai) — рестайлинг

> Внутр. код-имя «b2b», хост platform.cas.ai (b2b.cas.ai — legacy). Ролевые АРМ → [am-cabinet.md](am-cabinet.md).

## Цель документа

Спецификация для дизайнера на рестайлинг кабинета CAS. 

## Контекст

### Что такое CAS

CAS.AI — платформа управления рекламной медиацией в мобильных приложениях.

### Кабинет — зачем он

Кабинет b2b.cas.ai — основной инструмент **онбординга, управления и коммуникации** между клиентом и CAS.

**Jobs To Be Done** — путь клиента через кабинет от знакомства до денег:

```
Регистрация → Добавление приложений → Интеграция SDK → Настройка → Мониторинг → Выплаты
     │                │                     │              │            │            │
  Profile        Applications          Applications   Applications  Analytics   Payments
```

| Job | Вопрос клиента | Где в кабинете |
|-----|---------------|----------------|
| **Зарегистрироваться** | "Как начать работу с CAS?" | Profile: создать аккаунт, заполнить данные, указать реквизиты |
| **Внести приложения** | "Как добавить свою игру?" | Applications: зарегистрировать приложение (iOS/Android отдельно), указать bundle ID, ссылку на стор |
| **Проинтегрировать SDK** | "Как подключить?" | Applications: документация, SDK keys, гайд по интеграции, статус подключения |
| **Настроить медиацию** | "Какие сети, какие ставки?" | Applications: credentials сетей (для L2+), waterfall-конфигурация (будущее self-service) |
| **Следить за перформансом** | "Сколько я зарабатываю и почему?" | Analytics: QuickView (быстрый взгляд) + Reports (глубокий анализ) |
| **Получать выплаты** | "Когда и сколько мне заплатят?" | Payments: баланс, история, реквизиты |
| **Быть в курсе** | "Что сломалось? Что нового?" | Коммуникация: нотификации, алерты, SDK updates |
| **Получить помощь** | "У кого спросить?" | Human Touch: персональный менеджер, техсаппорт, чат |

Соответственно, кабинет состоит из четырёх блоков, покрывающих эти jobs:

| Блок | Jobs | Описание |
|------|------|----------|
| **Analytics** | Мониторинг | QuickView + Reports — "сколько зарабатываю и почему" |
| **Applications** | Приложения, интеграция, настройка | Регистрация, SDK, credentials, статус |
| **Payments** | Выплаты | Баланс, история, реквизиты |
| **Profile** | Аккаунт | Личные данные, безопасность, API keys |

Плюс сквозные элементы: **коммуникация** (нотификации, алерты, документация) и **human touch** (контакты команды).

| Элемент | Что внутри |
|---------|-----------|
| **Коммуникация** | Технические нотификации (app-ads.txt, сбои сетей), маркетинговые (publishing, новости), SDK updates, **документация** (SDK docs, API docs, гайды по интеграции, changelog) |
| **Human Touch** | Фото персонального менеджера, прямые ссылки на Telegram/WhatsApp, техсаппорт |

### Кто пользуется

| Тип | Описание | Частота захода | Основной job |
|-----|----------|---------------|--------------|
| **L1** | Базовый клиент, 1-3 приложения | 1-2 раза в неделю | "Всё ли ОК? Будут ли деньги?" |
| **L2** | Продвинутый, 5-30 приложений, свои аккаунты в сетях | Ежедневно | Разбивки по сетям/странам, оптимизация |
| **Pub** | Publishing-партнёр | Ежедневно | Revenue + UA spend + ROAS |
| **Admin** (внутренний) | Менеджер CAS | Постоянно | Портфель клиентов, здоровье аккаунтов |

### Что сейчас не так

1. **Выглядит устаревшим.** Пустые пространства, нет интерактива — ощущение что продукт заброшен. Хочется зайти и почувствовать что здесь живут.
2. **Первый визит пугает.** Человек только зарегистрировался — а ему красная ошибка, прочерки, пустой график. Десять секунд — и он ушёл.
3. **Не чувствуется что за продуктом стоят люди.** У нас живые менеджеры, быстрый саппорт в Telegram — но кабинет об этом молчит. Как будто ты один на один с интерфейсом.
4. **Коммуникация не продумана.** От первого касания до любого другого — нагромождение алертов, которые скорее пугают, чем помогают. Нет ни новостей, ни документации, ни подсказок.
5. **Аналитика уже выглядит свежо.** OneBI — новый блок аналитики — уже имеет современный дизайн. Остальной кабинет должен подтянуться, чтобы не было ощущения вставного зуба.

### Конкуренты-ориентиры

| Конкурент | Что взять | Скриншоты |
|-----------|----------|-----------|
| **AppLovin MAX** | KPI-карточки с цветовой кодировкой и дельтами, Compare Mode toggle, Advanced Reporting, sidebar навигация | `05-research/competitors/max/` |
| **Appodeal** | Баланс в хедере, sidebar с иконками, Payouts как отдельный блок | Скриншот в `assets/` |
| **Unity LevelPlay** | Real-Time Pivot, Ad Quality | `05-research/levelplay-console-research.md` |

---

## Принципы дизайна

1. **Desktop first.** 90%+ трафика — десктоп. Мобильная версия — адаптивная, без отдельного проектирования
2. **Тёмная + светлая тема.** Тёмная по умолчанию (запрос пользователей). Светлая как переключатель
3. **Цвета CAS.** Основные акценты: синий (#58A6FF), белый (#F0F6FC). Для метрик — уникальный цвет на каждую (не red/green для up/down — 8% мужчин дальтоники)
4. **Chip-based UI.** Фильтры, splits — компактные теги, не громоздкие формы
5. **Живой интерфейс.** Заполнять пространство полезным контентом: подсказки, новости, контакты, prediction. Не оставлять белых пятен
6. **Human touch.** Фотографии людей, прямые ссылки на чат, приветствия по имени. CAS — не безликая платформа
7. **Progressive disclosure.** L1 видит простое, L2 — может раскрыть сложное. Один интерфейс, разная глубина

---

## Глобальные элементы

### Layout: Sidebar + Header + Content

```
┌──────┬───────────────────────────────────────────────────────┐
│      │  [CAS.AI logo]          [$12,450]  [🔔3]  [👤 Oleg ▾] │
│      ├───────────────────────────────────────────────────────┤
│ SIDE │                                                       │
│ BAR  │                                                       │
│      │                    Content Area                       │
│      │                                                       │
│      │                                                       │
│      │                                                       │
│      ├───────────────────────────────────────────────────────┤
│      │  © 2026 CAS.AI  Terms  Privacy  Support  API Docs     │
└──────┴───────────────────────────────────────────────────────┘
```

### Sidebar (левая панель, основная навигация)

Collapsible sidebar — как у AppLovin MAX, Appodeal. Иконки + текст, при сворачивании — только иконки.

```
┌──────────────────────┐
│  📊 Analytics        │   ← default, QuickView + Reports
│  📱 Applications     │
│  💰 Payments         │
│  👤 Profile          │
├──────────────────────┤
│                      │
│  Your CAS Team       │
│  [📷] Serhii         │
│  Personal Manager    │
│  [💬] [📱]           │
│                      │
│  Need help? 🟢       │
├──────────────────────┤
│  📖 API Docs         │
│  📦 Resources        │
└──────────────────────┘
```

| Элемент | Поведение | Примечания |
|---------|-----------|------------|
| **Навигация** | 4 пункта: Analytics, Applications, Payments, Profile | Активный — акцентный цвет + indicator |
| **Sub-navigation** | Разворачивается при клике: Analytics → QuickView / Reports | Indent + мелкий шрифт |
| **Human Touch блок** | Фото менеджера + имя + ссылки Telegram/WhatsApp | Внизу sidebar, всегда видно. Данные из 1С |
| **Resources** | API Docs, SDK Docs, Blog, Changelog | Ссылки в нижней части sidebar |
| **Collapse** | Кнопка «‹» → sidebar сворачивается до иконок (~48px) | Состояние сохраняется в localStorage |

**Human Touch блок (в sidebar):**
- Фото реальных людей (не аватарки)
- Прямые ссылки на WhatsApp/Telegram (deeplinks)
- Статус online/offline (если реализуемо)
- Данные подтягиваются из 1С по привязке клиент → менеджер
- При свёрнутом sidebar — только иконка чата

### Header (фиксированный, облегчённый)

Навигации в header нет — она в sidebar. Header = информация + действия.

```
┌───────────────────────────────────────────────────────────────────┐
│  [CAS.AI logo]                      [$12,450]  [🔔 3]  [👤 Oleg ▾] │
└───────────────────────────────────────────────────────────────────┘
```

| Элемент | Поведение | Примечания |
|---------|-----------|------------|
| **Logo** | Клик → QuickView (home) | Лого CAS, слева |
| **Баланс** | `$12,450.20` — текущий доступный баланс | Всегда виден. Клик → Payments. Зелёный если >0, серый если 0 |
| **Notifications** | Bell icon + badge с количеством непрочитанных | Клик → dropdown (см. ниже) |
| **Профиль** | Аватар + имя + dropdown | Клик → быстрые действия |

**Notifications dropdown:**

```
┌─────────────────────────────────────────┐
│ Notifications                Dismiss All │
├─────────────────────────────────────────┤
│ 🔴 app-ads.txt not verified (2 apps)    │
│    3 hours ago                          │
├─────────────────────────────────────────┤
│ 🟢 SDK 4.6.0 available — changelog →   │
│    Yesterday                            │
├─────────────────────────────────────────┤
│ 💰 Payment $5,200 processed            │
│    Mar 27                               │
├─────────────────────────────────────────┤
│ View all →                              │
└─────────────────────────────────────────┘
```

- Три типа: технические (🔴), информационные (🟢), финансовые (💰)
- Приоритизация: критические сверху
- Каждая нотификация — кликабельна (ведёт на релевантный экран)
- "Dismiss All" и dismiss per item (×)

**Profile dropdown:**

```
┌──────────────────────────┐
│ 👤 Oleg Shlyamovych      │
│    oleg@psvgames.com     │
├──────────────────────────┤
│ 🌙 Dark Mode      [ON]  │
├──────────────────────────┤
│ → Log out                │
└──────────────────────────┘
```

Минимальный — Personal Data, Payment Details и прочее доступно через Profile в sidebar. Dropdown только для dark mode toggle и logout.

### Footer

```
┌──────────────────────────────────────────────────────────────────┐
│ © 2026 CAS.AI    Terms    Privacy    Support    API Docs    v2.1 │
└──────────────────────────────────────────────────────────────────┘
```

Минимальный, не липкий. Дублирует ссылки из sidebar для удобства.

---

## Блок: Profile

### Назначение

Настройки аккаунта клиента: личные данные, реквизиты для выплат, безопасность. Всё, что связано с "кто я" и "как мне платить".

**Не входит сюда:** приложения (→ Applications), аналитика (→ Analytics), история платежей (→ Payments).

### Точка входа

Profile dropdown в хедере → клик на "Personal Data" или имя/аватар.

### Навигация внутри блока

Табы или sidebar-меню:

```
Profile
├── Personal Data        ← данные пользователя
├── Payment Details      ← реквизиты для выплат
├── Security             ← пароль, 2FA
└── API Keys             ← ключи для интеграции
```

---

### Экран: Personal Data

**URL:** `/profile` или `/profile/personal`

**Назначение:** просмотр и редактирование персональных данных клиента.

#### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Personal Data                                    [✏ Edit]   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐   First Name:     Oleg                      │
│  │            │   Last Name:      Shlyamovych                │
│  │   [Photo]  │   Email:          oleg@psvgames.com  [✓]    │
│  │            │   Company:        PSV Game Studio            │
│  └────────────┘   Phone:          +380999990010              │
│                   Country:        Ukraine                    │
│                   Preferred       Telegram                   │
│                   messenger:                                 │
│                                                              │
│  Timezone:        UTC+2 (Kyiv)                               │
│  Language:        English                                    │
│  Registered:      Jun 12, 2024                               │
│  Account ID:      PSV-00412                                  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ⚠ Email not verified. [Resend verification →]               │
└──────────────────────────────────────────────────────────────┘
```

#### Поля

| Поле | Тип | Обязательное | Редактируемое | Примечания |
|------|-----|-------------|---------------|------------|
| **Photo** | Image upload | Нет | Да | Круглый аватар 80×80. Fallback: инициалы на цветном фоне |
| **First Name** | Text input | Да | Да | Max 50 chars |
| **Last Name** | Text input | Да | Да | Max 50 chars |
| **Email** | Email input | Да | Да (с подтверждением) | Значок ✓ если verified, ⚠ если нет |
| **Company** | Text input | Нет | Да | |
| **Phone** | Phone input | Нет | Да | С маской по стране |
| **Country** | Dropdown | Да | Да | Список стран |
| **Preferred Messenger** | Radio/Dropdown | Нет | Да | Telegram / WhatsApp / Email |
| **Timezone** | Dropdown | Да | Да | Влияет на отображение дат в аналитике |
| **Language** | Dropdown | Да | Да | English (пока единственный) |
| **Registered** | Text | — | Нет | Read-only |
| **Account ID** | Text | — | Нет | Read-only, copyable |

#### Поведение

| Действие | Результат |
|----------|-----------|
| Клик "Edit" | Поля становятся редактируемыми, появляются кнопки Save / Cancel |
| Save | Валидация → сохранение → toast "Changes saved" |
| Смена email | Отправляется verification link на новый email. Старый работает до подтверждения |
| Upload photo | Crop-modal (круг), max 5MB, jpg/png |

#### Состояния

| Состояние | Отображение |
|-----------|-------------|
| **View mode** | Все поля read-only, кнопка Edit |
| **Edit mode** | Поля активны, кнопки Save / Cancel |
| **Saving** | Кнопка Save → spinner, поля disabled |
| **Validation error** | Красная рамка на поле + текст ошибки под полем |
| **Success** | Toast "Changes saved" (зелёный, 3 сек, auto-dismiss) |

---

### Экран: Payment Details

**URL:** `/profile/payment-details`

**Назначение:** реквизиты для получения выплат. Клиент указывает, куда CAS должен перечислять деньги.

#### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Payment Details                                  [✏ Edit]   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Payment Method                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐         │
│  │  🏦 Bank Transfer    │  │  ₿ Crypto (USDT)     │         │
│  │  ● Active            │  │  ○ Available          │         │
│  └──────────────────────┘  └──────────────────────┘         │
│                                                              │
│  Bank Details                                                │
│  ─────────────────────────────────────                       │
│  Beneficiary:     PSV Game Studio LLC                        │
│  IBAN:            UA21 3223 1300 0002 6007 2335 6600 1       │
│  SWIFT/BIC:       UNJSUAUKXXX                                │
│  Bank:            Monobank (Universal Bank)                  │
│  Bank Address:    Kyiv, Ukraine                              │
│                                                              │
│  Payment Threshold                                           │
│  ─────────────────────────────────────                       │
│  Minimum payout:  $500                                       │
│  Current balance: $12,450.20                                 │
│  Next payout:     ~Apr 27, 2026                              │
│                                                              │
│  Tax Information                                             │
│  ─────────────────────────────────────                       │
│  Tax ID:          UA123456789                                │
│  W-8BEN:          ✓ Uploaded (expires Dec 2027)              │
│  [Upload new document]                                       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ℹ Changes to payment details require verification and take  │
│    up to 3 business days to process.                         │
└──────────────────────────────────────────────────────────────┘
```

#### Поля

| Поле | Тип | Примечания |
|------|-----|------------|
| **Payment Method** | Card selector | Bank Transfer / Crypto (USDT). Визуально — карточки с radio |
| **Beneficiary** | Text | Юрлицо или ФЛП |
| **IBAN** | Text | Маска, валидация формата |
| **SWIFT/BIC** | Text | 8 или 11 символов |
| **Bank** | Text | Auto-fill по SWIFT если возможно |
| **Bank Address** | Text | |
| **Crypto Wallet** | Text | Показывается если выбран Crypto. USDT (TRC-20/ERC-20) |
| **Payment Threshold** | Dropdown | $100 / $500 / $1000 / $5000. Default: $500 |
| **Tax ID** | Text | ИНН / VAT number |
| **Tax Documents** | File upload | W-8BEN, W-9, invoice template. Статус: ✓ / ⚠ expired / — not uploaded |

#### Состояния

| Состояние | Отображение |
|-----------|-------------|
| **Заполнено** | Все данные видны, кнопка Edit |
| **Не заполнено** | Wizard-подобный flow: "Set up your payment details to receive payouts" с пошаговой формой |
| **Ожидает верификации** | Жёлтый badge "Pending verification" + info text |
| **Документ истекает** | Жёлтый warning: "Your W-8BEN expires in 30 days" |
| **Документ истёк** | Красный alert: "Tax document expired — payouts paused until updated" |

---

### Экран: Security

**URL:** `/profile/security`

**Назначение:** управление паролем и двухфакторной аутентификацией.

#### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Security                                                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Password                                                    │
│  ─────────────────────────────────────                       │
│  Last changed:    14 days ago                                │
│  [Change Password]                                           │
│                                                              │
│  Two-Factor Authentication                                   │
│  ─────────────────────────────────────                       │
│  Status:          ⚠ Not enabled                              │
│  [Enable 2FA]                                                │
│                                                              │
│  ℹ We recommend enabling 2FA for all accounts with access    │
│    to payment settings.                                      │
│                                                              │
│  Active Sessions                                             │
│  ─────────────────────────────────────                       │
│  🖥 Chrome · Kyiv, UA · Current session                      │
│  📱 Safari · Kyiv, UA · 2 days ago              [Revoke]     │
│                                                              │
│  [Sign out of all other sessions]                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### Компоненты

**Change Password (modal или inline expand):**

| Поле | Тип | Валидация |
|------|-----|-----------|
| Current Password | Password input | Required |
| New Password | Password input | Min 8 chars, letters + numbers |
| Confirm Password | Password input | Должен совпадать |

Кнопки: Save / Cancel. Success → toast + "Last changed: just now".

**Enable 2FA (step-by-step flow):**

1. Показать QR-код для authenticator app (Google Authenticator / Authy)
2. Ввести 6-digit код для подтверждения
3. Показать backup codes (10 шт.) + кнопка Download / Copy
4. "2FA enabled ✓"

**Состояния 2FA:**

| Состояние | Отображение |
|-----------|-------------|
| Не включена | ⚠ жёлтый badge + рекомендация включить |
| Включена | ✓ зелёный badge + "Connected with authenticator app" |
| Backup codes | Ссылка "View/reset backup codes" (требует ввод текущего кода) |

**Active Sessions:**

| Поле | Описание |
|------|----------|
| Device/Browser | Chrome, Safari, Firefox + иконка |
| Location | City, Country (по IP) |
| Last active | Relative time |
| Current | Badge "Current session" |
| Revoke | Кнопка (не для текущей сессии) |

---

### Экран: API Keys

**URL:** `/profile/api-keys`

**Назначение:** ключи для программного доступа к данным CAS (Reporting API, SDK).

#### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  API Keys                                                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Reporting API Key                                           │
│  ─────────────────────────────────────                       │
│  xxxxxxxx-xxxx-xxxx-xxxx-xxxx····xxxx        [👁] [📋 Copy] │
│  Created: Jan 15, 2026                                       │
│  [Regenerate]                                                │
│                                                              │
│  SDK Key                                                     │
│  ─────────────────────────────────────                       │
│  cas_sdk_xxxxxxxxxxxx····xxxx                [👁] [📋 Copy] │
│  Created: Jun 12, 2024                                       │
│                                                              │
│  ℹ SDK Key is read-only and tied to your account.            │
│    Reporting API Key can be regenerated — old key will stop  │
│    working immediately.                                      │
│                                                              │
│  📖 API Documentation →                                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### Поведение

| Действие | Результат |
|----------|-----------|
| 👁 (eye icon) | Toggle: показать/скрыть полный ключ |
| 📋 Copy | Копировать в clipboard → toast "Copied!" |
| Regenerate | Confirmation modal: "Are you sure? Old key will stop working immediately." → [Regenerate] / [Cancel] |
| API Documentation → | Открывает docs в новой вкладке |

#### Состояния

| Состояние | Отображение |
|-----------|-------------|
| Ключи есть | Masked keys с кнопками show/copy |
| Нет ключей | "No API key generated yet. [Generate Key]" |
| Regenerated | Toast "New key generated" + старый ключ недействителен |

---

### Состояния блока Profile (общие)

#### Empty State (новый пользователь)

Если профиль не заполнен (только email из регистрации):

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  👋 Welcome to CAS!                                          │
│                                                              │
│  Complete your profile to get started:                       │
│                                                              │
│  [1] ✓ Create account                                        │
│  [2] → Fill in your details              [Complete now →]    │
│  [3] ○ Set up payment details                                │
│  [4] ○ Add your first app                                    │
│                                                              │
│  Your personal manager:                                      │
│  [📷] Serhii Shcherbyna                                     │
│  [💬 Chat on Telegram]                                       │
│                                                              │
│  "Hi! I'm here to help you get started.                      │
│   Feel free to reach out anytime."                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- Checklist-стиль (1-2-3-4)
- Прогресс: выполненные шаги — ✓, текущий — →, будущие — ○
- Human touch: фото менеджера + цитата + прямая ссылка на чат
- Этот checklist может показываться и на QuickView для новых пользователей

#### Loading

Skeleton placeholders: серые прямоугольники вместо текстовых полей, анимация pulse.

#### Error

```
Something went wrong loading your profile.
[Try again]
```

Не красная ошибка (помним отторжение) — нейтральный стиль с retry.

---

## Следующие блоки (TODO)

- **Analytics** — QuickView + Reports (см. также `design-spec-bi.md`)
- **Applications** — список, карточка, OAuth/credentials
- **Payments** — баланс, история, выплаты
- **Сквозные элементы** — онбординг тур, коммуникационная зона, нотификации

---

## Связанные документы

| Документ | Назначение |
|----------|-----------|
| `cabinet/overview.md` | Концепция кабинета + фаза 1 рестайлинга |
| `cabinet/current-state.md` | Текущее состояние (as-is) со скриншотами |
| `cabinet/competitive-research.md` | Обзор конкурентов |
| `cabinet/ux-patterns.md` | UX-паттерны и best practices |
| `design-spec-bi.md` | ТЗ на Analytics (QuickView + Reports) — детальное |
| `05-research/competitors/max/analysis.md` | Разбор AppLovin MAX по скриншотам |
| `05-research/cabinet-tz-shcherbyna.md` | Фидбэк Serhii Shcherbyna |
