# Legacy b2b-кабинет — FE-спецификация (архивный референс)

> Источник: wiki OneBI, page 289 (2026-04-03). Детальнее `current-state.md`.
> **Статус:** фиксация legacy b2b as-is (для рефакторинга). b2b.cas.ai — legacy на период перехода.
> Целевое состояние — на platform.cas.ai (см. `overview.md`, `../../01-platform/product-architecture.md`).
> Сюда перенесена суть `03-product/current-ui-audit.md` (заархивирован).

---

## 1. Header (шапка)

### Навигационные ссылки:

| Ссылка | URL | Условие отображения |
|----|----|----|
| Mediation | `/mediation` | Только для owner (`isOwner`) |
| Publishing | `/publishing` | owner **И** `havePublishing` |
| Payments | `/mypayments` | Только для owner |
| Applications | `/applications` | Всегда (для всех ролей) |
| Creatives | `/creative` | Только для пользователей `hasCreatives` |
| Cross Promo Campaigns | `/crosspromocampaigns` | Только для пользователей `hasCreatives` |

## 2. User Account Dropdown

### Пункты меню:

| \# | Пункт | Иконка | Действие |
|----|----|----|----|
| 1 | Personal data | `personalData` | Открыть модал `TheModalPersonalData` |
| 2 | Payment details | `payment` | Открыть модал `TheModalPaymentDetails` |
| 3 | Authorize Admob | `iconAuthorizeAdmob` | Редирект: `document.location.href = "/settings/oauth2callback"` |
| 4 | Authorize DTExchange | `iconAuthorizeAdmob` | Открыть модал `TheModalDTExchangeData` |
| 5 | Api documentation | `iconApi` | Открыть в новой вкладке: GitHub CAS-API-Documentation |

------------------------------------------------------------------------

### 2.1 Personal Data

#### Поля формы:

| \#  | Поле        | Тип            | Label         | Обязательное | Валидация |
|-----|-------------|----------------|---------------|--------------|-----------|
| 1   | FirstName   | `v-text-field` | First Name    | required     | —         |
| 2   | LastName    | `v-text-field` | Last Name     | required     | —         |
| 3   | CompanyName | `v-text-field` | Company Name  | required     | —         |
| 4   | Email       | `v-text-field` | Contact email | —            | —         |

**Закомментированные поля (не отображаются):** Phone, ZIP code, Country,
City, Address.

------------------------------------------------------------------------

### 2.2 Payment Details

#### Блокировка:

Если `paymentDetailsLocked === true` (приходит из `getAccountInfo`): -
Показывается `v-alert` warning: *"Changes to payment details are
blocked. Contact your manager."*

#### Защита от изменения перед выплатой:

При сохранении проверяется `getNextPaymentDay()`. Если до выплаты \< 3
дней, показывается warning и сохранение блокируется.

#### Выбор типа оплаты:

- Если тип не выбран: два варианта кнопками — **Payoneer** / **Wire
  Transfer**
- Если тип выбран: отображается текущий тип + кнопка "change"

------------------------------------------------------------------------

#### Поля при `paymentType === 'Payoneer'`:

| \# | Поле | Тип | Label | Валидация |
|----|----|----|----|----|
| 1 | payoneerAccount | `v-text-field` | Payoneer account | — |
| 2 | AccountHoldersName | `v-text-field` | Account Holder Name | Latin characters only, no symbols |
| 3 | UserAddress | `v-text-field` | Address specified when opening a bank account | Формат адреса, max 255 символов |
| 4 | BankCurrency | `v-form-select` | Bank Currency | Выбор из: `$ USD`, `€ EUR` |

------------------------------------------------------------------------

#### Поля при `paymentType === 'Wire Transfer'`:

