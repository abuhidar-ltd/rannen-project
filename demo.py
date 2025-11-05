#!/usr/bin/env python3
"""
===============================================
DEMO SCRIPT - SEE THE ENCRYPTION IN ACTION!
===============================================

This script demonstrates how the image encryption works.
It will:
1. Create a simple test image
2. Encrypt it with a password
3. Decrypt it back
4. Show you the results

Run this to see the magic happen!
"""

# Import what we need
from image_encryption import ImageEncryption
from PIL import Image, ImageDraw
import os


def create_test_image():
    """
    Create a simple test image to encrypt.
    We'll make a colorful square with some text!
    """
    print("\n" + "="*60)
    print("STEP 1: Creating a test image")
    print("="*60)
    
    # Create a new image: 400x300 pixels, light blue background
    # RGB means Red-Green-Blue color mode
    img = Image.new('RGB', (400, 300), color='lightblue')
    
    # Create a drawing object so we can draw on the image
    draw = ImageDraw.Draw(img)
    
    # Draw a red rectangle
    # Format: [x1, y1, x2, y2] where (x1,y1) is top-left, (x2,y2) is bottom-right
    draw.rectangle([50, 50, 150, 150], fill='red', outline='darkred', width=3)
    
    # Draw a green circle (ellipse)
    draw.ellipse([200, 50, 300, 150], fill='green', outline='darkgreen', width=3)
    
    # Draw a yellow triangle (polygon = many-sided shape)
    # We give it three points to make a triangle
    triangle_points = [(75, 200), (125, 250), (25, 250)]
    draw.polygon(triangle_points, fill='yellow', outline='orange', width=3)
    
    # Save the image
    filename = "test_image.png"
    img.save(filename)
    
    print(f"✅ Created test image: {filename}")
    print(f"   Size: 400x300 pixels")
    print(f"   Contains: red square, green circle, yellow triangle")
    
    return filename


def demo_encryption():
    """
    Main demo function.
    Shows the complete encrypt → decrypt process.
    """
    
    # Print welcome message
    print("\n" + "🔐 "*30)
    print("IMAGE ENCRYPTION DEMO")
    print("🔐 "*30)
    print("\nThis demo will show you how image encryption works!")
    print("Watch carefully and learn! 😊\n")
    
    # ========== STEP 1: CREATE TEST IMAGE ==========
    image_file = create_test_image()
    
    # ========== STEP 2: SET UP ENCRYPTION ==========
    print("\n" + "="*60)
    print("STEP 2: Setting up encryption")
    print("="*60)
    
    # Create an ImageEncryption object
    # Think of this as getting out your encryption toolbox
    encryptor = ImageEncryption()
    print("✅ Encryption tool ready!")
    
    # Choose a password for the demo
    password = "my_secret_password_123"
    print(f"✅ Using password: '{password}'")
    print("   (In real use, keep your password secret!)")
    
    # ========== STEP 3: ENCRYPT THE IMAGE ==========
    print("\n" + "="*60)
    print("STEP 3: Encrypting the image")
    print("="*60)
    print("Now we'll scramble the image using the password...")
    print()
    
    try:
        # Call the encrypt function
        # This does all the magic we explained in image_encryption.py!
        encrypted_file = encryptor.encrypt_image(image_file, password)
        
        print("\n✨ ENCRYPTION SUCCESSFUL! ✨")
        print(f"Original file: {image_file}")
        print(f"Encrypted file: {encrypted_file}")
        
        # Show file sizes
        original_size = os.path.getsize(image_file)
        encrypted_size = os.path.getsize(encrypted_file)
        print(f"\nFile sizes:")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Encrypted: {encrypted_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Error during encryption: {e}")
        return
    
    # ========== STEP 4: DECRYPT THE IMAGE ==========
    print("\n" + "="*60)
    print("STEP 4: Decrypting the image")
    print("="*60)
    print("Now we'll unscramble it using the same password...")
    print()
    
    try:
        # Call the decrypt function
        # This reverses the encryption using XOR!
        decrypted_file = encryptor.decrypt_image(encrypted_file, password)
        
        print("\n✨ DECRYPTION SUCCESSFUL! ✨")
        print(f"Encrypted file: {encrypted_file}")
        print(f"Decrypted file: {decrypted_file}")
        
        # Compare file sizes
        decrypted_size = os.path.getsize(decrypted_file)
        print(f"\nFile sizes:")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Decrypted: {decrypted_size:,} bytes")
        
        if original_size == decrypted_size:
            print("  ✅ Same size - good sign!")
        
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        return
    
    # ========== STEP 5: TEST WRONG PASSWORD ==========
    print("\n" + "="*60)
    print("STEP 5: Testing with WRONG password")
    print("="*60)
    print("Let's see what happens with the wrong password...")
    print()
    
    wrong_password = "wrong_password"
    print(f"Trying to decrypt with: '{wrong_password}'")
    print()
    
    try:
        # This should fail!
        encryptor.decrypt_image(encrypted_file, wrong_password)
        print("❌ Unexpected: decryption worked with wrong password!")
        
    except ValueError as e:
        # This is expected!
        print("✅ Good! Decryption failed as expected:")
        print(f"   {e}")
        print("   This proves the password protection works!")
    
    # ========== SUMMARY ==========
    print("\n" + "🎓 "*30)
    print("WHAT YOU LEARNED:")
    print("🎓 "*30)
    print("""
1. Images can be converted to bytes (raw numbers)
2. Passwords are converted to encryption keys using SHA256
3. XOR encryption scrambles the data:
   - original XOR key = encrypted
   - encrypted XOR key = original (magic!)
4. Wrong password = garbage data that won't open as an image
5. The encrypted file is about the same size as the original

FILES CREATED:
- test_image.png          (original image)
- test_image_encrypted.png (scrambled - can't view normally)
- test_image_decrypted.png (recovered image - should match original!)

Try opening these files to see the difference!
    """)
    
    # Ask if user wants to clean up
    print("="*60)
    cleanup = input("Delete test files? (y/n): ").strip().lower()
    
    if cleanup in ['y', 'yes']:
        # Delete all test files
        test_files = [
            "test_image.png",
            "test_image_encrypted.png",
            "test_image_decrypted.png"
        ]
        
        print("\n🧹 Cleaning up...")
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"   Deleted: {file}")
        print("✅ Cleanup complete!")
    else:
        print("\n📁 Test files kept for you to examine!")
    
    print("\n" + "🎉 "*30)
    print("DEMO COMPLETE!")
    print("🎉 "*30)
    print("\nNow you can try the real program: python3 main.py")
    print()


# Run the demo when script is executed
if __name__ == "__main__":
    demo_encryption()
