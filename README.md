# BLT Ideas

BLT Ideas is a collection of brainstorming proposals for potential future development of [OWASP BLT](https://github.com/OWASP-BLT/BLT). Each idea is scoped to a standalone 350-hour development slot and represents community-driven direction — not official project commitments.

For the full list of ideas, descriptions, differentiation guide, and hours analysis, visit the project page:

👉 **[https://owasp-blt.github.io/BLT-Ideas/](https://owasp-blt.github.io/BLT-Ideas/)**

For detailed written documentation, see [DETAILS.md](DETAILS.md).

---

## Development Setup

### Prerequisites

- Python 3.8 or newer
- A GitHub Personal Access Token *(optional — needed for live contributor data)*

### 1. Clone the repo

```bash
git clone https://github.com/OWASP-BLT/BLT-Ideas.git
cd BLT-Ideas
```

### 2. Set up your GitHub token

```bash
cp .env.example .env
# Edit .env and replace the placeholder with your real token
```

Create a token at **GitHub → Settings → Developer settings → Personal access tokens**.  
Required scopes: `read:org`, `public_repo`.

Without a token the generator still runs — it just skips live contributor data from the GitHub API.

### 3. Build the dashboard

**In VS Code** — press `Ctrl+Shift+B` (`Cmd+Shift+B` on macOS). This runs the default **Generate Dashboard** build task defined in [`.vscode/tasks.json`](.vscode/tasks.json).

**From the terminal:**

```bash
# Windows PowerShell
$env:GITHUB_TOKEN="ghp_yourtoken"; python scripts/generate_page.py

# macOS / Linux
GITHUB_TOKEN=ghp_yourtoken python scripts/generate_page.py
```

The script reads all `Idea-*.md` files, fetches GitHub data, and writes `docs/index.html`.

### 4. Preview locally

Open `docs/index.html` in any browser — no server required, it's a self-contained static file.

Or use the **Preview Dashboard** VS Code task (`Ctrl+Shift+P` → *Tasks: Run Task* → *Preview Dashboard*) to build and open in one step.

---

## How it works

| File | Purpose |
|---|---|
| `Idea-*.md` | Source of truth — one Markdown file per idea |
| `scripts/generate_page.py` | Reads Markdown files, calls GitHub API, writes `docs/index.html` |
| `docs/index.html` | Generated single-page dashboard (committed so GitHub Pages serves it directly) |
| `.github/workflows/` | CI that auto-regenerates `docs/index.html` on every push to `main` |
