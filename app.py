"""NLPApp desktop workspace. Run with python app.py."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from mydb import Database
from nlp_engine import LocalNLP

TOOLS = {
    "Sentiment analysis": ("sentiment_analysis", "English sentiment scores from VADER. Scores are proportions, not confidence estimates."),
    "Named entities": ("do_ner", "Find people, organizations, places, dates and more with the local English spaCy model."),
    "Summarization": ("do_summarize", "Extract the most relevant sentences from an English passage, in their original order."),
    "Spelling & basic grammar": ("do_grammer_spelling", "English spelling suggestions and a few grammar rules. Review changes before using them."),
    "Language detection": ("do_lang_detect", "Estimate a language code locally. Short or mixed-language passages may be unreliable."),
    "Headline generator": ("do_headline_generation", "Create a short extractive headline from a key sentence. No new facts are generated."),
}
SAMPLE = "Apple opened a new office in London on Monday. The team is excited about the excellent new workspace. The company plans to hire 200 engineers next year."


class NLPApp:
    def __init__(self, root=None):
        self.root = root if root is not None else tk.Tk()
        self.root.title("NLPApp | Offline text studio")
        self.root.geometry("1060x760")
        self.root.minsize(860, 650)
        self.root.configure(bg="#eef2f6")
        icon = Path(__file__).resolve().parent / "resources" / "favicon.ico"
        if icon.exists():
            try:
                self.root.iconbitmap(str(icon))
            except tk.TclError:
                pass
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f6")
        style.configure("TLabel", background="#eef2f6", foreground="#17283d", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"))
        style.configure("Muted.TLabel", foreground="#516278", font=("Segoe UI", 10))
        style.configure("TButton", padding=(14, 9), font=("Segoe UI", 10))
        style.configure("TEntry", padding=8)
        self.engine = LocalNLP()
        self.db = Database()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None
        self.screen_id = 0
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        try:
            self.db.migrate_legacy()
        except (OSError, ValueError) as exc:
            messagebox.showerror("Account storage", str(exc), parent=self.root)
        self.login_gui()

    def clear(self):
        self.screen_id += 1
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_gui(self, register=False):
        self.clear()
        box = ttk.Frame(self.root, padding=40)
        box.place(relx=.5, rely=.5, anchor="center", width=500)
        ttk.Label(box, text="NLPApp", style="Title.TLabel").pack(anchor="w")
        ttk.Label(box, text="Your text, processed on your computer.", style="Muted.TLabel").pack(anchor="w", pady=(4, 24))
        ttk.Label(box, text="Create a local account" if register else "Welcome back").pack(anchor="w", pady=(0, 12))
        entries = {}
        for field in (["Name", "Email", "Password"] if register else ["Email", "Password"]):
            ttk.Label(box, text=field).pack(anchor="w", pady=(8, 4))
            entry = ttk.Entry(box, show="*" if field == "Password" else "")
            entry.pack(fill="x")
            entries[field] = entry
        def submit():
            try:
                if register:
                    if not self.db.add_data(entries["Name"].get(), entries["Email"].get(), entries["Password"].get()):
                        raise ValueError("This email already has an account.")
                    messagebox.showinfo("Account created", "You can now sign in.", parent=self.root)
                    self.login_gui()
                elif self.db.search(entries["Email"].get(), entries["Password"].get()):
                    self.home_gui()
                else:
                    raise ValueError("Incorrect email or password.")
            except (ValueError, OSError) as exc:
                messagebox.showerror("Account", str(exc), parent=self.root)
        ttk.Button(box, text="Create account" if register else "Sign in", command=submit).pack(fill="x", pady=(20, 8))
        ttk.Button(box, text="Back to sign in" if register else "Create a local account", command=lambda: self.login_gui(not register)).pack(fill="x", pady=4)
        ttk.Button(box, text="Continue as guest", command=self.home_gui).pack(fill="x", pady=(12, 4))
        ttk.Label(box, text="No account or internet required for analysis.", style="Muted.TLabel").pack(pady=(12, 0))
        next(iter(entries.values())).focus_set()

    def home_gui(self):
        self.clear()
        self.result_text = ""
        main = ttk.Frame(self.root, padding=26)
        main.pack(fill="both", expand=True)
        header = ttk.Frame(main)
        header.pack(fill="x")
        ttk.Label(header, text="Text studio", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Sign out", command=self.login_gui).pack(side="right")
        ttk.Label(main, text="LOCAL PROCESSING  /  No API keys • No usage fees", style="Muted.TLabel").pack(anchor="w", pady=(4, 20))
        controls = ttk.Frame(main)
        controls.pack(fill="x")
        self.tool = tk.StringVar(value=next(iter(TOOLS)))
        selector = ttk.Combobox(controls, textvariable=self.tool, values=list(TOOLS), state="readonly", width=29)
        selector.pack(side="left")
        self.run_button = ttk.Button(controls, text="Analyze text", command=self.analyze)
        self.run_button.pack(side="left", padx=10)
        ttk.Button(controls, text="Load .txt", command=self.load_text).pack(side="right")
        ttk.Button(controls, text="Example", command=self.example).pack(side="right", padx=8)
        self.description = ttk.Label(main, text="", style="Muted.TLabel", wraplength=950)
        self.description.pack(anchor="w", pady=(12, 8))
        options = ttk.Frame(main)
        options.pack(fill="x", pady=(0, 8))
        self.entity_options = ttk.Frame(options)
        ttk.Label(self.entity_options, text="Optional entity text or label:").pack(side="left")
        self.entity_filter = ttk.Entry(self.entity_options, width=24)
        self.entity_filter.pack(side="left", padx=8)
        self.summary_options = ttk.Frame(options)
        ttk.Label(self.summary_options, text="Summary sentences:").pack(side="left")
        self.summary_count = ttk.Spinbox(self.summary_options, from_=1, to=10, width=4)
        self.summary_count.set("3")
        self.summary_count.pack(side="left", padx=8)
        def tool_changed(event=None):
            self.description.configure(text=TOOLS[self.tool.get()][1])
            self.entity_options.pack_forget()
            self.summary_options.pack_forget()
            if self.tool.get() == "Named entities":
                self.entity_options.pack(anchor="w")
            elif self.tool.get() == "Summarization":
                self.summary_options.pack(anchor="w")
        selector.bind("<<ComboboxSelected>>", tool_changed)
        tool_changed()
        panes = ttk.Panedwindow(main, orient="vertical")
        panes.pack(fill="both", expand=True)
        source = ttk.Frame(panes)
        result = ttk.Frame(panes)
        panes.add(source, weight=3)
        panes.add(result, weight=2)
        source_header = ttk.Frame(source)
        source_header.pack(fill="x")
        ttk.Label(source_header, text="Input text").pack(side="left")
        self.counter = ttk.Label(source_header, text="0 words · 0 characters", style="Muted.TLabel")
        self.counter.pack(side="right")
        self.input = ScrolledText(source, wrap="word", height=9, font=("Segoe UI", 11), relief="flat", padx=12, pady=12, undo=True)
        self.input.pack(fill="both", expand=True, pady=(6, 12))
        self.input.bind("<<Modified>>", self.update_count)
        ttk.Label(result, text="Result").pack(anchor="w")
        self.output = ScrolledText(result, wrap="word", height=6, font=("Segoe UI", 11), relief="flat", padx=12, pady=12, state="disabled")
        self.output.pack(fill="both", expand=True, pady=6)
        footer = ttk.Frame(main)
        footer.pack(fill="x", pady=(8, 0))
        self.status = ttk.Label(footer, text="Ready • analysis stays on this device", style="Muted.TLabel")
        self.status.pack(side="left")
        ttk.Button(footer, text="Save result", command=self.save_result).pack(side="right")
        ttk.Button(footer, text="Copy result", command=self.copy_result).pack(side="right", padx=8)

    def update_count(self, event=None):
        if self.input.edit_modified():
            text = self.input.get("1.0", "end-1c")
            self.counter.configure(text=f"{len(text.split()):,} words · {len(text):,} characters")
            self.input.edit_modified(False)

    def example(self):
        self.input.delete("1.0", "end")
        self.input.insert("1.0", SAMPLE)

    def load_text(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            try:
                if Path(path).stat().st_size > 200000:
                    raise ValueError("Choose a text file smaller than 200 KB.")
                text = Path(path).read_text(encoding="utf-8-sig")
                self.engine.validate(text)
                self.input.delete("1.0", "end")
                self.input.insert("1.0", text)
            except (OSError, ValueError) as exc:
                messagebox.showerror("Load text", str(exc), parent=self.root)

    def analyze(self):
        if self.future is not None:
            return
        try:
            text = self.engine.validate(self.input.get("1.0", "end-1c"))
            tool = self.tool.get()
            method = getattr(self.engine, TOOLS[tool][0])
            args = [text]
            if tool == "Named entities":
                args.append(self.entity_filter.get())
            elif tool == "Summarization":
                args.append(int(self.summary_count.get()))
                if not 1 <= args[-1] <= 10:
                    raise ValueError("Choose between 1 and 10 summary sentences.")
        except ValueError as exc:
            messagebox.showerror("Check input", str(exc), parent=self.root)
            return
        self.run_button.configure(state="disabled")
        self.status.configure(text=f"Running {tool.lower()} locally…")
        self.future = self.executor.submit(method, *args)
        screen_id = self.screen_id
        self.root.after(80, lambda: self.poll_result(tool, screen_id))

    @staticmethod
    def format_result(tool, value):
        if isinstance(value, str):
            return value
        if tool == "Sentiment analysis":
            lines = [f"Overall sentiment: {value['label']}", f"Compound score: {value['compound']:.3f} (−1 to +1)", ""]
            lines.extend(f"{item['label']}: {item['score']:.1%}" for item in value["scored_labels"])
            return "\n".join(lines)
        if tool == "Named entities":
            if not value:
                return "No matching entities found. Try removing the filter or using a longer passage."
            import spacy
            return "\n".join(f"{item['text']} — {spacy.explain(item['label']) or item['label']}" for item in value)
        return "\n".join(f"Language: {item['language']} · estimated probability {item['probability']:.1%}" for item in value)

    def poll_result(self, tool, screen_id):
        if not self.future.done():
            self.root.after(80, lambda: self.poll_result(tool, screen_id))
            return
        try:
            value = self.future.result()
            text = self.format_result(tool, value)
            if self.screen_id == screen_id:
                self.output.configure(state="normal")
                self.output.delete("1.0", "end")
                self.output.insert("1.0", text)
                self.output.configure(state="disabled")
                self.result_text = text
                self.status.configure(text=f"Finished: {tool} • processed locally")
        except Exception as exc:
            if self.screen_id == screen_id:
                messagebox.showerror("Analysis could not finish", str(exc), parent=self.root)
                self.status.configure(text="Analysis failed • check the message and try again")
        finally:
            self.future = None
            if self.run_button.winfo_exists():
                self.run_button.configure(state="normal")

    def copy_result(self):
        if self.result_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.result_text)
            self.status.configure(text="Result copied")

    def save_result(self):
        if not self.result_text:
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
        if path:
            try:
                Path(path).write_text(self.result_text, encoding="utf-8")
                self.status.configure(text="Result saved")
            except OSError as exc:
                messagebox.showerror("Save result", str(exc), parent=self.root)

    def close(self):
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.root.destroy()


if __name__ == "__main__":
    application = NLPApp()
    application.root.mainloop()
