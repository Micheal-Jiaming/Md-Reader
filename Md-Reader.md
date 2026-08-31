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

Ordinary editing shortcuts come free from the Tk text widget, which is created
with `undo=True`: `Ctrl+Z` undo, `Ctrl+Y` redo, `Ctrl+X`/`C`/`V` cut-copy-paste,
`Ctrl+A` select all.

The title bar shows a `*` next to the filename whenever there are unsaved edits.

---

## How to Use

1. **Double-click** `MD Reader.exe`, or
2. **Drag a `.md` file** onto the exe to open it directly, or
3. From a terminal:
   ```bash
   "MD Reader.exe" myfile.md
   ```

First launch takes a second or two while the onefile bundle unpacks.

### The window

Two panes in a `PanedWindow` — **editor** on the left, **preview** on the right —
with a draggable divider (each side has a 250 px minimum), and a status bar along
the bottom showing the file path plus word and character counts. The preview
re-renders 250 ms after you stop typing; `F5` forces it immediately.

**File** menu: New, Open, Save, Save As, Exit. **View** menu: Refresh preview.

**Unsaved-change protection** — with unsaved edits, opening another file, starting
a new one or closing prompts to save, discard, or cancel.

**File dialogs** — Open offers `*.md *.markdown *.mdown *.mkd *.mkdn`, then
`*.txt`, then all files; Save As defaults to `.md`.

### Markdown supported

The enabled `markdown` extensions are `extra`, `sane_lists`, `toc`, `nl2br` and
`codehilite` (with `noclasses=True`, so highlighting is inlined and needs no
stylesheet, and `guess_lang=False`, so an unlabelled block is not highlighted).

That covers headings, bold/italic, inline code, fenced and highlighted code
blocks, ordered and unordered lists, links, images, tables, blockquotes and
horizontal rules. Note `nl2br`: a single newline becomes a `<br>`, which is
GitHub-comment behaviour rather than strict Markdown, and surprises people who
expect a blank line to be required.

Images given as relative paths resolve next to the file you have open — the
preview is loaded with a `base_url` pointing at that file's directory, so a
relative image in an unsaved document has nothing to resolve against and will not
appear.

### Troubleshooting

| Problem | Cause and fix |
|---|---|
| Slow first launch | Normal — the onefile exe unpacks itself; later launches are quicker |
| `.md` double-click doesn't open it | The app isn't registered for `.md`; open the app and use File → Open, or drag the file onto the exe |
| Preview shows `Preview error:` | The `markdown` call raised; the exception text is shown in place of the render, so the app stays usable |
| SmartScreen warning | The exe is unsigned — More info → Run anyway |
| Explorer shows a generic or stale icon | Windows caches icons; refresh the folder or copy the exe elsewhere |

---

## Project Files

| File | Purpose |
|---|---|
| `md_editor.py` | Source code for the current reader + editor (278 lines) |
| `dist/MD Reader.exe` | The compiled standalone app (~24 MB) — **not** in version control; rebuild it, or download it from the GitHub release |
| `MD Reader.spec` | PyInstaller recipe, written by the build command below; `py -m PyInstaller "MD Reader.spec"` reruns the same build. Its paths are relative, so build from this folder |
| `generate_icon.py` | Draws the app icon with Pillow — edit and re-run to tweak the design |
| `icon.ico` | Multi-resolution app icon (16 / 32 / 48 / 64 / 128 / 256 px) |
| `icon_preview.png` | Large preview of the icon design |
| `md_reader.py` | Original read-only launcher (grip-based, superseded) |
| `Md-Reader.md` | This document — the single source of truth for the project |
| `VERSION` | Current version number, one line — see *Version control* below |
| `README.md` | GitHub landing page for the public repository — short by design, and points here |
| `LICENSE` | MIT licence, added when the repository was published |
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
| `origin` | `https://github.com/Micheal-Jiaming/Md-Reader` — **public** since 1.0.6 |
| `mirror` | `D:\claude\repos\Md-Reader.git` — local bare copy |

The repository name matches this document's filename (`Md-Reader`); the folder
keeps its lower-case name so existing paths and the build command still work.
Authentication is the GitHub CLI acting as git's credential helper
(`gh auth setup-git`), so pushes need no interactive prompt.

### Published publicly at 1.0.6

The user made this repository **public** on 1 September 2026, and it is the only
repository in this workspace that is. Every other project under `D:\claude` stays
private, so do not treat this as the new default or generalise it to a sibling
project — the standing rule is still private, and the user decides case by case.

Going public changes two things about the layout:

- **A `README.md` now exists alongside this document.** That is a deliberate,
  user-approved exception to the one-document-per-project convention, made because
  GitHub renders `README.md` as the repository's landing page and a visitor to a
  public project would otherwise see only a bare file list. Keep the README short —
  what the app is, how to download it, the feature and shortcut summary — and let it
  point here. **This document remains the record.** When a feature changes, check
  whether the README's summary or shortcut table needs the same edit; two documents
  that disagree are worse than one, which is the whole reason the one-doc rule
  exists.
- **The exe ships as a release asset.** `dist\MD Reader.exe` is still git-ignored,
  but each release now attaches it on GitHub so a visitor can run the app instead of
  only reading the source. Releases live outside git, so this does not conflict with
  keeping rebuildable binaries out of version control. Attach the freshly built exe
  when tagging a release:

  ```powershell
  gh release create v$(cat VERSION) "dist\MD Reader.exe" --title "..." --notes "..."
  ```

Because the history is public, remember that everything already pushed is visible —
including commit messages and author identity. There is nothing sensitive in it, but
a future secret would be unrecoverable rather than merely committed.

Tracked: `md_editor.py`, `md_reader.py`, `generate_icon.py`, `MD Reader.spec`,
`icon.ico`, `icon_preview.png`, `README.md`, `LICENSE`, and this document.
Ignored: `dist\`, `build\`, `__pycache__\` — all regenerated by the build command above, and a
stale exe cannot do what newer source does. `.gitattributes` sets `* -text` so
every file is stored and checked out byte for byte; Git for Windows is configured
`core.autocrlf=true` system-wide and would otherwise rewrite these LF files to
CRLF.

**Versioning.** `VERSION` holds the current number; every release is tagged
`v<number>`. The baseline was **1.0.0**, covering v3 of the Evolution list above —
that list numbers the state of the code, not releases. This document deliberately
does not enumerate the releases since: `git tag` and `git log VERSION` are the
record, and a list here would be one release stale the moment the next ships.

| Update | Bump | Example |
|---|---|---|
| Major — new or changed functionality | +0.1 | 1.0.0 → 1.1.0 |
| Minor — fixes, docs, small tweaks | +0.0.1 | 1.0.0 → 1.0.1 |

**One bump per task, however many commits it takes** — not one per commit. A
task that edits code and then updates this document is a single version; write
the new number into `VERSION` in the task's last commit and tag there. Documented
changes are never exempt: this file is what a later session works from, so a
wrong line in it is a defect like any other. The rule is deliberately mechanical,
because a rule needing judgement gets applied differently by every session.

Then tag and push both remotes:

```powershell
git -C "D:\claude\md-reader" commit -am "..."
git -C "D:\claude\md-reader" tag -a v$(cat VERSION) -m "..."
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
