# CAS.AI — Metrics Dictionary (Table View)

Единый словарь метрик платформы CAS.AI в табличном виде.
Формат предназначен для совместного редактирования, фильтрации и дальнейшего импорта в BI / PRD.

## Обозначения уровней доступа

| Уровень | Описание |
|---------|----------|
| L1 | Базовые клиенты медиации |
| L2 | Продвинутые клиенты медиации |
| PubC | Паблишинговый кандидат (валидация прототипа) |
| Pub | Паблишинг |
| Int | Внутренние метрики CAS |

| Символ | Значение |
|--------|----------|
| ✓ | Доступно |
| ○ | Планируется (future) |
| — | Не доступно |

---

## North Star Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| m1 | MRR | Monthly Recurring Revenue = Σ App Revenue (net) | Сколько мы зарабатываем в месяц? | — | Int | — |
| m2 | ARR | Annual Run Rate = MRR × 12 | Куда мы идём по году? | — | Int | — |
| m3 | Revenue Growth % | (MRR_t − MRR_t-1) / MRR_t-1 | Растём ли мы и с какой скоростью? | — | Int | — |

---

## App / Product Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| m4 | App Profit | Ad Revenue − UA Cost | Приложение прибыльно? | — | Pub | — |
| m5 | DAU | Daily Active Users: average number of unique active app users per day within the selected period and filters | Сколько в среднем активных пользователей в день за выбранный период? | ✓ | ✓ | ✓ |
| m6 | AVG Session Count | Avg Sessions per User per Day | Как часто пользователь заходит в игру? | — | ✓ | — |
| m7 | AVG Session Duration | Avg Session Length | Насколько «залипают» в игре? | — | ✓ | ✓ |
| m8 | DAV / DAU | Daily Active Viewers / DAU | Какой % DAU видит рекламу? | — | ✓ | — |
| m9 | conversion_PAU | Paying Active Users / DAU | Конвертируем ли DAU в платящих? | — | Pub | — |
| m12 | LTV | ARPDAU × Lifetime Days | Сколько приносит юзер за жизнь? | — | Pub | — |
| m37 | Active Users | Number of unique active app users based on selected filters (period, app, geo, platform) | Сколько активных пользователей за выбранный период? | ✓ | ✓ | ✓ |

---

