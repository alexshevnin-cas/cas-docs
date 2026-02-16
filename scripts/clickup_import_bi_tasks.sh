#!/bin/bash
# Import all BI MVP tasks to ClickUp
# Usage: bash scripts/clickup_import_bi_tasks.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/.env.clickup"

API_TOKEN="$CLICKUP_API_TOKEN"
LIST_ID="$CLICKUP_LIST_ID"
RUSLAN_ID="$CLICKUP_RUSLAN_ID"
ALEXEI_ID="$CLICKUP_ALEXEI_ID"
BORYS_ID="$CLICKUP_BORYS_ID"

create_task() {
  local name="$1"
  local desc="$2"
  local assignee="$3"

  local assignees_json="[]"
  if [ -n "$assignee" ]; then
    assignees_json="[$assignee]"
  fi

  local payload=$(python3 -c "
import json
print(json.dumps({
    'name': '''$name''',
    'markdown_description': '''$desc''',
    'tags': ['bi-mvp'],
    'assignees': $assignees_json
}))
")

  local result=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$LIST_ID/task" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local task_name=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','ERROR'))" 2>/dev/null)
  local task_url=$(echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin).get('url',''))" 2>/dev/null)
  echo "  OK: $task_name -> $task_url"
}

echo "=== Milestone 1: Каркас + Quick View ==="

create_task \
  "b2b.cas.ai Подключить шаблон и собрать каркас" \
  "Развернуть выбранный шаблон, настроить проект (Vue 3, роутинг), собрать каркас кабинета:\n- Sidebar (сворачиваемый): Analytics (активный), Apps, Docs, Support (заглушки), профиль пользователя\n- Навигация: вкладки Quick View / Reports\n- Тёмная тема по умолчанию\n- Деплой на стейдж\n\n**Блокер:** Выбор шаблона\n\n**Чеклист:**\n- Инициализировать проект на Vue 3\n- Подключить шаблон и стили\n- Sidebar с навигацией\n- Роутинг (Quick View / Reports)\n- Тёмная тема\n- Деплой на стейдж" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Quick View — карточки метрик" \
  "5 KPI-карточек в верхней части Quick View:\n1. DAU — средний за период\n2. Revenue — сумма Ad Revenue\n3. ARPDAU — Revenue / DAU\n4. eCPM — Revenue / Impressions × 1000\n5. Impressions/DAU — среднее кол-во показов на пользователя\n\nКаждая карточка: значение + динамика vs предыдущий аналогичный период (стрелка ▲▼ + %).\nДанные: хардкод / JSON.\n\n**Блокер:** Каркас\n\n**Чеклист:**\n- Компонент карточки (значение, дельта, иконка)\n- 5 карточек с моковыми данными\n- Динамика (% изменения, цвет: зелёный/красный)" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Quick View — Revenue Trend chart" \
  "Multi-line chart — выручка по дням за выбранный период.\n- All Apps: отдельная линия на приложение (с легендой и цветом)\n- Одно приложение: одна линия\nДанные: JSON-мок.\n\n**Блокер:** Каркас\n\n**Чеклист:**\n- Выбрать chart-библиотеку (из шаблона или ApexCharts/Chart.js)\n- Multi-line chart с легендой\n- Реакция на App Selector" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Quick View — Revenue by Network" \
  "Stacked horizontal bar + grid-раскладка сетей.\nДля каждой сети: revenue (\$), доля (%), eCPM.\nНеактивные сети: серым, \"No data\".\nСети: AppLovin, AdMob, Unity, ironSource, Meta AN, Bigo, Kidoz и др.\nДанные: JSON-мок.\n\n**Блокер:** Каркас\n\n**Чеклист:**\n- Stacked bar chart\n- Grid карточек сетей (revenue, %, eCPM)\n- Неактивные сети серым" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Quick View — App Selector и Period Selector" \
  "Два фильтра в шапке Quick View:\n1. App Selector: dropdown с поиском, мультивыбор, \"All Apps\" по умолчанию\n2. Period Selector: Today / Last 7d / Last 30d / This Month / Custom (date range picker)\nПри изменении — обновляются все компоненты на странице.\n\n**Блокер:** Каркас\n\n**Чеклист:**\n- App Selector (dropdown, поиск, мультивыбор)\n- Period Selector (пресеты + custom range)\n- Связь фильтров с карточками, графиками" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Деплой Quick View на стейдж" \
  "Развернуть собранный Quick View на стейдж-сервере. URL: cabinet.cas.ai или аналогичный субдомен. Показать команде, собрать первый фидбек.\n\n**Блокер:** Все задачи Quick View\n\n**Чеклист:**\n- Деплой на стейдж\n- Проверить тёмную тему\n- Демо команде" \
  "$RUSLAN_ID"

