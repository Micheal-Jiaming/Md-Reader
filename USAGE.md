# MD Reader — Usage Guide

How to run and use **MD Reader.exe**, a standalone Windows app for reading and editing Markdown (`.md`) files with a live preview.

---

## 1. Finding the App

Look for the **Markdown badge icon** — a white **"M" with a downward arrow** on a rounded indigo square. That's `MD Reader.exe`. The same icon appears in File Explorer, on the taskbar, in `Alt+Tab`, and in the app's own title bar.

> If Explorer still shows a generic icon, that's just a stale icon cache — press `F5` in the folder to refresh it.

---

## 2. Starting the App

You can open the app in any of these ways:

| Method | What to do |
|---|---|
| **Double-click** | Double-click `MD Reader.exe`. It opens with a blank document. |
| **Drag & drop** | Drag a `.md` file onto `MD Reader.exe` to open that file directly. |
| **Command line** | Run `"MD Reader.exe" myfile.md` in a terminal. |

> First launch may take a second or two — the single-file exe unpacks itself before the window appears.

---

## 3. The Window

The window is split into two panes:

- **Left — Editor:** where you type and edit your Markdown text.
- **Right — Preview:** a live, GitHub-styled rendering of what you've written.
- **Bottom — Status bar:** shows the current file path and word / character counts.

The preview refreshes automatically about a quarter-second after you stop typing.

---

## 4. Editing

Type in the left pane as you would in any text editor. Standard editing works:

- **Undo:** `Ctrl+Z`
- **Redo:** `Ctrl+Y`
- **Cut / Copy / Paste:** `Ctrl+X` / `Ctrl+C` / `Ctrl+V`
- **Select all:** `Ctrl+A`

The preview updates on its own. To force an immediate refresh, press **`F5`**.

---

## 5. Opening & Saving Files

| Action | Shortcut | Notes |
|---|---|---|
| **New** | `Ctrl+N` | Start a fresh, blank document. |
| **Open** | `Ctrl+O` | Choose an existing `.md` (or `.txt`) file. |
| **Save** | `Ctrl+S` | Save to the current file. If the file is new, acts like *Save As*. |
| **Save As** | `Ctrl+Shift+S` | Save to a new file name / location. |

These commands are also available under the **File** menu.

**Unsaved-change protection:** if you have unsaved edits and try to open another file, start a new one, or close the app, you'll be asked whether to **save**, **discard**, or **cancel** — so you won't lose work by accident.

**Title bar indicator:** the filename appears in the title bar. A `*` in front of it means you have unsaved changes.

---

## 6. Markdown You Can Use

The preview supports common Markdown, including:

| Feature | Example |
|---|---|
| Headings | `# H1`, `## H2`, `### H3` |
| Bold / italic | `**bold**`, `*italic*` |
| Inline code | `` `code` `` |
| Code block | ```` ```python ```` … ```` ``` ```` (syntax highlighted) |
| Lists | `- item` or `1. item` |
| Links | `[text](https://example.com)` |
| Images | `![alt](path/to/image.png)` |
| Tables | `\| A \| B \|` with a `\|---\|---\|` separator row |
| Blockquotes | `> quoted text` |
| Horizontal rule | `---` |

Images referenced by a relative path are resolved next to the file you have open.

---

## 7. Menus

- **File** — New, Open, Save, Save As, Exit.
- **View** — Refresh preview (`F5`).

---

## 8. Tips

- **Read-only viewing:** just open a file and read the right-hand preview — no need to touch the editor.
- **Quick note-taking:** launch with no file, type, then `Ctrl+S` to save wherever you like.
- **Resize the panes:** drag the divider between the editor and preview to make either side wider.

---

## 9. Troubleshooting

| Problem | Fix |
|---|---|
| App is slow to open the first time | Normal — the exe unpacks on first run; later launches are quicker. |
| A `.md` file won't open by double-click | The app isn't registered for `.md` files. Open the app first, then use **File → Open**, or drag the file onto the exe. |
| Preview shows "Preview error" | There's a formatting issue in the text; fix the Markdown and it re-renders. |
| Windows SmartScreen warning | The exe is unsigned. Choose **More info → Run anyway** if you trust the file. |
| Icon looks generic / outdated | Windows caches icons. Press `F5` in the folder, or copy the exe to another location, to see the current one. |

---

## 10. Using It on Another Computer

`MD Reader.exe` is fully self-contained — everything it needs is inside that one file.

- **To move it:** copy just `MD Reader.exe` (about 24 MB). It even runs from a USB stick.
- **The other PC needs nothing installed** — no Python, no libraries, no setup, no admin rights.
- **Requirements:** 64-bit **Windows 10 or later**. It will not run on macOS, Linux, or 32-bit Windows.

---

*MD Reader is fully offline — it renders Markdown locally and needs no internet connection.*
