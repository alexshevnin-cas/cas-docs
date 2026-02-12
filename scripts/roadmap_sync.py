#!/usr/bin/env python3
"""
roadmap_sync.py — Sync roadmap.md ↔ GitHub Issues ↔ Asana.

Usage:
    python3 scripts/roadmap_sync.py full       # reverse then forward (default)
    python3 scripts/roadmap_sync.py forward    # roadmap → GitHub → Asana
    python3 scripts/roadmap_sync.py reverse    # Asana → roadmap
    python3 scripts/roadmap_sync.py status     # show diff, no changes
    python3 scripts/roadmap_sync.py bootstrap  # link existing issues/tasks to roadmap

Flags:
    --dry-run   Show what would change without making changes
    --verbose   Show detailed output

Requires:
    - gh CLI (authenticated)
    - ~/.cas-sync.env with ASANA_TOKEN, ASANA_PROJECT_GID, ASANA_WORKSPACE_GID
"""

import argparse
import json
import os
import re
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

ROADMAP_PATH = Path(__file__).resolve().parent.parent / "03-product" / "roadmap.md"
LINKS_PATH = Path(__file__).resolve().parent / "roadmap-links.json"
ENV_PATH = Path.home() / ".cas-sync.env"

TRACK_MAP = {
    "Core": "Core / Ядро",
    "Data": "Data / Данные",
    "Portal": "Portal / Кабинет",
    "Services": "Services / Сервисы",
    "Finance": "Finance / Финансы",
    "Growth": "Growth / Рост",
    "DX": "DX / Dev Experience",
    "BX": "BX / Biz Experience",
}

# Initiative ID prefixes → track short name
ID_TRACK = {
    "C": "Core",
    "D": "Data",
    "P": "Portal",
    "S": "Services",
    "F": "Finance",
    "G": "Growth",
    "DX": "DX",
    "BX": "BX",
}

ASANA_HORIZON_OPTIONS = ["H1", "H2", "H1-H2", "Beyond", "Ongoing"]
ASANA_STATUS_OPTIONS = [
    "В работе",
    "Планируется",
    "Не начато",
    "Концепт",
    "Идея",
    "Ждёт",
    "Ждёт дизайн",
    "Готово",
    "Не формализовано",
    "Спецификация готова",
    "Существует неформально",
]

ROADMAP_ISSUE_PREFIX = "[Track]"

# ─── Config / Env ────────────────────────────────────────────────────────────


def load_env() -> dict:
    """Load key=value pairs from ~/.cas-sync.env."""
    env = {}
    if not ENV_PATH.exists():
        return env
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def get_repo() -> str:
    """Get OWNER/REPO from gh CLI."""
    result = subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: gh repo view failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


# ─── Roadmap Parser ─────────────────────────────────────────────────────────


class Initiative:
    """One row from a roadmap track table."""

    def __init__(
        self,
        id: str,
        name: str,
        horizon: str,
        status: str,
        deps: str,
        owner: str = "",
        deadline: str = "",
        track: str = "",
    ):
        self.id = id
        self.name = name
        self.horizon = horizon
        self.status = status
        self.deps = deps
        self.owner = owner
        self.deadline = deadline
        self.track = track

    def __repr__(self):
        return f"Initiative({self.id}, {self.name!r}, {self.status})"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "horizon": self.horizon,
            "status": self.status,
            "deps": self.deps,
            "owner": self.owner,
            "deadline": self.deadline,
            "track": self.track,
        }


def parse_roadmap(text: str) -> list[Initiative]:
    """Parse roadmap.md and extract all initiatives from track tables."""
    initiatives = []
    current_track = None

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect track heading: ## or ### Core / Ядро, Data / Данные, etc.
        heading_match = re.match(r"^#{2,3}\s+(.+?)$", line)
        if heading_match:
            heading = heading_match.group(1).strip()
            for short, full in TRACK_MAP.items():
                if heading == full or heading.startswith(full):
                    current_track = short
                    break

        # Detect table rows (skip header and separator)
        if current_track and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")]
            # Remove empty first/last from split
            cells = [c for c in cells if c != ""]
            if not cells:
                i += 1
                continue

            # Skip header row (contains #, Инициатива, etc.) and separator (---)
            if cells[0] in ("#", "---", "") or cells[0].startswith("---"):
                i += 1
                continue

            # Parse initiative row
            # Expected columns: #, Инициатива, Горизонт, Статус, Зависимости, [Владелец], [Срок]
            if len(cells) >= 5:
                init_id = cells[0].strip()
                # Validate it looks like an initiative ID
                if re.match(r"^[A-Z]+\d+[a-z]?$", init_id):
                    name = cells[1].strip()
                    # Strip markdown bold
                    name = re.sub(r"\*\*(.+?)\*\*", r"\1", name)
                    # Strip leading "— " prefix from name parts (e.g., "**MVP BI** — Quick View...")
                    # Keep the full name including description
                    horizon = cells[2].strip()
                    status = cells[3].strip()
                    deps = cells[4].strip()
                    owner = cells[5].strip() if len(cells) > 5 else ""
                    deadline = cells[6].strip() if len(cells) > 6 else ""

                    initiatives.append(
                        Initiative(
                            id=init_id,
                            name=name,
                            horizon=horizon,
                            status=status,
                            deps=deps,
                            owner=owner,
                            deadline=deadline,
                            track=current_track,
                        )
                    )

        i += 1

    return initiatives


