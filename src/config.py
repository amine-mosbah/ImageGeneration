"""
Global configuration for the Stable Diffusion Image Generation App.
"""
import os
import torch

# Model Configuration
SD_MODEL_ID = "runwayml/stable-diffusion-v1-5"

# Device Selection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# Generation Defaults
DEFAULT_NUM_INFERENCE_STEPS = 30
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_HEIGHT = 512
DEFAULT_WIDTH = 512
DEFAULT_STRENGTH = 0.75  # For img2img

# Safety Limits
MIN_STEPS = 1
MAX_STEPS = 100
MIN_GUIDANCE_SCALE = 1.0
MAX_GUIDANCE_SCALE = 20.0
MIN_RESOLUTION = 256
MAX_HEIGHT = 768
MAX_WIDTH = 768

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "generated")
LOG_DIR = os.path.join(BASE_DIR, "outputs", "logs")
MODEL_CACHE_DIR = os.path.join(BASE_DIR, "models_cache")

# UI Configuration
APP_TITLE = "🎨 Local Image Generation - Stable Diffusion"
APP_DESCRIPTION = """
Generate images locally using Stable Diffusion 1.5.
Choose between text-to-image and image-to-image generation with various style presets.
"""

# Safety Checker
ENABLE_SAFETY_CHECKER = False  # Set to True if you want content filtering
