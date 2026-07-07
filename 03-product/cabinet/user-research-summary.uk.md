# Кабінет — конспект користувацьких інтерв'ю

**Аудиторія:** новий продакт-менеджер на кабінетний трек.
**Мета документа:** за 30–40 хвилин отримати картину того, що кажуть користувачі про поточний кабінет b2b.cas.ai, які сегменти що просять і де головні болі.
**Період дослідження:** січень–квітень 2026.

> Для глибокого занурення в конкретне інтерв'ю — відкрити файл з колонки «Джерело».

---

## 1. Карта проведених інтерв'ю

### Зовнішні користувачі кабінету

| # | Дата | Респондент | Тип | Джерело | Головне |
|---|------|-----------|-----|---------|---------|
| 1 | 2026-01-30 | Dima Rom (FUNBURSTGAME, 15+ apps) | L2 | `05-research/L2-dima-rom.md` | Дашборд = діагностика «чи все завантажило сьогодні». Реальна аналітика — в Excel/Firebase. Просить розбивки по SDK/App version, темну тему, anomaly detection, фікс Payments |
| 2 | 2026-02-05 | Ілля Нікітін (ex-клієнт, пішов в AppLovin MAX) | Ex-client | `05-research/ex-client-nikitin.md` | Головна причина відходу — немає Reporting API і немає мультикористувацького доступу (ділив логін з командою). Також: інтеграція з MMP, документація, CMP |
| 3 | 2026-02-06 | Михайло Жвіков (Oktopus, Superhero) | Pub (маленький) | `05-research/pub-zhvikov-superhero.md` | Tenjin вистачає, детальний BI — перебір. Хоче «індикатор здоров'я проекту» і предиктивний LTV для пріоритизації розробки фіч |
| 4 | 2026-02-06 | Андрій Мельников (Car Crash) | Pub (мікро) | `05-research/pub-melnikov-carcrash.md` | Net income після комісії CAS, предиктивний дохід за місяць, ROAS в CAS (не в Tenjin), воронки >10 кроків, тренди ринку |
| 5 | 2026-02-06 | Ярослав Савенков (ZooqVPN) | L2 | `05-research/L2-savenkov-zooqvpn.md` | Найдетальніший UX-фідбек: 10 конкретних багів, unified report Spend+Revenue+Events, CAS↔AppsFlyer інтеграція, eCPM по ad type, нон-геймінг вертикаль |
| 6 | 2026-02-11 | Rinaz Khadiev (PSV studio) | Pub (маленький) | `05-research/pub-khadiev.md` | Щоденна діагностика мереж, network health view (включаючи 0 impr), креативи по мережах, баг date-фільтра, помилкові алерти по видалених apps |
| 7 | 2026-04-01 | Serhii Shcherbyna (sales mediation, **внутрішній**) | Internal/voice-of-customer | `05-research/cabinet-tz-shcherbyna.md` | Озвучує болі клієнтів на онбордингу: empty state = відторгнення за 10 секунд, app-ads.txt помилкові тривоги, SDK race, відсутність human touch |

### Внутрішні сесії (контекст для PM)

| # | Дата | Тема | Джерело |
|---|------|------|---------|
| 8 | 2026-03-30 | Онбординг Ruslan Novikov по кабінету — рекламна екосистема, 3 стовпи (apps/credentials/waterfall), бачення self-service | `05-research/internal-ruslan-cabinet-onboarding.md` |
| 9 | 2026-02-09 | Roadmap-talk: фазовий план, дизайнер на фрілансі, ClickHouse, toggle комісії gross/net | `05-research/roadmaptalk-analysis.md` |
| 10 | 2026-03-19 | Конкурентний аналіз кабінетів (AdMob, MAX, LevelPlay) | `03-product/cabinet/competitive-research.md` |
| 11 | 2026-03-19 | Deep-dive Unity LevelPlay console | `05-research/levelplay-console-research.md` |
| 12 | 2026-02-06 | UX-референси: Voodoo, Amplitude, Appodeal | `05-research/competitive-ux-reference.md` |

