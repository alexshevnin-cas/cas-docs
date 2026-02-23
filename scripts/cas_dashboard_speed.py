"""
Measure CAS.AI dashboard load speed via Playwright.
Usage: python3 scripts/cas_dashboard_speed.py

Three test scenarios per account:
  1. Default mode  (/mediation)        — 30d + 180d
  2. Chart mode    (/mediation?mode=ch) — 30d + 180d
  3. Chart mode + extra table columns   — 30d + 180d
     (Application, Network, Platform, DAU, ARPDAU)

Each scenario tests: periods, View-by groupings, metric card switches,
and platform filters.

Reads accounts from scripts/.env.cas-accounts.
"""

import time
from datetime import datetime, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ACCOUNTS = []
env_file = Path(__file__).parent / ".env.cas-accounts"
if env_file.exists():
    env_vars = {}
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            env_vars[key.strip()] = val.strip().strip('"')
    i = 1
    while f"CAS_ACCOUNT_{i}_EMAIL" in env_vars:
        ACCOUNTS.append((
            env_vars[f"CAS_ACCOUNT_{i}_EMAIL"],
            env_vars[f"CAS_ACCOUNT_{i}_PASSWORD"],
        ))
        i += 1

if not ACCOUNTS:
    print("Error: no accounts found in scripts/.env.cas-accounts")
    print("Format:")
    print('  CAS_ACCOUNT_1_EMAIL="user@example.com"')
    print('  CAS_ACCOUNT_1_PASSWORD="password"')
    exit(1)

BASE = "https://b2b.cas.ai/mediation"
SCREENSHOTS_DIR = Path(__file__).parent.parent / "assets"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

EXTRA_COLUMNS = ["Network", "Platform", "DAU", "ARPDAU"]

