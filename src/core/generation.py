"""
Core image generation functions for text-to-image and image-to-image.
"""
import torch
from PIL import Image
from typing import Optional, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    MIN_STEPS,
    MAX_STEPS,
    MIN_GUIDANCE_SCALE,
    MAX_GUIDANCE_SCALE,
    MIN_RESOLUTION,
    MAX_HEIGHT,
    MAX_WIDTH,
    DEFAULT_NUM_INFERENCE_STEPS,
    DEFAULT_GUIDANCE_SCALE,
    DEFAULT_STRENGTH
)
from core.styles import apply_style
from utils.system_utils import get_torch_generator, fix_seed
from utils.image_utils import to_rgb, validate_dimensions


def clamp_parameters(
    steps: int,
    guidance_scale: float,
    height: int,
    width: int,
    strength: Optional[float] = None
) -> Dict:
    """
    Validate and clamp generation parameters to safe ranges.
    
    Args:
        steps: Number of inference steps
        guidance_scale: Guidance scale value
        height: Image height
        width: Image width
        strength: Optional strength parameter for img2img
        
    Returns:
        Dict: Clamped parameters
    """
    clamped = {
        "steps": max(MIN_STEPS, min(int(steps), MAX_STEPS)),
        "guidance_scale": max(MIN_GUIDANCE_SCALE, min(float(guidance_scale), MAX_GUIDANCE_SCALE)),
        "height": height,
        "width": width
    }
    
    # Validate and fix dimensions
    clamped["width"], clamped["height"] = validate_dimensions(
        clamped["width"],
        clamped["height"],
        MIN_RESOLUTION,
        MAX_HEIGHT
    )
    
    if strength is not None:
        clamped["strength"] = max(0.0, min(float(strength), 1.0))
    
    return clamped


def generate_text2img(
    pipe,
    prompt: str,
    style: str = "None",
    num_inference_steps: int = DEFAULT_NUM_INFERENCE_STEPS,
    guidance_scale: float = DEFAULT_GUIDANCE_SCALE,
    height: int = 512,
    width: int = 512,
    seed: Optional[int] = None,
    device: str = "cuda"
) -> tuple[Image.Image, Dict]:
    """
    Generate an image from a text prompt.
    
    Args:
        pipe: StableDiffusionPipeline instance
        prompt: Text prompt describing the desired image
        style: Style preset name to apply
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale (how closely to follow prompt)
        height: Output image height
        width: Output image width
        seed: Random seed for reproducibility (None = random)
        device: Device string ("cuda" or "cpu")
        
    Returns:
        tuple: (Generated PIL Image, metadata dict)
    """
    # Validate prompt
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    # Apply style to prompt
    styled_prompt = apply_style(prompt.strip(), style)
    
    # Clamp parameters
    params = clamp_parameters(num_inference_steps, guidance_scale, height, width)
    
    # Fix seed
    fixed_seed = fix_seed(seed)
    generator = get_torch_generator(device, fixed_seed)
    
    # Generate metadata
    metadata = {
        "prompt": prompt,
        "styled_prompt": styled_prompt,
        "style": style,
        "steps": params["steps"],
        "guidance_scale": params["guidance_scale"],
        "height": params["height"],
        "width": params["width"],
        "seed": fixed_seed if fixed_seed is not None else "random",
        "type": "text2img"
    }
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {styled_prompt[:60]}...")
    print(f"   Size: {params['width']}x{params['height']}")
    print(f"   Steps: {params['steps']}, Guidance: {params['guidance_scale']}")
    print(f"   Seed: {metadata['seed']}")
    
    try:
        # Generate image
        result = pipe(
            prompt=styled_prompt,
            num_inference_steps=params["steps"],
            guidance_scale=params["guidance_scale"],
            height=params["height"],
            width=params["width"],
            generator=generator
        )
        
        image = result.images[0]
        print("✅ Image generated successfully!")
        
        return image, metadata
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        raise


def generate_img2img(
    pipe,
    prompt: str,
    init_image: Image.Image,
    strength: float = DEFAULT_STRENGTH,
    style: str = "None",
    num_inference_steps: int = DEFAULT_NUM_INFERENCE_STEPS,
    guidance_scale: float = DEFAULT_GUIDANCE_SCALE,
    seed: Optional[int] = None,
    device: str = "cuda"
) -> tuple[Image.Image, Dict]:
    """
    Transform an existing image using a text prompt.
    
    Args:
        pipe: StableDiffusionImg2ImgPipeline instance
        prompt: Text prompt describing desired transformation
        init_image: Input PIL Image to transform
        strength: How much to transform (0.0 = keep original, 1.0 = full transformation)
        style: Style preset name to apply
        num_inference_steps: Number of denoising steps
        guidance_scale: Guidance scale
        seed: Random seed for reproducibility (None = random)
        device: Device string ("cuda" or "cpu")
        
    Returns:
        tuple: (Transformed PIL Image, metadata dict)
    """
    # Validate inputs
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    if init_image is None:
        raise ValueError("Input image is required for image-to-image generation")
    
    # Apply style to prompt
    styled_prompt = apply_style(prompt.strip(), style)
    
    # Clamp parameters
    params = clamp_parameters(num_inference_steps, guidance_scale, 512, 512, strength)
    
    # Fix seed
    fixed_seed = fix_seed(seed)
    generator = get_torch_generator(device, fixed_seed)
    
    # Prepare image (convert to RGB)
    init_image = to_rgb(init_image)
    
    # Get image dimensions
    img_width, img_height = init_image.size
    img_width, img_height = validate_dimensions(img_width, img_height, MIN_RESOLUTION, MAX_HEIGHT)
    
    if (img_width, img_height) != init_image.size:
        from utils.image_utils import resize_to_dimensions
        init_image = resize_to_dimensions(init_image, img_width, img_height)
    
    # Generate metadata
    metadata = {
        "prompt": prompt,
        "styled_prompt": styled_prompt,
        "style": style,
        "strength": params["strength"],
        "steps": params["steps"],
        "guidance_scale": params["guidance_scale"],
        "height": img_height,
        "width": img_width,
        "seed": fixed_seed if fixed_seed is not None else "random",
        "type": "img2img"
    }
    
    print(f"🖼️  Transforming image...")
    print(f"   Prompt: {styled_prompt[:60]}...")
    print(f"   Size: {img_width}x{img_height}")
    print(f"   Strength: {params['strength']}")
    print(f"   Steps: {params['steps']}, Guidance: {params['guidance_scale']}")
    print(f"   Seed: {metadata['seed']}")
    
    try:
        # Generate image
        result = pipe(
            prompt=styled_prompt,
            image=init_image,
            strength=params["strength"],
            num_inference_steps=params["steps"],
            guidance_scale=params["guidance_scale"],
            generator=generator
        )
        
        image = result.images[0]
        print("✅ Image transformed successfully!")
        
        return image, metadata
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        raise
