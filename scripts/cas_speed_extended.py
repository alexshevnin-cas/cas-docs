"""
Babygamespub deep test on mode=ch:
  For each period (180d, 270d, 360d):
    1. Plain load
    2. + extra columns load
    3. + iOS filter (with columns still on)
    4. + Android filter (with columns still on)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cas_dashboard_speed import (
    ACCOUNTS, wait_for_data, login, set_custom_period,
    enable_extra_columns, disable_extra_columns,
    apply_platform_filter, undo_platform_filter,
    EXTRA_COLUMNS,
)
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_CH = "https://b2b.cas.ai/mediation?mode=ch"
PERIODS = [180, 270, 360]

# Last account = Babygamespub
EMAIL, PASSWORD = ACCOUNTS[-1]


def run():
    acc = {}
    short = EMAIL.split("@")[0]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        print(f"\n{'='*60}")
        print(f"  {EMAIL}")
        print(f"{'='*60}")
        login(page, EMAIL, PASSWORD)
        page.goto(BASE_CH, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        wait_for_data(page)

        for days in PERIODS:
            label = f"{days}d"
            print(f"\n  --- {label} ---")

            # 1) Plain
            try:
                set_custom_period(page, days=days)
                t = wait_for_data(page)
                acc[f"{label}"] = t
                print(f"    plain:       {t:.1f}s")
            except Exception as e:
                acc[f"{label}"] = None
                print(f"    plain:       FAIL ({e})")

            # 2) + extra columns
            try:
                enable_extra_columns(page, EXTRA_COLUMNS)
                t = wait_for_data(page)
                acc[f"{label}_cols"] = t
                print(f"    +cols:       {t:.1f}s")
            except Exception as e:
                acc[f"{label}_cols"] = None
                print(f"    +cols:       FAIL ({e})")

            # 3) + iOS filter (columns still on)
            try:
                apply_platform_filter(page, "ios")
                t = wait_for_data(page)
                acc[f"{label}_cols_ios"] = t
                print(f"    +cols +iOS:  {t:.1f}s")
                undo_platform_filter(page, "ios")
                wait_for_data(page)
            except Exception as e:
                acc[f"{label}_cols_ios"] = None
                print(f"    +cols +iOS:  FAIL ({e})")
                try:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                except Exception:
                    pass

            # 4) + Android filter (columns still on)
            try:
                apply_platform_filter(page, "android")
                t = wait_for_data(page)
                acc[f"{label}_cols_andr"] = t
                print(f"    +cols +Andr: {t:.1f}s")
                undo_platform_filter(page, "android")
                wait_for_data(page)
            except Exception as e:
                acc[f"{label}_cols_andr"] = None
                print(f"    +cols +Andr: FAIL ({e})")
                try:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                except Exception:
                    pass

            # Remove extra columns before next period
            try:
                disable_extra_columns(page, EXTRA_COLUMNS)
                wait_for_data(page)
            except Exception:
                pass

        page.screenshot(
            path=str(Path(__file__).parent.parent / "assets" / f"speed-deep-{short}.png"),
            full_page=True,
        )
        ctx.close()
        browser.close()

    # === Summary ===
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    fmt = lambda v: f"{v:.1f}s" if v is not None else "N/A"

    print(f"\n{'='*70}")
    print(f"  {short} — CH deep test — {ts}")
    print(f"{'='*70}")
    print(f"  {'Period':<8} {'plain':>7} {'+cols':>7} {'+cols+iOS':>10} {'+cols+Andr':>11}")
    print(f"  {'-'*8} {'-'*7} {'-'*7} {'-'*10} {'-'*11}")
    for days in PERIODS:
        label = f"{days}d"
        print(
            f"  {label:<8}"
            f" {fmt(acc.get(label)):>7}"
            f" {fmt(acc.get(f'{label}_cols')):>7}"
            f" {fmt(acc.get(f'{label}_cols_ios')):>10}"
            f" {fmt(acc.get(f'{label}_cols_andr')):>11}"
        )

    # === Append to report ===
    report_path = Path(__file__).parent.parent / "05-research" / "dashboard-speed-results.md"
    if report_path.exists():
        lines = [
            f"\n\n## Babygamespub deep test — CH mode ({ts})\n",
            "Extra columns: " + ", ".join(EXTRA_COLUMNS) + "\n",
            "| Period | Plain | +Cols | +Cols +iOS | +Cols +Android |",
            "|--------|-------|-------|------------|----------------|",
        ]
        for days in PERIODS:
            label = f"{days}d"
            lines.append(
                f"| {label}"
                f" | {fmt(acc.get(label))}"
                f" | {fmt(acc.get(f'{label}_cols'))}"
                f" | {fmt(acc.get(f'{label}_cols_ios'))}"
                f" | {fmt(acc.get(f'{label}_cols_andr'))} |"
            )
        lines.append("")
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\n  Appended to → {report_path}")


if __name__ == "__main__":
    run()
