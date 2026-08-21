# MD Reader

A standalone Windows Markdown **reader + editor** with live preview, built from Python and compiled to a single `.exe`.

---

## Overview

`MD Reader.exe` is a self-contained desktop app that lets you **edit Markdown on the left and see a live, GitHub-styled preview on the right** — all in one window, with no internet connection and no external services required.

It started as a read-only viewer and was upgraded into a full editor.

---

## Features

- **Two-pane layout** — editable text on the left, rendered preview on the right.
- **Live preview** — updates ~0.25 s after you stop typing.
- **Rich rendering** — headings, **bold** / *italic*, lists, tables, blockquotes, links, images, and syntax-highlighted code blocks.
- **File operations** — New, Open, Save, Save As.
- **Unsaved-change protection** — prompts to save before opening, creating, or closing.
- **Status bar** — shows the current file path plus word / character counts.
- **Flexible input** — opens a file passed on the command line or **dragged onto the exe**; otherwise starts blank.
- **Custom Markdown icon** — the classic "M + down-arrow" badge, shown in Explorer, the taskbar, and the title bar.
- **Fully offline** — renders locally inside the window.
- **Portable** — a single self-contained `.exe`; copy it to any 64-bit Windows 10+ PC and run it, no install required.

---

## Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| New | `Ctrl+N` |
| Open | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Refresh preview | `F5` |

The title bar shows a `*` next to the filename whenever there are unsaved edits.

---

## How to Use

1. **Double-click** `MD Reader.exe`, or
2. **Drag a `.md` file** onto the exe to open it directly, or
3. From a terminal:
   ```bash
   "MD Reader.exe" myfile.md
   ```

---

## Project Files

| File | Purpose |
|---|---|
| `md_editor.py` | Source code for the current reader + editor (237 lines) |
| `dist/MD Reader.exe` | The compiled standalone app (~24 MB) — **not** in version control, rebuild it |
| `MD Reader.spec` | PyInstaller recipe, written by the build command below; `py -m PyInstaller "MD Reader.spec"` reruns the same build. Its paths are relative, so build from this folder |
| `generate_icon.py` | Draws the app icon with Pillow — edit and re-run to tweak the design |
| `icon.ico` | Multi-resolution app icon (16 / 32 / 48 / 64 / 128 / 256 px) |
| `icon_preview.png` | Large preview of the icon design |
| `USAGE.md` | End-user usage guide |
| `md_reader.py` | Original read-only launcher (grip-based, superseded) |
| `Md-Reader.md` | This document — the single source of truth for the project |
| `VERSION` | Current version number, one line — see *Version control* below |
| `.gitignore`, `.gitattributes` | Exclude regenerable output; store files byte for byte |

---

## How It Was Built

**Tech stack**

- **Python 3.13** + **tkinter** — GUI window, editor pane, menus.
- **markdown** — converts Markdown text to HTML.
- **tkinterweb** — renders the HTML preview inside the window.
- **pygments** — syntax highlighting for code blocks.
- **Pillow** — generates the `.ico` app icon.
- **PyInstaller** — bundles everything into a single `.exe`.

**Build command**

```bash
py -m PyInstaller --noconfirm --onefile --windowed --name "MD Reader" \
  --icon icon.ico --add-data "icon.ico;." \
  --collect-all tkinterweb --collect-all markdown --collect-all pygments \
  md_editor.py
```

To rebuild after editing the source, re-run that command from the `md-reader`
folder. It also writes `MD Reader.spec`; once that exists,
`py -m PyInstaller --noconfirm "MD Reader.spec"` is the shorter equivalent.

To regenerate the icon first (only needed if you change its design):

```bash
py generate_icon.py
```

---

## Evolution

1. **v1 — Reader only:** cloned the [grip](https://github.com/joeyespo/grip) project from Git and wrapped it in a launcher exe. Rendered `.md` files GitHub-style in the browser (required internet + GitHub's API).
2. **v2 — Reader + Editor:** replaced with a native two-pane app that **renders locally and supports editing and saving**, removing the internet dependency.
3. **v3 — Custom icon (current):** embedded a purpose-built Markdown badge icon so the app is identifiable in Explorer, the taskbar, and its own title bar.

---

## Version control

This project is its own Git repository, with two remotes:

| Remote | Points at |
|---|---|
| `origin` | `https://github.com/Micheal-Jiaming/Md-Reader` — private |
| `mirror` | `D:\claude\repos\Md-Reader.git` — local bare copy |

The repository name matches this document's filename (`Md-Reader`); the folder
keeps its lower-case name so existing paths and the build command still work.
Authentication is the GitHub CLI acting as git's credential helper
(`gh auth setup-git`), so pushes need no interactive prompt.

Tracked: `md_editor.py`, `md_reader.py`, `generate_icon.py`, `MD Reader.spec`,
`icon.ico`, `icon_preview.png`, `USAGE.md`, and this document. Ignored: `dist\`,
`build\`, `__pycache__\` — all regenerated by the build command above, and a
stale exe cannot do what newer source does. `.gitattributes` sets `* -text` so
every file is stored and checked out byte for byte; Git for Windows is configured
`core.autocrlf=true` system-wide and would otherwise rewrite these LF files to
CRLF.

**Versioning.** `VERSION` holds the current number; every release is tagged
`v<number>`. The baseline is **1.0.0**, tagged `v1.0.0` — it covers v3 of the
Evolution list above, which is the state of the code, not a version number.
**1.0.1** recorded the move to GitHub.

| Update | Bump | Example |
|---|---|---|
| Major — new or changed functionality | +0.1 | 1.0.0 → 1.1.0 |
| Minor — fixes, docs, small tweaks | +0.0.1 | 1.0.0 → 1.0.1 |

Edit `VERSION` in the same commit as the change, then tag and mirror:

```powershell
git -C "D:\claude\md-reader" commit -am "..."
git -C "D:\claude\md-reader" tag -a v1.0.2 -m "..."
git -C "D:\claude\md-reader" push origin main --tags
git -C "D:\claude\md-reader" push mirror main --tags
```

---

## Portability

`MD Reader.exe` is built in PyInstaller's `--onefile` mode, so the Python interpreter and every library are bundled inside it. Copy the single file to another machine and run it — no Python, no installer, no admin rights.

| Requirement | Detail |
|---|---|
| Operating system | **Windows only** (macOS / Linux need a separate build on that OS) |
| Architecture | **64-bit (x64)**; also runs on Windows-on-ARM via emulation |
| Windows version | **Windows 10 or later** recommended |

Two things to expect on a new machine: Windows SmartScreen may warn that the exe is unsigned (choose **More info → Run anyway**), and the very first launch is a second or two slower while the bundle unpacks.
