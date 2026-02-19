# BI Filters & Splits — CAS (v0)

## Назначение
Документ фиксирует все фильтры и разрезы (splits / group by),
используемые в BI платформы CAS.

Используется как:
- справочник для BI
- основа для пользовательского кабинета
- база для разграничения доступов по ролям (L1 / L2 / Publishing)

Документ предназначен для редактирования и расширения.

---

## Общий принцип
- Фильтры ограничивают выборку данных  
- Разрезы (splits) определяют, как данные агрегируются  
- Наличие фильтра или разреза не означает доступность для всех клиентов  
- Доступность определяется отдельно (в следующих документах)

---

## Filters — Common

| Фильтр | Описание | Примечание |
|------|---------|-----------|
| Activity Date | Дата активности события или метрики | Основной временной фильтр |
| Install Date | Дата установки приложения | Используется для когорт |
| App | Приложение | Один или несколько app |
| Country | Страна пользователя | GEO анализ |
| OS | Операционная система | iOS / Android |
| OS Version | Версия операционной системы | |
| Package Version | Версия приложения на момент активности | |
| Install Package Version | Версия приложения на момент установки | Анализ релизов |
| Manufacturer | Производитель устройства | |
| Model | Модель устройства | |
| Device Type | Тип устройства | Phone / Tablet |
| Framework Version | Версия SDK / фреймворка | |
| Connection Type | Тип соединения | Wi-Fi / Cellular |
| Day Since Install | Дни с момента установки | Когортный анализ |
| Keywords | Теги или ключевые слова | Произвольные |

---

## Filters — Superadmin (Internal)

| Фильтр | Описание | Примечание |
|------|---------|-----------|
| Manager | Менеджер, закреплённый за приложениями | Фильтрует кастомеров и их бандлы |
| Customer | Клиент платформы CAS (за ним закреплены бандлы) | Связан с Manager через Admin |
| Date Created | Дата создания (подключения) клиента к платформе | Диапазон дат, быстрые пресеты по годам |

### Логика связей

```
Manager → Customer → Bundle(s) → Revenue / Metrics
```

- За каждым **Customer** закреплены **бандлы** (Bundle ID)
- За каждым **Customer** закреплён **Manager**
- Superadmin может фильтровать данные в любом разрезе: по менеджеру, кастомеру, дате подключения
- При выборе Manager — список Customer фильтруется автоматически
- При выборе Customer — данные ограничиваются бандлами этого кастомера

### Admin Panel

Управление связями Manager ↔ Customer доступно через экран **Admin** в левой навигации.

Структура:
- **Левая колонка** — список менеджеров с количеством кастомеров и бандлов
- **Правая колонка** — таблица кастомеров (ID, Customer, Manager, Bundles, Date Created)
- Переназначение менеджера — через inline dropdown в таблице
- Поиск по имени, ID или Bundle ID
- Сортировка по любому столбцу

### Менеджеры (текущие)

| ID | Имя | Роль |
|----|-----|------|
| m1 | Anton Smirnov | Senior AM |
| m2 | Serhii Shcherbyna | AM |
| m3 | Rashid Sabirov | AM |
| m4 | Buha Maksym | AM |
| m5 | Dmytro Dubniak | AM |

---

## Filters — Mediation

| Фильтр | Описание | Примечание |
|------|---------|-----------|
| Mediation Platform | Медиационная платформа (CAS, MAX, ironSource) | L2+ для мульти-медиации |
| Waterfall Configuration | Конфигурация водопада медиации | |
| Mediation Group | Группа медиации | |
| Round Number | Раунд показа / аукциона | |
| Bid Floor Range | Диапазон bid floor | |
| Ad Request Floor Range | Диапазон floor запроса | |
| Bid Price Range | Диапазон цены ставки | |

---

## Filters — Events & Monetization

| Фильтр | Описание | Примечание |
|------|---------|-----------|
| Event Name | Название события | |
| In-app Purchase | События внутриигровых покупок | |

---

## Splits / Group by — Monetization

| Разрез | Описание | Примечание |
|------|---------|-----------|
| Network (Monetization) | Рекламная сеть | Основной разрез дохода |
| Ad Type | Тип рекламы | Banner / Interstitial / Rewarded |
| Appodeal Segment | Сегмент Appodeal | |
| Placement (Monetization) | Плейсмент рекламы | |
| Ad Units | Ad Unit | |
| SDK Version | Версия SDK | |
| Framework | Фреймворк приложения | Unity / Native |
| Plugin Version | Версия плагина | |
| Network Account (Monetization) | Аккаунт рекламной сети | Multi-account |
| Zero IDFA | Наличие IDFA | Privacy / ATT |
| In-App Header Bidding | In-app Header Bidding | |
| Monetization Ad Units | Monetization Ad Unit | Внутренний уровень |
| Post Bid | Post-bid стадия | После аукциона |

---

## Splits / Group by — Attribution (UA)

| Разрез | Описание | Примечание |
|------|---------|-----------|
| Placement (UA) | UA-плейсмент | |
| Creative Name (UA) | Название креатива | |
| Source App (UA) | Приложение-источник | |
| Search Keywords | Поисковые ключевые слова | |
| Search Keywords ID | ID ключевого слова | |
| Agency | Агентство | |
| Agency (Source) | Источник агентства | |
| White Label Publisher | White-label паблишер | |
| Network (UA) | UA-сеть | |
| Is Organic (UA) | Органика / не органика | |
| Campaign (UA) | Кампания | |
| AdSet (UA) | Ad Set | |
| Creative (UA) | Креатив | |
| Studio | Студия | |
| Revenue Manager | Revenue Manager | |
| Attribution Agency | Атрибуционное агентство | |
| Is Claimed By Publisher | Claim от паблишера | |

---

## Связанные документы
- BI overview: `04-bi/bi-overview.md`
- Metrics dictionary: `04-bi/metrics-dictionary.md`
- Client types: `02-business-model/client-types.md`

---

## Границы документа
- Без UI
- Без логики прав доступа
- Без источников данных
- Без гарантий доступности для всех типов клиентов