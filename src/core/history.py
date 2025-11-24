"""
History and image saving functionality.
Manages saving generated images with metadata and retrieving recent generations.
"""
import os
import json
from datetime import datetime
from PIL import Image
from typing import Dict, List, Optional
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR


def generate_filename(metadata: Dict) -> str:
    """
    Generate a unique filename for a saved image.
    
    Args:
        metadata: Dictionary containing generation metadata
        
    Returns:
        str: Filename (without directory path)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    seed = metadata.get("seed", "random")
    style = metadata.get("style", "none").replace(" ", "_").lower()
    gen_type = metadata.get("type", "text2img")
    
    filename = f"{timestamp}_{gen_type}_{style}_{seed}.png"
    return filename


def save_image(
    image: Image.Image,
    metadata: Dict,
    output_dir: str = OUTPUT_DIR
) -> str:
    """
    Save a generated image with optional metadata sidecar.
    
    Args:
        image: PIL Image to save
        metadata: Dictionary containing generation parameters and info
        output_dir: Directory to save image to
        
    Returns:
        str: Full path to saved image
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    filename = generate_filename(metadata)
    filepath = os.path.join(output_dir, filename)
    
    # Save image
    image.save(filepath, "PNG")
    print(f"💾 Image saved: {filepath}")
    
    # Save metadata sidecar (JSON)
    metadata_filename = filename.replace(".png", ".json")
    metadata_filepath = os.path.join(output_dir, metadata_filename)
    
    # Add save timestamp to metadata
    metadata["saved_at"] = datetime.now().isoformat()
    metadata["filename"] = filename
    
    try:
        with open(metadata_filepath, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"📄 Metadata saved: {metadata_filepath}")
    except Exception as e:
        print(f"⚠️  Warning: Could not save metadata: {e}")
    
    return filepath


def load_metadata(image_path: str) -> Optional[Dict]:
    """
    Load metadata for an image if it exists.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Optional[Dict]: Metadata dictionary or None if not found
    """
    metadata_path = image_path.replace(".png", ".json")
    
    if not os.path.exists(metadata_path):
        return None
    
    try:
        with open(metadata_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load metadata from {metadata_path}: {e}")
        return None


def list_recent_images(output_dir: str = OUTPUT_DIR, limit: int = 10) -> List[str]:
    """
    List the most recent generated images.
    
    Args:
        output_dir: Directory to search for images
        limit: Maximum number of images to return
        
    Returns:
        List[str]: List of image file paths, sorted by modification time (newest first)
    """
    if not os.path.exists(output_dir):
        return []
    
    # Get all PNG files
    image_files = [
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.endswith(".png")
    ]
    
    # Sort by modification time (newest first)
    image_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Return limited list
    return image_files[:limit]


def get_image_count(output_dir: str = OUTPUT_DIR) -> int:
    """
    Get total count of generated images.
    
    Args:
        output_dir: Directory to count images in
        
    Returns:
        int: Number of PNG images found
    """
    if not os.path.exists(output_dir):
        return 0
    
    return len([f for f in os.listdir(output_dir) if f.endswith(".png")])


def clear_history(output_dir: str = OUTPUT_DIR, confirm: bool = False) -> int:
    """
    Delete all generated images and metadata (use with caution).
    
    Args:
        output_dir: Directory to clear
        confirm: Must be True to actually delete files
        
    Returns:
        int: Number of files deleted
    """
    if not confirm:
        print("⚠️  Clear operation not confirmed. Set confirm=True to delete files.")
        return 0
    
    if not os.path.exists(output_dir):
        return 0
    
    deleted = 0
    for filename in os.listdir(output_dir):
        if filename.endswith((".png", ".json")):
            filepath = os.path.join(output_dir, filename)
            try:
                os.remove(filepath)
                deleted += 1
            except Exception as e:
                print(f"⚠️  Could not delete {filepath}: {e}")
    
    print(f"🗑️  Deleted {deleted} files from {output_dir}")
    return deleted
