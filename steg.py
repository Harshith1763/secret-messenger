# from PIL import Image
# import numpy as np

# def encode_image(img_path, message, password):
#     """Hide message in image using LSB steganography"""
#     try:
#         img = Image.open(img_path)
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
        
#         # Convert message to binary with password protection
#         message += "%%%"  # End marker
#         binary_msg = ''.join([format(ord(c), '08b') for c in (password + message)])
        
#         pixels = np.array(img)
#         if len(binary_msg) > pixels.size:
#             raise ValueError("Message too long for image")
        
#         # LSB encoding
#         idx = 0
#         for row in pixels:
#             for pixel in row:
#                 for i in range(3):  # R,G,B channels
#                     if idx < len(binary_msg):
#                         pixel[i] = pixel[i] & ~1 | int(binary_msg[idx])
#                         idx += 1
        
#         return Image.fromarray(pixels)
#     except Exception as e:
#         raise Exception(f"Encoding failed: {str(e)}")

# def decode_image(img_path, password):
#     """Extract hidden message from image"""
#     try:
#         img = Image.open(img_path)
#         pixels = np.array(img)
        
#         binary_data = []
#         for row in pixels:
#             for pixel in row:
#                 for value in pixel[:3]:  # Read R,G,B
#                     binary_data.append(str(value & 1))
        
#         # Convert binary to string
#         all_bytes = [''.join(binary_data[i:i+8]) for i in range(0, len(binary_data), 8)]
#         decoded = ''.join([chr(int(byte, 2)) for byte in all_bytes])
        
#         # Verify password
#         if not decoded.startswith(password):
#             raise ValueError("Incorrect password or no hidden message")
        
#         return decoded[len(password):decoded.find('%%%')]  # Remove password and end marker
#     except Exception as e:
#         raise Exception(f"Decoding failed: {str(e)}")




from PIL import Image
import numpy as np
from io import BytesIO

def encode_image(img, message, password):
    """Hide message in image with password protection"""
    try:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        message += "%%%"
        binary_msg = ''.join([format(ord(c), '08b') for c in (password + message)])
        
        pixels = np.array(img)
        if len(binary_msg) > pixels.size:
            raise ValueError("Message too long for image")
        
        # Convert to int32 to prevent overflow
        pixels = pixels.astype(np.int32)
        
        idx = 0
        for row in pixels:
            for pixel in row:
                for i in range(3):  # R,G,B channels
                    if idx < len(binary_msg):
                        # Safely modify pixel value
                        new_val = (pixel[i] & ~1) | int(binary_msg[idx])
                        pixel[i] = np.clip(new_val, 0, 255)
                        idx += 1
        
        # Convert back to uint8 before saving
        return Image.fromarray(pixels.astype(np.uint8))
    
    except Exception as e:
        raise ValueError(f"Encoding error: {str(e)}")

def decode_image(img, password):
    """Extract message from image with password"""
    pixels = np.array(img)
    binary = ''.join([str(pixel[i] & 1) for row in pixels for pixel in row for i in range(3)])
    
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if byte:
            chars.append(chr(int(byte, 2)))
    decoded = ''.join(chars)
    
    if not decoded.startswith(password):
        raise ValueError("Incorrect password")
    
    return decoded[len(password):decoded.find('%%%')]