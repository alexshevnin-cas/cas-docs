# Текущий интерфейс → QuickView POC v1: список изменений

Источники: `03-product/current-ui-audit.md`, `04-bi/quickview-poc-scope.md`
Пример QuickView POC: https://alexshevnin-cas.github.io/onebi/

---

## Добавляется

1. **App selector в шапке** — сейчас выбор приложения спрятан внутри модального окна Filters, в POC выносится наверх как чип-дропдаун
2. **KPI-карточка DAU** — сейчас нет, добавляется
3. **KPI-карточка ARPDAU** — сейчас нет, добавляется
4. **Дельта % на каждой KPI-карточке** — зелёная/красная стрелка к предыдущему периоду, сейчас нет
5. **Тултипы на KPI-карточках** — описание метрики + формула, сейчас нет
6. **Revenue by Network виджет** — stacked bar + сетка с долями и eCPM по каждой сети, полностью новый блок
7. **Статус сетей** — active/inactive сети с счётчиком, сейчас нет
8. **Футер с таймстампом свежести данных** — "Data updated: 3 min ago", сейчас нет

## Меняется

9. **Период** — добавляется `This month`, `Today` пока не добавляем (нет IRLD данных), `LAST ACTUAL DAY` остаётся
10. **График** — остаётся линейный, но добавляется заливка под линией, точки с тултипами, горизонтальная сетка

## Убирается

11. **Таблица с пагинацией** — строки по приложениям (App / Impressions / eCPM / Est. Earnings)
12. **View by** (Total / Application / Country / Network)
13. **Compared to** (week-to-week, custom)
14. **Table Columns** (Date, Week, Month, Network, Model, Platform, Country, DAU, ARPDAU)
15. **Filters модальное окно** (Countries, Networks, Ad Type, Platform) — выбор приложения переезжает в шапку
16. **Presets**
17. **DOWNLOAD REPORT**