## Ad Revenue & Monetisation

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| m13 | Ad Revenue | Σ Ad Revenue | Сколько приносит реклама? | ✓ | ✓ | ○ |
| m41 | Total Revenue | Ad Revenue + IAP Revenue | Сколько всего выручки приносит продукт? | — | ✓ | — |
| m14 | ARPDAU | Total Revenue ÷ DAU (includes all revenue streams) | Эффективна ли общая монетизация на пользователя? | — | ✓ | — |
| m38 | Ad ARPDAU | Ad Revenue ÷ DAU (average ad revenue generated per daily active user over selected period) | Сколько рекламной выручки в среднем приносит один DAU? | ✓ | ✓ | ○ |
| m39 | IAP ARPDAU | IAP Revenue ÷ DAU (average in-app purchase revenue generated per daily active user over selected period) | Сколько IAP-выручки в среднем приносит один DAU? | — | Pub | — |
| m40 | Total ARPDAU | (Ad Revenue + IAP Revenue) ÷ DAU (average total revenue generated per daily active user over selected period) | Сколько всего выручки в среднем приносит один DAU? | — | ✓ | — |
| m42 | ARPU | Total Revenue ÷ Active Users (average revenue generated per active user over selected period) | Сколько выручки в среднем приносит один активный пользователь? | — | ✓ | — |
| m15 | Impressions / DAU | Impressions ÷ DAU | Достаточно ли рекламы на юзера? | ✓ | ✓ | — |
| m16 | Impr / Sess Banner | Banner Impressions ÷ Sessions | Достаточно ли баннеров? | — | ✓ | — |
| m17 | Impr / Sess Inter | Interstitial Impressions ÷ Sessions | Не теряем ли interstitial показы? | — | ✓ | — |
| m18 | Impr / Sess Reward | Rewarded Impressions ÷ Sessions | Достаточно ли rewarded возможностей? | — | ✓ | — |
| m19 | Ads / Session | Ads shown ÷ Sessions | Не перегружаем ли UX рекламой? | — | ✓ | — |
| m20 | eCPM | Effective Cost Per Mille = Revenue ÷ Impressions × 1000 (revenue per 1,000 ad impressions) | Сколько в среднем приносит 1 000 рекламных показов? | ✓ | ✓ | ○ |
| m53 | eCPM Interstitial | Revenue_interstitial ÷ Impressions_interstitial × 1000 (eCPM for interstitial ads: static + video) | Сколько в среднем приносит 1 000 interstitial-показов? | — | ✓ | — |
| m54 | eCPM Banner | Revenue_banner ÷ Impressions_banner × 1000 (eCPM for banner ads) | Сколько в среднем приносит 1 000 banner-показов? | — | ✓ | — |
| m55 | eCPM MREC | Revenue_mrec ÷ Impressions_mrec × 1000 (eCPM for MREC ads) | Сколько в среднем приносит 1 000 MREC-показов? | — | ✓ | — |
| m56 | eCPM Rewarded Video | Revenue_rewarded ÷ Impressions_rewarded × 1000 (eCPM for rewarded video ads) | Сколько в среднем приносит 1 000 rewarded video-показов? | — | ✓ | — |
| m57 | eCPM Native | Revenue_native ÷ Impressions_native × 1000 (eCPM for native ads) | Сколько в среднем приносит 1 000 native-показов? | — | ✓ | — |
| m21 | Fill Rate | Fills ÷ Requests × 100 | Теряем ли показы из‑за отсутствия спроса? | ✓ | ✓ | — |
| m22 | NoFill Rate | 1 − Fill Rate | Где потери выручки? | — | ✓ | — |
| m23 | SoV by Network | Impr_network ÷ total impr | Есть ли зависимость от одной сети? | — | ✓ | — |
| m36 | Active Users per Ad | Count of unique active users who were exposed to or attempted to interact with ads, based on selected filters (ad type, ad network, period) | Сколько уникальных пользователей реально взаимодействуют с рекламой? | — | ✓ | — |
| m46 | Impressions | Total number of ad impressions displayed | Сколько всего рекламных показов было отображено? | ✓ | ✓ | ○ |
| m47 | Clicks | Total number of clicks on ads | Сколько всего кликов по рекламе? | — | ✓ | — |
| m48 | CTR | Click-through rate = Clicks ÷ Impressions × 100 | Насколько кликабельна реклама? | ✓ | ✓ | — |
| m49 | Requests | Total number of ad requests made to the server | Сколько всего запросов рекламы отправлено? | — | ✓ | — |
| m50 | Finish video view | Number of times video ads have been viewed till the end | Сколько раз видеореклама была досмотрена до конца? | — | ✓ | — |
| m51 | Ad Engagement Rate | Ad Engaged Users ÷ Active Users × 100 | Какой процент активных пользователей взаимодействует с рекламой? | — | ✓ | — |
| m52 | Display Rate | Impressions ÷ Fills × 100 | Какой процент полученных рекламных ответов был реально показан? | — | ✓ | — |
| m58 | Ad Engaged Users | Number of users who have interacted with at least one ad during the selected period | Сколько пользователей взаимодействовали хотя бы с одной рекламой? | — | ✓ | — |
| m59 | Ad ARPU | Ad Revenue ÷ Active Users per Ad | Сколько рекламной выручки в среднем приносит один пользователь, взаимодействующий с рекламой? | — | ✓ | — |
| m60 | Ad ARPU Interstitial | Ad Revenue_interstitial ÷ Active Users_interstitial | Сколько рекламной выручки в среднем приносит один пользователь interstitial-рекламы? | — | ✓ | — |
| m61 | Ad ARPU Banner | Ad Revenue_banner ÷ Active Users_banner | Сколько рекламной выручки в среднем приносит один пользователь banner-рекламы? | — | ✓ | — |
| m62 | Ad ARPU MREC | Ad Revenue_mrec ÷ Active Users_mrec | Сколько рекламной выручки в среднем приносит один пользователь MREC-рекламы? | — | ✓ | — |
| m63 | Ad ARPU Native | Ad Revenue_native ÷ Active Users_native | Сколько рекламной выручки в среднем приносит один пользователь native-рекламы? | — | ✓ | — |
| m64 | Ad ARPU Rewarded Video | Ad Revenue_rewarded ÷ Active Users_rewarded | Сколько рекламной выручки в среднем приносит один пользователь rewarded video-рекламы? | — | ✓ | — |

