#!/usr/bin/env python3
"""
Installation and Setup Script for Image Encryption App

This script helps set up the environment and test the application.
"""

import subprocess
import sys
import os


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("Please use Python 3.7 or higher.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible.")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    dependencies = [
        "cryptography>=3.4.8",
        "Pillow>=8.0.0"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error installing {dep}: {e}")
            return False
    
    return True


def test_imports():
    """Test if all required modules can be imported."""
    print("\n🧪 Testing imports...")
    
    try:
        import cryptography
        print("✅ cryptography imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import cryptography: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Pillow: {e}")
        return False
    
    try:
        import tkinter
        print("✅ tkinter imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import tkinter: {e}")
        return False
    
    return True


def test_core_functionality():
    """Test the core encryption functionality."""
    print("\n🔐 Testing core functionality...")
    
    try:
        from image_encryption import ImageEncryption
        
        # Create encryptor
        encryptor = ImageEncryption()
        print("✅ ImageEncryption class created successfully")
        
        # Test key generation
        key, salt = encryptor.generate_key_from_password("test_password")
        print("✅ Key generation works")
        
        print("✅ Core functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Image Encryption App - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed.")
        print("Please install the dependencies manually:")
        print("pip install cryptography Pillow")
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed.")
        return False
    
    # Test core functionality
    if not test_core_functionality():
        print("\n❌ Core functionality test failed.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    
    print("\n📋 Next steps:")
    print("1. Run the GUI application: python3 gui_app.py")
    print("2. Run the demo script: python3 demo.py")
    print("3. Read the README.md for detailed usage instructions")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
