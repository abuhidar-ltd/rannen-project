#!/usr/bin/env python3
"""
===============================================
IMAGE ENCRYPTION - COMMAND LINE INTERFACE
===============================================

A super simple command-line program to encrypt and decrypt images!

HOW TO USE:
1. Run: python3 main.py
2. Choose what you want to do (encrypt or decrypt)
3. Enter the image filename
4. Enter a password
5. Done!

This is a LEARNING project - great for understanding:
- How to get user input
- How files work
- Basic encryption concepts (XOR)
"""

# Import our encryption class
from image_encryption import ImageEncryption
import os  # For checking if files exist


def print_header():
    """
    Print a nice welcome message.
    This makes the program look professional!
    """
    # ASCII art borders make it look cool
    print("\n" + "="*50)
    print("🔐  IMAGE ENCRYPTION TOOL")
    print("="*50)
    print("Encrypt and decrypt your images with a password!")
    print("="*50 + "\n")


def get_choice():
    """
    Ask user what they want to do.
    
    Returns:
    - "1" for encrypt
    - "2" for decrypt
    - "3" for quit
    """
    print("What do you want to do?")
    print("  1. Encrypt an image (lock it)")
    print("  2. Decrypt an image (unlock it)")
    print("  3. Quit")
    print()
    
    # Keep asking until we get a valid choice
    while True:
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        # Check if the choice is valid
        if choice in ["1", "2", "3"]:
            return choice
        else:
            # Invalid choice! Ask again
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


def get_image_path():
    """
    Ask user for the image file path.
    Keep asking until they give us a file that exists!
    
    Returns:
    - Path to the image file
    """
    while True:
        # Get the filename from user
        path = input("Enter image filename (e.g., photo.jpg): ").strip()
        
        # Check if the file exists
        if os.path.exists(path):
            # File exists! We're good!
            return path
        else:
            # File doesn't exist - tell user and ask again
            print(f"❌ File '{path}' not found! Please check the filename and try again.")
            print(f"   (Make sure the file is in this folder: {os.getcwd()})")
            print()


def get_password():
    """
    Ask user for a password.
    
    Note: This is very simple - the password will be visible as they type.
    Real programs use 'getpass' module to hide the password.
    
    Returns:
    - The password as a string
    """
    while True:
        password = input("Enter password: ").strip()
        
        # Make sure password is not empty
        if password:
            return password
        else:
            print("❌ Password cannot be empty! Try again.")


def encrypt_mode():
    """
    ENCRYPT MODE
    This function handles encrypting an image.
    """
    print("\n" + "-"*50)
    print("🔒 ENCRYPT MODE")
    print("-"*50)
    print("This will scramble your image so nobody can view it")
    print("without the password!")
    print()
    
    # Step 1: Get the image file
    image_path = get_image_path()
    
    # Step 2: Get the password
    print("\nChoose a strong password (you'll need it to decrypt later!)")
    password = get_password()
    
    # Step 3: Encrypt!
    print("\n" + "="*50)
    try:
        # Create an encryptor object
        encryptor = ImageEncryption()
        
        # Call the encrypt method
        encrypted_path = encryptor.encrypt_image(image_path, password)
        
        # Success!
        print("="*50)
        print(f"🎉 SUCCESS! Your image is now encrypted!")
        print(f"📁 Encrypted file saved as: {encrypted_path}")
        print(f"🔑 Remember your password: you'll need it to decrypt!")
        print("="*50)
        
    except Exception as e:
        # Something went wrong!
        print("="*50)
        print(f"❌ ERROR: {str(e)}")
        print("="*50)


def decrypt_mode():
    """
    DECRYPT MODE
    This function handles decrypting an image.
    """
    print("\n" + "-"*50)
    print("🔓 DECRYPT MODE")
    print("-"*50)
    print("This will unscramble an encrypted image using your password.")
    print()
    
    # Step 1: Get the encrypted file
    print("Select the encrypted file (usually ends with '_encrypted.png')")
    encrypted_path = get_image_path()
    
    # Step 2: Get the password
    print("\nEnter the SAME password you used to encrypt:")
    password = get_password()
    
    # Step 3: Decrypt!
    print("\n" + "="*50)
    try:
        # Create an encryptor object
        encryptor = ImageEncryption()
        
        # Call the decrypt method
        decrypted_path = encryptor.decrypt_image(encrypted_path, password)
        
        # Success!
        print("="*50)
        print(f"🎉 SUCCESS! Your image has been decrypted!")
        print(f"📁 Decrypted file saved as: {decrypted_path}")
        print(f"🖼️  You can now open and view it normally!")
        print("="*50)
        
    except ValueError as e:
        # Probably wrong password!
        print("="*50)
        print(f"❌ {str(e)}")
        print("💡 Tip: Make sure you're using the exact same password!")
        print("="*50)
        
    except Exception as e:
        # Some other error
        print("="*50)
        print(f"❌ ERROR: {str(e)}")
        print("="*50)


def main():
    """
    MAIN FUNCTION
    This is where the program starts!
    
    It's a simple loop:
    1. Show menu
    2. Get user's choice
    3. Do what they asked
    4. Repeat until they quit
    """
    
    # Show welcome message
    print_header()
    
    # Main program loop
    # This keeps running until user chooses to quit
    while True:
        # Get user's choice
        choice = get_choice()
        
        if choice == "1":
            # User wants to encrypt
            encrypt_mode()
            
        elif choice == "2":
            # User wants to decrypt
            decrypt_mode()
            
        elif choice == "3":
            # User wants to quit
            print("\n👋 Thanks for using Image Encryption Tool!")
            print("   Stay secure! 🔐\n")
            break  # Exit the loop (ends the program)
        
        # Add some space before showing menu again
        print("\n")


# This is a Python convention:
# Code here only runs if you execute this file directly
# (not if you import it as a module)
if __name__ == "__main__":
    # Start the program!
    main()

