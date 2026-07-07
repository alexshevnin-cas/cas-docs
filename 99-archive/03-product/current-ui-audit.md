# Текущий интерфейс b2b.cas.ai 

---

## 1. Верхняя навигация (горизонтальное меню)

| Пункт | URL | Статус |
|-------|-----|--------|
| **Mediation** | `/mediation` | Основной дашборд, работает |
| **Publishing** | `/publishing` | Заглушка |
| **Payments** | `/payments` | Заглушка |
| **Applications** | `/apps` | Заглушка |
| **Creatives** | `/creatives` | Заглушка |
| **Cross Promo Campaigns** | — | Заглушка |
| **$ USD** | — | Переключатель валюты (dropdown) |
| **Khadiev Publishing** | — | Аккаунт-меню (справа) |

---

## 2. Страница Mediation — структура

### 2.1 Заголовок

- **"Performance reporting"** + кнопка **DOWNLOAD REPORT**

### 2.2 KPI-карточки (3 шт.)

Верхний ряд метрик-сводки за выбранный период:

| Карточка | Пример значения |
|----------|----------------|
| **Est. Revenue** | $ 12,599.710 |
| **Impressions** | 16,240,265 |
| **eCPM** | $ 0.776 |

Плюс блок **Presets** (справа, "No presets found" — функционал сохранённых пресетов).

### 2.3 Панель управления графиком / таблицей

**Период:**
- `LAST ACTUAL DAY` | `7 DAYS` | `30 DAYS` | `CUSTOM`
- CUSTOM открывает Litepicker-календарь для произвольного диапазона

**Show graph:** чекбокс — вкл/выкл линейный график

**View by:** dropdown (группировка строк таблицы)
- `Total` (по умолчанию)
- `Application`
- `Country`
- `Network`

**Compared to:** dropdown (сравнение периодов)
- `None` (по умолчанию)
- `Last week to prior week`
- `Last weekend to prior weekend`
- `Custom date range`

**Table Columns:** dropdown с чекбоксами — управление колонками таблицы:
- `Application` (вкл. по умолчанию)
- `Date`
- `Week`
- `Month`
- `Network`
- `Model`
- `Platform`
- `Country`
- `DAU`
- `ARPDAU`

**Filters:** кнопка, открывает модальную панель

### 2.4 График

- Линейный график (line chart) Est. Revenue по дням
- Ось Y — доллары, ось X — даты
- Под графиком: легенда **Total** + ссылка **Active users**
- Кнопка **HIDE ALL**

### 2.5 Таблица данных

Колонки по умолчанию:

| Колонка | Описание |
|---------|----------|
| **App** | Название / ID приложения |
| **Impressions** | Показы (сортируемая) |
| **eCPM** | Доход на 1000 показов (сортируемая) |
| **Est. Earnings** | Расчётный доход (сортируемая) |

- Пагинация: `Showing 1 to 10 of 22` + страницы (1, 2, 3) + выбор кол-ва строк (10)
- Строка **Totals** внизу

---

## 3. Панель фильтров (модальное окно)

| Фильтр | Тип | Опции |
|--------|-----|-------|
| **Applications** | Dropdown (multiselect) | Список приложений аккаунта |
| **Countries** | Radio + multiselect | `Select all countries` / `Let me choose` → All Countries |
| **Networks** | Radio + multiselect | `Select all networks` / `Let me choose` → All Networks |
| **Ad Type** | Radio + multiselect | `Select all types` / `Let me choose` → All Ad Types |
| **Platform** | Checkboxes | `iOS` / `Android` |

Кнопки: **SAVE FILTER** | **CLEAR ALL** | **APPLY**
