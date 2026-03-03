#!/usr/bin/env python3
"""Generate a GitHub Pages site for BLT Ideas with overlap analysis,
discussion links, repo links, and interested contributors."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "OWASP-BLT"
REPO_NAME = "BLT-Ideas"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
ORG = "OWASP-BLT"

# Maximum number of contributors to display per idea row before truncating
MAX_DISPLAY_CONTRIBUTORS = 10

# Known BLT org repos for each idea (from file content "Repository:" lines and README)
IDEA_REPO_MAP = {
    "A": "OWASP-BLT/BLT",
    "B": "OWASP-BLT/BLT",
    "C": "OWASP-BLT/BLT",
    "D": "OWASP-BLT/BLT",
    "E": "OWASP-BLT/BLT",
    "E.1": "OWASP-BLT/BLT",
    "E.2": "OWASP-BLT/BLT",
    "F": "OWASP-BLT/BLT",
    "G": "OWASP-BLT/BLT-NetGuardian",
    "H": "OWASP-BLT/BLT",
    "I": "OWASP-BLT/BLT",
    "J": "OWASP-BLT/BLT",
    "K": "OWASP-BLT/BLT",
    "L": "OWASP-BLT/BLT",
    "L2": "OWASP-BLT/BLT",
    "M": "OWASP-BLT/BLT",
    "N": "OWASP-BLT/BLT",
    "O": "OWASP-BLT/BLT-Extension",
    "P": "OWASP-BLT/BLT",
    "Q": "OWASP-BLT/BLT",
    "R": "OWASP-BLT/BLT-Flutter",
    "RS": "OWASP-BLT/BLT",
    "S": "OWASP-BLT/BLT-CVE",
    "T": "OWASP-BLT/BLT-NetGuardian",
    "U": "OWASP-BLT/BLT",
    "V": "OWASP-BLT/BLT-API",
    "W": "OWASP-BLT/BLT",
    "X": "OWASP-BLT/BLT",
    "Y": "OWASP-BLT/BLT",
    "Z": "OWASP-BLT/BLT",
}


def github_api_rest(endpoint):
    """Call GitHub REST API."""
    if not GITHUB_TOKEN:
        return None
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "BLT-Ideas-Page-Generator",
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (URLError, HTTPError) as e:
        print(f"  REST API error for {endpoint}: {e}", file=sys.stderr)
        return None


def github_graphql(query):
    """Call GitHub GraphQL API."""
    if not GITHUB_TOKEN:
        return None
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "BLT-Ideas-Page-Generator",
    }
    data = json.dumps({"query": query}).encode()
    try:
        req = Request("https://api.github.com/graphql", data=data, headers=headers)
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (URLError, HTTPError) as e:
        print(f"  GraphQL API error: {e}", file=sys.stderr)
        return None


def get_file_contributors(filepath):
    """Get unique contributors for a specific file via git log."""
    try:
        result = subprocess.run(
            ["git", "log", "--format=%ae|||%an", "--follow", "--", filepath],
            capture_output=True,
            text=True,
            cwd=Path(filepath).parent if Path(filepath).is_absolute() else ".",
        )
        contributors = {}
        for line in result.stdout.strip().splitlines():
            if "|||" in line:
                email, name = line.split("|||", 1)
                email = email.strip()
                name = name.strip()
                if email and name:
                    contributors[email] = name
        return list(contributors.values())
    except Exception as e:
        print(f"  git log error for {filepath}: {e}", file=sys.stderr)
        return []


def get_discussion_participants(discussion_num):
    """Fetch participants from an OWASP-BLT org discussion via GraphQL."""
    if not discussion_num or not GITHUB_TOKEN:
        return []

    query = """
    {
      organization(login: "OWASP-BLT") {
        discussion(number: %s) {
          author { login }
          comments(first: 100) {
            nodes {
              author { login }
            }
          }
        }
      }
    }
    """ % discussion_num

    data = github_graphql(query)
    if not data or "data" not in data:
        return []

    participants = set()
    disc = (data.get("data") or {}).get("organization") or {}
    disc = disc.get("discussion") or {}
    if disc.get("author"):
        participants.add(disc["author"]["login"])
    for comment in (disc.get("comments") or {}).get("nodes") or []:
        if comment.get("author"):
            participants.add(comment["author"]["login"])
    return sorted(participants)


def get_pr_participants():
    """Fetch recent PR authors/commenters for this repo."""
    prs = github_api_rest(
        f"/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=all&per_page=100"
    )
    if not prs:
        return {}
    result = {}
    for pr in prs:
        number = pr.get("number")
        login = (pr.get("user") or {}).get("login", "")
        if login:
            result.setdefault(number, set()).add(login)
    return result


def parse_idea_file(path):
    """Parse a single Idea-*.md file and extract metadata."""
    content = path.read_text(encoding="utf-8")
    filename = path.stem  # e.g. "Idea-A"

    # Idea ID from filename
    idea_id = filename.replace("Idea-", "")  # e.g. "A", "B", "E.1", "RS"

    # Extract title from first heading
    title_match = re.search(r"^#+ (.+)", content, re.MULTILINE)
    raw_title = title_match.group(1).strip() if title_match else filename

    # Clean up title: remove leading "Idea X — " / "Idea X – " / "Idea X - " patterns.
    # The character class intentionally covers em dash (—), en dash (–), and hyphen (-).
    title = re.sub(
        r"^Idea\s+[A-Z0-9.]+\s*[—–\-]+\s*", "", raw_title, flags=re.IGNORECASE
    ).strip()
    # If title still starts with "Idea X" pattern, keep it as-is for short filenames
    if not title:
        title = raw_title

    # Extract one-liner
    oneliner = ""
    for pattern in [
        r"\*\*One line:\*\*\s*(.+?)(?:\n|$)",
        r"\*\*One line\*\*:\s*(.+?)(?:\n|$)",
        r"One line[:\s]+(.+?)(?:\n|$)",
    ]:
        m = re.search(pattern, content)
        if m:
            oneliner = m.group(1).strip().strip("*")
            break

    # Extract discussion URL
    disc_match = re.search(
        r"https://github\.com/orgs/OWASP-BLT/discussions/(\d+)", content
    )
    discussion_url = disc_match.group(0) if disc_match else ""
    discussion_num = disc_match.group(1) if disc_match else ""

    # Extract BLT org repo from "Repository:" line, else use known map
    repo_match = re.search(
        r"\*?\*?Repository[:\s]+\*?\*?\s*(OWASP[-/]\S+)", content, re.IGNORECASE
    )
    if repo_match:
        blt_repo = repo_match.group(1).rstrip(")")
        # Normalise OWASP/ → OWASP-BLT/
        blt_repo = re.sub(r"^OWASP/", "OWASP-BLT/", blt_repo)
    else:
        blt_repo = IDEA_REPO_MAP.get(idea_id, f"{REPO_OWNER}/BLT")

    # Find related ideas — any mention of "Idea X" where X is a known idea ID format:
    # single letter (A–Z), two-letter compound (RS), digit-suffixed (E.1, E.2, L2).
    related = set()
    for m in re.finditer(
        r"\bIdea\s+([A-Z]{1,2}[0-9]*(?:\.[0-9]+)?(?:\s*\(Extended\))?)\b", content
    ):
        other = m.group(1).strip()
        # Normalise "(Extended)" suffix
        if "(Extended)" in other:
            other = other.replace("(Extended)", "").strip() + " (Extended)"
        if other != idea_id:
            related.add(other)

    return {
        "id": idea_id,
        "filename": path.name,
        "raw_title": raw_title,
        "title": title,
        "one_liner": oneliner,
        "discussion_url": discussion_url,
        "discussion_num": discussion_num,
        "blt_repo": blt_repo,
        "related": sorted(related),
        "git_contributors": [],
        "discussion_participants": [],
    }


def sort_key(idea_id):
    """Sort ideas: single letters first, then compound IDs."""
    # Map E.1 → E, E.2 → E Extended, RS → after R, L2 → after L
    mapping = {
        "E.1": ("E", 1),
        "E.2": ("E", 2),
        "L2": ("L", 2),
        "RS": ("RS", 0),
    }
    if idea_id in mapping:
        letter, sub = mapping[idea_id]
    elif len(idea_id) == 1:
        letter, sub = idea_id, 0
    else:
        letter, sub = idea_id, 0
    return (letter, sub)


def build_overlap_matrix(ideas):
    """Build a symmetric overlap/dependency matrix."""
    idea_ids = [i["id"] for i in ideas]
    # Matrix: overlap[i][j] = True if idea i references idea j or vice-versa
    matrix = {a: {b: False for b in idea_ids} for a in idea_ids}

    for idea in ideas:
        for rel in idea["related"]:
            # Normalise: map "E (Extended)" → E.2, plain letters to their IDs
            target = rel
            if target in idea_ids:
                matrix[idea["id"]][target] = True
                matrix[target][idea["id"]] = True
            else:
                # Try to find partial match
                for other_id in idea_ids:
                    if target.startswith(other_id) or other_id.startswith(target):
                        matrix[idea["id"]][other_id] = True
                        matrix[other_id][idea["id"]] = True

    return matrix


def html_escape(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_html(ideas, overlap_matrix):
    """Generate a complete HTML page with sortable table and overlap analysis."""

    # Prepare table rows
    rows_html = []
    for idea in ideas:
        idea_id = idea["id"]
        title = html_escape(idea["title"])
        one_liner = html_escape(
            idea["one_liner"][:120] + ("…" if len(idea["one_liner"]) > 120 else "")
        )

        # Idea file link (in this repo)
        file_url = f"{REPO_URL}/blob/main/{idea['filename']}"
        idea_link = f'<a href="{file_url}" title="{html_escape(idea["raw_title"])}" target="_blank">Idea&nbsp;{html_escape(idea_id)}</a>'

        # BLT org repo link
        blt_repo = idea["blt_repo"]
        repo_url = f"https://github.com/{blt_repo}"
        repo_link = f'<a href="{repo_url}" target="_blank">{html_escape(blt_repo.split("/")[-1])}</a>'

        # Discussion link
        if idea["discussion_url"]:
            disc_link = f'<a href="{idea["discussion_url"]}" target="_blank">#{idea["discussion_num"]}</a>'
        else:
            disc_link = '<span class="muted">—</span>'

        # Related ideas
        related_links = []
        for rel in idea["related"]:
            # Find the idea with this ID to get its file URL
            rel_idea = next((i for i in ideas if i["id"] == rel), None)
            if rel_idea:
                rel_file_url = f"{REPO_URL}/blob/main/{rel_idea['filename']}"
                related_links.append(
                    f'<a href="{rel_file_url}" target="_blank" class="badge">Idea&nbsp;{html_escape(rel)}</a>'
                )
            else:
                related_links.append(
                    f'<span class="badge">Idea&nbsp;{html_escape(rel)}</span>'
                )
        related_html = " ".join(related_links) if related_links else '<span class="muted">—</span>'

        # Interested contributors (git + discussion)
        all_contributors = sorted(
            set(idea["git_contributors"] + idea["discussion_participants"])
        )
        if all_contributors:
            contrib_html = ", ".join(
                html_escape(c) for c in all_contributors[:MAX_DISPLAY_CONTRIBUTORS]
            )
            if len(all_contributors) > MAX_DISPLAY_CONTRIBUTORS:
                contrib_html += f' <small>(+{len(all_contributors) - MAX_DISPLAY_CONTRIBUTORS} more)</small>'
        else:
            contrib_html = '<span class="muted">—</span>'

        # Overlap count for sorting
        overlap_count = sum(
            1 for other_id, v in overlap_matrix.get(idea_id, {}).items() if v and other_id != idea_id
        )

        rows_html.append(
            f"""      <tr>
        <td data-sort="{html_escape(idea_id)}">{idea_link}</td>
        <td data-sort="{title}">{title}</td>
        <td class="oneliner" data-sort="{html_escape(idea["one_liner"])}">{one_liner}</td>
        <td data-sort="{html_escape(blt_repo)}">{repo_link}</td>
        <td data-sort="{(idea.get('discussion_num') or '0').zfill(6)}">{disc_link}</td>
        <td data-sort="{overlap_count:03d}">{related_html}</td>
        <td data-sort="{len(all_contributors):03d}">{contrib_html}</td>
      </tr>"""
        )

    # Overlap matrix HTML
    all_ids = [i["id"] for i in ideas]
    matrix_headers = "".join(
        f'<th class="matrix-head" title="Idea {html_escape(i)}">{html_escape(i)}</th>'
        for i in all_ids
    )
    matrix_rows = []
    for row_idea in ideas:
        rid = row_idea["id"]
        file_url = f"{REPO_URL}/blob/main/{row_idea['filename']}"
        cells = f'<td class="matrix-label"><a href="{file_url}" target="_blank">{html_escape(rid)}</a></td>'
        for col_id in all_ids:
            if col_id == rid:
                cells += '<td class="matrix-self">·</td>'
            elif overlap_matrix.get(rid, {}).get(col_id):
                cells += f'<td class="matrix-yes" title="Idea {html_escape(rid)} ↔ Idea {html_escape(col_id)}">✓</td>'
            else:
                cells += '<td class="matrix-no"></td>'
        matrix_rows.append(f"<tr>{cells}</tr>")

    table_rows = "\n".join(rows_html)
    matrix_rows_html = "\n".join(matrix_rows)
    total_ideas = len(ideas)

    # Ideas with the most connections
    top_connected = sorted(
        ideas,
        key=lambda i: sum(1 for v in overlap_matrix.get(i["id"], {}).values() if v),
        reverse=True,
    )[:5]
    top_connected_html = "".join(
        f'<li><strong>Idea {html_escape(i["id"])}</strong> — {html_escape(i["title"])} '
        f'({sum(1 for v in overlap_matrix.get(i["id"], {}).values() if v)} connections)</li>'
        for i in top_connected
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BLT Ideas — Analysis Dashboard</title>

  <!-- Inline theme init — must run before first paint to prevent flash -->
  <script>
    (function () {{
      var saved = localStorage.getItem('blt-theme');
      if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
        document.documentElement.classList.add('dark');
      }}
    }})();
  </script>

  <!-- Manrope typeface -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <!-- Tailwind CDN + design-system config -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{ manrope: ['Manrope', 'sans-serif'] }},
          colors: {{
            brand: {{ DEFAULT: '#E10101', hover: '#c40000' }},
          }},
        }},
      }},
    }};
  </script>

  <style>
    /* ── Design tokens ──────────────────────────────────────────────────── */
    :root {{
      --color-brand:       #E10101;
      --color-brand-hover: #c40000;
      /* Light mode */
      --bg-base:           #ffffff;
      --bg-subtle:         #f6f8fa;
      --bg-inset:          #eaeef2;
      --border-default:    #d0d7de;
      --border-muted:      #e8eaed;
      --text-primary:      #1f2328;
      --text-secondary:    #656d76;
      --text-muted:        #9198a1;
      --link-color:        #0969da;
      --accent-num:        #0550ae;
      /* Component tokens */
      --border-component:  #E5E5E5;
      --shadow-soft:       0 1px 3px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.06);
      --shadow-lift:       0 4px 12px rgba(0,0,0,.12), 0 8px 24px rgba(0,0,0,.08);
      --radius-section:    1rem;
      --radius-card:       0.75rem;
      --radius-small:      0.5rem;
      --radius-button:     0.375rem;
      --radius-badge:      9999px;
    }}
    .dark {{
      /* Dark mode */
      --bg-base:           #0d1117;
      --bg-subtle:         #161b22;
      --bg-inset:          #21262d;
      --border-default:    #30363d;
      --border-muted:      #21262d;
      --text-primary:      #f0f6fc;
      --text-secondary:    #8b949e;
      --text-muted:        #484f58;
      --link-color:        #58a6ff;
      --accent-num:        #58a6ff;
      --border-component:  #374151;
      --shadow-soft:       0 1px 3px rgba(0,0,0,.3), 0 4px 12px rgba(0,0,0,.2);
      --shadow-lift:       0 4px 16px rgba(0,0,0,.4), 0 8px 28px rgba(0,0,0,.25);
    }}

    /* ── Globals ────────────────────────────────────────────────────────── */
    html {{ scroll-behavior: smooth; }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Manrope', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      background: var(--bg-base);
      color: var(--text-primary);
      font-size: 14px;
      line-height: 1.5;
      transition: background-color 0.2s ease, color 0.2s ease;
    }}
    a {{ color: var(--link-color); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    header {{
      background: var(--bg-subtle);
      border-bottom: 1px solid var(--border-default);
      height: 4rem;
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      padding: 0 2rem;
    }}
    header h1 {{
      font-size: clamp(1rem, 2vw, 1.35rem);
      color: var(--text-primary);
      font-weight: 800;
      letter-spacing: -0.02em;
      margin: 0;
      line-height: 1;
      white-space: nowrap;
    }}
    /* Dark mode header overrides */
    .dark header {{
      background: linear-gradient(135deg, #161c2c 0%, #1e2438 100%);
      border-bottom-color: #2d3550;
    }}
    .dark header h1 {{ color: #e2e8f0; }}
    .dark header .btn-secondary {{
      color: #e6edf3;
      border-color: rgba(240,246,252,0.2);
    }}
    .dark header .btn-secondary:hover {{
      background: rgba(255,255,255,0.08);
      border-color: rgba(240,246,252,0.45);
    }}
    header p {{ color: #8b949e; margin-top: 6px; font-size: 13px; font-weight: 600; }}
    header a {{ font-weight: 600; }}
    .container {{ max-width: 80rem; margin: 0 auto; padding-top: 2.5rem; padding-bottom: 2.5rem; }}
    .stats {{
      display: flex; gap: 16px; flex-wrap: wrap;
    }}
    .stat-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-component);
      border-radius: var(--radius-card);
      padding: 16px 20px; flex: 1; min-width: 140px;
      box-shadow: var(--shadow-soft);
      transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .stat-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-lift);
    }}
    .stat-card .num {{
      font-size: clamp(1.5rem, 3vw, 2rem);
      font-weight: 800;
      color: #E10101;
      letter-spacing: -0.02em;
    }}
    .stat-card .label {{ font-size: 12px; color: #8b949e; margin-top: 4px; font-weight: 600; }}

    /* Filter / search */
    .toolbar {{
      display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; align-items: center;
    }}
    .toolbar input {{
      background: var(--bg-subtle); border: 1px solid var(--border-component);
      border-radius: var(--radius-button);
      color: var(--text-primary); padding: 7px 12px; font-size: 13px;
      width: 260px; min-height: 44px;
      transition: border-color 0.15s;
    }}
    .toolbar input:focus {{
      outline: none;
      border-color: var(--color-brand);
      box-shadow: 0 0 0 3px rgba(225,1,1,.15);
    }}
    .toolbar select {{
      background: var(--bg-subtle); border: 1px solid var(--border-component);
      border-radius: var(--radius-button);
      color: var(--text-primary); padding: 7px 10px; font-size: 13px;
      min-height: 44px; cursor: pointer;
      transition: border-color 0.15s;
    }}
    .toolbar select:focus {{
      outline: none;
      border-color: var(--color-brand);
      box-shadow: 0 0 0 3px rgba(225,1,1,.15);
    }}
    .toolbar label {{ font-size: 13px; color: #8b949e; font-weight: 600; }}

    /* Table */
    .table-wrap {{
      overflow-x: auto;
      overflow-y: auto;
      max-height: calc(100vh - 13rem);
      border: 1px solid var(--border-component);
      border-radius: var(--radius-section);
      box-shadow: var(--shadow-soft);
    }}
    table {{
      width: 100%; border-collapse: collapse; background: var(--bg-subtle);
    }}
    thead th {{
      position: sticky;
      top: 0;
      z-index: 2;
      background: var(--bg-inset); color: var(--text-secondary); font-size: 12px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .5px;
      padding: 10px 12px; border-bottom: 1px solid var(--border-component);
      cursor: pointer; user-select: none; white-space: nowrap;
    }}
    thead th:hover {{ background: var(--bg-subtle); color: var(--text-primary); }}
    thead th.sorted-asc::after  {{ content: " ↑"; color: var(--color-brand); }}
    thead th.sorted-desc::after {{ content: " ↓"; color: var(--color-brand); }}
    tbody tr {{ border-bottom: 1px solid var(--border-muted); transition: background .12s; }}
    tbody tr:last-child {{ border-bottom: none; }}
    tbody tr:hover {{ background: var(--bg-inset); }}
    td {{
      padding: 9px 12px; vertical-align: top; font-size: 13px;
    }}
    td.oneliner {{ max-width: 280px; color: var(--text-secondary); }}
    .muted {{ color: var(--text-muted); }}
    .badge {{
      display: inline-flex; align-items: center;
      background: var(--bg-inset); color: var(--link-color);
      border: 1px solid var(--border-component);
      border-radius: var(--radius-badge);
      padding: 2px 8px; font-size: 11px; font-weight: 600;
      margin: 1px; white-space: nowrap;
      transition: background 0.15s;
    }}
    .badge:hover {{ background: var(--bg-subtle); text-decoration: none; }}

    /* Section headings */
    h2 {{
      font-size: clamp(1rem, 2vw, 1.25rem);
      font-weight: 800;
      color: var(--text-primary);
      letter-spacing: -0.01em;
      border-bottom: 1px solid var(--border-default);
      padding-bottom: 8px;
    }}
    h3 {{
      font-size: clamp(0.9rem, 1.5vw, 1.05rem);
      font-weight: 800;
      color: var(--text-primary);
      letter-spacing: -0.01em;
    }}

    /* Overlap matrix */
    .matrix-wrap {{ overflow-x: auto; }}
    .matrix-wrap table {{
      width: auto; background: var(--bg-subtle);
      border: 1px solid var(--border-component);
      border-radius: var(--radius-card);
      box-shadow: var(--shadow-soft);
    }}
    .matrix-wrap th, .matrix-wrap td {{
      padding: 4px 6px; text-align: center; font-size: 11px; border: 1px solid var(--border-muted);
    }}
    .matrix-head {{ background: var(--bg-inset); color: var(--text-secondary); font-weight: 700; writing-mode: vertical-rl; white-space: nowrap; }}
    .matrix-label {{ background: var(--bg-inset); color: var(--text-secondary); font-weight: 700; text-align: left; padding: 4px 8px; white-space: nowrap; }}
    .matrix-yes {{ background: #1a4a2e; color: #3fb950; font-weight: 700; }}
    .matrix-no {{ background: var(--bg-subtle); }}
    .matrix-self {{ background: var(--bg-inset); color: var(--text-muted); }}

    /* Top connected */
    .top-list {{ list-style: none; }}
    .top-list li {{ padding: 8px 0; border-bottom: 1px solid var(--border-muted); font-size: 13px; }}
    .top-list li:last-child {{ border-bottom: none; }}

    /* Footer */
    footer {{
      text-align: center; color: var(--text-muted); font-size: 12px;
      padding: 32px 16px; border-top: 1px solid var(--border-muted); margin-top: 40px;
    }}

    /* ── Interactive base rules ─────────────────────────────────────────── */
    .btn-primary {{
      display: inline-flex; align-items: center; justify-content: center; gap: 6px;
      background: var(--color-brand); color: #fff;
      border: none; border-radius: var(--radius-button);
      padding: 0 16px; min-height: 44px; font-weight: 700; font-size: 13px;
      cursor: pointer; text-decoration: none;
      transition: background 0.15s, box-shadow 0.15s, transform 0.12s;
      box-shadow: var(--shadow-soft);
    }}
    .btn-primary:hover  {{ background: var(--color-brand-hover); transform: translateY(-1px); box-shadow: var(--shadow-lift); text-decoration: none; }}
    .btn-primary:active {{ transform: translateY(0); box-shadow: var(--shadow-soft); }}
    .btn-primary:focus-visible {{ outline: 3px solid var(--color-brand); outline-offset: 2px; }}

    .btn-secondary {{
      display: inline-flex; align-items: center; justify-content: center; gap: 6px;
      background: transparent; color: var(--text-primary);
      border: 1px solid var(--border-component); border-radius: var(--radius-button);
      padding: 0 16px; min-height: 44px; font-weight: 600; font-size: 13px;
      cursor: pointer; text-decoration: none;
      transition: border-color 0.15s, background 0.15s, transform 0.12s;
    }}
    .btn-secondary:hover  {{ border-color: var(--color-brand); background: var(--bg-subtle); transform: translateY(-1px); text-decoration: none; }}
    .btn-secondary:active {{ transform: translateY(0); }}
    .btn-secondary:focus-visible {{ outline: 3px solid var(--color-brand); outline-offset: 2px; }}

    a:focus-visible, button:focus-visible, select:focus-visible, input:focus-visible {{
      outline: 3px solid var(--color-brand);
      outline-offset: 2px;
      border-radius: var(--radius-button);
    }}

    /* \u2500\u2500 Dark-mode component overrides \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
    .dark .stat-card {{
      background: #161c2c;
      border-color: #2d3550;
    }}
    .dark .table-wrap,
    .dark .matrix-wrap > table {{
      background: #161c2c;
      border-color: #2d3550;
    }}
    .dark thead tr {{
      background: #1e2438;
    }}
    .dark thead th {{
      color: #8892aa;
      border-bottom-color: #2d3550;
      background: #1e2438;
    }}
    .dark tbody tr:hover {{
      background: #1e2438 !important;
    }}
    .dark tbody tr:nth-child(even) {{
      background: #131929;
    }}
    .dark .matrix-yes  {{ background: #0d3321; color: #3fb950; }}
    .dark .matrix-no   {{ background: #161c2c; }}
    .dark .matrix-self {{ background: #1e2438; }}
    .dark .matrix-head,
    .dark .matrix-label {{ background: #1e2438; color: #8892aa; border-color: #2d3550; }}
    .dark .toolbar input,
    .dark .toolbar select {{
      background: #1e2438;
      border-color: #2d3550;
      color: #e2e8f0;
    }}
    .dark .toolbar input::placeholder {{ color: #4b5268; }}
    body {{ display: flex; flex-direction: column; min-height: 100vh; }}

    .layout-wrap {{
      flex: 1;
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      align-items: start;
    }}

    #sidebar {{
      position: sticky;
      top: 4rem;
      height: calc(100vh - 4rem);
      overflow-y: auto;
      background: var(--bg-subtle);
      border-right: 1px solid var(--border-component);
      padding: 1.25rem 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 2px;
      transition: transform 0.25s cubic-bezier(.4,0,.2,1);
    }}

    .sidebar-label {{
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-muted);
      padding: 0.75rem 0.75rem 0.25rem;
    }}

    .sidebar-link {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0 0.75rem;
      border-radius: var(--radius-button);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
      text-decoration: none;
      min-height: 44px;
      transition: background 0.15s, color 0.15s;
    }}
    .sidebar-link:hover  {{ background: var(--bg-inset); color: var(--text-primary); text-decoration: none; }}
    .sidebar-link.active {{ color: var(--color-brand); background: rgba(225,1,1,.08); text-decoration: none; }}

    /* Overlay */
    #sidebar-overlay {{
      position: fixed;
      inset: 0;
      z-index: 35;
      background: rgba(0,0,0,.45);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }}
    #sidebar-overlay.visible {{ opacity: 1; pointer-events: all; }}

    /* Hamburger \u2192 X */
    .ham-line {{
      display: block;
      width: 20px; height: 2px;
      background: currentColor;
      border-radius: 2px;
      transition: transform 0.22s ease, opacity 0.22s ease;
      transform-origin: center;
    }}
    #hamburger[aria-expanded="true"] .ham-line:nth-child(1) {{ transform: translateY(6px) rotate(45deg); }}
    #hamburger[aria-expanded="true"] .ham-line:nth-child(2) {{ opacity: 0; transform: scaleX(0); }}
    #hamburger[aria-expanded="true"] .ham-line:nth-child(3) {{ transform: translateY(-6px) rotate(-45deg); }}

    .main-content {{ min-width: 0; }}

    /* Mobile: drawer */
    @media (max-width: 1023px) {{
      .layout-wrap {{ grid-template-columns: minmax(0, 1fr); }}
      #sidebar {{
        position: fixed;
        top: 0; left: 0;
        height: 100vh;
        z-index: 40;
        transform: translateX(-100%);
        box-shadow: var(--shadow-lift);
      }}
      #sidebar.open {{ transform: translateX(0); }}
      #hamburger {{ display: inline-flex !important; }}
    }}
    @media (min-width: 1024px) {{
      #sidebar-overlay {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <header>
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px;">
      <div>
        <h1 style="display:flex; align-items:center; gap:0.6rem; white-space:nowrap;">
          <img src="https://raw.githubusercontent.com/OWASP-BLT/BLT/refs/heads/main/website/static/img/owasp-blt-logo.svg"
               alt="OWASP BLT" height="22" style="display:block; flex-shrink:0;">
          Ideas &mdash; Analysis Dashboard
        </h1>
        <p>
          Auto-generated from
          <a href="{REPO_URL}" target="_blank">OWASP-BLT/BLT-Ideas</a>
          · {total_ideas} ideas · Sortable table · Overlap analysis · Discussion board links
        </p>
      </div>
      <button id="theme-toggle" title="Toggle dark / light mode"
        class="btn-secondary"
        style="flex-shrink:0; font-size:15px; padding: 0 12px;">
        <i class="fa-solid fa-moon" id="icon-moon"></i>
        <i class="fa-solid fa-sun"  id="icon-sun"  style="display:none"></i>
      </button>
    </div>
  </header>

  <div class="container px-4 sm:px-6 lg:px-8">
    <div class="space-y-10">
    <!-- Stats -->
    <div class="stats" id="stats">
      <div class="stat-card">
        <div class="num" id="stat-total">{total_ideas}</div>
        <div class="label">Total Ideas</div>
      </div>
      <div class="stat-card">
        <div class="num" id="stat-with-discussion">0</div>
        <div class="label">With Discussion Post</div>
      </div>
      <div class="stat-card">
        <div class="num" id="stat-with-overlaps">0</div>
        <div class="label">With Overlapping Ideas</div>
      </div>
      <div class="stat-card">
        <div class="num" id="stat-contributors">0</div>
        <div class="label">Unique Contributors</div>
      </div>
    </div>

    <!-- Main sortable table -->
    <div id="section-overview">
    <h2>📋 Ideas Overview</h2>
    <div class="toolbar mt-3">
      <input type="text" id="search" placeholder="Search ideas…" />
      <label>Filter repo:
        <select id="filter-repo">
          <option value="">All repos</option>
        </select>
      </label>
    </div>
    <div class="table-wrap">
      <table id="ideas-table">
        <thead>
          <tr>
            <th data-col="0">Idea</th>
            <th data-col="1">Title</th>
            <th data-col="2">One-Liner</th>
            <th data-col="3">BLT Repo</th>
            <th data-col="4">Discussion</th>
            <th data-col="5">Overlapping Ideas</th>
            <th data-col="6">Interested Contributors</th>
          </tr>
        </thead>
        <tbody>
{table_rows}
        </tbody>
      </table>
    </div>
    </div><!-- /overview-section -->

    <!-- Overlap Analysis -->
    <div id="section-overlap">
    <h2>🔗 Idea Overlap Matrix</h2>
    <p style="color:var(--text-secondary); font-size:13px; margin-top:8px; margin-bottom:12px;">
      ✓ = ideas reference each other (cross-cutting dependencies / integration points).
      Click any idea ID to view its full spec.
    </p>
    <div class="matrix-wrap mt-4">
      <table>
        <thead>
          <tr>
            <th class="matrix-label"></th>
            {matrix_headers}
          </tr>
        </thead>
        <tbody>
{matrix_rows_html}
        </tbody>
      </table>
    </div>

    <h3 class="mt-8" id="section-most-connected">🏆 Most-Connected Ideas</h3>
    <ul class="top-list mt-3">
{top_connected_html}
    </ul>
    </div><!-- /overlap-section -->
    </div><!-- /space-y-10 -->
  </div><!-- /container -->

  <footer>
    Generated by the
    <a href="{REPO_URL}/blob/main/.github/workflows/pages.yml" target="_blank">BLT Ideas Pages workflow</a>
    \u00b7 Data sourced from GitHub API and repository commit history
  </footer>
    </main><!-- /main-content -->
  </div><!-- /layout-wrap -->

  <script>
  (function() {{
    // ── Sorting ────────────────────────────────────────────────────────────
    const table = document.getElementById('ideas-table');
    const tbody = table.querySelector('tbody');
    let sortCol = 0, sortDir = 1;

    function getVal(row, col) {{
      const td = row.cells[col];
      return (td.dataset.sort || td.textContent).trim().toLowerCase();
    }}

    function sortTable(col) {{
      if (sortCol === col) sortDir = -sortDir;
      else {{ sortCol = col; sortDir = 1; }}
      const rows = Array.from(tbody.rows);
      rows.sort((a, b) => getVal(a, col) < getVal(b, col) ? -sortDir : sortDir);
      rows.forEach(r => tbody.appendChild(r));
      document.querySelectorAll('thead th').forEach((th, i) => {{
        th.classList.remove('sorted-asc', 'sorted-desc');
        if (i === col) th.classList.add(sortDir === 1 ? 'sorted-asc' : 'sorted-desc');
      }});
    }}

    document.querySelectorAll('thead th[data-col]').forEach(th => {{
      th.addEventListener('click', () => sortTable(parseInt(th.dataset.col)));
    }});
    sortTable(0); // default sort by idea ID

    // ── Search / filter ──────────────────────────────────────────────────
    const searchInput = document.getElementById('search');
    const repoFilter = document.getElementById('filter-repo');

    // Populate repo dropdown
    const repos = [...new Set(
      Array.from(tbody.rows).map(r => r.cells[3].textContent.trim())
    )].sort();
    repos.forEach(r => {{
      const opt = document.createElement('option');
      opt.value = r; opt.textContent = r;
      repoFilter.appendChild(opt);
    }});

    function applyFilter() {{
      const q = searchInput.value.toLowerCase();
      const repo = repoFilter.value.toLowerCase();
      let visible = 0;
      Array.from(tbody.rows).forEach(row => {{
        const text = row.textContent.toLowerCase();
        const rowRepo = row.cells[3].textContent.trim().toLowerCase();
        const show = (!q || text.includes(q)) && (!repo || rowRepo === repo);
        row.style.display = show ? '' : 'none';
        if (show) visible++;
      }});
    }}

    searchInput.addEventListener('input', applyFilter);
    repoFilter.addEventListener('change', applyFilter);

    // ── Stats ────────────────────────────────────────────────────────────
    const rows = Array.from(tbody.rows);
    document.getElementById('stat-with-discussion').textContent =
      rows.filter(r => r.cells[4].textContent.trim() !== '—').length;
    document.getElementById('stat-with-overlaps').textContent =
      rows.filter(r => r.cells[5].textContent.trim() !== '—').length;

    const allContribs = new Set();
    rows.forEach(r => {{
      r.cells[6].textContent.split(',').forEach(c => {{
        const t = c.trim();
        if (t && t !== '—') allContribs.add(t);
      }});
    }});
    document.getElementById('stat-contributors').textContent = allContribs.size;

    // ── Dark-mode toggle ─────────────────────────────────────────────────
    const themeToggle = document.getElementById('theme-toggle');
    const iconMoon    = document.getElementById('icon-moon');
    const iconSun     = document.getElementById('icon-sun');

    function syncToggleIcon() {{
      const dark = document.documentElement.classList.contains('dark');
      iconMoon.style.display = dark ? '' : 'none';
      iconSun.style.display  = dark ? 'none' : '';
    }}
    syncToggleIcon();

    themeToggle.addEventListener('click', function () {{
      const nowDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('blt-theme', nowDark ? 'dark' : 'light');
      syncToggleIcon();
    }});

    // \u2500\u2500 Mobile sidebar drawer \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    const hamburger = document.getElementById('hamburger');
    const sidebar   = document.getElementById('sidebar');
    const overlay   = document.getElementById('sidebar-overlay');

    function openSidebar() {{
      sidebar.classList.add('open');
      overlay.classList.add('visible');
      hamburger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }}
    function closeSidebar() {{
      sidebar.classList.remove('open');
      overlay.classList.remove('visible');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }}
    hamburger.addEventListener('click', function () {{
      sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
    }});
    overlay.addEventListener('click', closeSidebar);
    document.addEventListener('keydown', function (e) {{
      if (e.key === 'Escape' && sidebar.classList.contains('open')) closeSidebar();
    }});
    document.querySelectorAll('.sidebar-link').forEach(function (a) {{
      a.addEventListener('click', function () {{
        if (window.innerWidth < 1024) closeSidebar();
      }});
    }});

    // \u2500\u2500 Sidebar scroll-spy \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    var spySections = [
      {{ id: 'stats',                  el: document.getElementById('stats') }},
      {{ id: 'section-overview',       el: document.getElementById('section-overview') }},
      {{ id: 'section-overlap',        el: document.getElementById('section-overlap') }},
      {{ id: 'section-most-connected', el: document.getElementById('section-most-connected') }}
    ].filter(function (s) {{ return s.el; }});

    function updateActiveLink() {{
      var scrollY = window.scrollY + 120;
      var active  = spySections[0] ? spySections[0].id : '';
      spySections.forEach(function (s) {{
        if (s.el.getBoundingClientRect().top + window.scrollY <= scrollY) active = s.id;
      }});
      document.querySelectorAll('.sidebar-link').forEach(function (a) {{
        a.classList.toggle('active', a.getAttribute('href') === '#' + active);
      }});
    }}
    window.addEventListener('scroll', updateActiveLink, {{ passive: true }});
    updateActiveLink();

  }})();
  </script>
</body>
</html>
"""
    return html


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)

    if not GITHUB_TOKEN:
        print(
            "Warning: GITHUB_TOKEN is not set. "
            "Discussion participant data will be unavailable. "
            "Set the GITHUB_TOKEN environment variable for full API access.",
            file=sys.stderr,
        )

    print("Parsing idea files…")
    idea_files = sorted(repo_root.glob("Idea-*.md"), key=lambda p: sort_key(p.stem.replace("Idea-", "")))
    ideas = [parse_idea_file(p) for p in idea_files]
    print(f"  Found {len(ideas)} idea files")

    print("Fetching git contributors…")
    for idea in ideas:
        idea["git_contributors"] = get_file_contributors(idea["filename"])
        if idea["git_contributors"]:
            print(f"  {idea['filename']}: {idea['git_contributors']}")

    print("Fetching discussion participants…")
    for idea in ideas:
        if idea["discussion_num"]:
            print(f"  Fetching discussion #{idea['discussion_num']} for Idea {idea['id']}…")
            idea["discussion_participants"] = get_discussion_participants(
                idea["discussion_num"]
            )
            if idea["discussion_participants"]:
                print(f"    Participants: {idea['discussion_participants']}")

    print("Building overlap matrix…")
    overlap_matrix = build_overlap_matrix(ideas)

    print("Generating HTML…")
    html = generate_html(ideas, overlap_matrix)

    # Write output
    out_dir = repo_root / "docs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"  Written to {out_file}")

    # Write a minimal _config.yml so GitHub Pages serves docs/
    config_file = repo_root / "docs" / "_config.yml"
    if not config_file.exists():
        config_file.write_text("# GitHub Pages configuration\n", encoding="utf-8")

    print("Done.")


if __name__ == "__main__":
    main()