---

## 2. Сегменти користувачів — хто що хоче

CAS ділить клієнтів на 4 типи (повний опис: `02-business-model/client-types.md`). Підсумую через лінзу кабінету.

### L1 — базовий медіашний клієнт
- Підключив SDK, дивиться revenue вранці.
- Кабінет = «чи все гаразд».
- Йому достатньо: KPI-картки, тренд, top-додатки, баланс.
- **Нікого з L1 в інтерв'ю поки немає** — це прогалина в research.

### L2 — просунутий медіашний клієнт (Dima Rom, Savenkov)
- Робить аналітику сам, кабінет — одне з джерел.
- Хоче: drill-down (по мережах, версіях SDK/app, країнах), порівняння періодів, експорт, saved views, share link, темну тему, anomaly detection.
- **Головний біль: довіра до даних.** Мережі відвалюються мовчки, DAU розходиться з Firebase, аджастменти дублюються.
- **L2 ≠ однорідний сегмент.** ZooqVPN (non-gaming, VPN) не цікавиться мережами і версіями SDK — йому потрібен unified Spend+Revenue+Events. FUNBURSTGAME (gaming) живе діагностикою мереж. Не робити «середнє по лікарні».

### Pub — паблішер на договорі з CAS (Zhvikov, Melnikov, Khadiev)
- UA делегований CAS, розробник НЕ хоче лізти в waterfall і мережі.
- **2 з 3 маленьких Pub** кажуть: export/saved views/share — не потрібно. Підтверджена гіпотеза **Pub-lite**.
- Хоче: net income після всіх комісій, предиктивний дохід за місяць (особливо при сезонності), здоров'я проекту (red/green), ROAS, креативи по мережах (self-service навчання), тренди ринку.
- Khadiev — виняток: використовує кабінет щодня як діагностичний інструмент, бо маленька студія і сам веде продакт.

### PubC — кандидат у паблішинг
- Оцінює свій потенціал, ще не клієнт.
- Нікого з PubC в інтерв'ю кабінетної теми немає. Запити на функціонал ідуть від Pub.
- Референс — Voodoo: submit your game → автотест → метрики → рішення.

### Ex-client — той, хто пішов (Нікітін)
- Причина відходу: треба було закуповуватися в AppLovin для Blended-кампаній, у CAS не було Reporting API.
- Додатково: неможливість дати доступ команді (CMO, аналітик, закупник), відсутність документації, відсутність інтеграції з продуктовою аналітикою (Dev2Dev).

---

## 3. Наскрізні болі (повторюються у кількох респондентів)

| Біль | Хто згадував | Куди впливає |
|------|--------------|--------------|
| **Empty state = відторгнення за 10 сек** | Shcherbyna (бачить щодня на онбордингу) | Critical для retention нових |
| **Мережі відвалюються без повідомлення** | Dima Rom, Khadiev | Network health view, anomaly alerts |
| **Немає розбивки по версії SDK / app** | Dima Rom, Khadiev, Savenkov | OneBI breakdowns |
| **Date-фільтр / фільтри глючать** | Dima Rom, Khadiev, Savenkov | UX-баги |
| **eCPM агрегований по всіх ad types — обманює** | Savenkov | Quick View, формула KPI |
| **Net income vs Gross — незрозуміло** | Melnikov, Dima Rom (через адж.), Savenkov | Toggle gross/net, прозорість Payments |
| **Предиктивний дохід за місяць** | Zhvikov, Melnikov, Savenkov | Prediction Revenue віджет (вже в roadmap) |
| **Аналітика розкидана по сервісах** (Tenjin, Firebase, CAS) | Melnikov, Savenkov, Нікітін | Unified report, інтеграції з MMP |
| **Немає мультикористувацького доступу** | Нікітін (=причина відходу) | Team management (плейсхолдер в overview) |
| **Немає темної теми** | Dima Rom, Melnikov ("інтроверти о 3 ночі") | Глобальне UX-налаштування |
| **Документація тільки через менеджера** | Нікітін, неявно Khadiev | Help center / docs |

