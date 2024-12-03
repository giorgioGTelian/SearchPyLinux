import tkinter as tk
from tkinter import filedialog, messagebox
import qtag
import os


class QTagGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QTag GUI")

        # Path Selection
        self.path_label = tk.Label(root, text="Search Path:")
        self.path_label.pack(pady=5)
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_path)
        self.browse_button.pack(pady=5)

        # Tags Input
        self.tag_label = tk.Label(root, text="Tags (comma-separated):")
        self.tag_label.pack(pady=5)
        self.tag_entry = tk.Entry(root, width=50)
        self.tag_entry.pack(pady=5)

        # Options Selection
        self.options_label = tk.Label(root, text="Options:")
        self.options_label.pack(pady=5)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack()

        self.case_sensitive = tk.BooleanVar()
        self.case_sensitive_check = tk.Checkbutton(self.options_frame, text="-c Case sensitive", variable=self.case_sensitive)
        self.case_sensitive_check.grid(row=0, column=0, sticky="w")

        self.directories_only = tk.BooleanVar()
        self.directories_only_check = tk.Checkbutton(self.options_frame, text="-d Directories only", variable=self.directories_only)
        self.directories_only_check.grid(row=1, column=0, sticky="w")

        self.files_only = tk.BooleanVar()
        self.files_only_check = tk.Checkbutton(self.options_frame, text="-f Files only", variable=self.files_only)
        self.files_only_check.grid(row=2, column=0, sticky="w")

        self.local_search = tk.BooleanVar()
        self.local_search_check = tk.Checkbutton(self.options_frame, text="-l Local search", variable=self.local_search)
        self.local_search_check.grid(row=0, column=1, sticky="w")

        self.simple_search = tk.BooleanVar()
        self.simple_search_check = tk.Checkbutton(self.options_frame, text="-s Simple search", variable=self.simple_search)
        self.simple_search_check.grid(row=1, column=1, sticky="w")

        # Action Buttons
        self.search_button = tk.Button(root, text="Search", command=self.search_files)
        self.search_button.pack(pady=10)

        self.set_command_button = tk.Button(root, text="Set QTag as Command (-x)", command=self.set_qtag_command)
        self.set_command_button.pack(pady=5)

        # Results Display
        self.result_label = tk.Label(root, text="Results:")
        self.result_label.pack(pady=5)
        self.result_text = tk.Text(root, height=20, width=80, state=tk.DISABLED)
        self.result_text.pack(pady=5)

    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def search_files(self):
        user_path = self.path_entry.get().strip()
        tags = self.tag_entry.get().strip()
        if not user_path or not tags:
            messagebox.showwarning("Input Error", "Please provide both a search path and tags.")
            return

        # Set Defaults
        qtag.Defaults.userpath = user_path
        qtag.Defaults.new_argv = tags.split(',')

        # Apply Options
        qtag.Defaults.case_sensitive = self.case_sensitive.get()
        qtag.Defaults.onlydirs = self.directories_only.get()
        qtag.Defaults.onlyfiles = self.files_only.get()
        qtag.Defaults.recursive = not self.local_search.get()
        qtag.Defaults.extended = not self.simple_search.get()

        qtag.compile_regexes()

        # Execute Search
        self.display_results("Searching...")
        try:
            self.capture_output(qtag.scan_all)
        except Exception as e:
            self.display_results(f"Error: {e}")

    def set_qtag_command(self):
        try:
            qtag.set_qtag_command()
            messagebox.showinfo("Success", "QTag has been set as a command.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set QTag as command: {e}")

    def capture_output(self, func):
        """Capture and display the output of a qtag function."""
        import io
        import sys
        buffer = io.StringIO()
        sys.stdout = buffer
        func()
        sys.stdout = sys.__stdout__
        self.display_results(buffer.getvalue())

    def display_results(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = QTagGUI(root)
    root.mainloop()
