# CAS Docs — AI Copilot Context

## Что это за проект
База знаний для проектирования АРМ (кабинет + BI) платформы CAS.AI — ad mediation для мобильных разработчиков.

## Структура

```
01-platform/         — Что такое CAS, ограничения
02-business-model/   — Бизнес-модель, типы клиентов, финмодель
03-product/          — Продуктовые спецификации (кабинет, BI UX, онбординг, user stories)
04-bi/               — Справочник метрик и фильтров
05-research/         — Исследования: интервью, анализы (индекс в research-log.md)
05-research/raw/     — Сырые транскрипты (архив, НЕ ЧИТАТЬ)
06-marketing-site/   — Маркетинговый сайт cas.ai (лендинги, воронки, A/B тесты)
assets/              — Картинки (mockups, конкурентный анализ)
```

## Что читать в зависимости от задачи

| Задача | Файлы |
|--------|-------|
| Понять продукт | `01-platform/platform-overview.md` → `03-product/cabinet-overview.md` |
| Бизнес-контекст | `02-business-model/cas-business-model.md` + `client-types.md` |
| Проектировать UI | `03-product/design-spec-bi.md` + `04-bi/metrics-dictionary.md` + `04-bi/filters.md` |
| User stories | `03-product/user-stories.md` |
| R&D гипотезы | `03-product/rnd-hypotheses.md` |
| Онбординг | `03-product/onboarding-flow.md` |
| Стратегия и фазы | `03-product/product-strategy.md` |
| Что говорят клиенты | `05-research/research-log.md` → конкретные файлы |
| UX-референсы конкурентов | `05-research/competitive-ux-reference.md` + `assets/competitive/` |
| Финмодель | `02-business-model/fin-model-*.md` + CSV |
| Маркетинговый сайт | `06-marketing-site/website-plan.md` |
| Команда и роли | `01-platform/team.md` |
| Roadmap и синхронизация | `03-product/roadmap.md` + `scripts/roadmap_sync.py` |
| Тест скорости дашборда | см. секцию «Dashboard Speed Testing» ниже |

## Правила

- Один файл = один источник правды. Не дублировать контент между файлами.
- Сырые транскрипты хранить в `05-research/raw/`. **НИКОГДА не читать файлы из `raw/`** — они только для людей. Для AI использовать только структурированные анализы.
- Не выдумывать продуктовые факты. Если информации нет — спросить.
- Не создавать HTML/DOCX экспорты. Markdown — единственный формат.

## Dashboard Speed Testing

Автоматизированное тестирование скорости загрузки b2b.cas.ai/mediation через Playwright.

### Аккаунты (4 шт.)

Хранятся в `scripts/.env.cas-accounts` (не коммитится, в .gitignore):

| # | Email | Профиль |
|---|-------|---------|
| 1 | hadievv2048@gmail.com | Средний паблишер |
| 2 | anworlddirect@gmail.com | Средний паблишер |
| 3 | Fren2y.g@gmail.com | Маленький паблишер |
| 4 | Babygamespub@gmail.com | Крупный паблишер (самый тяжёлый) |

### Скрипты

- `scripts/cas_dashboard_speed.py` — основной тест: 3 сценария × все аккаунты
- `scripts/cas_speed_extended.py` — целевые тесты (длинные периоды, колонки+фильтры, один аккаунт)

### Методология

**Основной тест** (`cas_dashboard_speed.py`): для каждого аккаунта прогоняет 3 сценария:

1. **Default mode** (`/mediation`) — старый бэкенд, 30d + custom 90d
2. **Chart mode** (`/mediation?mode=ch`) — ClickHouse, 30d + custom 90d + 180d
3. **Chart+cols** (`?mode=ch` + extra columns) — Network, Platform, DAU, ARPDAU

В каждом сценарии измеряется:
- Загрузка периода (load)
- View-by переключения (Application, Country, Network)
- Метрика-карточки (Impressions, eCPM)
- Фильтры платформы (iOS, Android)

**Расширенный тест** (`cas_speed_extended.py`): настраиваемый — можно тестировать отдельные аккаунты, длинные периоды (270d, 360d), последовательность plain → +columns → +columns+filters.

### Результаты

- Консоль: таблица с таймингами при запуске
- Файл: `05-research/dashboard-speed-results.md` (автоматически, с таймстампом)
- Скриншоты: `assets/dashboard-speed-*.png`, `assets/speed-ext-*.png`
- Публикация: `public/dashboard-speed-results.md` → https://alexshevnin-cas.github.io/cas-docs/#/dashboard-speed-results

### Ключевые выводы (2026-02-23)

- Default mode деградирует катастрофически: Babygamespub 122s на 30d, timeout на 90d
- Chart mode (ClickHouse): 3.5–5.5s стабильно от 30d до 360d для всех аккаунтов
- Extra columns не влияют на скорость в CH mode
- Баг: в chart+cols режиме фильтры ломаются после 30d (iOS/Android = FAIL)

## Обработка новых интервью

Когда пользователь присылает транскрипт, обработать в 3 шага:

### Шаг 1: Структурированный анализ → `05-research/`

Использовать шаблон:

```markdown
# [Тип клиента] — [Имя/Компания]

**Дата:** YYYY-MM-DD
**Респондент:** Имя (роль, компания)
**Тип:** L1 / L2 / Pub / PubC / Ex-client
**Контекст:** 1-2 предложения о клиенте

---

## Профиль
- Масштаб (DAU, кол-во приложений)
- Платформы
- Текущий стек аналитики
- Опыт с CAS

## Ключевые боли
1. **[Боль]** — описание + цитата
2. ...

## Запросы к продукту
| Запрос | Приоритет (их) | Связь с существующими stories |
|--------|---------------|-------------------------------|
| ... | ... | US-L2-XX или NEW |

## Инсайты для продукта
- Что подтвердилось из наших гипотез
- Что нового узнали
- Что противоречит текущим планам

## Action Items
| # | Действие | Куда влияет |
|---|----------|------------|
| 1 | ... | user-stories.md / metrics-dictionary.md / ... |
```

### Шаг 2: Обновить существующие документы

По action items из шага 1 — добавить новые user stories, метрики, фильтры в соответствующие файлы.

### Шаг 3: Обновить research-log.md

Добавить строку в таблицу `05-research/research-log.md`.
