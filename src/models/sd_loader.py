"""
Stable Diffusion pipeline loader.
Handles loading and configuration of text-to-image and image-to-image pipelines.
"""
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from typing import Dict, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    SD_MODEL_ID,
    DEVICE,
    TORCH_DTYPE,
    MODEL_CACHE_DIR,
    ENABLE_SAFETY_CHECKER
)


def get_device() -> str:
    """
    Check if CUDA is available and return appropriate device.
    
    Returns:
        str: "cuda" if available, else "cpu"
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device}")
    if device == "cuda":
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
    return device


def load_text2img_pipeline(
    model_id: str = SD_MODEL_ID,
    device: Optional[str] = None,
    torch_dtype: Optional[torch.dtype] = None
) -> StableDiffusionPipeline:
    """
    Load Stable Diffusion text-to-image pipeline.
    
    Args:
        model_id: HuggingFace model identifier
        device: Device to load model on ("cuda" or "cpu")
        torch_dtype: Torch dtype (float16 for GPU, float32 for CPU)
        
    Returns:
        StableDiffusionPipeline: Loaded pipeline
    """
    if device is None:
        device = DEVICE
    if torch_dtype is None:
        torch_dtype = TORCH_DTYPE
    
    print(f"📥 Loading text-to-image pipeline: {model_id}")
    
    # Load pipeline
    try:
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            cache_dir=MODEL_CACHE_DIR,
            safety_checker=None if not ENABLE_SAFETY_CHECKER else "default",
            requires_safety_checker=ENABLE_SAFETY_CHECKER
        )
        
        # Move to device
        pipeline = pipeline.to(device)
        
        # Enable memory optimizations for CUDA
        if device == "cuda":
            # Enable attention slicing to reduce memory usage
            pipeline.enable_attention_slicing()
            
            # Optional: Enable VAE slicing for even lower memory
            # pipeline.enable_vae_slicing()
            
            # Optional: Enable sequential CPU offload (for low VRAM)
            # pipeline.enable_sequential_cpu_offload()
        
        print(f"✅ Text-to-image pipeline loaded successfully")
        return pipeline
        
    except Exception as e:
        print(f"❌ Error loading text-to-image pipeline: {e}")
        raise


def load_img2img_pipeline(
    model_id: str = SD_MODEL_ID,
    device: Optional[str] = None,
    torch_dtype: Optional[torch.dtype] = None
) -> StableDiffusionImg2ImgPipeline:
    """
    Load Stable Diffusion image-to-image pipeline.
    
    Args:
        model_id: HuggingFace model identifier
        device: Device to load model on ("cuda" or "cpu")
        torch_dtype: Torch dtype (float16 for GPU, float32 for CPU)
        
    Returns:
        StableDiffusionImg2ImgPipeline: Loaded pipeline
    """
    if device is None:
        device = DEVICE
    if torch_dtype is None:
        torch_dtype = TORCH_DTYPE
    
    print(f"📥 Loading image-to-image pipeline: {model_id}")
    
    # Load pipeline
    try:
        pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            cache_dir=MODEL_CACHE_DIR,
            safety_checker=None if not ENABLE_SAFETY_CHECKER else "default",
            requires_safety_checker=ENABLE_SAFETY_CHECKER
        )
        
        # Move to device
        pipeline = pipeline.to(device)
        
        # Enable memory optimizations for CUDA
        if device == "cuda":
            pipeline.enable_attention_slicing()
        
        print(f"✅ Image-to-image pipeline loaded successfully")
        return pipeline
        
    except Exception as e:
        print(f"❌ Error loading image-to-image pipeline: {e}")
        raise


def init_pipelines(
    model_id: str = SD_MODEL_ID,
    device: Optional[str] = None,
    torch_dtype: Optional[torch.dtype] = None
) -> Dict[str, any]:
    """
    Initialize both text-to-image and image-to-image pipelines.
    
    Args:
        model_id: HuggingFace model identifier
        device: Device to load models on
        torch_dtype: Torch dtype
        
    Returns:
        Dict containing both pipelines:
        {
            "text2img": StableDiffusionPipeline,
            "img2img": StableDiffusionImg2ImgPipeline
        }
    """
    print("🚀 Initializing Stable Diffusion pipelines...")
    print(f"Model: {model_id}")
    
    if device is None:
        device = get_device()
    if torch_dtype is None:
        torch_dtype = TORCH_DTYPE
    
    # Load both pipelines
    text2img_pipe = load_text2img_pipeline(model_id, device, torch_dtype)
    img2img_pipe = load_img2img_pipeline(model_id, device, torch_dtype)
    
    pipelines = {
        "text2img": text2img_pipe,
        "img2img": img2img_pipe,
        "device": device
    }
    
    print("🎉 All pipelines loaded and ready!")
    return pipelines
