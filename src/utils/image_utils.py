"""
Image utility functions for loading, resizing, and converting images.
"""
from PIL import Image
from typing import Tuple, Optional
import io


def load_image_from_bytes(bytes_data: bytes) -> Image.Image:
    """
    Load a PIL Image from bytes data.
    
    Args:
        bytes_data: Image data in bytes
        
    Returns:
        PIL.Image.Image: Loaded image
    """
    return Image.open(io.BytesIO(bytes_data))


def load_image_from_path(path: str) -> Image.Image:
    """
    Load a PIL Image from a file path.
    
    Args:
        path: Path to the image file
        
    Returns:
        PIL.Image.Image: Loaded image
    """
    return Image.open(path)


def to_rgb(image: Image.Image) -> Image.Image:
    """
    Convert image to RGB mode (Stable Diffusion expects RGB).
    
    Args:
        image: Input image
        
    Returns:
        PIL.Image.Image: Image in RGB mode
    """
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


def resize_image_to_max(
    image: Image.Image, 
    max_height: int, 
    max_width: int
) -> Image.Image:
    """
    Resize image if it exceeds maximum dimensions while maintaining aspect ratio.
    
    Args:
        image: Input image
        max_height: Maximum allowed height
        max_width: Maximum allowed width
        
    Returns:
        PIL.Image.Image: Resized image
    """
    width, height = image.size
    
    if width <= max_width and height <= max_height:
        return image
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Ensure dimensions are multiples of 8 (SD requirement)
    new_width = (new_width // 8) * 8
    new_height = (new_height // 8) * 8
    
    return image.resize((new_width, new_height), Image.LANCZOS)


def resize_to_dimensions(
    image: Image.Image,
    width: int,
    height: int
) -> Image.Image:
    """
    Resize image to specific dimensions.
    
    Args:
        image: Input image
        width: Target width (should be multiple of 8)
        height: Target height (should be multiple of 8)
        
    Returns:
        PIL.Image.Image: Resized image
    """
    # Ensure dimensions are multiples of 8
    width = (width // 8) * 8
    height = (height // 8) * 8
    
    return image.resize((width, height), Image.LANCZOS)


def validate_dimensions(width: int, height: int, min_size: int = 256, max_size: int = 768) -> Tuple[int, int]:
    """
    Validate and adjust dimensions to be within bounds and multiples of 8.
    
    Args:
        width: Requested width
        height: Requested height
        min_size: Minimum dimension size
        max_size: Maximum dimension size
        
    Returns:
        Tuple[int, int]: Valid (width, height)
    """
    # Clamp to min/max
    width = max(min_size, min(width, max_size))
    height = max(min_size, min(height, max_size))
    
    # Round to nearest multiple of 8
    width = (width // 8) * 8
    height = (height // 8) * 8
    
    return width, height