| \# | Поле | Тип | Label | Валидация | Условие |
|----|----|----|----|----|----|
| 1 | accountType | `v-radio-group` | Bank account type | — | Варианты: Business / Personal |
| 2 | BankCountry | `v-form-select` | Bank Country | — | Список стран (без Country_Id=51) |
| 3 | BankName | `v-text-field` | Bank Name | Не поддерживаются: Neteller, Paysera, Paytm Payments Bank, Wirecard | — |
| 4 | AccountHoldersName | `v-text-field` | Account Holder Name | Latin characters only, no symbols | — |
| 5 | SWIFT | `v-text-field` | SWIFT/BIC | Regex: `^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$` | — |
| 6 | IBAN | `v-text-field` | IBAN **или** Account Number | Label меняется: если BankCountry = USA (70) -\> "Account Number", иначе "IBAN" | — |
| 7 | VAT | `v-text-field` | VAT number | — | — |
| 8 | BankCurrency | `v-form-select` | Bank Currency | — | Выбор из: `$ USD`, `€ EUR` |
| 9 | UserAddress | `v-text-field` | Address specified when opening a bank account | Формат адреса, max 255 | — |
| 10 | UserCity | `v-text-field` | City/Town | — | — |
| 11 | UserZip | `v-text-field` | Postal/ZIP | — | — |
| 12 | UserCountry | `v-form-select` | Company registration country | — | Список стран (без Country_Id=51) |

##### Дополнительные поля при BankCountry = USA (Country_Id = 70):

| \# | Поле | Тип | Label | Валидация |
|----|----|----|----|----|
| 13 | ABANumber | `v-text-field` | ABA Routing Number | — |
| 14 | ACHNumber | `v-text-field` | ACH Routing Number | — |
| 15 | USAAccountType | `v-radio-group` | Account Type | required; варианты: Saving / Checking |

------------------------------------------------------------------------

### 2.3 Authorize Admob

Не модал. Прямой редирект:

```
document.location.href = "/settings/oauth2callback"
```

Серверная OAuth2-авторизация через Google.

------------------------------------------------------------------------

### 2.4 Authorize DTExchange

#### Поля формы:

| \#  | Поле         | Тип            | Label         | Обязательное |
|-----|--------------|----------------|---------------|--------------|
| 1   | accountId    | `v-text-field` | CLIENT_ID     | required     |
| 2   | accountToken | `v-text-field` | CLIENT_SECRET | required     |

------------------------------------------------------------------------

### 2.5 Api Documentation

Не модал. Открытие внешней ссылки в новой вкладке:

```
window.open('https://github.com/cleveradssolutions/CAS-API-Documentation', '_blank')
```

------------------------------------------------------------------------

## 3. Страница /payments

### Элементы страницы:

1.  **Заголовок:** `ThePageHeader` — title "Payments info", кнопка "?"
    открывает PDF: `/Instructions for Receiving Payments.pdf`
2.  **Баланс:** `Current balance: $ XX.XX` — отображается если список
    платежей не пуст; значение из первого элемента массива
    `paymentsList[0].currentBalance`
3.  **Уведомление о блокировке:** `TheBlockingPaymentDataNotification`
    (с `show-locked-notification="true"`)
4.  Если `paymentDetailsLocked` — постоянное предупреждение: *"Changes
    to payment details are blocked..."*
5.  Если до выплаты \<= 7 дней и \> 3 дней — предупреждение: *"Payday is
    \[date\]. Therefore, check your payment details..."*
6.  Dismissable (кроме locked), скрывается до конца дня
7.  **Уведомления:** `NotificationManager`
8.  **Таблица:** `PrimeTable`

------------------------------------------------------------------------

### 3.1 Таблица Payments

**Компонент:** `PrimeTable.vue` с `tableSource="payments"` **DataKey:**
`Payment_ID` **Поиск:** Отключен **Пагинация:** Если \> 10 строк,
пагинатор (10/25/50 строк на страницу) **Сортировка:** Multi-sort,
removable sort **Выделение строки:** Не используется (нет
`selectPrimeTableRow`)

#### Колонки:

| \# | field | Header | Sortable | Frozen | Width | Рендеринг ячейки |
|----|----|----|----|----|----|----|
| 1 | `period` | Period | да | **да** | 130px min | Текст, выровнен по левому краю |
| 2 | `accrual_sum_plus` | Accrual sum | да | нет | 140px | Число с символом валюты, `formatData()`, выровнено по правому краю |
| 3 | `accrual_sum_minus` | Commission | да | нет | 140px | Число с символом валюты, `formatData()`, выровнено по правому краю |
| 4 | `payment_date_by` | Payment date | да | нет | 170px | Текст, **отображается только если `comment` пуст** (пустая строка) |
| 5 | `payment_sum` | Payment sum | да | нет | 170px | Число с символом валюты, `formatData()`, выровнено по правому краю |
| 6 | `currentBalance` | Current balance | да | нет | 185px | Число с символом валюты, `formatData()`, выровнено по правому краю |
| 7 | `comment` | Comment | **нет** | нет | 35% | Текст, `formatData()`, выровнен по левому краю |
| 8 | `paymentTableActions` | *(пусто)* | **нет** | **да** | 75px | Иконки действий (см. ниже) |

