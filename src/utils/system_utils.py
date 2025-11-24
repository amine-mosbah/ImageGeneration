"""
System utility functions for device selection, seed handling, and directory management.
"""
import os
import random
import torch
from typing import Optional


def get_device() -> str:
    """
    Detect and return the appropriate device (cuda or cpu).
    
    Returns:
        str: "cuda" if GPU is available, otherwise "cpu"
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    return device


def fix_seed(seed: Optional[int]) -> Optional[int]:
    """
    Validate and fix seed value.
    
    Args:
        seed: The seed value to validate (can be None, -1, or a positive integer)
        
    Returns:
        Optional[int]: Valid seed or None for random generation
    """
    if seed is None or seed == -1 or seed == "":
        return None
    
    try:
        seed_int = int(seed)
        if seed_int < 0:
            return None
        return seed_int
    except (ValueError, TypeError):
        return None


def generate_random_seed() -> int:
    """
    Generate a random seed value.
    
    Returns:
        int: Random seed value
    """
    return random.randint(0, 2**32 - 1)


def ensure_directories(paths: list[str]) -> None:
    """
    Create directories if they don't exist.
    
    Args:
        paths: List of directory paths to create
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)
        print(f"Ensured directory exists: {path}")


def get_torch_generator(device: str, seed: Optional[int] = None) -> Optional[torch.Generator]:
    """
    Create a torch Generator with optional seed.
    
    Args:
        device: Device string ("cuda" or "cpu")
        seed: Optional seed value
        
    Returns:
        Optional[torch.Generator]: Generator object or None if no seed
    """
    if seed is None:
        return None
    
    generator = torch.Generator(device=device)
    generator.manual_seed(seed)
    return generator
