"""
===============================================
SUPER SIMPLE IMAGE ENCRYPTION - LEARNING VERSION
===============================================

This is a beginner-friendly image encryption program!

WHAT DOES IT DO?
- Takes an image file
- Uses a password to scramble it (encrypt)
- Can unscramble it back (decrypt) with the same password

HOW IT WORKS:
- Uses XOR encryption (super simple bitwise operation)
- XOR means: if you do it twice, you get back the original!
  Example: 5 XOR 3 XOR 3 = 5 (the second XOR undoes the first)

IMPORTANT: This is for LEARNING ONLY!
Real-world encryption is much more complex and secure.
"""

# IMPORTS - These are libraries we need
import os          # For file operations (checking if files exist, etc.)
import hashlib     # For converting password to a encryption key
from PIL import Image  # For opening and saving images
import io          # For working with bytes (raw data)


class ImageEncryption:
    """
    This class handles encrypting and decrypting images.
    Think of it like a toolbox with encrypt/decrypt tools inside!
    """
    
    def __init__(self):
        """
        This runs when you create a new ImageEncryption object.
        It just sets up what image types we support.
        """
        # List of image file extensions we can work with
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    def encrypt_image(self, image_path: str, password: str, output_path: str = None) -> str:
        """
        ENCRYPT AN IMAGE
        
        What this does:
        1. Load the image and convert it to raw bytes (0s and 1s)
        2. Convert the password into an encryption key
        3. Scramble the image bytes using XOR with the key
        4. Save the scrambled data to a file
        
        Parameters:
        - image_path: Path to the image you want to encrypt
        - password: Your secret password (keep it safe!)
        - output_path: Where to save encrypted file (optional, auto-generated if not provided)
        
        Returns:
        - The path where encrypted file was saved
        """
        
        # ========== STEP 0: CHECK IF FILE EXISTS ==========
        if not os.path.exists(image_path):
            # The file doesn't exist! Stop and tell the user.
            raise FileNotFoundError(f"File not found: {image_path}")
        
        # Check if the file is a supported image format
        # .lower() makes it lowercase so .PNG and .png both work
        # any() checks if at least one format matches
        if not any(image_path.lower().endswith(ext) for ext in self.supported_formats):
            raise ValueError(f"Not a supported image format. Use: {self.supported_formats}")
        
        # ========== STEP 1: LOAD IMAGE AND CONVERT TO BYTES ==========
        print(f"📸 Opening image: {image_path}")
        
        # 'with' automatically closes the file when done
        with Image.open(image_path) as img:
            
            # Make sure the image is in RGB color mode
            # RGB = Red, Green, Blue (standard for most images)
            if img.mode != 'RGB':
                print(f"   Converting from {img.mode} to RGB mode...")
                img = img.convert('RGB')
            
            # Now we convert the image to raw bytes
            # Think of this as turning a picture into a bunch of numbers
            img_bytes = io.BytesIO()  # Create a temporary storage in memory
            img.save(img_bytes, format='PNG')  # Save image as PNG into that storage
            image_data = img_bytes.getvalue()  # Get all the bytes as raw data
            
        print(f"   Image size: {len(image_data)} bytes")
        
        # ========== STEP 2: CONVERT PASSWORD TO ENCRYPTION KEY ==========
        # We can't use the password directly - we need to convert it to numbers
        # SHA256 is a "hash function" - it converts any text to a 256-bit number
        # .encode() converts text to bytes
        # .digest() gives us the final hash as bytes
        
        print(f"🔑 Creating encryption key from password...")
        key = hashlib.sha256(password.encode()).digest()
        print(f"   Key size: {len(key)} bytes (256 bits)")
        
        # ========== STEP 3: XOR ENCRYPTION ==========
        # This is the actual encryption!
        # XOR (^) is a bitwise operation that flips bits
        # image_byte XOR key_byte = encrypted_byte
        # encrypted_byte XOR key_byte = original_byte (magic!)
        
        print(f"🔒 Encrypting...")
        encrypted = bytearray()  # Empty list to store encrypted bytes
        
        # Loop through every byte in the image
        for i, byte in enumerate(image_data):
            # Get the corresponding key byte
            # % is modulo - if image is bigger than key, we wrap around and reuse key
            # Example: if key is 32 bytes and image is 100 bytes,
            #          byte 33 uses key[1], byte 34 uses key[2], etc.
            key_byte = key[i % len(key)]
            
            # XOR the image byte with the key byte (this is the encryption!)
            # ^ is the XOR operator in Python
            encrypted_byte = byte ^ key_byte
            encrypted.append(encrypted_byte)
        
        # ========== STEP 4: SAVE ENCRYPTED FILE ==========
        # Figure out where to save the encrypted file
        if output_path is None:
            # No output path provided, so create one automatically
            # Example: "photo.jpg" becomes "photo_encrypted.png"
            base = os.path.splitext(image_path)[0]  # Remove extension
            output_path = f"{base}_encrypted.png"
        
        print(f"💾 Saving encrypted file: {output_path}")
        
        # 'wb' means write in binary mode (for raw bytes, not text)
        with open(output_path, 'wb') as f:
            f.write(bytes(encrypted))  # Write all encrypted bytes to file
        
        print(f"✅ Encryption complete!")
        return output_path  # Return where we saved it
    
    def decrypt_image(self, encrypted_path: str, password: str, output_path: str = None) -> str:
        """
        DECRYPT AN IMAGE
        
        What this does:
        1. Read the encrypted file (scrambled bytes)
        2. Convert password to the same encryption key
        3. XOR the encrypted bytes with the key (this unscrambles them!)
        4. Try to open the result as an image
        5. Save the recovered image
        
        Parameters:
        - encrypted_path: Path to the encrypted file
        - password: The same password used to encrypt (must be exact!)
        - output_path: Where to save decrypted image (optional)
        
        Returns:
        - The path where decrypted image was saved
        """
        
        # ========== STEP 0: CHECK IF FILE EXISTS ==========
        if not os.path.exists(encrypted_path):
            raise FileNotFoundError(f"File not found: {encrypted_path}")
        
        # ========== STEP 1: READ ENCRYPTED FILE ==========
        print(f"📂 Reading encrypted file: {encrypted_path}")
        
        # 'rb' means read in binary mode (for raw bytes)
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()  # Read all the scrambled bytes
        
        print(f"   Encrypted file size: {len(encrypted_data)} bytes")
        
        # ========== STEP 2: CREATE THE SAME KEY FROM PASSWORD ==========
        # This MUST produce the exact same key as when we encrypted!
        # That's why we use the same SHA256 hash function
        print(f"🔑 Creating decryption key from password...")
        key = hashlib.sha256(password.encode()).digest()
        
        # ========== STEP 3: XOR DECRYPT ==========
        # Here's the cool part: XOR is its own inverse!
        # If we encrypted with: result = original XOR key
        # Then we decrypt with: original = result XOR key
        # It's the EXACT SAME operation!
        
        print(f"🔓 Decrypting...")
        decrypted = bytearray()  # Empty list for decrypted bytes
        
        # Loop through every encrypted byte
        for i, byte in enumerate(encrypted_data):
            # Get the same key byte we used for encryption
            key_byte = key[i % len(key)]
            
            # XOR again - this reverses the encryption!
            decrypted_byte = byte ^ key_byte
            decrypted.append(decrypted_byte)
        
        # ========== STEP 4: VERIFY IT'S A VALID IMAGE ==========
        # Try to open the decrypted bytes as an image
        # If the password was wrong, this will fail!
        print(f"🖼️  Verifying decrypted data is a valid image...")
        
        try:
            img_bytes = io.BytesIO(bytes(decrypted))  # Put bytes in memory
            img = Image.open(img_bytes)  # Try to open as image
            print(f"   ✅ Valid image! Size: {img.size}, Mode: {img.mode}")
        except Exception as e:
            # If we get here, decryption failed
            # Most likely reason: wrong password!
            raise ValueError("❌ Decryption failed! Wrong password or corrupted file.")
        
        # ========== STEP 5: SAVE DECRYPTED IMAGE ==========
        # Figure out where to save
        if output_path is None:
            base = os.path.splitext(encrypted_path)[0]  # Remove extension
            # If filename has "_encrypted", replace it with "_decrypted"
            if base.endswith('_encrypted'):
                output_path = base.replace('_encrypted', '_decrypted.png')
            else:
                output_path = f"{base}_decrypted.png"
        
        print(f"💾 Saving decrypted image: {output_path}")
        img.save(output_path, format='PNG')
        
        print(f"✅ Decryption complete!")
        return output_path
