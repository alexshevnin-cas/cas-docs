# Глоссарий финансовой модели CAS

**Источник:** CAS.AI Fin Model v0.3.4

> Модель это не план, а инструмент для диалога.

---

## Вкладка Assumptions (Допущения)

### ICP размеры клиентов
Gross Revenue приложения клиента в месяц:
- **L1:** $5,000
- **L2:** $12,500
- **L3:** $50,000
- **Unicorn:** $150,000

### RND параметры
| Параметр | Значение | Описание |
|----------|----------|----------|
| Прирост от VIP настройки монетизации | 15% | Uplift выручки от ручной работы команды |
| % выручки клиентов для VIP монетизации | 25% | Доля клиентов, получающих VIP-сервис |
| SDK + Optimal setup цель на конец года | 8% | Целевой uplift от новых фич SDK |
| Прирост от делегирования монетизации | 10% | Customer Free Resources Uplift |

### Publishing параметры
| Параметр | Значение | Описание |
|----------|----------|----------|
| Процент новых клиентов на паблишинг | 10% | Конверсия из медиации в паблишинг |
| Прирост клиентов на паблишинге X | 5 | Мультипликатор выручки |

---

## Вкладка Acquisition (Привлечение)

### Каналы привлечения

**Inbound:**
- **Ads Channel** — платная реклама (Google Ads, Facebook и др.)
- **TG / Reddit** — органика в сообществах
- **Partnerships / Influencers** — партнёрства
- **Organic / Other** — прямые заходы

**Current Clients:**
- **Referral Program** — реферальная программа

**Outbound:**
- **BD** — Business Development (прямые продажи)
- **LD** — Lead Development (работа с лидами)
- **Conf** — Конференции (GDC, Devcom и др.)

### Метрики
- **New L1/L2/L3/Unicorn Clients** — количество новых клиентов по сегментам
- **MMR uplift** — прирост месячной выручки от новых клиентов

---

## Вкладка Revenue (Выручка)

### Основные строки

| Строка | Описание |
|--------|----------|
| **Total Revenue CAS.AI** | Общая выручка компании |
| **Old Users** | Выручка от существующей базы (с учётом churn) |
| **New Users** | Выручка от новых клиентов (pipeline) |
| **Publishing** | Выручка от паблишинг-направления |
| **RND Optimal Setup MMR Uplift** | Прирост от новых фич SDK |
| **Accounting VIP Mon Setup** | Прирост от ручной настройки VIP-клиентов |

### Параметры

| Параметр | Формат | Описание |
|----------|--------|----------|
| **RND Optimal Setup Uplift** | % (1%→8%) | Процент прироста от SDK фич |
| **SDK Rollout** | % (60%→80%) | Доля DAU на новом SDK |
| **Customer Free Resources Uplift** | % (10%) | Прирост от делегирования |
| **Natural Churn** | коэфф. (1→0.92) | Накопительное удержание базы |
| **Prevention by Accounting** | коэфф. (0.01) | Эффект от удержания клиентов |
| **Seasonality** | коэфф. (0.9-1.1) | Сезонные колебания |

### Специальные строки

| Строка | Описание |
|--------|----------|
| **Fact** | Фактические данные (vs план) |
| **Force Major by Network** | Потери от проблем с рекламными сетями (DT, Pangle и др.) |
| **DAU (?)** | Placeholder для будущей метрики |

---

## Формулы и зависимости

### Total Revenue
```
Total Revenue = Old Users + New Users + Publishing + RND Uplift + VIP Setup - Force Major
```

### Old Users (динамика)
```
Old Users[month] = Old Users[prev] × Natural Churn × Seasonality + Prevention
```

### RND Optimal Setup MMR Uplift
```
RND Uplift = Old Users × RND Uplift % × SDK Rollout %
```

### Publishing Revenue
```
Publishing = (New Clients × Pub Conversion %) × X multiplier × Profit Share
```

---

## Следующие шаги (из модели)

- (?) Антифрод — учёт потерь от фрода
- (?) Сезонность — уточнение коэффициентов по историческим данным
- (?) DAU — привязка выручки к DAU для более точного прогноза

---

## Связанные документы
- Бизнес-модель: `02-business-model/cas-business-model.md`
- Типы клиентов: `02-business-model/client-types.md`
- Исходные данные: `02-business-model/Copy of CAS.AI Fin Model 0.3.4 - *.csv`
