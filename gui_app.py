"""
Super Simple Image Encryption App
Easy to use and understand!
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from image_encryption import ImageEncryption


class ImageEncryptionGUI:
    """Simple GUI for image encryption"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        self.encryptor = ImageEncryption()
        self.selected_file = ""
        self.password = tk.StringVar()
        
        self.create_widgets()
        self.center_window()
    
    def create_widgets(self):
        """Create the simple interface"""
        main = ttk.Frame(self.root, padding="30")
        main.grid(row=0, column=0)
        
        # Title
        title = ttk.Label(main, text="🔐 Image Encryption", font=('Arial', 18, 'bold'))
        title.grid(row=0, column=0, pady=(0, 30))
        
        # File selection
        ttk.Label(main, text="1. Select Image:", font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main)
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_entry = ttk.Entry(file_frame, state='readonly', width=35)
        self.file_entry.grid(row=0, column=0, padx=(0, 10))
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=1)
        
        # Password
        ttk.Label(main, text="2. Enter Password:", font=('Arial', 11)).grid(row=3, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(main, textvariable=self.password, show="*", width=35)
        password_entry.grid(row=4, column=0, pady=(0, 20))
        
        # Buttons
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=5, column=0, pady=(0, 20))
        
        ttk.Button(btn_frame, text="🔒 Encrypt", command=self.encrypt_image, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="🔓 Decrypt", command=self.decrypt_image, width=15).grid(row=0, column=1, padx=5)
        
        # Status
        self.status = ttk.Label(main, text="Ready", foreground='gray')
        self.status.grid(row=6, column=0)
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def browse_file(self):
        """Select a file"""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All", "*.*")]
        )
        if filename:
            self.selected_file = filename
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, os.path.basename(filename))
            self.file_entry.config(state='readonly')
            self.status.config(text="File selected", foreground='green')
    
    def encrypt_image(self):
        """Encrypt the image"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        # Output filename
        base = os.path.splitext(self.selected_file)[0]
        output = f"{base}_encrypted.png"
        
        self.status.config(text="Encrypting...", foreground='blue')
        self.root.update()
        
        try:
            self.encryptor.encrypt_image(self.selected_file, self.password.get(), output)
            messagebox.showinfo("Success!", f"Encrypted!\nSaved as: {os.path.basename(output)}")
            self.status.config(text="Encryption complete!", foreground='green')
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")
            self.status.config(text="Error", foreground='red')
    
    def decrypt_image(self):
        """Decrypt the image"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        # Output filename
        base = os.path.splitext(self.selected_file)[0]
        if base.endswith('_encrypted'):
            output = base.replace('_encrypted', '_decrypted.png')
        else:
            output = f"{base}_decrypted.png"
        
        self.status.config(text="Decrypting...", foreground='blue')
        self.root.update()
        
        try:
            self.encryptor.decrypt_image(self.selected_file, self.password.get(), output)
            messagebox.showinfo("Success!", f"Decrypted!\nSaved as: {os.path.basename(output)}")
            self.status.config(text="Decryption complete!", foreground='green')
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")
            self.status.config(text="Error", foreground='red')


def main():
    """Start the app"""
    root = tk.Tk()
    app = ImageEncryptionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
