"""
Measure CAS.AI dashboard load speed via Playwright.
Usage: python3 scripts/cas_dashboard_speed.py

Tests mode=ch with 7d, 30d, and custom 180d periods.
Reads accounts from scripts/.env.cas-accounts.
"""

import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

# Load accounts from .env.cas-accounts
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

URL = "https://b2b.cas.ai/mediation?mode=ch"


def wait_for_data(page, timeout=120):
    """Wait until 'Chart data is loading' disappears. Returns seconds waited."""
    t_start = time.time()
    deadline = t_start + timeout
    while time.time() < deadline:
        loading = page.locator("text=Chart data is loading").count()
        spinners = page.locator("text=loading").count()
        if loading == 0 and spinners == 0:
            break
        page.wait_for_timeout(1000)
    page.wait_for_timeout(1500)
    return time.time() - t_start


def login_and_goto(page, email, password):
    """Login via cas.ai and navigate to mode=ch URL."""
    page.goto("https://cas.ai", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)

    login_btn = page.locator("a.get-login-popup, button:has-text('Log in'), a:has-text('Log in')").first
    login_btn.click(force=True)
    page.wait_for_timeout(1500)

    popup = page.locator(".login-popup, .main-popup-wrap").first
    popup.locator('input[type="email"], input[name="email"], input[placeholder*="mail"], input[placeholder*="Email"]').first.fill(email)
    popup.locator('input[type="password"], input[name="password"]').first.fill(password)
    page.wait_for_timeout(500)

    popup.locator('button[type="submit"], button:has-text("Log in"), button:has-text("Sign in"), input[type="submit"]').first.click(force=True)

    try:
        page.wait_for_url("**/b2b.cas.ai/**", timeout=30000)
    except Exception:
        page.wait_for_timeout(5000)

    # Navigate to mode=ch
    if "mode=ch" not in page.url:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1000)


def set_custom_period(page, days=180):
    """Click CUSTOM, use Litepicker calendar to select date range, apply."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Click CUSTOM to open date picker
    page.locator("text=CUSTOM").click()
    page.wait_for_timeout(1500)

    # Litepicker: navigate back to start_date month
    now = datetime.now()
    months_back = (now.year - start_date.year) * 12 + (now.month - start_date.month)

    print(f"   Navigating {months_back} months back to {start_date.strftime('%B %Y')}...")
    for _ in range(months_back):
        page.locator(".button-previous-month").first.click(force=True)
        page.wait_for_timeout(300)

    # Click start date day (first click = range start)
    page.wait_for_timeout(300)
    start_day = str(start_date.day)
    left_month = page.locator(".month-item").first
    left_month.locator(f".day-item >> text='{start_day}'").first.click(force=True)
    page.wait_for_timeout(500)

    # Navigate forward to end date month
    print(f"   Navigating forward to {end_date.strftime('%B %Y')}...")
    for _ in range(months_back):
        page.locator(".button-next-month").last.click(force=True)
        page.wait_for_timeout(300)

    # Click end date day (second click = range end)
    page.wait_for_timeout(300)
    end_day = str(end_date.day)
    left_month = page.locator(".month-item").first
    left_month.locator(f".day-item >> text='{end_day}'").first.click(force=True)
    page.wait_for_timeout(500)

    # Click Apply
    page.locator("button:has-text('Apply'), button:has-text('APPLY')").first.click()
    page.wait_for_timeout(500)


def run_test():
    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for email, password in ACCOUNTS:
            print(f"\n{'='*60}")
            print(f"  {email} — mode=ch")
            print(f"{'='*60}")

            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()

            print(f"  Logging in...")
            login_and_goto(page, email, password)

            # 7 DAYS (default)
            print(f"  Waiting for 7 DAYS...")
            t_7d = wait_for_data(page)
            print(f"  7 DAYS:  {t_7d:.1f}s")

            # 30 DAYS
            print(f"  Switching to 30 DAYS...")
            page.locator("text=30 DAYS").click()
            page.wait_for_timeout(500)
            t_30d = wait_for_data(page)
            print(f"  30 DAYS: {t_30d:.1f}s")

            # CUSTOM 180 DAYS
            print(f"  Switching to CUSTOM (180 days)...")
            set_custom_period(page, days=180)
            t_180d = wait_for_data(page)
            print(f"  180 DAYS: {t_180d:.1f}s")

            # Screenshot
            screenshots_dir = Path(__file__).parent.parent / "assets"
            screenshots_dir.mkdir(exist_ok=True)
            short = email.split("@")[0]
            page.screenshot(path=str(screenshots_dir / f"dashboard-180d-{short}.png"), full_page=True)

            all_results.append({
                "email": email,
                "7d": t_7d,
                "30d": t_30d,
                "180d": t_180d,
            })

            context.close()

        browser.close()

    # === FINAL TABLE ===
    print("\n")
    print("=" * 70)
    print("  mode=ch SPEED TEST: 7d / 30d / 180d (custom)")
    print("=" * 70)
    print(f"  {'Account':<28} {'7 DAYS':>8} {'30 DAYS':>8} {'180 DAYS':>9}")
    print(f"  {'-'*28} {'-'*8} {'-'*8} {'-'*9}")

    for r in all_results:
        short = r["email"].split("@")[0][:24]
        print(f"  {short:<28} {r['7d']:>7.1f}s {r['30d']:>7.1f}s {r['180d']:>8.1f}s")

    print("=" * 70)


if __name__ == "__main__":
    run_test()
