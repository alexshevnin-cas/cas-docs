# CAS.AI — Карта компонентов

> **Версия:** 1.1
> **Дата:** 2026-02-24
> **Источник:** roadmap v3.0, план CTO, Trello SDK, OneBI прототип

---

## 1. Общая архитектура платформы

```mermaid
graph TB
    subgraph CLIENTS["КЛИЕНТЫ"]
        L1["L1 базовый"]
        L2["L2 продвинутый"]
        PubC["PubC кандидат"]
        Pub["Pub паблишер"]
    end

    subgraph INTERNAL["ВНУТРЕННИЕ РОЛИ"]
        Admin["Admin"]
        AM["Account Manager"]
        BD["BizDev"]
        CLev["C-level"]
    end

    subgraph PLATFORM["ЦАРЬ-ПЛАТФОРМА OneBI"]
        QV["Quick View"]
        REP["Reports"]
        ADMIND["Admin Dashboard"]
        AMPERF["AM Performance"]
        PUBD["Pub Dashboard"]
        PAY["Payments"]
        FUNNEL["Marketing Funnel"]
        ONBOARD["Onboarding"]
        HEALTH["Product Health"]
    end

    subgraph DATA["DATA PLATFORM"]
        CH["ClickHouse"]
        MV["Materialized Views"]
        ILRD["ILRD Processing"]
        SEM["Semantic Layer"]
        EVT["Event Server"]
        BXCON["Bitrix Connector"]
    end

    subgraph SDKC["SDK PRODUCTS"]
        SDK["CAS SDK v4"]
        PUBSDK["Publishing SDK"]
        SB["Server Bidding"]
    end

    subgraph SSPC["CAS SSP"]
        EX["CAS Exchange"]
        SSPCMS["SSP CMS"]
    end

    subgraph FINSYS["FINANCE"]
        F1C["1C legacy"]
        BILL["Billing"]
    end

    subgraph CRMSYS["CRM"]
        BX["Bitrix24"]
        HS["HubSpot"]
    end

    subgraph MKT["MARKETING"]
        SITE["cas.ai"]
    end

    subgraph NETS["AD NETWORKS"]
        ADMOB["AdMob"]
        APPL["AppLovin"]
        UADS["Unity Ads"]
        IRON["ironSource"]
        METAN["Meta AN"]
    end

    L1 & L2 --> QV & REP
    Pub --> PUBD
    PubC --> ONBOARD
    CLev --> FUNNEL & ADMIND
    Admin --> ADMIND
    AM --> AMPERF
    BD --> FUNNEL

    QV & REP --> MV
    ADMIND --> MV
    PUBD --> ILRD
    FUNNEL --> BXCON
    AMPERF --> BXCON
    HEALTH --> ILRD & EVT
    PAY --> BILL

    MV --> CH
    ILRD --> CH
    EVT --> CH
    SEM --> CH
    BXCON --> CH

    SDK -->|ILRD| CH
    SDK -->|events| EVT
    PUBSDK --> SDK
    SB -->|auction logs| CH

    SDK --- ADMOB & APPL & UADS & IRON & METAN
    SB --> ADMOB & APPL

    EX --- SDK
    SSPCMS --> EX

    F1C -->|migration| CH
    BILL --> F1C

    BX -->|API| BXCON
    HS -.-> BX
    SITE -->|signup| BX

    classDef done fill:#1a472a,stroke:#42b983,color:#fff
    classDef wip fill:#2a3a5c,stroke:#58A6FF,color:#fff
    classDef planned fill:#3a2a1a,stroke:#d29922,color:#fff
    classDef legacy fill:#4a1a1a,stroke:#f85149,color:#fff

    class SDK,EX,BX,HS,SITE,BILL,ADMOB,APPL,UADS,IRON,METAN done
    class MV,SB,PUBSDK,QV,REP wip
    class ILRD,SEM,EVT,BXCON,ADMIND,AMPERF,PUBD,FUNNEL,PAY,ONBOARD,HEALTH,SSPCMS planned
    class F1C legacy
```

Легенда: зеленый = продакшен, синий = в работе, оранжевый = планируется, красный = legacy

---

## 2. Поток данных

