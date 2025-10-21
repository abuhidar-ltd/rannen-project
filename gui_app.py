"""
Image Encryption GUI Application

A user-friendly GUI application for encrypting and decrypting images.
Built with tkinter for cross-platform compatibility.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from PIL import Image, ImageTk
from image_encryption import ImageEncryption


class ImageEncryptionGUI:
    """
    Main GUI class for the Image Encryption application.
    
    This class creates a user-friendly interface for encrypting and decrypting images.
    It includes file selection, password input, progress tracking, and image preview.
    """
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize encryption handler
        self.encryptor = ImageEncryption()
        
        # Variables
        self.selected_file = tk.StringVar()
        self.password = tk.StringVar()
        self.output_path = tk.StringVar()
        self.is_processing = False
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Center the window
        self.center_window()
    
    def setup_styles(self):
        """Configure custom styles for the GUI."""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('File.TButton', font=('Arial', 9))
        
        # Configure frame styles
        style.configure('Card.TFrame', relief='raised', borderwidth=1)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="🔐 Image Encryption Tool", 
            font=('Arial', 16, 'bold')
        )
        
        # File selection section
        self.file_frame = ttk.LabelFrame(self.main_frame, text="Select Image File", padding="10")
        
        self.file_entry = ttk.Entry(
            self.file_frame, 
            textvariable=self.selected_file, 
            width=50, 
            state='readonly'
        )
        
        self.browse_button = ttk.Button(
            self.file_frame, 
            text="Browse", 
            command=self.browse_file,
            style='File.TButton'
        )
        
        # Password section
        self.password_frame = ttk.LabelFrame(self.main_frame, text="Password", padding="10")
        
        self.password_entry = ttk.Entry(
            self.password_frame, 
            textvariable=self.password, 
            show="*", 
            width=30
        )
        
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(
            self.password_frame, 
            text="Show Password", 
            variable=self.show_password_var,
            command=self.toggle_password_visibility
        )
        
        # Output path section
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Output Location", padding="10")
        
        self.output_entry = ttk.Entry(
            self.output_frame, 
            textvariable=self.output_path, 
            width=50, 
            state='readonly'
        )
        
        self.output_browse_button = ttk.Button(
            self.output_frame, 
            text="Browse", 
            command=self.browse_output,
            style='File.TButton'
        )
        
        # Action buttons
        self.action_frame = ttk.Frame(self.main_frame)
        
        self.encrypt_button = ttk.Button(
            self.action_frame, 
            text="🔒 Encrypt Image", 
            command=self.encrypt_image,
            style='Action.TButton'
        )
        
        self.decrypt_button = ttk.Button(
            self.action_frame, 
            text="🔓 Decrypt Image", 
            command=self.decrypt_image,
            style='Action.TButton'
        )
        
        # Progress section
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            mode='indeterminate'
        )
        
        self.status_label = ttk.Label(
            self.progress_frame, 
            text="Ready to encrypt/decrypt images", 
            font=('Arial', 9)
        )
        
        # Log section
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Activity Log", padding="10")
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, 
            height=8, 
            width=70,
            font=('Consolas', 9)
        )
        
        # Image preview section
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="Image Preview", padding="10")
        
        self.preview_label = ttk.Label(
            self.preview_frame, 
            text="No image selected", 
            font=('Arial', 10, 'italic')
        )
        
        # Clear log button
        self.clear_log_button = ttk.Button(
            self.log_frame, 
            text="Clear Log", 
            command=self.clear_log,
            style='File.TButton'
        )
    
    def setup_layout(self):
        """Arrange widgets in the window."""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Title
        self.title_label.grid(row=0, column=0, pady=(0, 20))
        
        # File selection
        self.file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.file_frame.columnconfigure(0, weight=1)
        
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.browse_button.grid(row=0, column=1)
        
        # Password
        self.password_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.password_entry.grid(row=0, column=0, padx=(0, 10))
        self.show_password_check.grid(row=0, column=1)
        
        # Output path
        self.output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.output_frame.columnconfigure(0, weight=1)
        
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.output_browse_button.grid(row=0, column=1)
        
        # Action buttons
        self.action_frame.grid(row=4, column=0, pady=(0, 10))
        
        self.encrypt_button.grid(row=0, column=0, padx=(0, 10))
        self.decrypt_button.grid(row=0, column=1)
        
        # Progress
        self.progress_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.status_label.grid(row=1, column=0)
        
        # Log
        self.log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        self.clear_log_button.grid(row=1, column=0)
        
        # Preview
        self.preview_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.preview_label.grid(row=0, column=0)
        
        # Configure main frame row weights
        self.main_frame.rowconfigure(6, weight=1)
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def browse_file(self):
        """Open file dialog to select an image file."""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("Encrypted files", "*.enc"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=file_types
        )
        
        if filename:
            self.selected_file.set(filename)
            self.update_preview(filename)
            self.auto_set_output_path(filename)
            self.log_message(f"Selected file: {os.path.basename(filename)}")
    
    def browse_output(self):
        """Open file dialog to select output location."""
        if not self.selected_file.get():
            messagebox.showwarning("Warning", "Please select an input file first.")
            return
        
        input_file = self.selected_file.get()
        is_encrypted = self.encryptor.is_encrypted_file(input_file)
        
        if is_encrypted:
            # For decryption, suggest removing _encrypted suffix and adding _decrypted
            suggested_name = os.path.splitext(input_file)[0]
            if suggested_name.endswith('_encrypted'):
                suggested_name = suggested_name.replace('_encrypted', '_decrypted.png')
            elif suggested_name.endswith('.enc'):
                suggested_name = suggested_name[:-4] + "_decrypted.png"
            else:
                suggested_name += "_decrypted.png"
        else:
            # For encryption, suggest adding _encrypted suffix with .png extension
            base_name = os.path.splitext(input_file)[0]
            suggested_name = base_name + "_encrypted.png"
        
        filename = filedialog.asksaveasfilename(
            title="Save As",
            initialvalue=suggested_name,
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("Encrypted files", "*.enc"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.output_path.set(filename)
            self.log_message(f"Output path set: {os.path.basename(filename)}")
    
    def auto_set_output_path(self, input_file):
        """Automatically set output path based on input file."""
        is_encrypted = self.encryptor.is_encrypted_file(input_file)
        
        if is_encrypted:
            # For decryption
            suggested_name = os.path.splitext(input_file)[0]
            if suggested_name.endswith('_encrypted'):
                suggested_name = suggested_name.replace('_encrypted', '_decrypted.png')
            elif suggested_name.endswith('.enc'):
                suggested_name = suggested_name[:-4] + "_decrypted.png"
            else:
                suggested_name += "_decrypted.png"
        else:
            # For encryption - create PNG with embedded encrypted data
            base_name = os.path.splitext(input_file)[0]
            suggested_name = base_name + "_encrypted.png"
        
        self.output_path.set(suggested_name)
    
    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def update_preview(self, file_path):
        """Update the image preview."""
        try:
            if not os.path.exists(file_path):
                self.preview_label.config(text="File not found")
                return
            
            # Check if it's an encrypted file
            if self.encryptor.is_encrypted_file(file_path):
                # For our new format, show the decoy image (the random noise)
                # This is what people will see when you share it online
                self.preview_label.config(text="Encrypted image (noise pattern - safe to share)")
                
                # Still show the decoy image visually so user can see what others will see
                with Image.open(file_path) as img:
                    # Resize image to fit preview (max 200x150)
                    img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage for tkinter
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update preview label
                    self.preview_label.config(image=photo, text="Decoy image (noise)")
                    self.preview_label.image = photo  # Keep a reference
                return
            
            # Load and resize image for preview
            with Image.open(file_path) as img:
                # Resize image to fit preview (max 200x150)
                img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage for tkinter
                photo = ImageTk.PhotoImage(img)
                
                # Update preview label
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo  # Keep a reference
                
        except Exception as e:
            self.preview_label.config(text=f"Preview error: {str(e)}")
    
    def log_message(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the activity log."""
        self.log_text.delete(1.0, tk.END)
    
    def start_processing(self):
        """Start the processing animation."""
        self.is_processing = True
        self.progress_bar.start()
        self.encrypt_button.config(state='disabled')
        self.decrypt_button.config(state='disabled')
        self.browse_button.config(state='disabled')
        self.output_browse_button.config(state='disabled')
    
    def stop_processing(self):
        """Stop the processing animation."""
        self.is_processing = False
        self.progress_bar.stop()
        self.encrypt_button.config(state='normal')
        self.decrypt_button.config(state='normal')
        self.browse_button.config(state='normal')
        self.output_browse_button.config(state='normal')
    
    def encrypt_image(self):
        """Encrypt the selected image."""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select an image file first.")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password.")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify an output path.")
            return
        
        # Check if file is already encrypted
        if self.encryptor.is_encrypted_file(self.selected_file.get()):
            messagebox.showwarning("Warning", "The selected file appears to be already encrypted.")
            return
        
        # Start encryption in a separate thread
        self.start_processing()
        self.status_label.config(text="Encrypting image...")
        
        def encrypt_thread():
            try:
                self.log_message("Starting encryption...")
                encrypted_path, salt = self.encryptor.encrypt_image(
                    self.selected_file.get(),
                    self.password.get(),
                    self.output_path.get()
                )
                
                self.root.after(0, lambda: self.encryption_success(encrypted_path))
                
            except Exception as e:
                self.root.after(0, lambda: self.operation_error(f"Encryption failed: {str(e)}"))
        
        threading.Thread(target=encrypt_thread, daemon=True).start()
    
    def decrypt_image(self):
        """Decrypt the selected encrypted image."""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select an encrypted file first.")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "Please enter the decryption password.")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify an output path.")
            return
        
        # Check if file appears to be encrypted
        if not self.encryptor.is_encrypted_file(self.selected_file.get()):
            messagebox.showwarning("Warning", "The selected file doesn't appear to be encrypted.")
            return
        
        # Start decryption in a separate thread
        self.start_processing()
        self.status_label.config(text="Decrypting image...")
        
        def decrypt_thread():
            try:
                self.log_message("Starting decryption...")
                decrypted_path = self.encryptor.decrypt_image(
                    self.selected_file.get(),
                    self.password.get(),
                    self.output_path.get()
                )
                
                self.root.after(0, lambda: self.decryption_success(decrypted_path))
                
            except Exception as e:
                self.root.after(0, lambda: self.operation_error(f"Decryption failed: {str(e)}"))
        
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def encryption_success(self, encrypted_path):
        """Handle successful encryption."""
        self.stop_processing()
        self.status_label.config(text="Encryption completed successfully!")
        
        self.log_message(f"Encryption completed: {os.path.basename(encrypted_path)}")
        
        messagebox.showinfo(
            "Success", 
            f"Image encrypted successfully!\n\nSaved to: {encrypted_path}"
        )
        
        # Update preview to show encrypted file status
        self.preview_label.config(text="Encrypted file - preview not available")
    
    def decryption_success(self, decrypted_path):
        """Handle successful decryption."""
        self.stop_processing()
        self.status_label.config(text="Decryption completed successfully!")
        
        self.log_message(f"Decryption completed: {os.path.basename(decrypted_path)}")
        
        messagebox.showinfo(
            "Success", 
            f"Image decrypted successfully!\n\nSaved to: {decrypted_path}"
        )
        
        # Update preview to show decrypted image
        self.update_preview(decrypted_path)
    
    def operation_error(self, error_message):
        """Handle operation errors."""
        self.stop_processing()
        self.status_label.config(text="Operation failed")
        
        self.log_message(f"ERROR: {error_message}")
        
        messagebox.showerror("Error", error_message)


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = ImageEncryptionGUI(root)
    
    # Add some helpful tips
    app.log_message("🔐 Welcome to Image Encryption Tool!")
    app.log_message("NEW: Encrypted images now look like random noise!")
    app.log_message("Safe to share online - only visible with correct password")
    app.log_message("")
    app.log_message("1. Select an image file to encrypt or encrypted PNG to decrypt")
    app.log_message("2. Enter a strong password")
    app.log_message("3. Choose output location (optional)")
    app.log_message("4. Click Encrypt or Decrypt button")
    app.log_message("")
    app.log_message("💡 Tip: The encrypted image will appear as random RGB noise")
    app.log_message("   Perfect for sharing sensitive images online!")
    app.log_message("")
    
    root.mainloop()


if __name__ == "__main__":
    main()
