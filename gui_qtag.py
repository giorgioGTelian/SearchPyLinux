import tkinter as tk
from tkinter import filedialog, messagebox
import os
import qtag

class QTagGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QTag GUI")

        # Search Path
        self.path_label = tk.Label(root, text="Search Path:")
        self.path_label.pack(pady=5)
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_path)
        self.browse_button.pack(pady=5)

        # Tags
        self.tag_label = tk.Label(root, text="Tags (comma-separated):")
        self.tag_label.pack(pady=5)
        self.tag_entry = tk.Entry(root, width=50)
        self.tag_entry.pack(pady=5)

        # Action Buttons
        self.search_button = tk.Button(root, text="Search", command=self.search_files)
        self.search_button.pack(pady=10)
        self.add_tag_button = tk.Button(root, text="Add Tag", command=lambda: self.manage_tag('add'))
        self.add_tag_button.pack(pady=5)
        self.delete_tag_button = tk.Button(root, text="Delete Tag", command=lambda: self.manage_tag('delete'))
        self.delete_tag_button.pack(pady=5)

        # Results Area
        self.result_label = tk.Label(root, text="Results:")
        self.result_label.pack(pady=5)
        self.result_text = tk.Text(root, height=15, width=60, state=tk.DISABLED)
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

        # Set Defaults and execute search
        qtag.Defaults.userpath = user_path
        qtag.Defaults.new_argv = tags.split(',')
        qtag.compile_regexes()

        self.display_results("Searching...")
        try:
            self.capture_output(qtag.scan_all)
        except Exception as e:
            self.display_results(f"Error: {e}")

    def manage_tag(self, action):
        tag = self.tag_entry.get().strip()
        if not tag:
            messagebox.showwarning("Input Error", "Please provide a tag.")
            return

        qtag.Defaults.new_tag = f":{tag}" if action == 'delete' else tag
        try:
            self.capture_output(lambda: qtag.manage_tag_new(tag, f"{action}_tag"))
        except Exception as e:
            self.display_results(f"Error: {e}")

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
