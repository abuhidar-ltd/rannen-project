# Image Encryption App - Super Simple!

A super simple image encryption app perfect for learning! Uses basic XOR encryption - easy to understand and modify.

## Features

- 🎓 **Super Simple**: Easy XOR encryption - perfect for learning!
- 🖼️ **Image Support**: Works with JPG, PNG, BMP, GIF, TIFF
- 🎨 **Simple GUI**: Clean, easy-to-use interface
- 💡 **Educational**: Code is simple enough to understand and modify

## Installation

```bash
pip install -r requirements.txt
```

Then run:
```bash
python gui_app.py
```

## How to Use

Super simple 3 steps:

1. **Click Browse** → Select an image file
2. **Enter a password**
3. **Click Encrypt or Decrypt**

That's it! Encrypted files are saved with `_encrypted.png` and decrypted files with `_decrypted.png`.

## How It Works (Simple!)

### XOR Encryption

The app uses **XOR encryption** - the simplest form of encryption!

```
Original byte:  10110101
Key byte:       11001010
XOR →         01111111  (encrypted)

To decrypt, XOR again with same key!
Encrypted:     01111111
Key byte:      11001010
XOR →        10110101  (back to original!)
```

### What Happens:

1. **Load Image**: Image is converted to bytes
2. **Create Key**: Password is hashed with SHA256 to create a key
3. **XOR Encrypt**: Each byte of image is XOR'd with key byte
4. **Save**: Encrypted bytes saved to file

### To Decrypt:

Same process in reverse - just XOR again with the same key!

## Code Structure

### `image_encryption.py`
- **`encrypt_image()`**: Encrypts an image file
- **`decrypt_image()`**: Decrypts an encrypted file
- **`is_encrypted_file()`**: Checks if a file is encrypted

### `gui_app.py`
- **`ImageEncryptionGUI`**: Simple GUI class
- Just 3 functions: browse, encrypt, decrypt

## Requirements

- Python 3.7+
- Pillow (PIL) for image handling
- tkinter (usually comes with Python)

That's it! No complex crypto libraries needed.

## Why This is Great for Learning

✅ **Simple Code**: Easy to read and understand  
✅ **Basic Concepts**: Learn XOR, hashing, byte manipulation  
✅ **Easy to Modify**: Try different encryption methods!  
✅ **No Complex Libraries**: Just Python + Pillow

## Try Modifying!

Want to learn more? Try:
- Change the hash function (use MD5, SHA512, etc.)
- Add your own encryption method
- Try different key generation
- Add image compression

## Note

⚠️ **Educational Use**: XOR encryption is simple but not super secure for real-world use.  
🔒 For learning, it's perfect! For real security, use AES encryption.

---

**Perfect for CS projects and learning encryption!**