#### Колонка Actions (`paymentTableActions`) — условный рендеринг:

Отображается **одна из двух** иконок в зависимости от данных строки:

| Условие | Иконка | Действие | Дополнительное условие |
|----|----|----|----|
| `accrual_sum_plus` **или** `accrual_sum_minus` не пусты | `receiptGrey` (квитанция) | Открыть модал Payment Content | Не отображается если `comment === "Transfer balance to dollar"` |
| `payment_sum > 0` | `invoice` (инвойс) | Скачать PDF-инвойс | Только если `CreateInvoice === true` |

**Скачивание инвойса:**
`GET /mypayments/invoice?paymentId=X&currency=USD` -\> blob -\>
автоматическое скачивание файла `invoice.pdf`

------------------------------------------------------------------------

### 3.2 Модал Payment Content

#### Заголовок модала:

- **Payment Num**: `paymentId`
- **Payment Summ**: `$ XX.XX` (с символом валюты, 2 десятичных знака)

#### Таблица содержимого платежа (Vuetify `v-data-table`):

| \# | field | Header | Sortable | Рендеринг ячейки |
|----|----|----|----|----|
| 1 | `Bundle_ID` | Bundle Id | да | `Bundle_ID (AppName)` — AppName в скобках если есть |
| 2 | `Name` | Accrual Name | да | Текст |
| 3 | `Amount` | Accrual Summ | да | `$ XX.XX` — только если `Amount != 0` |
| 4 | `Income` | *(colspan с Amount)* | да | `$ XX.XX` — только если `Income != 0` |

> Колонки 3 и 4 объединены в заголовке под общий "Accrual Summ" через
> colspan=2.

------------------------------------------------------------------------

## 4. Страница /applications

### Элементы страницы:

1.  **Заголовок:** `ThePageHeader` — title "Applications", кнопка "+" с
    текстом "Add Application"
2.  **Уведомление о блокировке:** `TheBlockingPaymentDataNotification`
    (без `show-locked-notification`)
3.  **Уведомления:** `NotificationManager`
4.  **Таблица:** `PrimeTable` с поиском
5.  **Модал:** `TheModalAddApplication` (условное отображение)

------------------------------------------------------------------------

### 4.1 Таблица Applications

**Компонент:** `PrimeTable.vue` с `tableSource="applications"`
**DataKey:** `App_ID` **Поиск:** Включен, label "Search app", поиск по
полям: `['Name', 'Bundle_ID']` **Пагинация:** Если \> 10 строк
**Сортировка:** Multi-sort **Выделение строки:** Да — клик по строке
открывает модал редактирования

#### Колонки:

| \# | field | Header | Sortable | Frozen | Width | Рендеринг ячейки |
|----|----|----|----|----|----|----|
| 1 | `Name` | App | да | **да** | 300px min/max | Текст — имя приложения |
| 2 | `Bundle_ID` | Bundle | да | **да** | 300px min/max | Текст — bundle ID |
| 3 | `StoreName` | Store | да | нет | 175px | Текст — название стора (capitalizeFirstLetter) |
| 4 | `Orientation` | Orientation | да | нет | 150px | Текст с маппингом: `portrait` -\> "Portrait", `landscape` -\> "Landscape", `both-portrait` -\> "Both (Portrait preferable)", `both-landscape` -\> "Both (Landscape preferable)" |
| 5 | `AdsGroup` | Ads | **нет** | нет | 122px | **Компонент `TheAdsGroup`** — 6 иконок рекламных форматов (active/inactive): Interstitial, Banner, Rewarded, AppOpen, MREC, Native. Каждая иконка отображается активной если соответствующий флаг `=== 1` |
| 6 | `Coppa` | Coppa | **нет** | нет | 105px min | Иконка галочки (`tableCheck`) если значение `=== 1`, иначе пусто |
| 7 | `UseCrossPromo` | Cross promo | **нет** | нет | 110px | Иконка галочки если `=== 1`, иначе пусто |
| 8 | `AppAds` | Status app-ads.txt | **нет** | нет | 112px | Иконка: `appadsSuccess` (зеленая) если `== 0`, `appadsFailure` (красная) если != 0. Клик -\> внешняя ссылка на GitHub app-ads.txt |
| 9 | `AdmobPolicy` | Admob Policy | **нет** | нет | 100px | Список кнопок с иконкой `adsClick` для каждого policy-элемента. Клик -\> модал Admob Policy. Отображается только если `!= null` |
| 10 | `appTableActions` | *(пусто)* | **нет** | нет | 30px min | Кнопка "..." (три точки) -\> dropdown контекстного меню |

