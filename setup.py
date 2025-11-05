#!/usr/bin/env python3
"""
===============================================
SETUP SCRIPT - GET READY TO USE THE PROGRAM
===============================================

This script helps you set up everything you need.

It will:
1. Check if you have Python 3.7 or newer
2. Install required libraries (PIL/Pillow for images)
3. Test that everything works

Just run: python3 setup.py
"""

import subprocess  # For running pip install commands
import sys         # For checking Python version
import os          # For file operations


def check_python_version():
    """
    Check if Python version is new enough.
    We need Python 3.7 or higher.
    
    Why? Because we use f-strings and other modern features.
    """
    print("\n" + "="*60)
    print("STEP 1: Checking Python version")
    print("="*60)
    
    # sys.version_info gives us the Python version
    # It has: major (like 3), minor (like 12), micro (like 0)
    version = sys.version_info
    
    print(f"Your Python version: {version.major}.{version.minor}.{version.micro}")
    
    # Check if version is too old
    # We need at least Python 3.7
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ PROBLEM: Your Python is too old!")
        print("   This program needs Python 3.7 or newer.")
        print("   Please upgrade Python and try again.")
        return False
    
    print("✅ Python version is compatible!")
    return True


def install_dependencies():
    """
    Install the required Python libraries.
    
    We need:
    - Pillow (PIL): For working with images
    
    Note: We removed cryptography since we're using simple XOR,
          and tkinter since we removed the GUI.
    """
    print("\n" + "="*60)
    print("STEP 2: Installing required libraries")
    print("="*60)
    
    # List of libraries we need
    # Format: "library_name>=minimum_version"
    dependencies = [
        "Pillow>=8.0.0"  # PIL for images
    ]
    
    print("Libraries to install:")
    for dep in dependencies:
        print(f"  - {dep}")
    print()
    
    # Try to install each one
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            
            # Run: pip install <dependency>
            # subprocess.check_call() runs a command and waits for it to finish
            # sys.executable is the path to python (e.g., /usr/bin/python3)
            subprocess.check_call([
                sys.executable,  # python3
                "-m",            # run as module
                "pip",           # the pip module
                "install",       # install command
                dep,             # what to install
                "--user"         # install for this user only (safer)
            ])
            
            print(f"✅ {dep} installed successfully!")
            print()
            
        except subprocess.CalledProcessError as e:
            # Installation failed!
            print(f"❌ Failed to install {dep}")
            print(f"   Error: {e}")
            print("\nTroubleshooting:")
            print("  1. Try running: pip install --user Pillow")
            print("  2. Or try: python3 -m pip install --user Pillow")
            print("  3. If that fails, check your internet connection")
            return False
            
        except Exception as e:
            # Some other unexpected error
            print(f"❌ Unexpected error: {e}")
            return False
    
    return True


def test_imports():
    """
    Test if all required libraries can be imported.
    This makes sure everything installed correctly!
    """
    print("\n" + "="*60)
    print("STEP 3: Testing if libraries work")
    print("="*60)
    
    # Test 1: Try to import PIL (Pillow)
    try:
        from PIL import Image
        print("✅ Pillow (PIL) works - can handle images!")
    except ImportError as e:
        print(f"❌ Failed to import Pillow: {e}")
        print("   Try installing it manually: pip install --user Pillow")
        return False
    
    return True


def test_encryption():
    """
    Test if our encryption code actually works.
    We'll create a tiny test image and try to encrypt it.
    """
    print("\n" + "="*60)
    print("STEP 4: Testing encryption functionality")
    print("="*60)
    
    try:
        # Import our encryption class
        from image_encryption import ImageEncryption
        print("✅ ImageEncryption class loaded!")
        
        # Create a tiny test image (10x10 pixels, white)
        from PIL import Image
        test_img = Image.new('RGB', (10, 10), color='white')
        test_img.save('_test_tiny.png')
        print("✅ Created test image: _test_tiny.png")
        
        # Try to encrypt it
        encryptor = ImageEncryption()
        encrypted = encryptor.encrypt_image('_test_tiny.png', 'test123')
        print(f"✅ Encryption works! Created: {encrypted}")
        
        # Try to decrypt it
        decrypted = encryptor.decrypt_image(encrypted, 'test123')
        print(f"✅ Decryption works! Created: {decrypted}")
        
        # Clean up test files
        os.remove('_test_tiny.png')
        os.remove(encrypted)
        os.remove(decrypted)
        print("✅ Cleaned up test files")
        
        print("\n🎉 All tests passed! Everything works!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
        # Try to clean up if test files exist
        for f in ['_test_tiny.png', '_test_tiny_encrypted.png', '_test_tiny_decrypted.png']:
            if os.path.exists(f):
                os.remove(f)
        
        return False


def main():
    """
    Main setup function.
    Runs all the setup steps in order.
    """
    
    # Print welcome message
    print("\n" + "🔧 "*30)
    print("IMAGE ENCRYPTION - SETUP")
    print("🔧 "*30)
    print("\nThis will set up everything you need to run the program.")
    print("It will take just a minute!")
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python version too old")
        return False
    
    # Step 2: Install libraries
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install libraries")
        return False
    
    # Step 3: Test imports
    if not test_imports():
        print("\n❌ Setup failed: Libraries not working")
        return False
    
    # Step 4: Test encryption
    if not test_encryption():
        print("\n❌ Setup failed: Encryption not working")
        return False
    
    # All done!
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE! 🎉")
    print("="*60)
    print("\nYou're all set! Here's what you can do now:\n")
    print("1. Run the demo to see how it works:")
    print("   python3 demo.py")
    print()
    print("2. Use the main program to encrypt your own images:")
    print("   python3 main.py")
    print()
    print("3. Learn by reading the code - it's full of comments!")
    print("   - image_encryption.py: The encryption logic")
    print("   - main.py: The user interface")
    print("   - demo.py: Example usage")
    print("\nHave fun learning about encryption! 🔐")
    print()
    
    return True


# Run setup when script is executed
if __name__ == "__main__":
    success = main()
    # Exit with code 0 if success, 1 if failed
    sys.exit(0 if success else 1)
