# Синхронизация roadmap

Синхронизируй roadmap.md с GitHub Issues и Asana.

## Что сделать

Определи намерение пользователя из контекста разговора:

1. **"синкани" / "sync" / без уточнений** → `python3 scripts/roadmap_sync.py full`
2. **"push" / "запуши" / "вперёд"** → `python3 scripts/roadmap_sync.py forward`
3. **"pull" / "подтяни" / "обратно"** → `python3 scripts/roadmap_sync.py reverse`
4. **"статус" / "status" / "что расходится"** → `python3 scripts/roadmap_sync.py status`
5. **"bootstrap" / "привяжи"** → `python3 scripts/roadmap_sync.py bootstrap`

Дополнительные аргументы пользователя:
- "dry-run" / "покажи что будет" → добавь `--dry-run`
- "подробно" / "verbose" → добавь `--verbose`

## Правила

- Перед `forward` или `full` — проверь `git diff 03-product/roadmap.md`, чтобы понять что изменилось
- После выполнения — покажи краткий отчёт: сколько создано, обновлено, пропущено
- Если скрипт упал — покажи ошибку и предложи решение
- Если `~/.cas-sync.env` не существует — предупреди и предложи создать

## Пример вывода

```
Синхронизация roadmap.md ↔ GitHub ↔ Asana

Изменения:
- P1: обновлён статус → "В работе" (GitHub #12, Asana)
- G10: создан GitHub #45, Asana task
- C3: Asana completed → roadmap "Готово"

Итого: 2 обновлено, 1 создано, 0 ошибок
```
