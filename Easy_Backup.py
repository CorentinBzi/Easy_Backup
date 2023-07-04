import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinter.ttk import Progressbar, Style
from customtkinter import CTkButton, CTkFrame
from ttkthemes import ThemedStyle


def get_folder_size(folder):
    total_size = 0
    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size


def convert_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / (1024 ** 3):.2f} GB"


class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(r'my_icon.ico')
        self.root.title("Easy Backup")
        self.root.geometry("800x400")
        self.style = ThemedStyle(root)
        self.style.set_theme("equilux")

        # Create style for Progressbar
        style = Style()
        style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')

        self.source_text = StringVar()
        self.source_text.set("Folder(s) to backup:")
        self.source_label = tk.Label(root, textvariable=self.source_text, font=("Helvetica", 12, "bold"))
        self.source_label.pack(pady=10)

        self.source_frame = CTkFrame(root)
        self.source_frame.pack(pady=10)

        self.source_button = CTkButton(self.source_frame, text="Select", command=self.select_source)
        self.source_button.pack(side=tk.LEFT, padx=10)

        self.default_button = CTkButton(self.source_frame, text="Select by default", command=self.select_default_source)
        self.default_button.pack(side=tk.LEFT, padx=10)

        self.destination_text = StringVar()
        self.destination_text.set("Backup folder:")
        self.destination_label = tk.Label(root, textvariable=self.destination_text, font=("Helvetica", 12, "bold"))
        self.destination_label.pack(pady=10)

        self.destination_button = CTkButton(root, text="Select", command=self.select_destination)
        self.destination_button.pack(pady=10)

        self.backup_button = CTkButton(root, text="Perform backup", command=self.start_backup)
        self.backup_button.pack(pady=10)

        self.progress_text = StringVar()
        self.progress_label = tk.Label(root, textvariable=self.progress_text, font=("Helvetica", 12, "bold"))
        self.progress_text.set("Progress: 0%")
        self.progress_label.pack(pady=10)

        self.progressbar = Progressbar(root, orient="horizontal", length=200, mode="determinate", style="green.Horizontal.TProgressbar")
        self.progressbar.pack()

        self.current_file_label = tk.Label(root, text="")
        self.current_file_label.pack(pady=10)

        # Error handling
        self.error_text = StringVar()
        self.error_label = tk.Label(root, textvariable=self.error_text)
        self.error_label.pack(pady=10)

    def select_source(self):
        self.source_dir = filedialog.askdirectory(title="Select the folder(s) to backup")
        if self.source_dir:
            size = get_folder_size(self.source_dir)
            self.source_text.set(f"Folder(s) to backup: {self.source_dir} (Size: {convert_size(size)})")

    def select_default_source(self):
        self.source_dir = os.path.expanduser("~\\Documents")
        size = get_folder_size(self.source_dir)
        self.source_text.set(f"Folder(s) to backup: {self.source_dir} (Size: {convert_size(size)})")

    def select_destination(self):
        self.destination_dir = filedialog.askdirectory(title="Select the backup folder")
        if self.destination_dir:
            available_size = shutil.disk_usage(self.destination_dir).free
            self.destination_text.set(f"Backup folder: {self.destination_dir} (Available size: {convert_size(available_size)})")

    def start_backup(self):
        if not hasattr(self, "source_dir") or not hasattr(self, "destination_dir"):
            messagebox.showerror("Error", "Please select the source and destination folders.")
            return

        total_size = get_folder_size(self.source_dir)
        available_size = shutil.disk_usage(self.destination_dir).free
        if total_size > available_size:
            messagebox.showerror("Error", "The size of the data to backup is larger than the available size for backup.")
            return

        self.progressbar["maximum"] = total_size
        self.progressbar["value"] = 0

        self.backup_files(self.source_dir, self.destination_dir)

        messagebox.showinfo("Backup completed", "The backup was successfully performed.")

    def backup_files(self, source, destination):
        for path, dirs, files in os.walk(source):
            for f in files:
                source_path = os.path.join(path, f)
                relative_path = os.path.relpath(source_path, source)
                destination_path = os.path.join(destination, relative_path)
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                try:
                    shutil.copy2(source_path, destination_path)
                except Exception as e:
                    self.error_text.set(f"Error copying file: {source_path}. Error: {e}")
                self.progressbar["value"] += os.path.getsize(source_path)
                percentage = (self.progressbar["value"] / self.progressbar["maximum"]) * 100
                self.progress_text.set(f"Progress: {percentage:.2f}%")
                self.current_file_label.config(text=f"Processing file: {source_path}")
                self.root.update()


root = tk.Tk()
app = BackupApp(root)
root.mainloop()
