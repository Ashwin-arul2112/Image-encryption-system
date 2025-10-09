import os
from PIL import Image
import numpy as np

def load_image(image_path: str):
    """
    Loads an image from the given path, converts it to RGB for consistent
    encryption, and returns the image data as a NumPy array and its original mode.
    
    Args:
        image_path: The path to the image file.
    
    Returns:
        A tuple containing the image data as a NumPy array and the original image mode.
    """
    try:
        with Image.open(image_path) as img:
            original_mode = img.mode
            img_rgb = img.convert('RGB')
            return np.array(img_rgb), original_mode
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None, None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None

def save_image(image_array: np.ndarray, output_path: str, original_mode: str):
    """
    Saves a NumPy array as an image file, converting it back to its original mode.
    
    Args:
        image_array: The NumPy array containing the image data.
        output_path: The path to save the image file.
        original_mode: The original color mode of the image (e.g., 'RGB', 'L').
    """
    try:
        # Check if the array needs to be reshaped for color or grayscale
        if image_array.ndim == 3:
            img = Image.fromarray(image_array.astype(np.uint8), 'RGB')
        else:
            img = Image.fromarray(image_array.astype(np.uint8), 'L')
        
        # Convert back to the original mode before saving
        final_img = img.convert(original_mode)
        final_img.save(output_path)
    except Exception as e:
        print(f"Error saving image: {e}")
