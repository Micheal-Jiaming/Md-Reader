<p align="center">
  <img src="icon_preview.png" alt="MD Reader" width="120">
</p>

<h1 align="center">MD Reader</h1>

<p align="center">
  A standalone Windows Markdown <strong>reader and editor</strong> — type on the left,
  watch a GitHub-styled preview render on the right.
  <br>
  One portable <code>.exe</code>. No installer, no Python, no internet.
</p>

<p align="center">
  <a href="https://github.com/Micheal-Jiaming/Md-Reader/releases/latest"><img src="https://img.shields.io/github/v/release/Micheal-Jiaming/Md-Reader?label=download" alt="Latest release"></a>
  <img src="https://img.shields.io/badge/platform-Windows%2010%2B%20x64-blue" alt="Windows 10+ x64">
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python 3.13">
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-green" alt="MIT licence"></a>
</p>

---

## Download

Grab **`MD Reader.exe`** from the [latest release](https://github.com/Micheal-Jiaming/Md-Reader/releases/latest) and double-click it. There is nothing to install and nothing to configure.

Requires 64-bit Windows 10 or later. The executable is unsigned, so SmartScreen warns you the first time — choose **More info → Run anyway**. The very first launch takes a second or two while the single-file bundle unpacks itself.

## What it does

- **Two panes, one window** — an editable text pane on the left, a live rendered preview on the right, with a draggable divider.
- **Live preview** — re-renders 250 ms after you stop typing; `F5` forces it immediately.
- **GitHub-styled rendering** — headings, bold and italic, lists, tables, blockquotes, links, images, horizontal rules, and syntax-highlighted fenced code blocks.
- **Real file handling** — New, Open, Save and Save As, with a prompt to save before you open another file, start a new one, or quit.
- **Opens files the obvious ways** — double-click the app, drag a `.md` file onto the exe, or pass a path on the command line.
- **Fully offline** — `MD Reader.exe` converts and renders Markdown inside its own process. There is no telemetry and no server round-trip to display your file. (A document that itself references remote images or stylesheets will still fetch those, as any renderer would.)
- **Portable** — copy the one file to any supported machine and run it.

## Keyboard shortcuts

| Action | Shortcut |
|---|---|
| New | `Ctrl+N` |
| Open | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Refresh preview | `F5` |

Ordinary editing shortcuts come free from the Tk text widget, which is created with `undo=True`: undo, redo, cut, copy, paste and select-all all behave as expected. The title bar shows a `*` beside the filename while there are unsaved edits.

## Built with

Python 3.13 and **tkinter** for the window and editor, **markdown** for conversion, **tkinterweb** to render the HTML preview in-window, **pygments** for code highlighting, **Pillow** to generate the icon, and **PyInstaller** to bundle it all into one executable.

## Build from source

```bash
py -m pip install markdown tkinterweb pygments pillow pyinstaller
py -m PyInstaller --noconfirm "MD Reader.spec"
```

The build lands in `dist/MD Reader.exe`. Build from the repository root — the spec file uses relative paths. To run it without packaging, `py md_editor.py`.

> **A note on `md_reader.py`.** That file is the original v1 launcher, kept for project history and superseded by `md_editor.py`. It is **not** the app described above and does not share its offline guarantee: it renders through [grip](https://github.com/joeyespo/grip), which uploads the file's contents to GitHub's Markdown API. Don't point it at anything confidential.

## Documentation

**[`Md-Reader.md`](Md-Reader.md)** is the full project document: architecture and implementation reasoning, the complete feature and usage reference, Markdown extensions and their quirks, a troubleshooting table, the build command in long form, portability notes, and the versioning scheme. This README is only the landing page — the project document is the record.

## Licence

[MIT](LICENSE).
