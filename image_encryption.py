"""
Super Simple Image Encryption
Just XOR encryption - easy to understand!
"""

import os
import hashlib
from PIL import Image
import io


class ImageEncryption:
    """Simple image encryption using XOR - perfect for learning!"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    def encrypt_image(self, image_path: str, password: str, output_path: str = None) -> str:
        """
        Encrypt image - super simple!
        1. Load image → convert to bytes
        2. Make key from password  
        3. XOR each byte with key
        4. Save encrypted file
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")
        
        # Check file type
        if not any(image_path.lower().endswith(ext) for ext in self.supported_formats):
            raise ValueError(f"Not a supported image format. Use: {self.supported_formats}")
        
        # Step 1: Load image and convert to bytes
        with Image.open(image_path) as img:
            # Make sure it's RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            image_data = img_bytes.getvalue()
        
        # Step 2: Make key from password (simple hash)
        key = hashlib.sha256(password.encode()).digest()
        
        # Step 3: XOR encrypt (repeat key if needed)
        encrypted = bytearray()
        for i, byte in enumerate(image_data):
            key_byte = key[i % len(key)]  # Reuse key if image is bigger
            encrypted.append(byte ^ key_byte)
        
        # Step 4: Save encrypted file
        if output_path is None:
            base = os.path.splitext(image_path)[0]
            output_path = f"{base}_encrypted.png"
        
        with open(output_path, 'wb') as f:
            f.write(bytes(encrypted))
        
        return output_path
    
    def decrypt_image(self, encrypted_path: str, password: str, output_path: str = None) -> str:
        """
        Decrypt image - same as encrypt (XOR is reversible!)
        1. Read encrypted file
        2. Make same key from password
        3. XOR again (decrypts!)
        4. Save as image
        """
        if not os.path.exists(encrypted_path):
            raise FileNotFoundError(f"File not found: {encrypted_path}")
        
        # Step 1: Read encrypted file
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Step 2: Make same key from password
        key = hashlib.sha256(password.encode()).digest()
        
        # Step 3: XOR decrypt (same as encrypt!)
        decrypted = bytearray()
        for i, byte in enumerate(encrypted_data):
            key_byte = key[i % len(key)]
            decrypted.append(byte ^ key_byte)
        
        # Step 4: Try to open as image
        try:
            img_bytes = io.BytesIO(bytes(decrypted))
            img = Image.open(img_bytes)
        except:
            raise ValueError("Decryption failed! Wrong password or file corrupted.")
        
        # Step 5: Save decrypted image
        if output_path is None:
            base = os.path.splitext(encrypted_path)[0]
            if base.endswith('_encrypted'):
                output_path = base.replace('_encrypted', '_decrypted.png')
            else:
                output_path = f"{base}_decrypted.png"
        
        img.save(output_path, format='PNG')
        return output_path
    
    def is_encrypted_file(self, file_path: str) -> bool:
        """Check if file looks encrypted - just check filename for now"""
        if not os.path.exists(file_path):
            return False
        
        # Simple check: has "_encrypted" in name or ends with .enc
        return '_encrypted' in file_path or file_path.endswith('.enc')