def update_roadmap_status(text: str, init_id: str, new_status: str) -> str:
    """Update a single initiative's status in roadmap.md text. Returns new text."""
    lines = text.splitlines()
    result = []
    for line in lines:
        if line.startswith("|"):
            cells = [c.strip() for c in line.split("|")]
            cells_clean = [c for c in cells if c != ""]
            if len(cells_clean) >= 5 and cells_clean[0] == init_id:
                # Replace status cell (index 3)
                # Rebuild the line preserving formatting
                parts = line.split("|")
                # parts[0] is empty (before first |), parts[-1] is empty (after last |)
                # Status is the 4th content cell → parts[4]
                if len(parts) >= 6:
                    parts[4] = f" {new_status} "
                    line = "|".join(parts)
        result.append(line)
    return "\n".join(result)


def get_track_for_id(init_id: str) -> str:
    """Get track short name from initiative ID prefix."""
    # Handle multi-letter prefixes first (DX, BX)
    for prefix in sorted(ID_TRACK.keys(), key=len, reverse=True):
        if init_id.startswith(prefix):
            return ID_TRACK[prefix]
    return ""


# ─── Links store ─────────────────────────────────────────────────────────────


def load_links() -> dict:
    """Load roadmap-links.json. Returns {init_id: {gh: int, asana: str}}."""
    if not LINKS_PATH.exists():
        return {}
    return json.loads(LINKS_PATH.read_text())


