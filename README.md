# Image Encryption GUI Application

A user-friendly Python application for encrypting and decrypting images using AES encryption. This tool provides a simple graphical interface to protect your images with strong encryption.

## Features

- 🔐 **Strong Encryption**: Uses AES-256 encryption with PBKDF2 key derivation
- 🖼️ **Image Support**: Supports JPG, PNG, BMP, GIF, and TIFF formats
- 🎨 **User-Friendly GUI**: Clean and intuitive interface built with tkinter
- 🔍 **Image Preview**: Preview images before encryption
- 📝 **Activity Logging**: Track all operations with timestamps
- ⚡ **Threaded Operations**: Non-blocking encryption/decryption
- 🛡️ **Error Handling**: Comprehensive error handling and user feedback

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**
   ```bash
   # If you have the files in a directory
   cd image_encryption_app
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python gui_app.py
   ```

## Usage

### Basic Workflow

1. **Launch the application**
   ```bash
   python gui_app.py
   ```

2. **Select an image file**
   - Click "Browse" to select an image file
   - Supported formats: JPG, JPEG, PNG, BMP, GIF, TIFF
   - The application will automatically detect if a file is encrypted (.enc)

3. **Enter a password**
   - Choose a strong password for encryption/decryption
   - Use the "Show Password" checkbox to verify your input

4. **Set output location** (optional)
   - The application suggests default output paths
   - Click "Browse" to choose a custom location

5. **Encrypt or Decrypt**
   - Click "🔒 Encrypt Image" to encrypt
   - Click "🔓 Decrypt Image" to decrypt
   - Monitor progress in the activity log

### File Types

- **Input**: Regular image files (.jpg, .png, etc.) or encrypted files (.enc)
- **Output**: Encrypted files (.enc) or decrypted images (.png)

## How It Works

### Encryption Process

1. **Image Loading**: The application loads the image using PIL (Pillow)
2. **Format Conversion**: Converts the image to PNG format for consistent handling
3. **Key Derivation**: Uses PBKDF2 with SHA-256 to derive encryption key from password
4. **Encryption**: Encrypts image data using Fernet (AES-256)
5. **File Output**: Saves encrypted data with salt for later decryption

### Decryption Process

1. **File Reading**: Reads the encrypted file and extracts salt
2. **Key Derivation**: Recreates the encryption key using the same password and salt
3. **Decryption**: Decrypts the data using Fernet
4. **Image Reconstruction**: Converts decrypted bytes back to image format
5. **File Output**: Saves the decrypted image

### Security Features

- **PBKDF2 Key Derivation**: 100,000 iterations for strong key generation
- **Random Salt**: Each encryption uses a unique salt
- **AES-256 Encryption**: Industry-standard symmetric encryption
- **Secure Password Handling**: Passwords are not stored or logged

## Project Structure

```
image_encryption_app/
├── requirements.txt          # Python dependencies
├── image_encryption.py       # Core encryption/decryption logic
├── gui_app.py               # Main GUI application
├── README.md                # This file
└── demo.py                  # Demo script for testing
```

## Code Explanation

### Core Components

#### 1. ImageEncryption Class (`image_encryption.py`)

The main encryption class that handles:
- Password-based key generation using PBKDF2
- Image encryption and decryption
- File format validation
- Error handling

**Key Methods:**
- `generate_key_from_password()`: Creates encryption key from password
- `encrypt_image()`: Encrypts an image file
- `decrypt_image()`: Decrypts an encrypted file
- `is_encrypted_file()`: Detects encrypted files

#### 2. ImageEncryptionGUI Class (`gui_app.py`)

The GUI application that provides:
- File selection dialogs
- Password input with visibility toggle
- Image preview functionality
- Progress tracking and logging
- Threaded operations for responsiveness

**Key Features:**
- **File Management**: Browse and select input/output files
- **Password Security**: Secure password input with show/hide option
- **Preview System**: Display image thumbnails before encryption
- **Activity Logging**: Timestamped log of all operations
- **Error Handling**: User-friendly error messages

### GUI Layout

The interface is organized into sections:

1. **File Selection**: Browse and select image files
2. **Password Input**: Secure password entry with visibility toggle
3. **Output Location**: Choose where to save encrypted/decrypted files
4. **Action Buttons**: Encrypt and Decrypt operations
5. **Progress Tracking**: Visual progress indicator and status
6. **Activity Log**: Detailed log of all operations
7. **Image Preview**: Thumbnail preview of selected images

## Security Considerations

### Password Strength
- Use strong, unique passwords for each image
- Consider using a password manager
- Avoid common passwords or dictionary words

### File Handling
- Encrypted files (.enc) contain sensitive data
- Store encrypted files securely
- Delete original images after encryption if desired
- Backup encrypted files safely

### Best Practices
- Test decryption before deleting originals
- Keep passwords secure and accessible
- Use different passwords for different images
- Regularly backup encrypted files

## Troubleshooting

### Common Issues

1. **"Unsupported image format"**
   - Ensure the file is a supported image format
   - Try converting the image to PNG or JPG first

2. **"Decryption failed"**
   - Verify the password is correct
   - Ensure the file is actually encrypted
   - Check if the file is corrupted

3. **"File not found"**
   - Verify the file path is correct
   - Check file permissions
   - Ensure the file hasn't been moved or deleted

4. **GUI not responding**
   - Large images may take time to process
   - Check the activity log for progress updates
   - Wait for the operation to complete

### Performance Tips

- **Large Images**: Very large images may take longer to process
- **Memory Usage**: The application loads entire images into memory
- **File Size**: Encrypted files are typically larger than originals

## Advanced Usage

### Command Line Interface

You can also use the encryption module directly:

```python
from image_encryption import ImageEncryption

# Create encryptor instance
encryptor = ImageEncryption()

# Encrypt an image
encrypted_path, salt = encryptor.encrypt_image("image.jpg", "password")

# Decrypt an image
decrypted_path = encryptor.decrypt_image("image.enc", "password")
```

### Custom Integration

The `ImageEncryption` class can be integrated into other applications:

```python
# Example: Batch encryption
import os
from image_encryption import ImageEncryption

encryptor = ImageEncryption()
password = "your_password"

for filename in os.listdir("images/"):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        input_path = os.path.join("images", filename)
        output_path = os.path.join("encrypted", filename + ".enc")
        encryptor.encrypt_image(input_path, password, output_path)
```

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding new image format support
- Enhancing the GUI

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **cryptography**: For providing secure encryption capabilities
- **Pillow (PIL)**: For image processing functionality
- **tkinter**: For the GUI framework (included with Python)

---

**Note**: This tool is for educational and personal use. Always ensure you have proper backups and understand the implications of encrypting your files.