---

## In‑App Purchases

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| i1 | Paying Users | Count of unique devices with at least one IAP purchase during the selected period | Сколько платящих пользователей? | — | Pub | — |
| i2 | Paying User Conversion | Paying Users ÷ DAU × 100 | Конвертируем ли DAU в платящих? | — | Pub | — |
| i3 | IAP Revenue | Total revenue generated from in‑app purchases during the selected period | Сколько заработали на IAP? | — | Pub | — |
| i4 | Number of IAP Refunds | Number of in‑app purchase refunds during the selected period | Сколько рефандов? | — | Pub | — |
| i5 | Sum of IAP Refunds | Total monetary amount of in‑app purchase refunds during the selected period | Сумма рефандов? | — | Pub | — |
| i6 | IAP Revenue before fees | In‑app purchase revenue before platform fees are deducted | Доход до комиссии платформы? | — | Pub | — |
| i7 | IAP Revenue After Refunds Without Subscriptions | In‑app purchase revenue after refunds, excluding subscription revenue | Чистый IAP без подписок? | — | Pub | — |
| i8 | Number of Purchases | Total number of in‑app purchase transactions during the selected period | Сколько покупок? | — | Pub | — |
| i9 | Number of Purchases per User | Number of Purchases ÷ Active Users | Покупок на пользователя? | — | Pub | — |
| i10 | Number of Purchases per Paying User | Number of Purchases ÷ Paying Users | Покупок на платящего? | — | Pub | — |
| i11 | IAP ARPU | IAP Revenue ÷ Active Users | IAP-доход на пользователя? | — | Pub | — |
| i12 | IAP ARPPU | IAP Revenue ÷ Paying Users | IAP-доход на платящего? | — | Pub | — |

---

## Session Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| s1 | Ad Session Length | Average ad session length for the selected period. Ad session is the period from session start to last shown impression | Длина ad-сессии? | — | ✓ | — |
| s2 | Session Length | Average total session duration for the selected period | Длина сессии? | — | ✓ | — |
| s3 | Time per User (Ad Session) | Total ad session time ÷ Active Users | Время ad-сессий на пользователя? | — | ✓ | — |
| s4 | Time per User | Total session time ÷ Active Users | Время сессий на пользователя? | — | ✓ | — |
| s5 | Sessions per User | Total sessions ÷ Active Users | Сессий на пользователя? | — | ✓ | — |
| s6 | Impressions per Session | Total ad impressions ÷ Total sessions | Показов на сессию? | — | ✓ | — |
| s7 | Session Count (Total) | Total number of sessions during the selected period | Всего сессий? | — | ✓ | — |
| s8 | Ad Session Count (Total) | Total number of ad sessions during the selected period | Всего ad-сессий? | — | ✓ | — |

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| s1 | Ad Session Length | Average ad session length for the selected period. Ad session is the period from session start to last shown impression | — | — | ✓ | — |
| s2 | Session Length | Average total session duration for the selected period | — | — | ✓ | — |
| s3 | Time per User (Ad Session) | Total ad session time ÷ Active Users | — | — | ✓ | — |
| s4 | Time per User | Total session time ÷ Active Users | — | — | ✓ | — |
| s5 | Sessions per User | Total sessions ÷ Active Users | — | — | ✓ | — |
| s6 | Impressions per Session | Total ad impressions ÷ Total sessions | — | — | ✓ | — |
| s7 | Session Count (Total) | Total number of sessions during the selected period | — | — | ✓ | — |
| s8 | Ad Session Count (Total) | Total number of ad sessions during the selected period | — | — | ✓ | — |

---