def save_links(links: dict):
    """Save roadmap-links.json atomically."""
    tmp = LINKS_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(links, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(LINKS_PATH)


# ─── GitHub Client ───────────────────────────────────────────────────────────


class GitHubClient:
    """GitHub operations via gh CLI."""

    def __init__(self, repo: str, dry_run: bool = False, verbose: bool = False):
        self.repo = repo
        self.dry_run = dry_run
        self.verbose = verbose

    def _gh(self, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
        cmd = ["gh"] + args + ["-R", self.repo]
        if self.verbose:
            print(f"  $ {' '.join(cmd)}", file=sys.stderr)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"ERROR: gh {' '.join(args)}: {result.stderr}", file=sys.stderr)
        return result

    def _gh_api(self, endpoint: str, method: str = "GET", body: dict = None) -> dict | list | None:
        cmd = ["gh", "api", endpoint, "-H", "Accept: application/vnd.github+json"]
        if method != "GET":
            cmd += ["--method", method]
        if body:
            for k, v in body.items():
                if isinstance(v, list):
                    for item in v:
                        cmd += ["-f", f"{k}[]={item}"]
                elif isinstance(v, bool):
                    cmd += ["-F", f"{k}={'true' if v else 'false'}"]
                elif isinstance(v, int):
                    cmd += ["-F", f"{k}={v}"]
                else:
                    cmd += ["-f", f"{k}={v}"]
        if self.verbose:
            print(f"  $ {' '.join(cmd)}", file=sys.stderr)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            if self.verbose:
                print(f"  gh api error: {result.stderr}", file=sys.stderr)
            return None
        if result.stdout.strip():
            return json.loads(result.stdout)
        return None

    def list_issues(self, label: str = None, state: str = "all") -> list[dict]:
        """List issues. Returns list of {number, title, state, labels}."""
        cmd = ["issue", "list", "--state", state, "--json", "number,title,state,labels", "--limit", "200"]
        if label:
            cmd += ["--label", label]
        result = self._gh(cmd, check=False)
        if result.returncode != 0:
            return []
        return json.loads(result.stdout) if result.stdout.strip() else []

    def get_issue(self, number: int) -> dict | None:
        result = self._gh(
            ["issue", "view", str(number), "--json", "number,title,state,labels,body"],
            check=False,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)

    def create_issue(self, title: str, body: str, labels: list[str] = None) -> int | None:
        """Create issue. Returns issue number."""
        if self.dry_run:
            print(f"  [DRY-RUN] Would create issue: {title}")
            return None
        cmd = ["issue", "create", "--title", title, "--body", body]
        if labels:
            for l in labels:
                cmd += ["--label", l]
        result = self._gh(cmd, check=False)
        if result.returncode != 0:
            print(f"  ERROR creating issue: {result.stderr}", file=sys.stderr)
            return None
        # Parse issue URL to get number
        url = result.stdout.strip()
        match = re.search(r"/issues/(\d+)", url)
        return int(match.group(1)) if match else None

    def update_issue(self, number: int, title: str = None, body: str = None, state: str = None, labels: list[str] = None):
        """Update an existing issue."""
        if self.dry_run:
            parts = []
            if title:
                parts.append(f"title={title!r}")
            if state:
                parts.append(f"state={state}")
            print(f"  [DRY-RUN] Would update issue #{number}: {', '.join(parts)}")
            return
        # Use gh api for more control
        data = {}
        if title:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state:
            data["state"] = state
        if labels:
            data["labels"] = labels
        if data:
            self._gh_api(f"/repos/{self.repo}/issues/{number}", method="PATCH", body=data)

    def close_issue(self, number: int):
        if self.dry_run:
            print(f"  [DRY-RUN] Would close issue #{number}")
            return
        self._gh(["issue", "close", str(number)], check=False)

    def reopen_issue(self, number: int):
        if self.dry_run:
            print(f"  [DRY-RUN] Would reopen issue #{number}")
            return
        self._gh(["issue", "reopen", str(number)], check=False)

    def ensure_labels(self, labels: list[str]):
        """Ensure labels exist in the repo."""
        existing = self._gh_api(f"/repos/{self.repo}/labels?per_page=100")
        if not existing:
            existing = []
        existing_names = {l["name"] for l in existing}

        track_colors = {
            "Core": "d93f0b",
            "Data": "0075ca",
            "Portal": "7057ff",
            "Services": "e4e669",
            "Finance": "008672",
            "Growth": "d876e3",
            "DX": "fbca04",
            "BX": "b60205",
            "H1": "c5def5",
            "H2": "bfdadc",
            "H1-H2": "d4c5f9",
            "Beyond": "f9d0c4",
            "Ongoing": "ededed",
            "roadmap": "1d76db",
        }

        for label in labels:
            if label not in existing_names:
                if self.dry_run:
                    print(f"  [DRY-RUN] Would create label: {label}")
                else:
                    color = track_colors.get(label, "ededed")
                    self._gh_api(
                        f"/repos/{self.repo}/labels",
                        method="POST",
                        body={"name": label, "color": color},
                    )


# ─── Asana Client ────────────────────────────────────────────────────────────


class AsanaClient:
    """Asana operations via REST API (urllib only)."""

    BASE = "https://app.asana.com/api/1.0"

    def __init__(
        self,
        token: str,
        project_gid: str,
        workspace_gid: str,
        dry_run: bool = False,
        verbose: bool = False,
    ):
        self.token = token
        self.project_gid = project_gid
        self.workspace_gid = workspace_gid
        self.dry_run = dry_run
        self.verbose = verbose
        self._sections_cache: dict[str, str] = {}
        self._custom_fields_cache: dict[str, dict] = {}
        self._ssl_ctx = ssl.create_default_context()
        # macOS Python may lack system certs; fall back to certifi or unverified
        try:
            import certifi
            self._ssl_ctx.load_verify_locations(certifi.where())
        except ImportError:
            self._ssl_ctx.check_hostname = False
            self._ssl_ctx.verify_mode = ssl.CERT_NONE

    def _request(self, method: str, path: str, body: dict = None) -> dict | None:
        url = f"{self.BASE}{path}"
        data = None
        if body:
            data = json.dumps({"data": body}).encode()

        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Content-Type", "application/json")

        if self.verbose:
            print(f"  Asana {method} {path}", file=sys.stderr)

        try:
            with urllib.request.urlopen(req, context=self._ssl_ctx) as resp:
                resp_data = resp.read().decode()
                if resp_data:
                    return json.loads(resp_data)
                return None
        except urllib.error.HTTPError as e:
            body_text = e.read().decode() if e.fp else ""
            print(
                f"  Asana API error: {e.code} {method} {path}: {body_text}",
                file=sys.stderr,
            )
            return None

    def _get_paginated(self, path: str, params: dict = None) -> list:
        """Get all results with pagination."""
        results = []
        query = ""
        if params:
            query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())

        url = f"{path}?{query}" if query else path
        while url:
            resp = self._request("GET", url)
            if not resp:
                break
            results.extend(resp.get("data", []))
            next_page = resp.get("next_page")
            if next_page and next_page.get("uri"):
                # next_page uri is relative
                url = next_page["uri"].replace(self.BASE, "")
            else:
                break
        return results

    def get_sections(self) -> dict[str, str]:
        """Get sections {name: gid} for the project."""
        if self._sections_cache:
            return self._sections_cache
        sections = self._get_paginated(f"/projects/{self.project_gid}/sections")
        self._sections_cache = {s["name"]: s["gid"] for s in sections}
        return self._sections_cache

    def ensure_section(self, name: str) -> str:
        """Ensure section exists, return gid."""
        sections = self.get_sections()
        if name in sections:
            return sections[name]
        if self.dry_run:
            print(f"  [DRY-RUN] Would create Asana section: {name}")
            return "dry-run-section"
        resp = self._request(
            "POST",
            f"/projects/{self.project_gid}/sections",
            {"name": name},
        )
        if resp:
            gid = resp["data"]["gid"]
            self._sections_cache[name] = gid
            return gid
        return ""

    def get_custom_fields(self) -> dict[str, dict]:
        """Get custom fields on the project. Returns {name: {gid, enum_options, type}}."""
        if self._custom_fields_cache:
            return self._custom_fields_cache
        resp = self._request(
            "GET",
            f"/projects/{self.project_gid}?opt_fields=custom_field_settings.custom_field.name,custom_field_settings.custom_field.gid,custom_field_settings.custom_field.type,custom_field_settings.custom_field.enum_options",
        )
        if not resp:
            return {}
        fields = {}
        for setting in resp.get("data", {}).get("custom_field_settings", []):
            cf = setting.get("custom_field", {})
            fields[cf["name"]] = {
                "gid": cf["gid"],
                "type": cf.get("type", ""),
                "enum_options": {
                    opt["name"]: opt["gid"]
                    for opt in cf.get("enum_options", [])
                    if opt.get("enabled", True)
                },
            }
        self._custom_fields_cache = fields
        return fields

    def create_custom_field(self, name: str, field_type: str, enum_options: list[str] = None) -> str:
        """Create a custom field in the workspace and add to project."""
        if self.dry_run:
            print(f"  [DRY-RUN] Would create Asana custom field: {name} ({field_type})")
            return "dry-run-field"

        body = {
            "name": name,
            "resource_subtype": field_type,
            "workspace": self.workspace_gid,
        }
        if field_type == "enum" and enum_options:
            body["enum_options"] = [{"name": opt} for opt in enum_options]

        resp = self._request("POST", "/custom_fields", body)
        if not resp:
            return ""
        field_gid = resp["data"]["gid"]

        # Add to project
        self._request(
            "POST",
            f"/projects/{self.project_gid}/addCustomFieldSetting",
            {"custom_field": field_gid},
        )

        # Clear cache
        self._custom_fields_cache = {}
        return field_gid

    def ensure_custom_fields(self):
        """Ensure required custom fields exist on the project."""
        fields = self.get_custom_fields()

        required = {
            "Горизонт": ("enum", ASANA_HORIZON_OPTIONS),
            "Статус": ("enum", ASANA_STATUS_OPTIONS),
            "Initiative ID": ("text", None),
        }

        for name, (ftype, options) in required.items():
            if name not in fields:
                print(f"  Creating custom field: {name}")
                self.create_custom_field(name, ftype, options)

    def search_tasks(self, text: str = None, completed: bool = None) -> list[dict]:
        """Search tasks in the project."""
        params = {
            "projects.any": self.project_gid,
            "opt_fields": "name,completed,custom_fields,notes,gid,memberships.section.name",
        }
        if text:
            params["text"] = text
        if completed is not None:
            params["completed"] = str(completed).lower()
        return self._get_paginated(f"/workspaces/{self.workspace_gid}/tasks/search", params)

    def get_all_tasks(self) -> list[dict]:
        """Get all tasks in the project."""
        return self._get_paginated(
            f"/tasks",
            {
                "project": self.project_gid,
                "opt_fields": "name,completed,custom_fields,notes,gid,memberships.section.name",
            },
        )

    def get_task(self, gid: str) -> dict | None:
        resp = self._request(
            "GET",
            f"/tasks/{gid}?opt_fields=name,completed,custom_fields,notes,memberships.section.name",
        )
        return resp.get("data") if resp else None

    def create_task(
        self,
        name: str,
        notes: str = "",
        section_gid: str = None,
        custom_fields: dict = None,
    ) -> str | None:
        """Create a task. Returns task gid."""
        if self.dry_run:
            print(f"  [DRY-RUN] Would create Asana task: {name}")
            return None

        body = {
            "name": name,
            "notes": notes,
            "projects": [self.project_gid],
        }
        if custom_fields:
            body["custom_fields"] = custom_fields

        resp = self._request("POST", "/tasks", body)
        if not resp:
            return None
        task_gid = resp["data"]["gid"]

        # Move to section
        if section_gid:
            self._request(
                "POST",
                f"/sections/{section_gid}/addTask",
                {"task": task_gid},
            )

        return task_gid

    def update_task(self, gid: str, updates: dict):
        """Update a task."""
        if self.dry_run:
            print(f"  [DRY-RUN] Would update Asana task {gid}: {updates}")
            return
        self._request("PUT", f"/tasks/{gid}", updates)

    def complete_task(self, gid: str):
        self.update_task(gid, {"completed": True})

    def uncomplete_task(self, gid: str):
        self.update_task(gid, {"completed": False})

    def get_initiative_id_from_task(self, task: dict) -> str:
        """Extract Initiative ID custom field value from task."""
        for cf in task.get("custom_fields", []):
            if cf.get("name") == "Initiative ID":
                return cf.get("text_value", "") or cf.get("display_value", "") or ""
        return ""

    def build_custom_field_values(self, init: Initiative) -> dict:
        """Build custom_fields dict for Asana API from initiative data."""
        fields = self.get_custom_fields()
        cf = {}

        if "Initiative ID" in fields:
            cf[fields["Initiative ID"]["gid"]] = init.id

        if "Горизонт" in fields:
            horizon_field = fields["Горизонт"]
            if init.horizon in horizon_field.get("enum_options", {}):
                cf[horizon_field["gid"]] = horizon_field["enum_options"][init.horizon]

        if "Статус" in fields:
            status_field = fields["Статус"]
            if init.status in status_field.get("enum_options", {}):
                cf[status_field["gid"]] = status_field["enum_options"][init.status]

        return cf