```mermaid
flowchart LR
    subgraph SRC["ИСТОЧНИКИ"]
        S1["CAS SDK"]
        S2["Ad Networks"]
        S3["Bitrix24"]
        S4["1C"]
        S5["Google Ads"]
        S6["MMP"]
    end

    subgraph ING["INGESTION"]
        I1["ILRD Pipeline"]
        I2["Network ETL"]
        I3["Bitrix API"]
        I4["1C Export"]
        I5["Spend Import"]
        I6["MMP Adapter"]
    end

    subgraph STORE["STORAGE"]
        RAW["ClickHouse raw"]
        MAT["Materialized Views"]
        SEML["Semantic Layer"]
    end

    subgraph APIL["API"]
        REST["REST API JSON"]
    end

    subgraph UIL["UI OneBI"]
        U1["Quick View"]
        U2["Reports"]
        U3["Admin"]
        U4["Marketing Funnel"]
        U5["Payments"]
    end

    S1 --> I1
    S2 --> I2
    S3 --> I3
    S4 --> I4
    S5 --> I5
    S6 --> I6

    I1 & I2 & I3 & I4 & I5 & I6 --> RAW
    RAW --> MAT --> SEML --> REST
    REST --> U1 & U2 & U3 & U4 & U5

    classDef done fill:#1a472a,stroke:#42b983,color:#fff
    classDef wip fill:#2a3a5c,stroke:#58A6FF,color:#fff
    classDef planned fill:#3a2a1a,stroke:#d29922,color:#fff

    class S1,S2,S3,S4 done
    class I2,RAW,MAT wip
    class I1,I3,I4,I5,I6,SEML,REST,U1,U2,U3,U4,U5,S5,S6 planned
```

---

## 3. Маркетинговая воронка

```mermaid
flowchart TD
    subgraph CHAN["КАНАЛЫ"]
        C1["Google Ads"]
        C2["Organic SEO"]
        C3["Referral"]
        C4["Conferences"]
        C5["Content"]
    end

    subgraph ACQ["ПРИВЛЕЧЕНИЕ"]
        LAND["Landing cas.ai"]
        SIGN["Signup"]
    end

    subgraph CRM["CRM Bitrix24"]
        LEAD["Lead - 3111 per 18mo"]
        QUAL["Qualification - 88% drop"]
        ASSIGN["Assign AM"]
    end

    subgraph ONB["ONBOARDING"]
        SDKI["SDK Integration"]
        FDATA["First Data"]
        MSET["Monetization Setup"]
    end

    subgraph REV["REVENUE OneBI"]
        FREV["First Revenue"]
        MRR["MRR Growth"]
        UPS["Upsell L1-L2-Pub"]
    end

    subgraph DASH["C-LEVEL DASHBOARD P13"]
        M1["CAC by channel"]
        M2["Conversion by stage"]
        M3["Time to first revenue"]
        M4["LTV by channel"]
        M5["Marketing ROI"]
        M6["AM effectiveness"]
    end

    C1 & C2 & C3 & C4 & C5 -->|utm| LAND
    LAND --> SIGN
    SIGN -->|webhook| LEAD
    LEAD --> QUAL
    QUAL -->|12% pass| ASSIGN
    ASSIGN --> SDKI
    SDKI --> FDATA
    FDATA --> MSET
    MSET --> FREV
    FREV --> MRR
    MRR --> UPS

    LEAD -.->|D10 Bitrix connector| M2 & M6
    FREV -.->|D12 attribution| M3 & M4
    C1 & C2 & C3 & C4 & C5 -.->|D11 spend data| M1 & M5

    style QUAL fill:#4a1a1a,stroke:#f85149,color:#fff
```

---

## 4. SDK и рекламные сети

