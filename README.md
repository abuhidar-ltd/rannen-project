# 🔐 Image Encryption Tool - Learning Edition

A **super simple** command-line image encryption tool designed for learning!

## 📚 What Is This?

This is a beginner-friendly program that:
- Encrypts images with a password (scrambles them so they're unreadable)
- Decrypts them back with the same password
- Uses XOR encryption (simple but great for learning!)
- Has **LOTS of comments** to help you learn

## ⚠️ Important Note

**This is for LEARNING ONLY!** Real-world encryption is much more complex. Don't use this for actual security needs!

## 🚀 Quick Start

### 1. Setup (First Time Only)

Run the setup script to install everything you need:

```bash
python3 setup.py
```

This will:
- Check your Python version
- Install required libraries (just Pillow for images)
- Test that everything works

### 2. Try the Demo

See the encryption in action with a simple demo:

```bash
python3 demo.py
```

This will:
- Create a test image
- Encrypt it with a password
- Decrypt it back
- Show you what happens with the wrong password

### 3. Use the Program

Encrypt your own images:

```bash
python3 main.py
```

Follow the on-screen instructions!

## 📖 How It Works

### The Simple Explanation

1. **Image → Bytes**: Convert the image to raw data (numbers)
2. **Password → Key**: Turn your password into an encryption key using SHA256
3. **XOR Magic**: Use XOR operation to scramble the bytes
   - `original XOR key = encrypted`
   - `encrypted XOR key = original` (it reverses itself!)
4. **Save**: Write the scrambled bytes to a file

### XOR Explained

XOR is a simple bitwise operation:
- `5 XOR 3 = 6`
- `6 XOR 3 = 5` (back to original!)

This "reversible" property makes it perfect for encryption!

## 📁 Files Explained

| File | What It Does | Difficulty |
|------|--------------|------------|
| `image_encryption.py` | The encryption logic (XOR, hashing, etc.) | ⭐⭐ Medium |
| `main.py` | Command-line interface for users | ⭐ Easy |
| `demo.py` | Demonstration script | ⭐ Easy |
| `setup.py` | Installation and testing | ⭐ Easy |
| `requirements.txt` | List of required libraries | ⭐ Easy |

**All files have TONS of comments to help you learn!**

## 💡 Learning Tips

1. **Start with `demo.py`** - Run it and see what happens
2. **Read `main.py`** - Simple user interface, easy to understand
3. **Study `image_encryption.py`** - The core logic with detailed comments
4. **Experiment!** - Try encrypting different images, changing the code, etc.

## 🎯 What You'll Learn

- How to work with files in Python
- Converting images to bytes and back
- Using hash functions (SHA256)
- XOR encryption (simple but educational!)
- Creating command-line interfaces
- Error handling
- Python classes and methods

## 🔍 Example Usage

### Encrypting an Image

```bash
$ python3 main.py

What do you want to do?
  1. Encrypt an image (lock it)
  2. Decrypt an image (unlock it)
  3. Quit

Enter your choice (1, 2, or 3): 1
Enter image filename (e.g., photo.jpg): photo.jpg
Enter password: my_secret_password

🎉 SUCCESS! Your image is now encrypted!
📁 Encrypted file saved as: photo_encrypted.png
```

### Decrypting an Image

```bash
What do you want to do?
  1. Encrypt an image (lock it)
  2. Decrypt an image (unlock it)
  3. Quit

Enter your choice (1, 2, or 3): 2
Enter image filename: photo_encrypted.png
Enter password: my_secret_password

🎉 SUCCESS! Your image has been decrypted!
📁 Decrypted file saved as: photo_decrypted.png
```

## ❓ Common Questions

**Q: Is this secure for real use?**  
A: No! This is for learning only. Real encryption needs more security layers.

**Q: What image formats are supported?**  
A: JPG, PNG, BMP, GIF, TIFF - most common formats!

**Q: What if I forget my password?**  
A: The file is unrecoverable! Keep your passwords safe.

**Q: Can I see the encrypted image?**  
A: You can open it, but it will look like random noise/garbage.

## 🛠️ Requirements

- Python 3.7 or higher
- Pillow library (for image handling)

That's it! No complex dependencies.

## 🎓 Next Steps

Once you understand this program:
1. Try modifying the code (maybe add different encryption methods?)
2. Read about AES encryption (real-world standard)
3. Learn about key derivation functions (PBKDF2, bcrypt)
4. Study cryptographic best practices

## 📝 License

This is a learning project - use it freely for educational purposes!

## 🤝 Contributing

This is a simple learning tool. Feel free to:
- Add more comments
- Improve error messages
- Create additional examples
- Share with other learners!

---

**Happy Learning! 🔐✨**

*Remember: The best way to learn is by reading the code and trying things out!*
