"""
Bitrix CRM — full lead extraction with funnel timing analysis.

Extracts all leads, determines source (TRUE_ABOUT → SOURCE_ID → UTM_SOURCE),
gets stage transition history, calculates days between stages,
compares across 4 half-years: H2 2024, H1 2025, H2 2025, H1 2026.

Output:
  - 05-research/bitrix-funnel-extract.csv  (full raw data)
  - 05-research/bitrix-funnel-analysis.md  (analysis by half-year)
"""

import json
import csv
import time
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict
import statistics
import subprocess
import urllib.parse

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

env_file = Path(__file__).parent / ".env.crm"
env_vars = {}
for line in env_file.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, val = line.split("=", 1)
        env_vars[key.strip()] = val.strip().strip('"')

WEBHOOK = env_vars["BITRIX_WEBHOOK"]
OUT_DIR = Path(__file__).parent.parent / "05-research"

# TRUE_ABOUT enum mapping (UF_CRM_1734002585)
TRUE_ABOUT_MAP = {
    "573": "Google Ads",
    "563": "Client",
    "564": "TG Monetization",
    "565": "Oleg Shlyamovych",
    "566": "Reddit",
    "567": "YouTube",
    "568": "Turkish forum",
    "569": "Other",
    "570": "LinkedIn",
    "574": "Evgeny Grishakov",
    "575": "Conference",
    "601": "Second Account",
    "604": "Organic Search",
    "617": "BD Igor Maiorov",
    "577": "BD Zoriana Omelchuk",
}

# SOURCE_ID mapping (from Bitrix CRM statuses)
SOURCE_MAP = {
    "CALL": "Facebook",
    "EMAIL": "TG Monetization",
    "STORE": "Google Ads",
    "ADVERTISING": "Reddit",
    "PARTNER": "YouTube",
    "WEBFORM": "LinkedIn",
    "UC_6ERC5J": "Instagram",
    "TRADE_SHOW": "Other",
    "2|TELEGRAM": "Conference",
    "WEB": "Oleg Shlyamovych",
    "OTHER": "Evgeny Grishakov",
    "3": "BD Abd elrahman Abbas",
    "4": "BD Zoriana Omelchuk",
    "UC_93QREH": "Publishing",
    "UC_NDXL17": "Client",
    "UC_D9LVEE": "Second Account",
}

# STATUS_ID → canonical label (exact as from crm.status.list)
# Will be populated from API at runtime
STATUS_LABELS = {}  # filled in extract()

# Funnel milestones for timing analysis (use STATUS_ID as keys)
MILESTONE_IDS = [
    "NEW",          # Не обработанные лиды
    "IN_PROCESS",   # Лиды в работе
    "UC_75KI16",    # Звонок BD
    "4",            # Собеседование
    "3",            # MQL
    "10",           # Создан Чат
    "11",           # Интеграция
    "5",            # A/B test
    "6",            # Прошел A/B test
    "CONVERTED",    # Успешный клиент СAS
]

# Rejection milestones (tracked separately, not in main funnel timing)
REJECTION_IDS = [
    "PROCESSED",    # Нет ответа
    "13",           # NON SQL
    "2",            # NON MQL
    "7",            # Отказавшиеся
]

# Display labels for milestones (clean)
MILESTONE_LABELS = {
    "NEW": "NEW",
    "IN_PROCESS": "В работе",
    "UC_75KI16": "Звонок BD",
    "PROCESSED": "Нет ответа",
    "4": "Собеседование",
    "13": "NON SQL",
    "2": "NON MQL",
    "3": "MQL",
    "10": "Создан Чат",
    "11": "Интеграция",
    "5": "A/B test",
    "6": "Прошёл A/B",
    "7": "Отказавшиеся",
    "CONVERTED": "Клиент",
}

# Funnel depth order (for determining max stage)
STAGE_DEPTH = {
    "NEW": 0, "IN_PROCESS": 1, "UC_75KI16": 2, "PROCESSED": 3,
    "4": 4, "13": 5, "1": 6, "2": 7, "3": 8,
    "10": 9, "11": 10, "12": 11, "5": 12, "6": 13,
    "7": 14, "8": 15, "9": 16, "CONVERTED": 17, "JUNK": -1,
}

