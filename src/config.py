"""
Global configuration for the Stable Diffusion Image Generation App.
"""
import os
import torch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# MODE CONFIGURATION
# ============================================================
# Set to "local" to use local models (requires GPU for speed)
# Set to "api" to use Hugging Face API (free, no GPU needed)
# Set to "auto" to use API if HF_TOKEN exists, otherwise local
GENERATION_MODE = "api"  # Options: "local", "api", "auto"

# Model Configuration
SD_MODEL_ID = "runwayml/stable-diffusion-v1-5"  # For local mode
API_MODEL_ID = "black-forest-labs/FLUX.1-dev"  # For API mode

# Device Selection (for local mode)
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
APP_TITLE = "🎨 AI Image Generation - Stable Diffusion"
APP_DESCRIPTION = """
Generate images using Stable Diffusion 1.5.
Supports both local generation (GPU) and cloud API (free).
Choose between text-to-image and image-to-image generation with various style presets.
"""

# API Configuration
HF_API_TOKEN = os.getenv("HF_TOKEN", "")

# Safety Checker
ENABLE_SAFETY_CHECKER = False  # Set to True if you want content filtering


# Helper function to determine active mode
def get_active_mode() -> str:
    """
    Determine which generation mode to use.
    
    Returns:
        "local" or "api"
    """
    if GENERATION_MODE == "local":
        return "local"
    elif GENERATION_MODE == "api":
        return "api"
    elif GENERATION_MODE == "auto":
        # Use API if token is configured, otherwise local
        if HF_API_TOKEN and HF_API_TOKEN.startswith("hf_"):
            return "api"
        else:
            return "local"
    else:
        return "local"  # Default fallback