## Retention Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| r1 | Retention D1 | Users D1 / Users D0 (% пользователей, вернувшихся на 1-й день) | Зацепила ли игра? | — | ✓ | ✓ |
| r2 | Retention D3 | Users D3 / Users D0 | Удерживаем ли в первые дни? | — | ✓ | ✓ |
| r3 | Retention D7 | Users D7 / Users D0 | Есть ли устойчивое удержание? | — | ✓ | — |
| r4 | Retention D14 | Users D14 / Users D0 | Остаются ли на 2 неделе? | — | ✓ | — |
| r5 | Retention D30 | Users D30 / Users D0 | Остаются ли через месяц? | — | Pub | — |
| r6 | Retention D60 | Users D60 / Users D0 | Долгосрочное удержание? | — | Pub | — |
| r7 | Retention D90 | Users D90 / Users D0 | Удержание через квартал? | — | Pub | — |
| r8 | Rolling Retention D7 | Users active D0-D7 / Users D0 | Сколько были активны хотя бы раз за неделю? | — | Pub | — |
| r9 | Rolling Retention D30 | Users active D0-D30 / Users D0 | Сколько были активны хотя бы раз за месяц? | — | Pub | — |
| r10 | Churn Rate D7 | 1 - Retention D7 | Какой % теряем к 7 дню? | — | ✓ | — |
| r11 | Churn Rate D30 | 1 - Retention D30 | Какой % теряем к 30 дню? | — | Pub | — |
| r12 | Stickiness | DAU / MAU | Насколько часто пользователи возвращаются? | — | ✓ | — |
| r13 | Avg Lifetime Days | Среднее количество дней активности пользователя | Сколько дней в среднем живёт пользователь? | — | Pub | — |

---

## Cohort Session Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| cs0 | Time per User (Ad Session) — Lifetime | Average ad session time per user over full lifetime (cohort lifetime view) | Какова суммарная ad‑вовлечённость пользователя за жизнь? | — | Pub | — |
| cs1 | Time per User (Lifetime) | Average total session time per user over full lifetime (cohort lifetime view) | Насколько пользователь вовлечён за весь жизненный цикл? | — | Pub | — |
| cs2 | Time per User (Ad Session) — Daily | Average ad session time per user per day (daily cohort view) | Как меняется ad‑вовлечённость по дням жизни? | — | Pub | — |
| cs3 | Time per User (Ad Session) — Monthly | Average ad session time per user per month (monthly cohort view) | Как меняется ad‑вовлечённость по месяцам жизни? | — | Pub | — |
| cs4 | Time per User — Daily | Average total session time per user per day (daily cohort view) | Как растёт/падает вовлечённость со временем? | — | Pub | — |
| cs5 | Time per User — Monthly | Average total session time per user per month (monthly cohort view) | Есть ли долгосрочный engagement? | — | Pub | — |
| cs6 | Sessions per User — Lifetime | Total sessions ÷ Lifetime Active Users | Насколько часто пользователь возвращается за жизнь? | — | Pub | — |
| cs7 | Sessions per User — Daily | Average sessions per user per day (cohort) | Как меняется частота сессий по дням жизни? | — | Pub | — |
| cs8 | Sessions per User — Monthly | Average sessions per user per month (cohort) | Как меняется частота сессий по месяцам жизни? | — | Pub | — |

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| cs0 | Time per User (Ad Session) — Lifetime | Average ad session time per user over full lifetime (cohort lifetime view) | Какова суммарная ad‑вовлечённость пользователя за жизнь? | — | Pub | — |
| cs1 | Time per User (Lifetime) | Average total session time per user over full lifetime (cohort lifetime view) | Насколько пользователь вовлечён за весь жизненный цикл? | — | Pub | — |
| cs2 | Time per User (Ad Session) — Daily | Average ad session time per user per day (daily cohort view) | Как меняется ad‑вовлечённость по дням жизни? | — | Pub | — |
| cs3 | Time per User (Ad Session) — Monthly | Average ad session time per user per month (monthly cohort view) | Как меняется ad‑вовлечённость по месяцам жизни? | — | Pub | — |
| cs4 | Time per User — Daily | Average total session time per user per day (daily cohort view) | Как растёт/падает вовлечённость со временем? | — | Pub | — |
| cs5 | Time per User — Monthly | Average total session time per user per month (monthly cohort view) | Есть ли долгосрочный engagement? | — | Pub | — |
| cs6 | Sessions per User — Lifetime | Total sessions ÷ Lifetime Active Users | Насколько часто пользователь возвращается за жизнь? | — | Pub | — |
| cs7 | Sessions per User — Daily | Average sessions per user per day (cohort) | Как меняется частота сессий по дням жизни? | — | Pub | — |
| cs8 | Sessions per User — Monthly | Average sessions per user per month (cohort) | Как меняется частота сессий по месяцам жизни? | — | Pub | — |