# Half-year definitions
HALVES = [
    ("H2 2024", date(2024, 7, 1), date(2024, 12, 31)),
    ("H1 2025", date(2025, 1, 1), date(2025, 6, 30)),
    ("H2 2025", date(2025, 7, 1), date(2025, 12, 31)),
    ("H1 2026", date(2026, 1, 1), date(2026, 6, 30)),
]

# Downloads enum
DOWNLOADS_MAP = {
    "293": "0-5K",
    "294": "5K-50K",
    "295": "50K+",
}

# Med/Pub enum
TYPE_MAP = {
    "909": "Mediation",
    "908": "Publishing",
}


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------


def api_get(url):
    """GET request via curl (bypasses macOS Python SSL issues)."""
    result = subprocess.run(
        ["curl", "-sk", "--max-time", "60", url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return json.loads(result.stdout)


def api_call(method, params=None):
    """Call Bitrix REST API with pagination (GET)."""
    base = f"{WEBHOOK}/{method}"
    all_results = []
    start = 0

    while True:
        p = dict(params or {})
        p["start"] = start
        qs = urllib.parse.urlencode(p, doseq=True)
        result = api_get(f"{base}?{qs}")

        items = result.get("result", [])
        all_results.extend(items)
        total = result.get("total", 0)
        nxt = result.get("next")

        print(f"  {method}: fetched {len(all_results)}/{total}", end="\r")

        if nxt is None or len(all_results) >= total:
            break
        start = nxt
        time.sleep(0.5)  # rate limit

    print(f"  {method}: {len(all_results)} total        ")
    return all_results


def get_status_list():
    """Get lead status labels."""
    result = api_get(f"{WEBHOOK}/crm.status.list")
    statuses = {}
    for s in result.get("result", []):
        if s.get("ENTITY_ID") == "STATUS":
            statuses[s["STATUS_ID"]] = s["NAME"]
    return statuses


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------


def extract():
    print("=== Bitrix CRM Full Extraction ===\n")

    # 1. Get status labels
    print("[1/3] Loading status labels...")
    status_labels = get_status_list()
    print(f"  {len(status_labels)} statuses loaded")

    # 2. Get all leads
    print("\n[2/3] Fetching all leads...")
    fields = [
        "ID", "TITLE", "STATUS_ID", "SOURCE_ID", "SOURCE_DESCRIPTION",
        "DATE_CREATE", "DATE_MODIFY", "DATE_CLOSED",
        "UF_CRM_1734002585",   # TRUE_ABOUT
        "UF_CRM_1722246548185", # Downloads
        "UF_CRM_1762858254",   # Med/Pub
        "UF_CRM_1723549442162", # Country
        "UTM_SOURCE", "UTM_MEDIUM", "UTM_CAMPAIGN",
        "ASSIGNED_BY_ID",
    ]
    params = {f"select[{i}]": f for i, f in enumerate(fields)}
    params["order[ID]"] = "asc"
    # Filter: created from 2024-07-01
    params["filter[>=DATE_CREATE]"] = "2024-07-01"

    leads = api_call("crm.lead.list", params)
    print(f"\n  Total leads: {len(leads)}")

    # 3. Get stage history for each lead (batch approach)
    print("\n[3/3] Fetching stage history...")
    lead_histories = {}
    batch_size = 50
    lead_ids = [l["ID"] for l in leads]

    for i in range(0, len(lead_ids), batch_size):
        batch_ids = lead_ids[i:i + batch_size]
        # Build batch request
        cmd = {}
        for j, lid in enumerate(batch_ids):
            cmd[f"cmd[h{j}]"] = (
                f"crm.stagehistory.list?"
                f"entityTypeId=1&"
                f"order[CREATED_TIME]=asc&"
                f"filter[OWNER_ID]={lid}"
            )

        try:
            qs = urllib.parse.urlencode(cmd, doseq=True)
            result = api_get(f"{WEBHOOK}/batch?{qs}")

            cmd_result = result.get("result", {}).get("result", {})
            for j, lid in enumerate(batch_ids):
                hist_data = cmd_result.get(f"h{j}", {})
                items = hist_data.get("items", []) if isinstance(hist_data, dict) else []
                lead_histories[lid] = items
        except Exception as e:
            print(f"  batch error at {i}: {e}")
            # Fallback: individual requests
            for lid in batch_ids:
                try:
                    items = api_call("crm.stagehistory.list", {
                        "entityTypeId": 1,
                        "order[CREATED_TIME]": "asc",
                        "filter[OWNER_ID]": lid,
                    })
                    lead_histories[lid] = items if isinstance(items, list) else items.get("items", [])
                except Exception:
                    lead_histories[lid] = []

        print(f"  histories: {min(i + batch_size, len(lead_ids))}/{len(lead_ids)}", end="\r")
        time.sleep(0.5)

    print(f"  histories: {len(lead_histories)} loaded        ")

    # ---------------------------------------------------------------------------
    # Process leads
    # ---------------------------------------------------------------------------
    print("\n=== Processing ===")

    rows = []
    for lead in leads:
        lid = lead["ID"]
        created = lead.get("DATE_CREATE", "")[:10]

        # Determine source (priority: TRUE_ABOUT → SOURCE_ID → UTM_SOURCE)
        true_about_id = lead.get("UF_CRM_1734002585") or ""
        source_id = lead.get("SOURCE_ID") or ""
        utm_source = lead.get("UTM_SOURCE") or ""

        if true_about_id and true_about_id in TRUE_ABOUT_MAP:
            source = TRUE_ABOUT_MAP[true_about_id]
            source_method = "true_about"
        elif source_id and source_id in SOURCE_MAP:
            source = SOURCE_MAP[source_id]
            source_method = "source_id"
        elif utm_source:
            # Normalize UTM
            utm_lower = utm_source.lower().strip()
            if "google" in utm_lower:
                source = "Google Ads"
            elif "facebook" in utm_lower or "fb" in utm_lower:
                source = "Facebook"
            elif "reddit" in utm_lower:
                source = "Reddit"
            elif "youtube" in utm_lower or "yt" in utm_lower:
                source = "YouTube"
            elif "telegram" in utm_lower or "tg" in utm_lower:
                source = "TG Monetization"
            elif "linkedin" in utm_lower:
                source = "LinkedIn"
            elif "organic" in utm_lower:
                source = "Organic Search"
            else:
                source = f"UTM:{utm_source}"
            source_method = "utm"
        else:
            source = "(не размечен)"
            source_method = "none"

        # Current status
        status_id = lead.get("STATUS_ID", "")
        status_name = status_labels.get(status_id, status_id)

        # Downloads, type
        downloads = DOWNLOADS_MAP.get(lead.get("UF_CRM_1722246548185", ""), "")
        lead_type = TYPE_MAP.get(lead.get("UF_CRM_1762858254", ""), "")

        # Stage history → transitions with dates (keyed by STATUS_ID)
        history = lead_histories.get(lid, [])
        stage_dates = {}  # STATUS_ID → first date reached

        if history:
            for item in history:
                sid = item.get("STATUS_ID", "")
                ts = item.get("CREATED_TIME", "")[:10]
                if sid and ts and sid not in stage_dates:
                    stage_dates[sid] = ts
        else:
            # Fallback: at least current status with create date
            if status_id:
                stage_dates[status_id] = created

        # Calculate days between milestones
        milestone_days = {}
        prev_mid = None
        prev_date = None
        for mid in MILESTONE_IDS:
            if mid in stage_dates:
                d = datetime.strptime(stage_dates[mid], "%Y-%m-%d").date()
                if prev_mid and prev_date:
                    key = f"{MILESTONE_LABELS[prev_mid]}→{MILESTONE_LABELS[mid]}"
                    milestone_days[key] = (d - prev_date).days
                prev_mid = mid
                prev_date = d

        # Total days (created → last known stage)
        if stage_dates:
            all_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in stage_dates.values()]
            total_days = (max(all_dates) - min(all_dates)).days
        else:
            total_days = 0

        # Determine half-year
        created_date = datetime.strptime(created, "%Y-%m-%d").date() if created else None
        half_year = ""
        if created_date:
            for label, start, end in HALVES:
                if start <= created_date <= end:
                    half_year = label
                    break

        # Max funnel stage reached (deepest)
        max_stage = ""
        max_depth = -1
        for sid in stage_dates:
            depth = STAGE_DEPTH.get(sid, -1)
            if depth > max_depth:
                max_depth = depth
                max_stage = status_labels.get(sid, sid)

        row = {
            "ID": lid,
            "Created": created,
            "HalfYear": half_year,
            "Source": source,
            "SourceMethod": source_method,
            "TrueAbout": TRUE_ABOUT_MAP.get(true_about_id, ""),
            "SourceID": SOURCE_MAP.get(source_id, source_id),
            "UTM": utm_source,
            "Status": status_name,
            "MaxStage": max_stage,
            "Downloads": downloads,
            "Type": lead_type,
            "TotalDays": total_days,
            "Title": lead.get("TITLE", ""),
        }

        # Add milestone timing columns
        for i in range(len(MILESTONE_IDS) - 1):
            key = f"{MILESTONE_LABELS[MILESTONE_IDS[i]]}→{MILESTONE_LABELS[MILESTONE_IDS[i+1]]}"
            row[key] = milestone_days.get(key, "")

        # Add stage dates (milestones + rejections)
        for mid in MILESTONE_IDS:
            row[f"date_{MILESTONE_LABELS[mid]}"] = stage_dates.get(mid, "")
        for rid in REJECTION_IDS:
            row[f"date_{MILESTONE_LABELS[rid]}"] = stage_dates.get(rid, "")

        rows.append(row)

    # ---------------------------------------------------------------------------
    # Save CSV
    # ---------------------------------------------------------------------------
    csv_path = OUT_DIR / "bitrix-funnel-extract.csv"
    if rows:
        fieldnames = list(rows[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nCSV saved → {csv_path} ({len(rows)} rows)")

    # ---------------------------------------------------------------------------
    # Build analysis
    # ---------------------------------------------------------------------------
    print("\n=== Building analysis ===")

    # Filter out Second Account
    rows = [r for r in rows if r["Source"] != "Second Account"]

    # Filter: only paid advertising
    AD_SOURCES = {"Google Ads", "Facebook"}
    ad_rows = [r for r in rows if r["Source"] in AD_SOURCES]

    md = []
    md.append("# Битрикс CRM — Воронка по рекламным каналам\n")
    md.append(f"**Дата выгрузки:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md.append(f"**Фильтр:** только реклама (Google Ads, Facebook)")
    md.append(f"**Лидов (реклама):** {len(ad_rows)} из {len(rows)} общих")
    md.append(f"**Период:** H2 2024 — H1 2026")
    md.append(f"**Источник приоритет:** TRUE_ABOUT → SOURCE_ID → UTM_SOURCE\n")

    # --- Volume by source × half-year ---
    md.append("## Объём лидов по полугодиям\n")

    source_totals = defaultdict(int)
    source_half = defaultdict(lambda: defaultdict(int))
    for r in ad_rows:
        src = r["Source"]
        hy = r["HalfYear"]
        source_totals[src] += 1
        if hy:
            source_half[src][hy] += 1

    sorted_sources = sorted(source_totals.keys(), key=lambda s: -source_totals[s])
    half_labels = [h[0] for h in HALVES]

    md.append("| Источник | " + " | ".join(half_labels) + " | Всего |")
    md.append("|----------|" + "|".join(["-----:" for _ in half_labels]) + "|------:|")
    for src in sorted_sources:
        cells = [str(source_half[src].get(h, "")) for h in half_labels]
        md.append(f"| {src} | " + " | ".join(cells) + f" | {source_totals[src]} |")
    total_cells = [str(sum(source_half[s].get(h, 0) for s in sorted_sources)) for h in half_labels]
    md.append(f"| **ИТОГО** | " + " | ".join(total_cells) + f" | {len(ad_rows)} |")
    md.append("")

    # --- Funnel by half-year ---
    md.append("## Воронка по полугодиям\n")

    ml = MILESTONE_LABELS  # shortcut

    for hy_label, _, _ in HALVES:
        hy_rows = [r for r in ad_rows if r["HalfYear"] == hy_label]
        if not hy_rows:
            continue

        md.append(f"### {hy_label} ({len(hy_rows)} лидов)\n")

        stage_counts = {}
        for mid in MILESTONE_IDS:
            lbl = ml[mid]
            cnt = sum(1 for r in hy_rows if r.get(f"date_{lbl}", ""))
            stage_counts[mid] = cnt

        # Also count rejections
        for rid in REJECTION_IDS:
            lbl = ml[rid]
            stage_counts[rid] = sum(1 for r in hy_rows if r.get(f"date_{lbl}", ""))

        md.append("| Этап | Достигли | % от всех | Шаг |")
        md.append("|------|--------:|----------:|----:|")
        prev_cnt = len(hy_rows)
        for mid in MILESTONE_IDS:
            cnt = stage_counts[mid]
            pct = cnt / len(hy_rows) * 100 if hy_rows else 0
            step = f"{cnt/prev_cnt*100:.0f}%" if prev_cnt > 0 and cnt > 0 else "—"
            md.append(f"| {ml[mid]} | {cnt} | {pct:.0f}% | {step} |")
            if cnt > 0:
                prev_cnt = cnt
        # Rejection row
        md.append("|  |  |  |  |")
        md.append("| **Отбраковка:** |  |  |  |")
        for rid in REJECTION_IDS:
            cnt = stage_counts[rid]
            pct = cnt / len(hy_rows) * 100 if hy_rows else 0
            md.append(f"| ↳ {ml[rid]} | {cnt} | {pct:.0f}% |  |")
        md.append("")

    # --- H1 2026 monthly breakdown ---
    md.append("### H1 2026 — помесячно\n")

    for month_num, month_name in [(1, "Январь 2026"), (2, "Февраль 2026")]:
        m_rows = [r for r in ad_rows
                  if r["HalfYear"] == "H1 2026"
                  and r["Created"][:7] == f"2026-{month_num:02d}"]
        if not m_rows:
            continue

        md.append(f"**{month_name}** ({len(m_rows)} лидов)\n")

        stage_counts = {}
        for mid in MILESTONE_IDS:
            lbl = ml[mid]
            stage_counts[mid] = sum(1 for r in m_rows if r.get(f"date_{lbl}", ""))
        for rid in REJECTION_IDS:
            lbl = ml[rid]
            stage_counts[rid] = sum(1 for r in m_rows if r.get(f"date_{lbl}", ""))

        md.append("| Этап | Достигли | % от всех | Шаг |")
        md.append("|------|--------:|----------:|----:|")
        prev_cnt = len(m_rows)
        for mid in MILESTONE_IDS:
            cnt = stage_counts[mid]
            pct = cnt / len(m_rows) * 100 if m_rows else 0
            step = f"{cnt/prev_cnt*100:.0f}%" if prev_cnt > 0 and cnt > 0 else "—"
            md.append(f"| {ml[mid]} | {cnt} | {pct:.0f}% | {step} |")
            if cnt > 0:
                prev_cnt = cnt
        md.append("|  |  |  |  |")
        md.append("| **Отбраковка:** |  |  |  |")
        for rid in REJECTION_IDS:
            cnt = stage_counts[rid]
            pct = cnt / len(m_rows) * 100 if m_rows else 0
            md.append(f"| ↳ {ml[rid]} | {cnt} | {pct:.0f}% |  |")
        md.append("")

    # --- Funnel by source × half-year ---
    md.append("## Воронка по каналам × полугодие\n")

    for src in sorted_sources:
        md.append(f"### {src}\n")
        for hy_label, _, _ in HALVES:
            hy_rows = [r for r in ad_rows if r["HalfYear"] == hy_label and r["Source"] == src]
            if not hy_rows:
                continue

            md.append(f"**{hy_label}** ({len(hy_rows)} лидов)\n")

            stage_counts = {}
            for mid in MILESTONE_IDS:
                lbl = ml[mid]
                cnt = sum(1 for r in hy_rows if r.get(f"date_{lbl}", ""))
                stage_counts[mid] = cnt

            md.append("| Этап | Достигли | % от всех |")
            md.append("|------|--------:|----------:|")
            for mid in MILESTONE_IDS:
                cnt = stage_counts[mid]
                pct = cnt / len(hy_rows) * 100 if hy_rows else 0
                md.append(f"| {ml[mid]} | {cnt} | {pct:.0f}% |")
            md.append("")

    # --- Timing analysis by half-year ---
    md.append("## Динамика воронки в днях\n")
    md.append("Медиана дней между стадиями (только рекламные лиды, дошедшие до стадии).\n")

    transitions = []
    for i in range(len(MILESTONE_IDS) - 1):
        transitions.append(f"{ml[MILESTONE_IDS[i]]}→{ml[MILESTONE_IDS[i+1]]}")

    md.append("| Переход | " + " | ".join(h[0] for h in HALVES) + " |")
    md.append("|---------|" + "|".join(["-----:" for _ in HALVES]) + "|")

    for trans in transitions:
        cells = []
        for hy_label, _, _ in HALVES:
            hy_rows = [r for r in ad_rows if r["HalfYear"] == hy_label]
            values = [r[trans] for r in hy_rows if r.get(trans, "") != "" and r[trans] != ""]
            values = [int(v) for v in values if str(v).lstrip("-").isdigit()]
            if values:
                med = statistics.median(values)
                cells.append(f"{med:.0f}d (n={len(values)})")
            else:
                cells.append("—")
        md.append(f"| {trans} | " + " | ".join(cells) + " |")
    md.append("")

    # --- Total lead-to-client days ---
    client_label = ml["CONVERTED"]
    md.append(f"### Общее время лид → {client_label}\n")
    md.append("| Полугодие | Медиана дней | Среднее дней | n |")
    md.append("|-----------|------------:|-------------:|--:|")

    for hy_label, _, _ in HALVES:
        hy_rows = [r for r in ad_rows if r["HalfYear"] == hy_label]
        client_rows = [r for r in hy_rows if r.get(f"date_{client_label}", "")]
        if client_rows:
            days = [r["TotalDays"] for r in client_rows if r["TotalDays"] > 0]
            if days:
                med = statistics.median(days)
                avg = statistics.mean(days)
                md.append(f"| {hy_label} | {med:.0f} | {avg:.0f} | {len(days)} |")
            else:
                md.append(f"| {hy_label} | — | — | 0 |")
        else:
            md.append(f"| {hy_label} | — | — | 0 |")
    md.append("")

    # --- Timing by source ---
    md.append("## Скорость воронки по каналам\n")
    md.append(f"Медиана дней NEW → {client_label}.\n")

    md.append("| Источник | Медиана | Среднее | n |")
    md.append("|----------|--------:|--------:|--:|")

    for src in sorted_sources:
        src_rows = [r for r in ad_rows if r["Source"] == src and r.get("date_Клиент", "")]
        if src_rows:
            days = [r["TotalDays"] for r in src_rows if r["TotalDays"] > 0]
            if days:
                med = statistics.median(days)
                avg = statistics.mean(days)
                md.append(f"| {src} | {med:.0f}d | {avg:.0f}d | {len(days)} |")
    md.append("")

    # --- Conversion by source × half-year ---
    md.append("## Конверсия по каналам и полугодиям\n")

    md.append("| Источник | " + " | ".join(h[0] for h in HALVES) + " |")
    md.append("|----------|" + "|".join(["----------:" for _ in HALVES]) + "|")

    for src in sorted_sources:
        cells = []
        for hy_label, _, _ in HALVES:
            hy_src = [r for r in ad_rows if r["Source"] == src and r["HalfYear"] == hy_label]
            clients = [r for r in hy_src if r.get("date_Клиент", "")]
            if hy_src:
                pct = len(clients) / len(hy_src) * 100
                cells.append(f"{len(clients)}/{len(hy_src)} ({pct:.0f}%)")
            else:
                cells.append("—")
        md.append(f"| {src} | " + " | ".join(cells) + " |")
    md.append("")

    # Save markdown
    md_path = OUT_DIR / "bitrix-funnel-analysis.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Analysis saved → {md_path}")

    print("\nDone!")


if __name__ == "__main__":
    extract()
