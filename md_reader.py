"""MD Reader launcher.

Double-click to run: pops up a file picker, then serves the chosen
Markdown file with grip (GitHub-style rendering) and opens it in the
default browser. The console window shows the local URL and lets you
stop the server with Ctrl+C.
"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def pick_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Select a Markdown file to read",
        filetypes=[
            ("Markdown files", "*.md *.markdown *.mdown *.mkd *.mkdn"),
            ("All files", "*.*"),
        ],
    )
    root.destroy()
    return path


def main():
    # Allow passing a file directly (e.g. drag-onto-exe or CLI arg).
    path = sys.argv[1] if len(sys.argv) > 1 else pick_file()
    if not path:
        print("No file selected. Exiting.")
        return

    import grip

    print("=" * 60)
    print(f"  Reading: {path}")
    print("  Opening in your browser at http://localhost:6419")
    print("  Press Ctrl+C in this window to stop the reader.")
    print("=" * 60)

    try:
        grip.serve(path, browser=True)
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as exc:  # noqa: BLE001
        # Surface errors in a dialog too, in case the console is missed.
        try:
            r = tk.Tk()
            r.withdraw()
            messagebox.showerror("MD Reader error", str(exc))
            r.destroy()
        except Exception:
            pass
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