```mermaid
flowchart TB
    subgraph APP["MOBILE APP"]
        CASSDK["CAS SDK v4"]
        PSDK["Publishing SDK"]
    end

    subgraph AUC["AUCTION"]
        WF["Waterfall client-side"]
        SBAUC["Server Bidding s2s"]
    end

    subgraph SSPE["CAS SSP"]
        CASEX["CAS Exchange"]
        VAST4["VAST 3.0-4.0+"]
        VPAID["VPAID"]
        NATV["Native Ads"]
    end

    subgraph SBDONE["SB Done"]
        NC["Chartboost"]
    end

    subgraph SBPLAN["SB Stage 1"]
        NL["Liftoff"]
        NI["inMobi"]
        NM["Mintegral"]
        NP["Pangle"]
        NY["Yandex"]
    end

    subgraph WFNET["Waterfall Only"]
        NA["AdMob"]
        NAL["AppLovin"]
        NU["Unity Ads"]
        NIS["ironSource"]
        NME["Meta AN"]
    end

    subgraph DATAOUT["DATA OUTPUT"]
        ILRDO["ILRD to ClickHouse"]
        EVTO["Events to Event Server"]
        NRO["Network Reports"]
    end

    PSDK --> CASSDK
    CASSDK --> WF
    CASSDK --> SBAUC
    CASSDK --> CASEX
    CASEX --> VAST4 & VPAID & NATV

    WF --> NA & NAL & NU & NIS & NME
    SBAUC --> NC & NL & NI & NM & NP & NY

    CASSDK -->|impression-level| ILRDO
    CASSDK -->|session, IAP| EVTO
    NA & NAL & NU -->|daily| NRO

    classDef done fill:#1a472a,stroke:#42b983,color:#fff
    classDef wip fill:#2a3a5c,stroke:#58A6FF,color:#fff
    classDef planned fill:#3a2a1a,stroke:#d29922,color:#fff

    class CASSDK,CASEX,NA,NAL,NU,NIS,NME,NC done
    class SBAUC,PSDK,VAST4 wip
    class VPAID,NATV,NL,NI,NM,NP,NY planned
```

---

## 5. Платформа — views по ролям

```mermaid
flowchart TB
    subgraph B2BV["B2B VIEWS"]
        VQV["Quick View - MVP"]
        VREP["Reports - MVP"]
        VPAY["Payments - F1"]
        VL2["L2 Features - P2"]
        VPUB["Pub Dashboard - P5"]
        VPUBC["PubC Portal - P4"]
        VONB["Onboarding - P3"]
    end

    subgraph INTV["INTERNAL VIEWS"]
        VADM["Admin Dashboard - P6"]
        VAM["AM Performance - P14"]
        VFUN["Marketing Funnel - P13"]
        VHL["Product Health - P11"]
    end

    subgraph SSPV["SSP VIEWS"]
        VCMS["SSP CMS - SSP-3"]
        VSAN["SSP Analytics - SSP-4"]
    end

    RL1["L1"] --> VQV & VREP & VPAY
    RL2["L2"] --> VQV & VREP & VPAY & VL2
    RPUB["Pub"] --> VQV & VREP & VPAY & VPUB
    RPC["PubC"] --> VONB & VPUBC & VQV
    RCEO["CEO"] --> VADM & VFUN & VAM
    RADM["Admin"] --> VADM & VHL & VREP
    RAM["AM"] --> VAM & VHL & VREP
    RBD["BD"] --> VFUN & VADM

    classDef wip fill:#2a3a5c,stroke:#58A6FF,color:#fff
    classDef planned fill:#3a2a1a,stroke:#d29922,color:#fff

    class VQV,VREP wip
    class VPAY,VL2,VPUB,VPUBC,VONB,VADM,VAM,VFUN,VHL,VCMS,VSAN planned
```

---

## 6. Критический путь — timeline