SCENARIOS = [
    {"name": "default",    "label": "Default mode",      "url": BASE,              "custom_days": [90]},
    {"name": "chart",      "label": "Chart mode (ch)",   "url": f"{BASE}?mode=ch", "custom_days": [90, 180]},
    {"name": "chart+cols", "label": "Chart+cols (ch)",   "url": f"{BASE}?mode=ch", "custom_days": [90, 180], "extra_columns": True},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def wait_for_data(page, timeout=120):
    """Wait until loading indicators disappear. Returns seconds waited."""
    t0 = time.time()
    deadline = t0 + timeout
    while time.time() < deadline:
        if (page.locator("text=Chart data is loading").count() == 0
                and page.locator("text=loading").count() == 0):
            break
        page.wait_for_timeout(1000)
    page.wait_for_timeout(1500)
    return time.time() - t0


def login(page, email, password):
    """Login and land on b2b.cas.ai."""
    # Try direct b2b login
    page.goto("https://b2b.cas.ai/login", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    if page.locator('input[type="email"], input[name="email"]').count() > 0:
        page.locator('input[type="email"], input[name="email"]').first.fill(email)
        page.locator('input[type="password"], input[name="password"]').first.fill(password)
        page.wait_for_timeout(500)
        page.locator('button[type="submit"], button:has-text("Log in")').first.click(force=True)
        page.wait_for_timeout(8000)
        if "b2b.cas.ai" in page.url and "/login" not in page.url:
            return
    # Fallback: cas.ai popup
    page.goto("https://cas.ai", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)
    page.locator("a.get-login-popup, button:has-text('Log in'), a:has-text('Log in')").first.click(force=True)
    page.wait_for_timeout(1500)
    popup = page.locator(".login-popup, .main-popup-wrap").first
    popup.locator('input[type="email"], input[name="email"], input[placeholder*="mail"]').first.fill(email)
    popup.locator('input[type="password"], input[name="password"]').first.fill(password)
    page.wait_for_timeout(500)
    popup.locator('button[type="submit"], button:has-text("Log in"), button:has-text("Sign in")').first.click(force=True)
    try:
        page.wait_for_url("**/b2b.cas.ai/**", timeout=30000)
    except Exception:
        page.wait_for_timeout(5000)


def set_custom_period(page, days=180):
    """Click CUSTOM, pick date range via Litepicker, apply."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    page.get_by_role("button", name="Custom").click()
    page.wait_for_timeout(1500)
    months_back = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    for _ in range(months_back):
        page.locator(".button-previous-month").first.click(force=True)
        page.wait_for_timeout(300)
    page.wait_for_timeout(300)
    page.locator(".month-item").first.locator(
        f".day-item >> text='{start_date.day}'"
    ).first.click(force=True)
    page.wait_for_timeout(500)
    for _ in range(months_back):
        page.locator(".button-next-month").last.click(force=True)
        page.wait_for_timeout(300)
    page.wait_for_timeout(300)
    page.locator(".month-item").first.locator(
        f".day-item >> text='{end_date.day}'"
    ).first.click(force=True)
    page.wait_for_timeout(500)
    page.locator("button:has-text('Apply'), button:has-text('APPLY')").first.click()
    page.wait_for_timeout(500)


def select_view_by(page, option):
    """Pick a View-by option from the custom dropdown."""
    sb = page.locator(".select-bar")
    vb = sb.locator(".select-box").nth(0)
    vb.locator(".selected").click()
    page.wait_for_timeout(500)
    vb.locator(f".option:has-text('{option}')").click()
    page.wait_for_timeout(500)


def open_filters(page):
    page.locator("button.filter").click()
    page.wait_for_timeout(1500)


def click_filter_apply(page):
    page.locator("button.filter_btn:has-text('Apply')").click()
    page.wait_for_timeout(500)


def apply_platform_filter(page, platform):
    open_filters(page)
    if platform == "ios":
        page.get_by_text("iOS", exact=True).first.click()
    elif platform == "android":
        page.get_by_text("Android", exact=True).first.click()
    page.wait_for_timeout(300)
    click_filter_apply(page)


def undo_platform_filter(page, platform):
    open_filters(page)
    if platform == "ios":
        page.get_by_text("iOS", exact=True).first.click()
    elif platform == "android":
        page.get_by_text("Android", exact=True).first.click()
    page.wait_for_timeout(300)
    click_filter_apply(page)


def enable_extra_columns(page, columns):
    """Open Table Columns dropdown and check extra columns."""
    page.locator("text=Table Columns").first.click()
    page.wait_for_timeout(800)
    for col in columns:
        item = page.locator(f".checkelement:has(.v-label:text-is('{col}'))")
        if item.count() > 0 and item.first.is_visible():
            item.first.click()
            page.wait_for_timeout(300)
    page.locator("text=Show graph:").click()
    page.wait_for_timeout(500)


def disable_extra_columns(page, columns):
    """Uncheck previously added columns."""
    page.locator("text=Table Columns").first.click()
    page.wait_for_timeout(800)
    for col in columns:
        item = page.locator(f".checkelement:has(.v-label:text-is('{col}'))")
        if item.count() > 0 and item.first.is_visible():
            # Only uncheck if it's currently checked
            is_checked = "is-dirty" in (item.first.get_attribute("class") or "")
            if is_checked:
                item.first.click()
                page.wait_for_timeout(300)
    page.locator("text=Show graph:").click()
    page.wait_for_timeout(500)


# ---------------------------------------------------------------------------
# Single-scenario test
# ---------------------------------------------------------------------------


def run_period_block(page, period_label, r):
    """Run view-by, metric cards, and filter tests for the current period."""
    p = period_label  # e.g. "30d", "90d", "180d"

    # View by
    for vb in ["Application", "Country", "Network"]:
        try:
            select_view_by(page, vb)
            t = wait_for_data(page)
            r[f"{p}_vb_{vb.lower()}"] = t
            print(f"    {p} vb {vb:<12} {t:.1f}s")
        except Exception:
            r[f"{p}_vb_{vb.lower()}"] = None
            print(f"    {p} vb {vb:<12} FAIL")
    try:
        select_view_by(page, "Total")
        wait_for_data(page)
    except Exception:
        pass

    # Metric cards
    for mc in ["Impressions", "eCPM"]:
        try:
            page.locator(f"text='{mc}'").first.click()
            page.wait_for_timeout(500)
            t = wait_for_data(page)
            r[f"{p}_mc_{mc.lower()}"] = t
            print(f"    {p} {mc:<14} {t:.1f}s")
        except Exception:
            r[f"{p}_mc_{mc.lower()}"] = None
    try:
        page.locator("text='Est. Revenue'").first.click()
        page.wait_for_timeout(500)
        wait_for_data(page)
    except Exception:
        pass

    # Filters
    for plat, label in [("ios", "iOS"), ("android", "Android")]:
        try:
            apply_platform_filter(page, plat)
            t = wait_for_data(page)
            r[f"{p}_flt_{plat}"] = t
            print(f"    {p} {label:<14} {t:.1f}s")
            undo_platform_filter(page, plat)
            wait_for_data(page)
        except Exception:
            r[f"{p}_flt_{plat}"] = None
            print(f"    {p} {label:<14} FAIL")
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(500)
            except Exception:
                pass


def run_scenario(page, scenario):
    """Run all sub-tests on the currently loaded page. Returns dict of timings."""
    r = {}
    custom_days_list = scenario.get("custom_days", [180])

    # --- 30 DAYS ---
    page.get_by_role("button", name="30 days").click()
    page.wait_for_timeout(500)
    t = wait_for_data(page)
    r["30d"] = t
    print(f"    30d:  {t:.1f}s")
    run_period_block(page, "30d", r)

    # --- Custom periods ---
    for days in custom_days_list:
        label = f"{days}d"
        try:
            set_custom_period(page, days=days)
            t = wait_for_data(page)
            r[label] = t
            print(f"    {label}: {t:.1f}s")
            run_period_block(page, label, r)
        except Exception:
            r[label] = None
            print(f"    {label}: FAIL")

    return r


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run_test():
    # results[scenario_name][email] = {metric: time}
    results = {s["name"]: {} for s in SCENARIOS}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for email, password in ACCOUNTS:
            print(f"\n{'='*70}")
            print(f"  {email}")
            print(f"{'='*70}")

            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()
            login(page, email, password)

            for scenario in SCENARIOS:
                sname = scenario["name"]
                print(f"\n  --- {scenario['label']} ---")

                page.goto(scenario["url"], wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)
                wait_for_data(page)

                if scenario.get("extra_columns"):
                    enable_extra_columns(page, EXTRA_COLUMNS)
                    wait_for_data(page)

                r = run_scenario(page, scenario)
                results[sname][email] = r

                if scenario.get("extra_columns"):
                    try:
                        page.keyboard.press("Escape")
                        page.wait_for_timeout(500)
                        disable_extra_columns(page, EXTRA_COLUMNS)
                        page.wait_for_timeout(500)
                    except Exception:
                        pass  # columns will reset on next page load

            # Screenshot
            short = email.split("@")[0]
            page.screenshot(
                path=str(SCREENSHOTS_DIR / f"dashboard-speed-{short}.png"),
                full_page=True,
            )
            context.close()

        browser.close()

    # === REPORT ===
    print("\n\n")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 100)
    print(f"  CAS.AI DASHBOARD SPEED TEST — {ts}")
    print("=" * 100)

    def fmt(v):
        return f"{v:.1f}s" if v is not None else "N/A"

    def short(email):
        return email.split("@")[0][:20]

    for scenario in SCENARIOS:
        sname = scenario["name"]
        data = results[sname]
        if not data:
            continue

        custom_days = scenario.get("custom_days", [180])
        all_periods = ["30d"] + [f"{d}d" for d in custom_days]

        print(f"\n  {'─'*96}")
        print(f"  {scenario['label'].upper()}")
        print(f"  {'─'*96}")

        for period in all_periods:
            print(f"\n  {period}:")
            print(f"  {'Account':<22} {'load':>6}"
                  f"  {'vbApp':>6} {'vbCntry':>7} {'vbNet':>6}"
                  f"  {'Impr':>6} {'eCPM':>6}"
                  f"  {'iOS':>6} {'Andr':>6}")
            print(f"  {'-'*22} {'-'*6}"
                  f"  {'-'*6} {'-'*7} {'-'*6}"
                  f"  {'-'*6} {'-'*6}"
                  f"  {'-'*6} {'-'*6}")

            for email_addr in [a[0] for a in ACCOUNTS]:
                r = data.get(email_addr, {})
                print(f"  {short(email_addr):<22}"
                      f" {fmt(r.get(period)):>6}"
                      f"  {fmt(r.get(f'{period}_vb_application')):>6}"
                      f" {fmt(r.get(f'{period}_vb_country')):>7}"
                      f" {fmt(r.get(f'{period}_vb_network')):>6}"
                      f"  {fmt(r.get(f'{period}_mc_impressions')):>6}"
                      f" {fmt(r.get(f'{period}_mc_ecpm')):>6}"
                      f"  {fmt(r.get(f'{period}_flt_ios')):>6}"
                      f" {fmt(r.get(f'{period}_flt_android')):>6}")

    print("\n" + "=" * 100)

    # === SAVE MARKDOWN REPORT ===
    report_path = Path(__file__).parent.parent / "05-research" / "dashboard-speed-results.md"
    md = []
    md.append(f"# Dashboard Speed Test — {ts}\n")
    md.append(f"Accounts: {len(ACCOUNTS)}  \n")
    md.append(f"Scenarios: {', '.join(s['label'] for s in SCENARIOS)}\n")

    for scenario in SCENARIOS:
        sname = scenario["name"]
        data = results[sname]
        if not data:
            continue

        custom_days = scenario.get("custom_days", [180])
        all_periods = ["30d"] + [f"{d}d" for d in custom_days]

        md.append(f"\n## {scenario['label']}\n")

        for period in all_periods:
            md.append(f"\n### {period}\n")
            md.append("| Account | Load | vbApp | vbCountry | vbNetwork | Impressions | eCPM | iOS | Android |")
            md.append("|---------|------|-------|-----------|-----------|-------------|------|-----|---------|")

            for email_addr in [a[0] for a in ACCOUNTS]:
                r = data.get(email_addr, {})
                md.append(
                    f"| {short(email_addr)} "
                    f"| {fmt(r.get(period))} "
                    f"| {fmt(r.get(f'{period}_vb_application'))} "
                    f"| {fmt(r.get(f'{period}_vb_country'))} "
                    f"| {fmt(r.get(f'{period}_vb_network'))} "
                    f"| {fmt(r.get(f'{period}_mc_impressions'))} "
                    f"| {fmt(r.get(f'{period}_mc_ecpm'))} "
                    f"| {fmt(r.get(f'{period}_flt_ios'))} "
                    f"| {fmt(r.get(f'{period}_flt_android'))} |"
                )

    md.append("")
    report_path.write_text("\n".join(md), encoding="utf-8")
    print(f"\n  Report saved → {report_path}")


if __name__ == "__main__":
    run_test()