---

## Impressions Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| im1 | Impressions per User | Average number of ad impressions displayed per active user during the selected period | Сколько рекламы в среднем видит один пользователь? | ✓ | ✓ | — |
| im2 | Impressions per User — Interstitial (Daily) | Interstitial Impressions (Daily) ÷ Active Users | Сколько interstitial‑показов получает пользователь в день? | — | ✓ | — |
| im3 | Impressions per User — Interstitial (Monthly) | Interstitial Impressions (Monthly) ÷ Active Users | Сколько interstitial‑показов получает пользователь в месяц? | — | ✓ | — |
| im4 | Impressions per User — Rewarded Video (Daily) | Rewarded Impressions (Daily) ÷ Active Users | Сколько rewarded‑показов получает пользователь в день? | — | ✓ | — |
| im5 | Impressions per User — Rewarded Video (Monthly) | Rewarded Impressions (Monthly) ÷ Active Users | Сколько rewarded‑показов получает пользователь в месяц? | — | ✓ | — |
| im6 | Impressions per User — Banner (Daily) | Banner Impressions (Daily) ÷ Active Users | Сколько banner‑показов получает пользователь в день? | — | ✓ | — |
| im7 | Impressions per User — Banner (Monthly) | Banner Impressions (Monthly) ÷ Active Users | Сколько banner‑показов получает пользователь в месяц? | — | ✓ | — |
| im8 | Impressions per User — MREC (Daily) | MREC Impressions (Daily) ÷ Active Users | Сколько MREC‑показов получает пользователь в день? | — | ✓ | — |
| im9 | Impressions per User — MREC (Monthly) | MREC Impressions (Monthly) ÷ Active Users | Сколько MREC‑показов получает пользователя в месяц? | — | ✓ | — |
| im10 | CTR — Interstitial | Clicks_interstitial ÷ Impressions_interstitial × 100 | Насколько кликабельны interstitial‑объявления? | — | ✓ | — |
| im11 | CTR — Interstitial (Daily) | Clicks_interstitial (Daily) ÷ Impressions_interstitial (Daily) × 100 | Как меняется CTR interstitial по дням? | — | ✓ | — |
| im12 | CTR — Interstitial (Monthly) | Clicks_interstitial (Monthly) ÷ Impressions_interstitial (Monthly) × 100 | Как меняется CTR interstitial по месяцам? | — | ✓ | — |
| im13 | CTR — Banner | Clicks_banner ÷ Impressions_banner × 100 | Насколько кликабельны баннеры? | — | ✓ | — |
| im14 | CTR — Banner (Daily) | Clicks_banner (Daily) ÷ Impressions_banner (Daily) × 100 | Как меняется CTR баннеров по дням? | — | ✓ | — |
| im15 | CTR — Banner (Monthly) | Clicks_banner (Monthly) ÷ Impressions_banner (Monthly) × 100 | Как меняется CTR баннеров по месяцам? | — | ✓ | — |
| im16 | CTR — MREC | Clicks_mrec ÷ Impressions_mrec × 100 | Насколько кликабельны MREC‑объявления? | — | ✓ | — |
| im17 | CTR — MREC (Daily) | Clicks_mrec (Daily) ÷ Impressions_mrec (Daily) × 100 | Как меняется CTR MREC по дням? | — | ✓ | — |
| im18 | CTR — MREC (Monthly) | Clicks_mrec (Monthly) ÷ Impressions_mrec (Monthly) × 100 | Как меняется CTR MREC по месяцам? | — | ✓ | — |
| im19 | CTR — Rewarded Video | Clicks_rewarded ÷ Impressions_rewarded × 100 | Насколько кликабелен rewarded video? | — | ✓ | — |
| im20 | CTR — Rewarded Video (Daily) | Clicks_rewarded (Daily) ÷ Impressions_rewarded (Daily) × 100 | Как меняется CTR rewarded video по дням? | — | ✓ | — |
| im21 | CTR — Rewarded Video (Monthly) | Clicks_rewarded (Monthly) ÷ Impressions_rewarded (Monthly) × 100 | Как меняется CTR rewarded video по месяцам? | — | ✓ | — |

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| im1 | Impressions per User | Average number of ad impressions displayed per active user | Сколько рекламы видит пользователь? | ✓ | ✓ | — |
| im2 | Impressions per User — Interstitial (Daily) | Interstitial Impressions (Daily) ÷ Active Users | Сколько interstitial показов на пользователя в день? | — | ✓ | — |
| im3 | Impressions per User — Interstitial (Monthly) | Interstitial Impressions (Monthly) ÷ Active Users | Сколько interstitial показов на пользователя в месяц? | — | ✓ | — |
| im4 | Impressions per User — Rewarded Video (Daily) | Rewarded Impressions (Daily) ÷ Active Users | Сколько rewarded‑показов на пользователя в день? | — | ✓ | — |
| im5 | Impressions per User — Rewarded Video (Monthly) | Rewarded Impressions (Monthly) ÷ Active Users | Сколько rewarded‑показов на пользователя в месяц? | — | ✓ | — |
| im6 | Impressions per User — Banner (Daily) | Banner Impressions (Daily) ÷ Active Users | Сколько banner‑показов на пользователя в день? | — | ✓ | — |
| im7 | Impressions per User — Banner (Monthly) | Banner Impressions (Monthly) ÷ Active Users | Сколько banner‑показов на пользователя в месяц? | — | ✓ | — |
| im8 | Impressions per User — MREC (Daily) | MREC Impressions (Daily) ÷ Active Users | Сколько MREC‑показов на пользователя в день? | — | ✓ | — |
| im9 | Impressions per User — MREC (Monthly) | MREC Impressions (Monthly) ÷ Active Users | Сколько MREC‑показов на пользователя в месяц? | — | ✓ | — |
| im10 | CTR — Interstitial | Clicks_interstitial ÷ Impressions_interstitial × 100 | Насколько кликабельны interstitial? | — | ✓ | — |
| im11 | CTR — Interstitial (Daily) | Clicks_interstitial (Daily) ÷ Impressions_interstitial (Daily) × 100 | Как меняется CTR interstitial по дням? | — | ✓ | — |
| im12 | CTR — Interstitial (Monthly) | Clicks_interstitial (Monthly) ÷ Impressions_interstitial (Monthly) × 100 | Как меняется CTR interstitial по месяцам? | — | ✓ | — |
| im13 | CTR — Banner | Clicks_banner ÷ Impressions_banner × 100 | Насколько кликабельны баннеры? | — | ✓ | — |
| im14 | CTR — Banner (Daily) | Clicks_banner (Daily) ÷ Impressions_banner (Daily) × 100 | Как меняется CTR баннеров по дням? | — | ✓ | — |
| im15 | CTR — Banner (Monthly) | Clicks_banner (Monthly) ÷ Impressions_banner (Monthly) × 100 | Как меняется CTR баннеров по месяцам? | — | ✓ | — |
| im16 | CTR — MREC | Clicks_mrec ÷ Impressions_mrec × 100 | Насколько кликабельны MREC? | — | ✓ | — |
| im17 | CTR — MREC (Daily) | Clicks_mrec (Daily) ÷ Impressions_mrec (Daily) × 100 | Как меняется CTR MREC по дням? | — | ✓ | — |
| im18 | CTR — MREC (Monthly) | Clicks_mrec (Monthly) ÷ Impressions_mrec (Monthly) × 100 | Как меняется CTR MREC по месяцам? | — | ✓ | — |
| im19 | CTR — Rewarded Video | Clicks_rewarded ÷ Impressions_rewarded × 100 | Насколько кликабелен rewarded video? | — | ✓ | — |
| im20 | CTR — Rewarded Video (Daily) | Clicks_rewarded (Daily) ÷ Impressions_rewarded (Daily) × 100 | Как меняется CTR rewarded по дням? | — | ✓ | — |
| im21 | CTR — Rewarded Video (Monthly) | Clicks_rewarded (Monthly) ÷ Impressions_rewarded (Monthly) × 100 | Как меняется CTR rewarded по месяцам? | — | ✓ | — |


