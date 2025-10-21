#!/usr/bin/env python3
"""
Demo Script for Image Encryption Application

This script demonstrates the functionality of the image encryption tool
by creating test images and performing encryption/decryption operations.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from image_encryption import ImageEncryption


def create_sample_images():
    """Create sample images for testing."""
    print("Creating sample images...")
    
    # Create a colorful test image
    img1 = Image.new('RGB', (400, 300), color='lightblue')
    draw1 = ImageDraw.Draw(img1)
    
    # Add text
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    draw1.text((50, 50), "Sample Image 1", fill='darkblue', font=font)
    draw1.text((50, 80), "This is a test image for encryption", fill='darkblue', font=font)
    
    # Add shapes
    draw1.rectangle([50, 120, 150, 170], fill='red', outline='darkred', width=2)
    draw1.ellipse([200, 120, 300, 170], fill='green', outline='darkgreen', width=2)
    draw1.polygon([(350, 120), (375, 170), (325, 170)], fill='yellow', outline='orange', width=2)
    
    img1.save("sample_image_1.png")
    print("✓ Created sample_image_1.png")
    
    # Create a gradient test image
    img2 = Image.new('RGB', (300, 200), color='white')
    draw2 = ImageDraw.Draw(img2)
    
    # Create a gradient effect
    for y in range(200):
        color_value = int(255 * (y / 200))
        draw2.line([(0, y), (300, y)], fill=(color_value, 100, 255 - color_value))
    
    draw2.text((50, 50), "Gradient Test", fill='white', font=font)
    draw2.text((50, 80), "Colorful gradient image", fill='white', font=font)
    
    img2.save("sample_image_2.png")
    print("✓ Created sample_image_2.png")
    
    # Create a simple logo-style image
    img3 = Image.new('RGBA', (200, 200), color=(0, 0, 0, 0))  # Transparent background
    draw3 = ImageDraw.Draw(img3)
    
    # Draw a simple logo
    draw3.ellipse([20, 20, 180, 180], fill='blue', outline='darkblue', width=3)
    draw3.ellipse([50, 50, 150, 150], fill='white', outline='lightblue', width=2)
    draw3.text((70, 90), "LOGO", fill='blue', font=font)
    
    img3.save("sample_logo.png")
    print("✓ Created sample_logo.png")
    
    return ["sample_image_1.png", "sample_image_2.png", "sample_logo.png"]


def test_encryption_decryption():
    """Test the encryption and decryption functionality."""
    print("\n" + "="*50)
    print("TESTING ENCRYPTION/DECRYPTION")
    print("="*50)
    
    # Create encryptor instance
    encryptor = ImageEncryption()
    
    # Test password
    test_password = "demo_password_123"
    
    # Create sample images
    sample_files = create_sample_images()
    
    print(f"\nTesting with password: '{test_password}'")
    
    for i, image_file in enumerate(sample_files, 1):
        print(f"\n--- Test {i}: {image_file} ---")
        
        try:
            # Test encryption
            print("Encrypting...")
            encrypted_path, salt = encryptor.encrypt_image(image_file, test_password)
            print(f"✓ Encrypted: {encrypted_path}")
            
            # Verify encrypted file exists
            if os.path.exists(encrypted_path):
                original_size = os.path.getsize(image_file)
                encrypted_size = os.path.getsize(encrypted_path)
                print(f"  Original size: {original_size:,} bytes")
                print(f"  Encrypted size: {encrypted_size:,} bytes")
                print(f"  Size increase: {((encrypted_size - original_size) / original_size * 100):.1f}%")
            
            # Test decryption
            print("Decrypting...")
            decrypted_path = encryptor.decrypt_image(encrypted_path, test_password)
            print(f"✓ Decrypted: {decrypted_path}")
            
            # Verify decrypted file exists
            if os.path.exists(decrypted_path):
                decrypted_size = os.path.getsize(decrypted_path)
                print(f"  Decrypted size: {decrypted_size:,} bytes")
            
            # Test file detection
            is_encrypted = encryptor.is_encrypted_file(encrypted_path)
            print(f"  File detection: {'✓ Correctly identified as encrypted' if is_encrypted else '✗ Failed to identify as encrypted'}")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    print(f"\n{'='*50}")
    print("TESTING COMPLETED")
    print("="*50)


def test_error_handling():
    """Test error handling scenarios."""
    print("\n" + "="*50)
    print("TESTING ERROR HANDLING")
    print("="*50)
    
    encryptor = ImageEncryption()
    
    # Test cases
    test_cases = [
        {
            "name": "Non-existent file",
            "file": "non_existent_file.jpg",
            "password": "test",
            "expected_error": "FileNotFoundError"
        },
        {
            "name": "Wrong password",
            "file": "sample_image_1.enc",
            "password": "wrong_password",
            "expected_error": "Decryption failed"
        },
        {
            "name": "Invalid file format",
            "file": "requirements.txt",  # Text file, not image
            "password": "test",
            "expected_error": "Unsupported image format"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Error Test {i}: {test_case['name']} ---")
        
        try:
            if test_case['name'] == "Wrong password":
                # First create an encrypted file
                if os.path.exists("sample_image_1.png"):
                    encryptor.encrypt_image("sample_image_1.png", "correct_password")
            
            # Try the operation
            if test_case['file'].endswith('.enc'):
                encryptor.decrypt_image(test_case['file'], test_case['password'])
            else:
                encryptor.encrypt_image(test_case['file'], test_case['password'])
            
            print(f"✗ Expected error but operation succeeded")
            
        except Exception as e:
            print(f"✓ Caught expected error: {str(e)}")
    
    print(f"\n{'='*50}")
    print("ERROR HANDLING TEST COMPLETED")
    print("="*50)


def cleanup_files():
    """Clean up test files."""
    print("\nCleaning up test files...")
    
    files_to_remove = [
        "sample_image_1.png",
        "sample_image_2.png", 
        "sample_logo.png",
        "sample_image_1.enc",
        "sample_image_2.enc",
        "sample_logo.enc",
        "sample_image_1_decrypted.png",
        "sample_image_2_decrypted.png",
        "sample_logo_decrypted.png"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"✓ Removed {file}")


def main():
    """Main demo function."""
    print("Image Encryption Application - Demo Script")
    print("="*50)
    
    try:
        # Test basic functionality
        test_encryption_decryption()
        
        # Test error handling
        test_error_handling()
        
        # Ask user if they want to clean up
        print(f"\n{'='*50}")
        response = input("Demo completed! Clean up test files? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            cleanup_files()
        else:
            print("Test files preserved for manual inspection.")
        
        print("\nDemo completed successfully!")
        print("\nTo run the GUI application, use:")
        print("python gui_app.py")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        cleanup_files()
    except Exception as e:
        print(f"\nDemo failed with error: {str(e)}")
        cleanup_files()


if __name__ == "__main__":
    main()
