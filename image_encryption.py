"""
Image Encryption Module

This module provides functionality to encrypt and decrypt images using AES encryption.
It handles image data conversion, encryption/decryption, and file I/O operations.
"""

import os
import base64
import random
import struct
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image
import io


class ImageEncryption:
    """
    A class to handle image encryption and decryption operations.
    
    This class uses AES encryption with Fernet (symmetric encryption) to encrypt
    image data. It converts images to bytes, encrypts them, and saves the result.
    """
    
    def __init__(self):
        """Initialize the ImageEncryption class."""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> bytes:
        """
        Generate an encryption key from a password using PBKDF2.
        
        Args:
            password (str): The password to derive the key from
            salt (bytes, optional): Salt for key derivation. If None, generates a random salt.
            
        Returns:
            bytes: The derived encryption key
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_image(self, image_path: str, password: str, output_path: str = None) -> tuple[str, bytes]:
        """
        Encrypt an image file and create a decoy image with random RGB values.
        
        Args:
            image_path (str): Path to the image file to encrypt
            password (str): Password for encryption
            output_path (str, optional): Path for the encrypted file. If None, uses original path with .png extension
            
        Returns:
            tuple: (output_file_path, salt) - The path to the encrypted file and the salt used
        """
        try:
            # Validate input file
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Check file extension
            file_ext = os.path.splitext(image_path)[1].lower()
            if file_ext not in self.supported_formats:
                raise ValueError(f"Unsupported image format: {file_ext}")
            
            # Load and convert image to bytes
            with Image.open(image_path) as img:
                # Get original dimensions for decoy image
                original_width, original_height = img.size
                
                # Convert to RGB if necessary (for JPEG compatibility)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Save image to bytes buffer
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')  # Use PNG to preserve quality
                image_data = img_buffer.getvalue()
            
            # Generate encryption key and salt
            key, salt = self.generate_key_from_password(password)
            
            # Encrypt the image data
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(image_data)
            
            # Create decoy image with random RGB values but embed encrypted data
            decoy_path = self._create_decoy_image_with_data(
                original_width, original_height, salt, encrypted_data
            )
            
            # Determine output path
            if output_path is None:
                base_name = os.path.splitext(image_path)[0]
                output_path = f"{base_name}_encrypted.png"
            
            # Copy decoy image to output path
            import shutil
            shutil.copy2(decoy_path, output_path)
            os.remove(decoy_path)  # Clean up temp file
            
            return output_path, salt
            
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def _create_decoy_image_with_data(self, width: int, height: int, salt: bytes, encrypted_data: bytes) -> str:
        """
        Create a decoy image with random RGB values that contains the encrypted data.
        
        Args:
            width (int): Width of the decoy image
            height (int): Height of the decoy image
            salt (bytes): Salt used for encryption
            encrypted_data (bytes): Encrypted image data
            
        Returns:
            str: Path to the temporary decoy image file
        """
        # Combine salt and encrypted data
        data_to_embed = salt + encrypted_data
        data_length = len(data_to_embed)
        
        # Each pixel can hold 3 bytes (RGB), so calculate how many pixels we need
        pixels_for_data = (data_length + 2) // 3  # Round up
        total_pixels = width * height
        
        # Ensure we have enough pixels for the data plus length header
        if pixels_for_data + 2 > total_pixels:
            # If image is too small, we need to expand it
            # Calculate new minimal dimensions
            needed_pixels = pixels_for_data + 2
            new_width = width
            new_height = height
            while new_width * new_height < needed_pixels:
                new_width = max(new_width + 1, int((needed_pixels / new_height) + 0.5))
                new_height = max(new_height + 1, int((needed_pixels / new_width) + 0.5))
            width, height = new_width, new_height
            total_pixels = width * height
        
        # Create pixel data
        pixels = []
        
        # First 2 pixels: store data length (6 bytes: 4 for length + 2 padding)
        data_length_bytes = struct.pack('>I', data_length)  # 4-byte big-endian integer
        for i in range(2):
            start_idx = i * 3
            if start_idx + 2 < len(data_length_bytes):
                r, g, b = data_length_bytes[start_idx:start_idx+3]
            else:
                remaining = data_length_bytes[start_idx:]
                r = remaining[0] if len(remaining) > 0 else 0
                g = remaining[1] if len(remaining) > 1 else 0
                b = remaining[2] if len(remaining) > 2 else 0
            pixels.append((r, g, b))
        
        # Embed the actual data
        for i in range(0, len(data_to_embed), 3):
            if i + 2 < len(data_to_embed):
                r, g, b = data_to_embed[i], data_to_embed[i+1], data_to_embed[i+2]
            else:
                # Pad with zeros if needed
                remaining = data_to_embed[i:]
                r = remaining[0] if len(remaining) > 0 else 0
                g = remaining[1] if len(remaining) > 1 else 0
                b = remaining[2] if len(remaining) > 2 else 0
            pixels.append((r, g, b))
        
        # Fill remaining pixels with random RGB values
        random.seed(42)  # Use fixed seed for consistent but random-looking noise
        while len(pixels) < total_pixels:
            pixels.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # Create the decoy image
        decoy_img = Image.new('RGB', (width, height))
        decoy_img.putdata(pixels[:total_pixels])
        
        # Save to temporary file
        import tempfile
        temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(temp_fd)  # Close the file descriptor
        decoy_img.save(temp_path, format='PNG')
        
        return temp_path
    
    def decrypt_image(self, encrypted_path: str, password: str, output_path: str = None) -> str:
        """
        Decrypt an encrypted image file that has encrypted data embedded in pixels.
        
        Args:
            encrypted_path (str): Path to the encrypted file (PNG image with embedded data)
            password (str): Password for decryption
            output_path (str, optional): Path for the decrypted image
            
        Returns:
            str: The path to the decrypted image file
        """
        try:
            # Validate input file
            if not os.path.exists(encrypted_path):
                raise FileNotFoundError(f"Encrypted file not found: {encrypted_path}")
            
            # Extract embedded data from the image
            salt, encrypted_data = self._extract_data_from_image(encrypted_path)
            
            # Generate decryption key using the same salt
            key, _ = self.generate_key_from_password(password, salt)
            
            # Decrypt the data
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Convert bytes back to image
            img_buffer = io.BytesIO(decrypted_data)
            img = Image.open(img_buffer)
            
            # Determine output path
            if output_path is None:
                base_name = os.path.splitext(encrypted_path)[0]
                if base_name.endswith('_encrypted'):
                    output_path = base_name.replace('_encrypted', '_decrypted.png')
                else:
                    output_path = base_name + '_decrypted.png'
            
            # Save decrypted image
            img.save(output_path, format='PNG')
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def _extract_data_from_image(self, image_path: str) -> tuple[bytes, bytes]:
        """
        Extract embedded salt and encrypted data from a decoy image.
        
        Args:
            image_path (str): Path to the image with embedded data
            
        Returns:
            tuple: (salt, encrypted_data) - The extracted salt and encrypted data
        """
        try:
            # Load the image
            with Image.open(image_path) as img:
                img = img.convert('RGB')
                pixels = list(img.getdata())
            
            # Read first 2 pixels to get data length
            length_pixels = pixels[:2]
            length_bytes = bytearray()
            
            for r, g, b in length_pixels:
                length_bytes.extend([r, g, b])
            
            # Extract the 4-byte length (first 4 bytes of the 6 bytes)
            data_length = struct.unpack('>I', bytes(length_bytes[:4]))[0]
            
            # Calculate how many pixels we need to read for the data
            pixels_needed = (data_length + 2) // 3  # +2 for rounding up division
            
            # Extract data from pixels (skip first 2 pixels which contain length)
            data_pixels = pixels[2:2 + pixels_needed]
            data_bytes = bytearray()
            
            for r, g, b in data_pixels:
                data_bytes.extend([r, g, b])
            
            # Truncate to exact length
            embedded_data = bytes(data_bytes[:data_length])
            
            # Split into salt (first 16 bytes) and encrypted data
            salt = embedded_data[:16]
            encrypted_data = embedded_data[16:]
            
            return salt, encrypted_data
            
        except Exception as e:
            raise Exception(f"Failed to extract data from image: {str(e)}")
    
    def is_encrypted_file(self, file_path: str) -> bool:
        """
        Check if a file appears to be an encrypted image file.
        
        Args:
            file_path (str): Path to the file to check
            
        Returns:
            bool: True if the file appears to be encrypted, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            # Check if file has .enc extension (old format)
            if file_path.endswith('.enc'):
                return True
            
            # Check if it's a PNG file that might contain embedded encrypted data
            if not file_path.lower().endswith('.png'):
                return False
            
            # Try to load as an image and check if it contains embedded data
            try:
                with Image.open(file_path) as img:
                    img = img.convert('RGB')
                    pixels = list(img.getdata())
                
                # Check if we have at least 2 pixels for the length header
                if len(pixels) < 2:
                    return False
                
                # Try to extract the data length from first 2 pixels
                length_pixels = pixels[:2]
                length_bytes = bytearray()
                
                for r, g, b in length_pixels:
                    length_bytes.extend([r, g, b])
                
                # Check if the first 4 bytes look like a reasonable data length
                if len(length_bytes) >= 4:
                    try:
                        data_length = struct.unpack('>I', bytes(length_bytes[:4]))[0]
                        # Reasonable check: data length should be at least 16 (salt) and not too large
                        if 16 <= data_length <= 100 * 1024 * 1024:  # 16 bytes to 100MB
                            # Additional check: see if we can extract salt+data
                            pixels_needed = (data_length + 2) // 3
                            if len(pixels) >= 2 + pixels_needed:
                                return True
                    except (struct.error, ValueError):
                        pass
                
            except Exception:
                # If we can't process as an image, it's not our encrypted format
                pass
            
            return False
            
        except Exception:
            return False


# Example usage and testing functions
def create_test_image():
    """Create a simple test image for demonstration purposes."""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a simple test image
    img = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "This is a test image for encryption!"
    draw.text((50, 150), text, fill='darkblue', font=font)
    
    # Add some shapes
    draw.rectangle([50, 50, 150, 100], outline='red', width=3)
    draw.ellipse([250, 50, 350, 100], outline='green', width=3)
    
    return img


if __name__ == "__main__":
    # Example usage
    encryptor = ImageEncryption()
    
    # Create a test image
    test_img = create_test_image()
    test_img.save("test_image.png")
    
    # Test encryption
    password = "my_secret_password"
    encrypted_path, salt = encryptor.encrypt_image("test_image.png", password)
    print(f"Image encrypted and saved to: {encrypted_path}")
    
    # Test decryption
    decrypted_path = encryptor.decrypt_image(encrypted_path, password)
    print(f"Image decrypted and saved to: {decrypted_path}")
    
    print("Encryption/Decryption test completed successfully!")