---

## 4. Конкретні UX-баги (треба знати в обличчя)

| # | Баг | Джерело |
|---|-----|---------|
| 1 | Date picker скидається при перемиканні — треба клікати двічі | Khadiev, Dima Rom |
| 2 | Збережені фільтри (presets) зникають / «не завжди працюють» | Dima Rom, Savenkov |
| 3 | Ліміт 15 додатків у групі — недостатньо для портфелів | Dima Rom |
| 4 | Кнопка Export прихована — клієнт не знаходить | Savenkov |
| 5 | Фільтри не показують що вибрано (немає chips/tags) | Savenkov |
| 6 | Кілька додатків одним кольором на графіку | Savenkov |
| 7 | Попапи без окремих URL — не можна поділитися посиланням | Savenkov |
| 8 | Помилкові хрестики app-ads.txt на 130+ apps | Shcherbyna |
| 9 | Помилкові алерти по видалених додатках в Applications | Khadiev |
| 10 | Незакриваний банер (Bigo, app-ads.txt) | Khadiev, загальне |
| 11 | Bundle ID замість імен додатків | усі |
| 12 | Default бекенд `/mediation` катастрофічно повільний (до 122s) | спід-тести, див. `05-research/dashboard-speed-results.md` |
| 13 | Аджастменти в Payments дублюються, сума не сходиться | Dima Rom |
| 14 | Іконки додатків не підтягуються | Dima Rom |

---

## 5. Топ-запити фіч (агреговано)

### Аналітика
- **DAU + ARPDAU в KPI-картках** (зараз приховано в Table Columns) — усі
- **Дельти ±% до попереднього періоду** на KPI — Savenkov, Quick View POC
- **Compare mode** (два періоди поруч) — Savenkov, Pub
- **Розбивка по версії SDK і версії додатку** — Dima Rom, Khadiev, Savenkov
- **Network health view** — усі мережі, включаючи 0 impressions і непідключені — Khadiev
- **Anomaly detection** — підсвічування провалів і нулів — Dima Rom, Khadiev
- **Unified report Spend + Revenue + Events** по GEO+AdType — Savenkov (критично)
- **CAS ↔ AppsFlyer / MMP інтеграція** — Savenkov, Нікітін
- **Predictive revenue / LTV** за місяць — Zhvikov, Melnikov, Savenkov

### Фінанси / прозорість
- **Net income після комісії CAS** (toggle gross/net) — Melnikov, Dima Rom
- **Estimated vs finalized** revenue
- **Monthly summary** в Payments + фільтри по періоду/типу
- **Export Payments** (CSV/PDF) — Savenkov

### Self-service & команда
- **Reporting API** — Нікітін (=причина відходу), L2
- **Team management** + ролі — Нікітін (=причина відходу)
- **Saved views + share link** — L2 (Savenkov, Dima Rom)
- **Документація / help center** — Нікітін

### Pub-специфіка
- **Creative performance по мережах** (self-service навчання, не управління UA) — Khadiev
- **Індикатор здоров'я проекту** (red/green) — Zhvikov
- **Тренди ринку** (що хайпить в Google Play / App Store) — Melnikov
- **Воронки >10 кроків** (для ігор з довгою прогресією) — Melnikov

### Онбординг
- **Friendly empty state** замість червоної помилки — Shcherbyna (головний bottleneck)
- **Human touch блок** (фото менеджера, посилання на WhatsApp/Telegram) — Shcherbyna
- **Guided tour** для першої сесії
- **SDK gate** — спочатку реєстрація додатку, потім доступ до інтеграції

