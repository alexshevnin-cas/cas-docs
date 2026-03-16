# Research Log

Индекс всех проведённых исследований. Сырые транскрипты не хранятся — только структурированные анализы.

---

| # | Дата | Респондент | Тип | Файл | Ключевые находки |
|---|------|-----------|-----|------|-----------------|
| 1 | 2026-01-30 | Dima Rom (FUNBURSTGAME LTD) | L2 | `L2-dima-rom.md` | Нужны разбивки по SDK/App version, экспорт, сравнение сетей, anomaly detection |
| 2 | 2026-02-05 | Илья Никитин (ex-клиент → MAX) | Ex-client | `ex-client-nikitin.md` | Мультипользовательский доступ, роли, причины ухода на AppLovin MAX |
| 3 | 2026-02-02 | Alexei + Aleksandr Osyka | Internal | `internal-osyka-payments-b2b.md` | Payments UI редизайн, H1/H2 roadmap, BI инфра ~$50K, дизайнер нужен, Superset отклонён |
| 4 | 2026-02-06 | Михаил Жвиков (Oktopus, Superhero) | Pub | `pub-zhvikov-superhero.md` | Tenjin хватает, детальный BI — перебор, хотят предиктивный LTV для приоритизации разработки, индикатор здоровья проекта |
| 5 | 2026-02-06 | Андрей Мельников (Car Crash) | Pub | `pub-melnikov-carcrash.md` | Net income после комиссии CAS, предиктивный доход за месяц, A/B-тесты в дашборде, тренды рынка, Voodoo как референс self-service, воронки >10 шагов |
| 6 | 2026-02-06 | Ярослав Савенков (ZooqVPN) | L2 | `L2-savenkov-zooqvpn.md` | Unified report (Spend+Revenue+Events), CAS↔AppsFlyer интеграция, eCPM по ad type не агрегированный, 10 UX-багов, Desktop SDK как новая ниша, ad churn A/B analysis |
| 7 | 2026-02-06 | — | Competitive | `competitive-ux-reference.md` | UX-референсы: Voodoo (PubC self-service, status badge), Amplitude (graph+table, share link), Appodeal (predictive LTV как маркетинг) |
| 8 | 2026-02-09 | Alexei + Osyka + Kapatsyn | Internal | `roadmaptalk-analysis.md` | Фазовый план подтверждён, дизайнер на фрилансе, ClickUp пока, self-hosted ClickHouse, toggle комиссии gross/net, карточка приложения, Denis SDK roadmap alignment |
| 9 | 2026-02-11 | Rinaz Khadiev | Pub | `pub-khadiev.md` | Ежедневная диагностика сетей, разбивка по версиям, network health view (все сети вкл. 0 impr), креативы по сетям self-service, баг дата-фильтра, Pub-lite подтверждён (не нужны export/saved views), BX: скорость реакции команды |
| 10 | 2026-02-12 | Alexei + Aleksandr Osyka | Internal | `internal-osyka-overview.md` | Обзор всех треков, self-service отложен на H2+, Горик=реальный R&D, менеджеры без аналитических инструментов, регламент онбординга, PubC retention program (догревание), Creative Management валидация, C11+G10 добавлены |
| 11 | 2026-02-12 | Oleg + Osyka + Kapatsyn + Ещенко + Alexei | Internal | `internal-google-sdk-partnership.md` | Google предложил SDK Product Portfolio: SDK Console, App Integrity, Family Ads, deprecation notifications. Решение: бэклог Q2-Q3, контакт поддерживать. Проблема детских приложений (переименованный SDK). C12 добавлен |
| 12 | 2026-02-16 | — | CRM Data | `bitrix-crm-analysis.md` | Анализ Битрикс: 3111 лидов (июл 2024 — фев 2026). Конверсия: 9.4% (2024) → 4.3% (2025). Bottleneck = квалификация (88% отсев). 79% лидов без SOURCE_ID. Publishing = 4% vs 60% в финмодели. Прогноз 2026: 91-144 клиента (3 сценария) |
| 13 | 2026-02-18 | — | CRM Data | `hubspot-pipeline-analysis.md` | HubSpot пайплайн: 391 контакт (Lead+Opp, без Approached), оценено 222. Суммарный потенциал $1.95M/мес. Топ: Igor Maiorov $707K (95/238), Yuliia Turovych $671K (51/54), Taras Poraiko $304K (20/20). Victoria Huz — 25 контактов, 76% без данных |
| 14 | 2026-02-20 | — | Meeting Prep | `nikita-meeting-brief-2026-02-20.md` | Traction Scorecards по 4 inbound-каналам (Google Ads, YouTube, TG/Reddit, SEO) + GoToMarket (Рома/Tenjin, Настя/Growth). CSV-шаблон: `traction-scorecard-template.csv` |
| 15 | 2026-02-25 | Alexei + Borys + Kapatsyn + Horyk | Internal | `realtime-ads.md` | Real-time BI на ILRD: дискреп ~1.7-5%, компенсационные коэффициенты, Китай отключён, ILRD уже включён для всех (~4000 apps). Когортный анализ как отдельная ценность ILRD |
| 16 | 2026-02-26 | Alexei + Ruslan | Internal | `internal-ruslan-bi-vocab.md` | DDD как паттерн, API отдельным репо, Admin API параллельный слой, Data Catalog нужен, real-time = раз в час, критерии успеха Этапов 1-2 |
| 17 | 2026-02-25 | Alexei + Denis + Osyka | Internal | `cas-sdk-stabe.md` | SDK тестирование сломано, нет QA-процесса, предложение Alpha/Beta/Stable треков, Олена как QA |
| 18 | 2026-02-24 | — | Framework | `cpo-effectiveness-framework.md` | Три линзы CPO: Say-Do Ratio (нед), Outcomes (мес), Empowered Teams (квартал) |
| 19 | 2026-03-11 | Alexei + Denis + Yuriy Vityuk + Osyka | Internal | `SDK-in-Asana-Backlog-c3a3f77f-4535.md` | Роли SDK подтверждены (Denis=Lead, Olena=QA, Yuriy=R&D PM, Anton=бета-координатор), Asana миграция, release policy v0.3 |
| 20 | 2026-03-11 | Yuriy Vityuk | Internal | `cas-test-pipeline.md` | A/B test pipeline: 50/50 когорты, 500 юзеров × 5 стран, eCPM/ARPDAU/crash как метрики |
| 21 | 2026-03-11 | All-Hands (Osyka, Oleg, Igor, Nikita, Smirnov, Horyk, Shevnin, Borys, Kapatsyn, Denis) | Internal | `all-hands-2026-03-11.md` | Первый data-driven all-hands. $1.98M vs $2.14M план (-7.3%). DT Exchange ~5% потерь. SDK stable version кризис. 1С бутылочное горлышко. Publishing деприоритизирован. Ed Hugo канал ($200-300K потенциал). OneBI демо→апрель |
| 22 | 2026-03-12 | Hanna Novatska (координатор креативов) | Internal | `internal-novatska-creatives.md` | Текущий процесс управления креативами: ручное переименование, заливка на сети. Нейминговая конвенция (V/SV/B/PLAY + код 1С). 8+ креативщиков. Проблемы: неконсистентный нейминг ломает аналитику, нет каталога, нет превью. Продуктовый документ: `03-product/creatives-catalog.md` |
