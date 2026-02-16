"""
Create a single task in ClickUp via API.
Usage: python scripts/clickup_create_task.py

Set environment variables before running:
  export CLICKUP_API_TOKEN="pk_..."
  export CLICKUP_LIST_ID="901234567"
"""

import os
import json
import urllib.request
import urllib.error

API_TOKEN = os.environ.get("CLICKUP_API_TOKEN", "")
LIST_ID = os.environ.get("CLICKUP_LIST_ID", "")

if not API_TOKEN:
    print("Error: set CLICKUP_API_TOKEN environment variable")
    print("  export CLICKUP_API_TOKEN='pk_...'")
    exit(1)

if not LIST_ID:
    print("Error: set CLICKUP_LIST_ID environment variable")
    print("  export CLICKUP_LIST_ID='901234567'")
    exit(1)

# Test task
task = {
    "name": "[B2B] Выбрать и согласовать UI-шаблон",
    "description": (
        "Проанализировать платные Vue-шаблоны и выбрать подходящий.\n\n"
        "Критерии: Vue 3, Tailwind (или современный CSS), тёмная тема, "
        "качественные таблицы (зебра, sticky header, сортировка), "
        "отсутствие jQuery и legacy JS.\n\n"
        "Бюджет: $100–200.\n\n"
        "Результат: ссылка на шаблон + короткий обзор "
        "(что берём из коробки, что дописываем).\n\n"
        "**Чеклист:**\n"
        "- Обзор 3–5 шаблонов\n"
        "- Проверить стек (Vue 3, Tailwind, chart-библиотека)\n"
        "- Проверить качество таблиц\n"
        "- Проверить тёмную тему\n"
        "- Согласовать с Алексеем (внешний вид)"
    ),
    "markdown_description": True,
    "tags": ["bi-mvp", "milestone-1"],
}

url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json",
}

data = json.dumps(task).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        print(f"Task created: {result['name']}")
        print(f"URL: {result['url']}")
        print(f"ID: {result['id']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}: {body}")