---

## Network Metrics

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| n1 | Network Revenue | Revenue from specific ad network | Сколько приносит сеть? | — | ✓ | — |
| n2 | Network eCPM | Revenue_net ÷ Impr_net × 1000 | Какая сеть платит лучше? | — | ✓ | — |
| n3 | Network Fill Rate | Filled_net ÷ Requests_net | Какая сеть заполняет лучше? | — | ✓ | — |
| n4 | Network SoV | Impr_net ÷ Total_impr | Какая доля показов у сети? | — | ✓ | — |
| n5 | Network Latency | Avg response time (ms) | Тормозит ли сеть показы? | — | ✓ | — |
| n6 | Network Win Rate | Auctions won ÷ Auctions participated | Как часто сеть выигрывает аукцион? | — | ✓ | — |
| n7 | Network Bid Price | Avg bid in auction | Сколько сеть готова платить? | — | ✓ | — |
| n8 | Network CTR | Clicks_net ÷ Impr_net | Качественный ли трафик сети? | — | ✓ | — |
| n9 | Network Render Rate | Rendered ÷ Loaded | Показывается ли загруженная реклама? | — | ✓ | — |
| n10 | Bidding vs Waterfall | Revenue split by auction type | Что эффективнее — bidding или waterfall? | — | ✓ | — |