---

## 6. Що важливо знати про сам кабінет

> Глибоко — `03-product/cabinet/overview.md` (цільове) і `current-state.md` (as-is).

### Що є зараз
- 4 сторінки: Mediation, Publishing, Payments, Applications + dropdown акаунту.
- Mediation і Publishing — **два різних UX** (різні контроли, різний візуал) для одного завдання (аналітика).
- Applications — список з COPPA/app-ads.txt статусами. **Немає картки додатку**, немає метрик поруч.
- Payments — 254 рядки з 2024 без фільтрів. Домінують fraud adjustments.
- Account — мінімальний dropdown. Немає team, немає 2FA, немає forgot password.
- Конфігурація waterfall — **один JSON на клієнта**, правиться вручну, саппорт у Telegram.

### Що в роботі (Q2 2026, Phase 1 — рестайлінг)
Вирішено на зустрічі з Shcherbyna 2026-04-01:
- **4 блоки замість 4 сторінок:** Analytics / Applications / Payments / Profile.
- **Баланс у хедері** (як у Appodeal).
- **Publishing → таб всередині Analytics** (єдиний UX з Mediation).
- **OAuth credentials → переїжджають в Applications** (логічно правильне місце).
- **QuickView** = перший екран після логіну (KPI + тренд + revenue by network).
- **Prediction Revenue** віджет (особливо для empty state нових).
- **Human touch блок** — фото менеджера + WhatsApp/Telegram, дані з 1С.
- **Імена додатків зі стора** замість bundle ID.
- **Friendly empty state**, гайд тур, фікс помилкових тривог app-ads.txt.
- **Дизайнер Данило Кузнєцов** — перший досвід з B2B dashboards. Старт ~07.04.

### Принципи
- **Managed зараз → self-service ціль.** Спочатку прозорість (показати), потім контроль (дати рулити).
- **Один інтерфейс — різні дані.** Кабінет адаптується під тип клієнта (L1/L2/Pub).
- **Three pillars** налаштування додатку: Apps, Network credentials, Waterfall configs. У L1 credentials вшиті, у L2+ — свої.

---

## 7. Що не покрито дослідженням (прогалини)

- **L1 — жодного інтерв'ю.** Базовий сегмент, ~80% клієнтів, ніхто не опитаний з лупою кабінету.
- **Тільки 1 Ex-client.** Воронка відходу = велика сліпа пляма.
- **PubC** на кабінеті — немає.
- **Внутрішні ролі** (Admin, Monetisation, UA, BD) — у кабінеті не інтерв'ювали, є тільки опосередковано через Shcherbyna і Osyka.
- **iOS-only клієнти** — вибірка скошена в бік Android/cross-platform.
- **Великі L2** (>$100K MAU) — Babygamespub є в speed-тестах, але не в інтерв'ю.

Це потенційні перші дослідження для нового PM.

---

## 8. Корисні посилання (в порядку читання)

| Коли | Що прочитати |
|------|--------------|
| Старт | `01-platform/platform-overview.md` (що таке CAS) → `02-business-model/client-types.md` (сегменти) |
| Кабінет | `03-product/cabinet/overview.md` (цільове) → `current-state.md` (as-is) → `competitive-research.md` |
| Конкурент в глибині | `05-research/levelplay-console-research.md` |
| Аналітика (OneBI) | `03-product/design-spec-bi.md` + `04-bi/metrics-dictionary.md` + `04-bi/filters.md` |
| User stories | `03-product/user-stories.md` |
| Бізнес-модель | `02-business-model/cas-business-model.md` |
| Стратегія і фази | `03-product/product-strategy-1pager.md` + `03-product/roadmap.md` |
| Швидкість дашборду | `05-research/dashboard-speed-results.md` (живі дані по 4 акаунтах) |
| Усі дослідження | `05-research/research-log.md` (індекс) |