```mermaid
gantt
    title CAS.AI Roadmap 2026
    dateFormat YYYY-MM-DD
    axisFormat %b

    section Org
    Team formation              :org1, 2026-01-01, 2026-03-31
    Bus factor elimination      :org2, 2026-02-01, 2026-06-30

    section Core SDK
    SDK stability               :c1, 2026-01-01, 2026-12-31
    Server Bidding Stage 1      :crit, sb1, 2026-01-15, 2026-04-30
    Server Bidding Stage 2      :sb2, after sb1, 60d
    Publishing SDK              :c18, 2026-02-01, 2026-05-31
    Cross Promo                 :c19, 2026-03-01, 2026-08-31

    section SSP
    Exchange VAST VPAID         :ssp1, 2026-02-01, 2026-07-31
    SSP new formats             :ssp2, after ssp1, 90d

    section Data
    Materialized Views          :crit, d1, 2026-02-01, 2026-04-30
    Self-hosted ClickHouse      :d2, 2026-03-01, 2026-06-30
    ILRD Processing             :crit, d3, after d1, 150d
    Event Server                :d7, 2026-04-01, 2026-09-30
    1C to ClickHouse            :d9, 2026-06-01, 2026-10-31
    Bitrix connector            :d10, after d1, 90d
    Attribution bridge          :d12, after d10, 90d

    section Portal
    MVP BI                      :crit, p1, after d1, 60d
    Admin Dashboard             :p6, after p1, 90d
    L2 Features                 :crit, p2, after d3, 60d
    Onboarding                  :p3, after p1, 120d
    Marketing Funnel            :p13, after d12, 90d
    Platform release            :milestone, p7, 2026-11-30, 0d

    section Finance
    Payments UI                 :f1, 2026-04-01, 2026-06-30
    1C migration                :f4, 2026-07-01, 2026-11-30

    section Growth
    SOURCE_ID cleanup           :g12, 2026-03-01, 2026-04-30
    Landings                    :g1, 2026-03-01, 2026-04-15
    Content machine             :g3, 2026-03-01, 2026-12-31
    Channel attribution         :g13, after g12, 90d
```

---

## 7. Команды и зоны

```mermaid
flowchart LR
    subgraph CTO["Vova CTO"]
        TINF["Infrastructure"]
        TBE["Core Backend"]
        TCMS["CMS Dev"]
    end

    subgraph SDKL["Denis SDK Lead"]
        TCLI["Client Side"]
        TSDK["CAS SDK"]
        TSB["Server Bidding"]
        TEX["CAS Exchange"]
    end

    subgraph DATAL["Boris Data Lead"]
        TDE["Data Engineering"]
        TCH["ClickHouse"]
        TILRD["ILRD"]
        TEVT["Event Server"]
    end

    subgraph FRONT["Ruslan Frontend"]
        TOBI["OneBI Platform"]
    end

    subgraph PROD["Alexei PO"]
        TSPEC["Specs"]
        TUX["UX Prototype"]
        TQA["QA"]
    end

    subgraph MKTL["Nikita Marketing"]
        TSITE["cas.ai"]
        TCONT["Content"]
    end

    subgraph FINL["Tolik Finance"]
        T1C["1C System"]
        TREF["Referral"]
    end

    TINF -.->|CI/CD| TSDK & TOBI & TCH
    TBE -.->|API| TOBI
    TCLI --> TSDK & TSB & TEX
    TDE --> TCH & TILRD & TEVT
    TCH -->|data| TOBI
    TSPEC -->|specs| TOBI & TSDK

    style CTO fill:#1a2a3a,stroke:#58A6FF
    style SDKL fill:#1a3a2a,stroke:#42b983
    style DATAL fill:#3a2a1a,stroke:#d29922
    style FRONT fill:#2a1a3a,stroke:#a371f7
    style PROD fill:#3a1a2a,stroke:#f778ba
    style MKTL fill:#1a3a3a,stroke:#39d2c0
    style FINL fill:#4a1a1a,stroke:#f85149
```

---

## Статусы компонентов — сводка

| Компонент | Статус | Владелец | Bus Factor |
|-----------|--------|----------|-----------|
| CAS SDK v4 | prod | Денис | 1 чел |
| CAS Exchange | prod | Денис | 1 чел |
| Server Bidding | WIP | Денис | 1 чел |
| Publishing SDK | WIP | Юра | 1 чел |
| B2B кабинет legacy | legacy | Вова/Руслан | - |
| OneBI прототип | WIP | Алексей | - |
| OneBI продакшен | planned | Руслан | 1 чел |
| ClickHouse | prod | Борис | 1 чел |
| Materialized Views | WIP | Борис | 1 чел |
| ILRD Processing | planned | Борис | 1 чел |
| Bitrix connector | planned | - | - |
| 1C | legacy | Толик | 1 чел |
| cas.ai сайт | prod | Женя 1нед/мес | partial |
| Bitrix24 | prod | AM team | ok |
| Superset | prod internal | Борис | 1 чел |

Bus factor критичен: 6 из 15 компонентов на одном человеке.