echo ""
echo "=== Milestone 2: Reports ==="

create_task \
  "b2b.cas.ai Reports — chip-based фильтры" \
  "Фильтры в виде chip-ов (теги с ×):\n- Period (обязательный)\n- App (обязательный)\n- Platform (iOS / Android)\n- Country\n- Ad Type (Rewarded, Interstitial, Banner, AppOpen)\nКнопка [+] для добавления фильтров. × для удаления.\nРеференс: Appodeal.\n\n**Блокер:** Milestone 1" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Reports — разбивки (Splits)" \
  "Chip-based выбор разбивок:\n- Date, App, Platform, Ad Type, Country\n- Порядок chips = порядок группировки\n- Drag & drop для изменения порядка\nКнопки [Apply] и [Reset].\n\n**Блокер:** Milestone 1" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Reports — таблица данных" \
  "Основной компонент Reports:\n- Sticky header\n- Sticky footer с итогами (TOTAL)\n- Сортировка по клику на заголовок\n- Зебра-стайл (чередование строк)\n- Грамотные заголовки, тогглы сортировки\nМетрики-столбцы: Revenue, DAU, ARPDAU, eCPM, Fill Rate, Impressions (выбираются пользователем).\n\n**Блокер:** Фильтры + Splits" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Reports — toggle Table/Chart + CSV Export" \
  "- Toggle переключатель: Table (по умолчанию) / Chart (bar или line)\n- Кнопка CSV Export — выгрузка текущего среза в CSV\n\n**Блокер:** Таблица" \
  "$RUSLAN_ID"

echo ""
echo "=== Milestone 3: Живые данные ==="

create_task \
  "b2b.cas.ai Подготовить materialized views для BI" \
  "Подготовить данные в ClickHouse для MVP BI:\n- Revenue, DAU, Impressions по дням / приложениям / сетям / платформам / странам / ad type\n- Materialized views с преагрегацией\n- Latency target: < 2 сек\nСвязь: roadmap D1." \
  "$BORYS_ID"

create_task \
  "b2b.cas.ai Отчёт по производительности БД" \
  "Проанализировать эффект добавленных индексов. Оценить, достаточно ли текущей производительности или нужна миграция на ClickHouse. Подготовить отчёт для Бориса." \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Переключить фронт на живой API" \
  "Заменить моковые данные / B2B на ClickHouse API. Добавить лимит 50K строк с сообщением пользователю. UI не меняется — только источник данных.\n\n**Блокер:** Materialized views + Reports готов" \
  "$RUSLAN_ID"

create_task \
  "b2b.cas.ai Описать формулы метрик для бэкенда" \
  "Документировать формулы расчёта метрик, какие доступны из B2B данных, какие потребуют ClickHouse. Передать Руслану.\nСправочник: 04-bi/metrics-dictionary.md" \
  "$BORYS_ID"

echo ""
echo "=== Организационные ==="

create_task \
  "b2b.cas.ai Прикрепить документацию в Slack-канал" \
  "Собрать в одном месте:\n- Ссылка на прототип OneBI\n- Ссылки от дизайнера (референсы, элементы)\n- Спецификации (design-spec-bi, metrics-dictionary)\n- План проекта" \
  "$ALEXEI_ID"

create_task \
  "b2b.cas.ai Настроить стейдж-окружение" \
  "Настроить стейдж-сервер для BI-кабинета (субдомен cas.ai). Должен быть доступен команде без запуска локально." \
  "$RUSLAN_ID"

echo ""
echo "Done! All tasks created."
