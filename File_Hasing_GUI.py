import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os
import time

# Global variables to store selected paths
source_folder = None
destination_folder = None

def hash_folder(folder_path):
    """Generate SHA-256 hash for an entire folder by hashing all file contents."""
    sha256 = hashlib.sha256()

    for root, dirs, files in os.walk(folder_path):
        for filename in sorted(files):  # Sort files for consistency
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "rb") as f:
                    while chunk := f.read(8192):  # Read in chunks
                        sha256.update(chunk)
            except Exception as e:
                print(f"Skipping {file_path}: {e}")

    return sha256.hexdigest()

def save_hash_to_file(hash_value, folder_path, destination):
    """Save the hash to a text file in the destination folder."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"hash_{os.path.basename(folder_path)}_{timestamp}.txt"
    file_path = os.path.join(destination, filename)

    with open(file_path, "w") as f:
        f.write(f"Folder: {folder_path}\n")
        f.write(f"SHA-256 Hash: {hash_value}\n")

    messagebox.showinfo("Success", f"Hash saved to:\n{file_path}")

def browse_source():
    """Select folder to hash."""
    global source_folder
    source_folder = filedialog.askdirectory()
    if source_folder:
        source_label.config(text=f"Source: {source_folder}")

def browse_destination():
    """Select destination folder to save hash file."""
    global destination_folder
    destination_folder = filedialog.askdirectory()
    if destination_folder:
        destination_label.config(text=f"Destination: {destination_folder}")

def run_hash():
    """Perform the hashing and saving process."""
    if not source_folder or not destination_folder:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    hash_value = hash_folder(source_folder)
    save_hash_to_file(hash_value, source_folder, destination_folder)

def main():
    global source_label, destination_label
    root = tk.Tk()
    root.title("Folder Hasher")
    root.geometry("400x300")

    # Source folder selection
    source_label = tk.Label(root, text="No source folder selected", wraplength=350)
    source_label.pack(pady=10)

    browse_source_button = tk.Button(root, text="Select Folder to Hash", command=browse_source)
    browse_source_button.pack(pady=5)

    # Destination folder selection
    destination_label = tk.Label(root, text="No destination folder selected", wraplength=350)
    destination_label.pack(pady=10)

    browse_destination_button = tk.Button(root, text="Select Destination Folder", command=browse_destination)
    browse_destination_button.pack(pady=5)

    # Run hashing
    run_button = tk.Button(root, text="Generate & Save Hash", command=run_hash)
    run_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