# ─── Sync Engine ─────────────────────────────────────────────────────────────


class SyncEngine:
    """Orchestrates sync between roadmap.md, GitHub Issues, and Asana."""

    def __init__(
        self,
        gh: GitHubClient,
        asana: AsanaClient | None,
        dry_run: bool = False,
        verbose: bool = False,
    ):
        self.gh = gh
        self.asana = asana
        self.dry_run = dry_run
        self.verbose = verbose
        self.links = load_links()
        self.changes: list[str] = []

    def _log(self, msg: str):
        self.changes.append(msg)
        print(f"  {msg}")

    def _save_roadmap(self, text: str):
        """Atomically write roadmap.md."""
        if self.dry_run:
            return
        tmp = ROADMAP_PATH.with_suffix(".tmp")
        tmp.write_text(text)
        tmp.replace(ROADMAP_PATH)

    # ── Issue title/body formatting ──

    def _issue_title(self, init: Initiative) -> str:
        return f"{ROADMAP_ISSUE_PREFIX} {init.id}: {init.name}"

    def _issue_body(self, init: Initiative) -> str:
        lines = [
            f"**Track:** {init.track}",
            f"**Initiative:** {init.id}",
            f"**Horizon:** {init.horizon}",
            f"**Status:** {init.status}",
        ]
        if init.deps and init.deps != "—":
            lines.append(f"**Dependencies:** {init.deps}")
        if init.owner:
            lines.append(f"**Owner:** {init.owner}")
        if init.deadline:
            lines.append(f"**Deadline:** {init.deadline}")
        lines.append("")
        lines.append("---")
        lines.append("*Managed by roadmap_sync.py — do not edit title format*")
        return "\n".join(lines)

    def _asana_task_name(self, init: Initiative) -> str:
        return f"{init.id}: {init.name}"

    def _asana_task_notes(self, init: Initiative, gh_issue_num: int = None) -> str:
        lines = [
            f"Track: {init.track}",
            f"Horizon: {init.horizon}",
        ]
        if init.deps and init.deps != "—":
            lines.append(f"Dependencies: {init.deps}")
        if init.owner:
            lines.append(f"Owner: {init.owner}")
        if init.deadline:
            lines.append(f"Deadline: {init.deadline}")
        if gh_issue_num:
            lines.append("")
            lines.append(f"GitHub: https://github.com/{self.gh.repo}/issues/{gh_issue_num}")
        return "\n".join(lines)

    # ── Reverse sync: Asana → roadmap ──

    def reverse(self):
        """Pull completion status from Asana → roadmap.md."""
        print("\n▸ Reverse sync: Asana → roadmap.md")

        if not self.asana:
            print("  Skipping: Asana not configured")
            return

        if not self.links:
            print("  No links found. Run 'bootstrap' first.")
            return

        roadmap_text = ROADMAP_PATH.read_text()
        initiatives = parse_roadmap(roadmap_text)
        init_map = {i.id: i for i in initiatives}

        # Get all Asana tasks
        asana_tasks = self.asana.get_all_tasks()
        asana_by_init = {}
        for task in asana_tasks:
            init_id = self.asana.get_initiative_id_from_task(task)
            if init_id:
                asana_by_init[init_id] = task

        changes_made = False
        for init_id, link in self.links.items():
            asana_gid = link.get("asana")
            if not asana_gid:
                continue

            task = asana_by_init.get(init_id)
            if not task:
                continue

            init = init_map.get(init_id)
            if not init:
                continue

            # Asana completed → roadmap "Готово"
            if task.get("completed") and init.status != "Готово":
                self._log(f"  {init_id}: Asana completed → roadmap 'Готово' (was '{init.status}')")
                roadmap_text = update_roadmap_status(roadmap_text, init_id, "Готово")
                changes_made = True

            # Asana uncompleted but roadmap says "Готово" → revert to Asana status
            elif not task.get("completed") and init.status == "Готово":
                # Check Asana custom field for real status
                asana_status = ""
                for cf in task.get("custom_fields", []):
                    if cf.get("name") == "Статус" and cf.get("display_value"):
                        asana_status = cf["display_value"]
                if asana_status and asana_status != "Готово":
                    self._log(f"  {init_id}: Asana reopened → roadmap '{asana_status}' (was 'Готово')")
                    roadmap_text = update_roadmap_status(roadmap_text, init_id, asana_status)
                    changes_made = True

        if changes_made:
            self._save_roadmap(roadmap_text)
            if not self.dry_run:
                self._log("roadmap.md updated")
        else:
            print("  No changes from Asana")

    # ── Forward sync: roadmap → GitHub → Asana ──

    def forward(self):
        """Push roadmap changes → GitHub Issues → Asana."""
        print("\n▸ Forward sync: roadmap.md → GitHub Issues → Asana")

        roadmap_text = ROADMAP_PATH.read_text()
        initiatives = parse_roadmap(roadmap_text)

        if not initiatives:
            print("  No initiatives found in roadmap.md")
            return

        # Ensure labels exist
        all_labels = set()
        for init in initiatives:
            all_labels.add("roadmap")
            all_labels.add(init.track)
            all_labels.add(init.horizon)
        self.gh.ensure_labels(list(all_labels))

        for init in initiatives:
            self._sync_initiative_forward(init)

        save_links(self.links)

    def _sync_initiative_forward(self, init: Initiative):
        """Sync one initiative: roadmap → GitHub → Asana."""
        link = self.links.get(init.id, {})
        gh_num = link.get("gh")
        asana_gid = link.get("asana")

        # ── GitHub Issue ──
        labels = ["roadmap", init.track, init.horizon]

        if gh_num:
            # Update existing issue
            issue = self.gh.get_issue(gh_num)
            if issue:
                new_title = self._issue_title(init)
                new_body = self._issue_body(init)
                needs_update = False

                if issue["title"] != new_title:
                    needs_update = True
                if issue.get("body", "").strip() != new_body.strip():
                    needs_update = True

                # Check state
                if init.status == "Готово" and issue["state"] == "OPEN":
                    self._log(f"{init.id}: closing GitHub #{gh_num} (status=Готово)")
                    self.gh.close_issue(gh_num)
                elif init.status != "Готово" and issue["state"] == "CLOSED":
                    self._log(f"{init.id}: reopening GitHub #{gh_num} (status={init.status})")
                    self.gh.reopen_issue(gh_num)

                if needs_update:
                    self._log(f"{init.id}: updating GitHub #{gh_num}")
                    self.gh.update_issue(gh_num, title=new_title, body=new_body, labels=labels)
        else:
            # Create new issue
            title = self._issue_title(init)
            body = self._issue_body(init)
            self._log(f"{init.id}: creating GitHub issue")
            gh_num = self.gh.create_issue(title, body, labels)
            if gh_num:
                if init.id not in self.links:
                    self.links[init.id] = {}
                self.links[init.id]["gh"] = gh_num

        # ── Asana Task ──
        if not self.asana:
            return

        section_name = TRACK_MAP.get(init.track, init.track)
        section_gid = self.asana.ensure_section(section_name)
        cf_values = self.asana.build_custom_field_values(init)

        if asana_gid:
            # Update existing task
            task = self.asana.get_task(asana_gid)
            if task:
                updates = {}
                new_name = self._asana_task_name(init)
                if task.get("name") != new_name:
                    updates["name"] = new_name

                new_notes = self._asana_task_notes(init, gh_num)
                if task.get("notes", "").strip() != new_notes.strip():
                    updates["notes"] = new_notes

                if cf_values:
                    updates["custom_fields"] = cf_values

                if init.status == "Готово" and not task.get("completed"):
                    self._log(f"{init.id}: completing Asana task")
                    self.asana.complete_task(asana_gid)
                elif init.status != "Готово" and task.get("completed"):
                    self._log(f"{init.id}: uncompleting Asana task")
                    self.asana.uncomplete_task(asana_gid)

                if updates:
                    self._log(f"{init.id}: updating Asana task")
                    self.asana.update_task(asana_gid, updates)
        else:
            # Create new task
            self._log(f"{init.id}: creating Asana task")
            notes = self._asana_task_notes(init, gh_num)
            asana_gid = self.asana.create_task(
                name=self._asana_task_name(init),
                notes=notes,
                section_gid=section_gid,
                custom_fields=cf_values,
            )
            if asana_gid:
                if init.id not in self.links:
                    self.links[init.id] = {}
                self.links[init.id]["asana"] = asana_gid

    # ── Status ──

    def status(self):
        """Show current diff between roadmap, GitHub, and Asana."""
        print("\n▸ Status: roadmap.md ↔ GitHub ↔ Asana")

        roadmap_text = ROADMAP_PATH.read_text()
        initiatives = parse_roadmap(roadmap_text)
        init_map = {i.id: i for i in initiatives}

        print(f"\n  Roadmap: {len(initiatives)} initiatives")
        print(f"  Links: {len(self.links)} linked")

        # Track stats
        by_track: dict[str, list] = {}
        by_status: dict[str, int] = {}
        for init in initiatives:
            by_track.setdefault(init.track, []).append(init)
            by_status[init.status] = by_status.get(init.status, 0) + 1

        print("\n  By track:")
        for track, inits in sorted(by_track.items()):
            print(f"    {track}: {len(inits)}")

        print("\n  By status:")
        for status, count in sorted(by_status.items(), key=lambda x: -x[1]):
            print(f"    {status}: {count}")

        # Unlinked initiatives
        unlinked = [i for i in initiatives if i.id not in self.links]
        if unlinked:
            print(f"\n  Unlinked ({len(unlinked)}):")
            for i in unlinked:
                print(f"    {i.id}: {i.name}")

        # Orphan links (in links but not in roadmap)
        orphans = [lid for lid in self.links if lid not in init_map]
        if orphans:
            print(f"\n  Orphan links ({len(orphans)}) — in links but not in roadmap:")
            for lid in orphans:
                print(f"    {lid}: gh=#{self.links[lid].get('gh', '?')}")

        # Status mismatches (if Asana configured)
        if self.asana and self.links:
            print("\n  Checking Asana status mismatches...")
            asana_tasks = self.asana.get_all_tasks()
            asana_by_init = {}
            for task in asana_tasks:
                init_id = self.asana.get_initiative_id_from_task(task)
                if init_id:
                    asana_by_init[init_id] = task

            mismatches = []
            for init_id, link in self.links.items():
                if not link.get("asana"):
                    continue
                task = asana_by_init.get(init_id)
                init = init_map.get(init_id)
                if not task or not init:
                    continue

                if task.get("completed") and init.status != "Готово":
                    mismatches.append(f"    {init_id}: Asana=completed, roadmap='{init.status}'")
                elif not task.get("completed") and init.status == "Готово":
                    mismatches.append(f"    {init_id}: Asana=open, roadmap='Готово'")

            if mismatches:
                print(f"\n  Status mismatches ({len(mismatches)}):")
                for m in mismatches:
                    print(m)
            else:
                print("  No status mismatches")

    # ── Bootstrap ──

    def bootstrap(self):
        """Link existing GitHub issues and Asana tasks to roadmap initiatives."""
        print("\n▸ Bootstrap: linking existing items")

        roadmap_text = ROADMAP_PATH.read_text()
        initiatives = parse_roadmap(roadmap_text)

        if not initiatives:
            print("  No initiatives found in roadmap.md")
            return

        print(f"  Found {len(initiatives)} initiatives in roadmap")

        # Ensure custom fields in Asana
        if self.asana:
            print("  Ensuring Asana custom fields...")
            self.asana.ensure_custom_fields()

        # Ensure labels in GitHub
        all_labels = {"roadmap"}
        for init in initiatives:
            all_labels.add(init.track)
            all_labels.add(init.horizon)
        print(f"  Ensuring {len(all_labels)} GitHub labels...")
        self.gh.ensure_labels(list(all_labels))

        # Get existing GitHub issues
        gh_issues = self.gh.list_issues(state="all")
        gh_by_id: dict[str, dict] = {}
        for issue in gh_issues:
            # Match by [Track] ID: prefix in title
            match = re.match(r"\[Track\]\s+([A-Z]+\d+[a-z]?):", issue["title"])
            if match:
                gh_by_id[match.group(1)] = issue

        print(f"  Found {len(gh_by_id)} existing GitHub issues with [Track] prefix")

        # Get existing Asana tasks
        asana_by_id: dict[str, dict] = {}
        if self.asana:
            asana_tasks = self.asana.get_all_tasks()
            for task in asana_tasks:
                init_id = self.asana.get_initiative_id_from_task(task)
                if init_id:
                    asana_by_id[init_id] = task
                else:
                    # Try matching ID in name: "ID: ...", "[Track] ID: ...", etc.
                    match = re.search(r"(?:^|\]\s*)([A-Z]+\d+[a-z]?):\s", task.get("name", ""))
                    if match:
                        asana_by_id[match.group(1)] = task

            print(f"  Found {len(asana_by_id)} existing Asana tasks")

        # Link and create
        linked = 0
        created_gh = 0
        created_asana = 0

        for init in initiatives:
            if init.id not in self.links:
                self.links[init.id] = {}

            # GitHub
            if init.id in gh_by_id:
                self.links[init.id]["gh"] = gh_by_id[init.id]["number"]
                linked += 1
            elif not self.links[init.id].get("gh"):
                self._log(f"{init.id}: creating GitHub issue")
                labels = ["roadmap", init.track, init.horizon]
                gh_num = self.gh.create_issue(
                    self._issue_title(init),
                    self._issue_body(init),
                    labels,
                )
                if gh_num:
                    self.links[init.id]["gh"] = gh_num
                    created_gh += 1

            # Asana
            if self.asana:
                if init.id in asana_by_id:
                    self.links[init.id]["asana"] = asana_by_id[init.id]["gid"]
                    # Update custom fields on existing task
                    cf_values = self.asana.build_custom_field_values(init)
                    if cf_values:
                        self.asana.update_task(asana_by_id[init.id]["gid"], {"custom_fields": cf_values})
                    linked += 1
                elif not self.links[init.id].get("asana"):
                    gh_num = self.links[init.id].get("gh")
                    section_name = TRACK_MAP.get(init.track, init.track)
                    section_gid = self.asana.ensure_section(section_name)
                    cf_values = self.asana.build_custom_field_values(init)

                    self._log(f"{init.id}: creating Asana task")
                    asana_gid = self.asana.create_task(
                        name=self._asana_task_name(init),
                        notes=self._asana_task_notes(init, gh_num),
                        section_gid=section_gid,
                        custom_fields=cf_values,
                    )
                    if asana_gid:
                        self.links[init.id]["asana"] = asana_gid
                        created_asana += 1

        save_links(self.links)
        print(f"\n  Summary: {linked} linked, {created_gh} GitHub issues created, {created_asana} Asana tasks created")
        print(f"  Links saved to {LINKS_PATH}")

    # ── Full sync ──

    def full(self):
        """Full sync: reverse then forward."""
        self.reverse()
        self.forward()

    # ── Report ──

    def report(self):
        """Print summary of changes made."""
        if self.changes:
            print(f"\n▸ Changes ({len(self.changes)}):")
            for c in self.changes:
                print(f"  {c}")
        else:
            print("\n▸ No changes made")


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Sync roadmap.md ↔ GitHub Issues ↔ Asana",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="full",
        choices=["full", "forward", "reverse", "status", "bootstrap"],
        help="Sync command (default: full)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    # Load env
    env = load_env()
    if not env and args.command != "status":
        print(f"WARNING: {ENV_PATH} not found. Asana sync will be skipped.", file=sys.stderr)
        print(f"Create it with ASANA_TOKEN, ASANA_PROJECT_GID, ASANA_WORKSPACE_GID", file=sys.stderr)

    # Check roadmap exists
    if not ROADMAP_PATH.exists():
        print(f"ERROR: {ROADMAP_PATH} not found", file=sys.stderr)
        sys.exit(1)

    # Get repo
    repo = get_repo()
    if args.verbose:
        print(f"Repo: {repo}")

    # Init clients
    gh = GitHubClient(repo, dry_run=args.dry_run, verbose=args.verbose)

    asana = None
    asana_token = env.get("ASANA_TOKEN")
    asana_project = env.get("ASANA_PROJECT_GID")
    asana_workspace = env.get("ASANA_WORKSPACE_GID")
    if asana_token and asana_project and asana_workspace:
        asana = AsanaClient(
            token=asana_token,
            project_gid=asana_project,
            workspace_gid=asana_workspace,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )

    engine = SyncEngine(gh, asana, dry_run=args.dry_run, verbose=args.verbose)

    # Dispatch
    if args.dry_run:
        print("═══ DRY RUN ═══")

    commands = {
        "full": engine.full,
        "forward": engine.forward,
        "reverse": engine.reverse,
        "status": engine.status,
        "bootstrap": engine.bootstrap,
    }

    commands[args.command]()
    engine.report()

    if args.dry_run:
        print("\n═══ DRY RUN — no changes made ═══")


if __name__ == "__main__":
    main()
