"""
Style presets for image generation.
Contains predefined styles that modify prompts with prefixes/suffixes.
"""
from typing import Dict, List


# Style preset definitions
STYLE_PRESETS = {
    "None": {
        "prompt_prefix": "",
        "prompt_suffix": "",
        "extra_params": {},
        "description": "No style modifications"
    },
    "Realistic Photography": {
        "prompt_prefix": "a high-resolution photograph of ",
        "prompt_suffix": ", ultra realistic, 8k, detailed lighting, professional photography",
        "extra_params": {},
        "description": "Photorealistic style with high detail"
    },
    "Anime": {
        "prompt_prefix": "anime style illustration of ",
        "prompt_suffix": ", vibrant colors, clean line art, detailed, high quality anime",
        "extra_params": {},
        "description": "Japanese anime/manga style"
    },
    "3D Render": {
        "prompt_prefix": "3D render of ",
        "prompt_suffix": ", octane render, highly detailed, studio lighting, 8k, CGI",
        "extra_params": {},
        "description": "3D rendered, Pixar/CGI style"
    },
    "Oil Painting": {
        "prompt_prefix": "oil painting of ",
        "prompt_suffix": ", classical art style, brush strokes, artistic, masterpiece",
        "extra_params": {},
        "description": "Traditional oil painting style"
    },
    "Watercolor": {
        "prompt_prefix": "watercolor painting of ",
        "prompt_suffix": ", soft colors, artistic, flowing, delicate, traditional art",
        "extra_params": {},
        "description": "Watercolor painting style"
    },
    "Cyberpunk": {
        "prompt_prefix": "cyberpunk style ",
        "prompt_suffix": ", neon lights, futuristic, high tech, dystopian, vibrant colors",
        "extra_params": {},
        "description": "Futuristic cyberpunk aesthetic"
    },
    "Fantasy Art": {
        "prompt_prefix": "fantasy art illustration of ",
        "prompt_suffix": ", magical, ethereal, detailed, epic, artstation trending",
        "extra_params": {},
        "description": "Fantasy and magical themes"
    },
    "Pixel Art": {
        "prompt_prefix": "pixel art of ",
        "prompt_suffix": ", 8-bit, retro gaming style, detailed pixels, nostalgic",
        "extra_params": {},
        "description": "Retro pixel art style"
    },
    "Comic Book": {
        "prompt_prefix": "comic book style illustration of ",
        "prompt_suffix": ", bold lines, vibrant colors, superhero art, dynamic",
        "extra_params": {},
        "description": "Comic book illustration style"
    }
}


def list_styles() -> List[str]:
    """
    Get list of available style names.
    
    Returns:
        List[str]: List of style preset names
    """
    return list(STYLE_PRESETS.keys())


def get_style_info(style_name: str) -> Dict:
    """
    Get information about a specific style.
    
    Args:
        style_name: Name of the style
        
    Returns:
        Dict: Style configuration including prefix, suffix, params, and description
    """
    return STYLE_PRESETS.get(style_name, STYLE_PRESETS["None"])


def apply_style(base_prompt: str, style_name: str) -> str:
    """
    Apply a style preset to a base prompt.
    
    Args:
        base_prompt: The user's original prompt
        style_name: Name of the style to apply
        
    Returns:
        str: Modified prompt with style prefix and suffix
    """
    if not base_prompt or not base_prompt.strip():
        return base_prompt
    
    style = STYLE_PRESETS.get(style_name, STYLE_PRESETS["None"])
    
    # Combine prefix + prompt + suffix
    styled_prompt = f"{style['prompt_prefix']}{base_prompt}{style['prompt_suffix']}"
    
    return styled_prompt.strip()


def get_style_description(style_name: str) -> str:
    """
    Get the description of a style.
    
    Args:
        style_name: Name of the style
        
    Returns:
        str: Style description
    """
    style = STYLE_PRESETS.get(style_name, STYLE_PRESETS["None"])
    return style.get("description", "")
