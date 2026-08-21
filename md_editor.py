"""MD Reader / Editor.

A single-window Markdown app: edit on the left, live GitHub-style
preview on the right. Supports New / Open / Save / Save As, keyboard
shortcuts, unsaved-change protection, and opening a file passed on the
command line (or dragged onto the .exe).
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont

import markdown
from tkinterweb import HtmlFrame


APP_NAME = "MD Reader / Editor"

# Markdown -> HTML conversion (rich extensions; code highlighting inline).
_MD_EXTENSIONS = ["extra", "sane_lists", "toc", "nl2br", "codehilite"]
_MD_CONFIGS = {"codehilite": {"noclasses": True, "guess_lang": False}}

_CSS = """
<style>
  body {
    font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 15px; line-height: 1.6; color: #24292f;
    background: #ffffff; margin: 0; padding: 24px 28px; max-width: 900px;
  }
  h1, h2 { border-bottom: 1px solid #d0d7de; padding-bottom: .3em; }
  h1 { font-size: 1.9em; } h2 { font-size: 1.5em; } h3 { font-size: 1.25em; }
  code {
    background: #f6f8fa; padding: .2em .4em; border-radius: 6px;
    font-family: "Cascadia Code", Consolas, monospace; font-size: 90%;
  }
  pre { background: #f6f8fa; padding: 14px; border-radius: 6px; overflow: auto; }
  pre code { background: transparent; padding: 0; }
  blockquote {
    margin: 0; padding: 0 1em; color: #57606a; border-left: .25em solid #d0d7de;
  }
  table { border-collapse: collapse; }
  th, td { border: 1px solid #d0d7de; padding: 6px 13px; }
  tr:nth-child(2n) { background: #f6f8fa; }
  a { color: #0969da; text-decoration: none; }
  img { max-width: 100%; }
  hr { border: none; border-top: 1px solid #d0d7de; }
</style>
"""


class MarkdownApp(tk.Tk):
    def __init__(self, initial_path=None):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1100x700")
        self.minsize(600, 400)

        self.current_path = None
        self.saved_text = ""            # content as last loaded/saved
        self._preview_job = None        # debounce handle

        self._apply_window_icon()
        self._build_menu()
        self._build_body()
        self._bind_shortcuts()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        if initial_path and os.path.isfile(initial_path):
            self._load_path(initial_path)
        else:
            self._set_new_document()
        self.update_preview()

    # -- UI construction --------------------------------------------------
    def _apply_window_icon(self):
        """Set the title-bar/taskbar icon, whether run as script or frozen exe."""
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "icon.ico")
        if os.path.isfile(path):
            try:
                self.iconbitmap(path)
            except Exception:  # noqa: BLE001 - cosmetic only
                pass

    def _build_menu(self):
        menubar = tk.Menu(self)
        filem = tk.Menu(menubar, tearoff=0)
        filem.add_command(label="New\tCtrl+N", command=self.new_file)
        filem.add_command(label="Open…\tCtrl+O", command=self.open_file)
        filem.add_separator()
        filem.add_command(label="Save\tCtrl+S", command=self.save_file)
        filem.add_command(label="Save As…\tCtrl+Shift+S", command=self.save_file_as)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filem)

        viewm = tk.Menu(menubar, tearoff=0)
        viewm.add_command(label="Refresh preview\tF5", command=self.update_preview)
        menubar.add_cascade(label="View", menu=viewm)
        self.config(menu=menubar)

    def _build_body(self):
        paned = tk.PanedWindow(self, orient="horizontal", sashwidth=6,
                               bg="#d0d7de")
        paned.pack(fill="both", expand=True)

        # left: editor
        left = tk.Frame(paned)
        editor_font = tkfont.Font(family="Cascadia Code", size=12)
        self.text = tk.Text(left, wrap="word", undo=True, font=editor_font,
                            bg="#fbfbfb", fg="#24292f", insertbackground="#24292f",
                            padx=10, pady=10, bd=0)
        yscroll = tk.Scrollbar(left, command=self.text.yview)
        self.text.configure(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        paned.add(left, minsize=250, width=520)

        # right: preview
        right = tk.Frame(paned)
        self.preview = HtmlFrame(right, messages_enabled=False)
        self.preview.pack(fill="both", expand=True)
        paned.add(right, minsize=250)

        # status bar
        self.status = tk.Label(self, anchor="w", bd=1, relief="sunken",
                               bg="#f6f8fa", fg="#57606a")
        self.status.pack(fill="x", side="bottom")

        self.text.bind("<<Modified>>", self._on_modified)

    def _bind_shortcuts(self):
        self.bind_all("<Control-n>", lambda e: (self.new_file(), "break")[1])
        self.bind_all("<Control-o>", lambda e: (self.open_file(), "break")[1])
        self.bind_all("<Control-s>", lambda e: (self.save_file(), "break")[1])
        self.bind_all("<Control-S>", lambda e: (self.save_file_as(), "break")[1])
        self.bind_all("<F5>", lambda e: self.update_preview())

    # -- change tracking / preview ---------------------------------------
    def _on_modified(self, _event=None):
        # <<Modified>> fires once until the flag is reset; reset so it keeps firing.
        if self.text.edit_modified():
            self.text.edit_modified(False)
            self._schedule_preview()
            self._refresh_title()

    def _schedule_preview(self):
        if self._preview_job is not None:
            self.after_cancel(self._preview_job)
        self._preview_job = self.after(250, self.update_preview)

    def update_preview(self, _event=None):
        self._preview_job = None
        raw = self.text.get("1.0", "end-1c")
        try:
            body = markdown.markdown(raw, extensions=_MD_EXTENSIONS,
                                     extension_configs=_MD_CONFIGS)
        except Exception as exc:  # noqa: BLE001
            body = f"<pre>Preview error:\n{exc}</pre>"
        base = None
        if self.current_path:
            base = "file:///" + os.path.dirname(
                os.path.abspath(self.current_path)).replace("\\", "/") + "/"
        self.preview.load_html(f"<html><head>{_CSS}</head><body>{body}</body></html>",
                               base_url=base)
        self._update_status()

    # -- document state ---------------------------------------------------
    def _is_dirty(self):
        return self.text.get("1.0", "end-1c") != self.saved_text

    def _refresh_title(self):
        name = os.path.basename(self.current_path) if self.current_path else "Untitled"
        star = "*" if self._is_dirty() else ""
        self.title(f"{star}{name} — {APP_NAME}")

    def _update_status(self):
        raw = self.text.get("1.0", "end-1c")
        words = len(raw.split())
        chars = len(raw)
        where = self.current_path if self.current_path else "(unsaved)"
        self.status.config(text=f"  {where}    |    {words} words, {chars} chars")

    def _set_new_document(self):
        self.current_path = None
        self.text.delete("1.0", "end")
        self.saved_text = ""
        self.text.edit_modified(False)
        self._refresh_title()

    def _load_path(self, path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(APP_NAME, f"Could not open file:\n{exc}")
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.current_path = path
        self.saved_text = content
        self.text.edit_modified(False)
        self._refresh_title()

    def _confirm_discard(self):
        """Return True if it's OK to proceed (discard/handle unsaved changes)."""
        if not self._is_dirty():
            return True
        ans = messagebox.askyesnocancel(
            APP_NAME, "You have unsaved changes. Save before continuing?")
        if ans is None:
            return False            # cancel
        if ans:
            return self.save_file()  # only proceed if save succeeded
        return True                  # discard

    # -- file commands ----------------------------------------------------
    def new_file(self):
        if not self._confirm_discard():
            return
        self._set_new_document()
        self.update_preview()

    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            title="Open Markdown file",
            filetypes=[("Markdown", "*.md *.markdown *.mdown *.mkd *.mkdn"),
                       ("Text", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        self._load_path(path)
        self.update_preview()

    def save_file(self):
        if self.current_path is None:
            return self.save_file_as()
        return self._write_to(self.current_path)

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            title="Save Markdown file", defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Text", "*.txt"),
                       ("All files", "*.*")])
        if not path:
            return False
        return self._write_to(path)

    def _write_to(self, path):
        content = self.text.get("1.0", "end-1c")
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(content)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(APP_NAME, f"Could not save file:\n{exc}")
            return False
        self.current_path = path
        self.saved_text = content
        self.text.edit_modified(False)
        self._refresh_title()
        self._update_status()
        return True

    def on_exit(self):
        if self._confirm_discard():
            self.destroy()


def main():
    initial = sys.argv[1] if len(sys.argv) > 1 else None
    MarkdownApp(initial).mainloop()


if __name__ == "__main__":
    main()