---

## Experimentation

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| m24 | Experiment ID | Experiment identifier | К какому тесту относятся данные? | — | Pub | — |
| m25 | Cohort ID | User → Test / Control | Пользователь в одной когорте? | — | Pub | — |
| m26 | ARPDAU uplift % | (Test − Control) / Control | Дал ли тест прирост? | — | Pub | — |
| m27 | Revenue uplift $ | ARPDAU uplift × DAU | Сколько денег дал тест? | — | Pub | — |
| m28 | DAU Parity | DAU_test vs control | Валиден ли эксперимент? | — | Pub | — |
| m29 | Stability D1/D3/D7 | Uplift over time | Устойчив ли результат? | — | Pub | — |
| m30 | Rollback Flag | Auto yes / no | Нужно ли откатить тест? | — | Pub | — |

---

## User Acquisition (UA)

| ID | Метрика | Описание / Формула | Бизнес-вопрос | L1 | L2 | PubC |
|----|--------|--------------------|---------------|----|----|------|
| m31 | UA Cost | Installs × CPI | Сколько тратим на трафик? | — | Pub | — |
| m32 | Installs | New Users | Сколько привели юзеров? | — | Pub | — |
| m33 | CPI | Cost ÷ Installs | Сколько стоит юзер? | — | Pub | ✓ |
| m34 | ROAS D7 / D30 | Revenue ÷ Cost | Окупается ли трафик? | — | Pub | ✓ |
| m35 | Payback Days | Day when ROAS = 100% | Когда вернём инвестиции? | — | Pub | — |
| m43 | ROAS, To-Date | Cumulative Total Revenue (Ad + IAP) ÷ UA Spend × 100% (from install date to current moment) | Окупился ли трафик на текущий момент? | — | Pub | — |
| m44 | Profit (Calendar) | Total Revenue − UA Spend (calculated for a specific calendar day or selected period) | Прибыльны ли мы за выбранный день или период? | — | Pub | — |
| m45 | ATT Opt-In Rate | Percentage of users who select "Allow" when presented with the App Tracking Transparency (ATT) prompt | Какой процент пользователей разрешает трекинг (ATT)? | — | Pub | — |

---

## Сводка по уровням доступа

| Уровень | Количество метрик | Фокус |
|---------|-------------------|-------|
| PubC | 7 + 5○ | Валидация: DAU, Active Users, Retention D1/D3, CPI, ROAS, Session Length. Планируется: Revenue, ARPDAU, eCPM, Impressions |
| L1 | 12 | Базовая монетизация: + Fill Rate, CTR, Impressions/DAU |
| L2 | 70+ | Углублённая аналитика: сессии, retention (D1-D14, Stickiness), детализация по типам рекламы, сети |
| Pub | 100+ | Полная картина: когорты, LTV, retention (D30-D90), IAP, UA, эксперименты |