------------------------------------------------------------------------

### 4.2 Модал Add/Edit Application

**Триггер открытия:** Кнопка "Add Application" в заголовке (режим
создания) **или** клик по строке таблицы (режим редактирования)

Форма реализована как **stepper из 2 шагов**.

#### Step 1 — App Settings:

| \# | Поле | Тип | Описание | Значения / Валидация |
|----|----|----|----|----|
| 1 | Store_ID | `v-radio-group` | Choose an app store | **Apple App Store** (2), **Google Play Market** (1) |
| 2 | Name | `v-text-field` | Custom app name | Произвольный текст |
| 3 | Bundle_ID | `v-text-field` | Connect your live app (Search by App name / Store ID) | **Обязательное**, readonly при редактировании, иконка поиска |
| 4 | iOS_PackageId | `v-text-field` | iOS Bundle Id | **Только при Store_ID = 2** (Apple). Обязательное |
| 5 | Published | `v-radio-group` | App publication | **App is live in the App store** (1), **App is not live yet** (0) |
| 6 | Coppa | `v-checkbox` | COPPA compliance | Checkbox: *"This app is directed to children under 13..."* |

**Текст под COPPA:** *"In accordance with the Children's Online Privacy
Protection Act we require all products that use CAS ads to identify
whether or not they are directed at children under the age of 13 in the
United States."*

**Кнопки Step 1:**

| Кнопка | Действие                                         |
|--------|--------------------------------------------------|
| Close  | Закрыть модал                                    |
| Next   | Перейти к Step 2 (disabled если форма невалидна) |
| Save   | Сохранить (без перехода на Step 2)               |

#### Step 2 — Ads Settings:

| \# | Поле | Тип | Описание | Значения |
|----|----|----|----|----|
| 1 | Orientation | `v-radio-group` | App orientation | **Portrait**, **Landscape**, **Both (Portrait preferable)**, **Both (Landscape preferable)** |
| 2 | UseCrossPromo | `v-checkbox` | Cross Promo Ads | *"Use this app in Cross Promo Campaigns"* |
| 3 | — | `v-btn` text | Placement setting | Открывает вложенный модал Ads Settings |

**Кнопки Step 2:**

| Кнопка | Действие             |
|--------|----------------------|
| Close  | Закрыть модал        |
| Back   | Вернуться к Step 1   |
| Save   | Сохранить приложение |

#### Режим редактирования:

- Все поля pre-populated из `selectedApplication` в store
- `Bundle_ID` — readonly
- `isEdit = true` -\> в запрос передается `isModify: true` и `app_Id`

------------------------------------------------------------------------

### 4.3 Модал Placement Settings

#### Рекламные форматы (6 штук, по 3 в ряд):

| \# | Поле | Label | Описание |
|----|----|----|----|
| 1 | IsInterstitial | Interstitial | Full-page ad at natural breaks and transitions |
| 2 | IsRewarded | Rewarded | Rewards users for watching ads |
| 3 | IsBanner | Banner | Rectangular ads, can auto-refresh |
| 4 | IsAppOpen | App open | Monetize app load screens |
| 5 | IsMREC | MREC | Medium Rectangle 300x250 ads |
| 6 | IsNative | Native | Ads presented through native UI components |

Каждый формат: - `v-checkbox` (toggle 0/1) - Иконка (active / nonactive
— разные картинки) - Текстовое описание формата

------------------------------------------------------------------------

### 4.4 Dropdown действий строки таблицы

**Триггер:** Клик на кнопку "..." в колонке `appTableActions`.

#### Пункты меню:

| \# | Пункт | Действие |
|----|----|----|
| 1 | Download CAS settings | `POST /apps/settings` -\> скачать JSON-файл с настройками |
| 2 | Show Admob App ID | Открыть модал `TheModalAdmobAppID` — показывает Admob App ID |

------------------------------------------------------------------------
