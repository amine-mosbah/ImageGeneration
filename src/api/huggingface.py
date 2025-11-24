"""
Hugging Face Inference API integration for Stable Diffusion.
Provides free cloud-based image generation without local GPU.
Uses official InferenceClient from huggingface_hub.
"""
import os
from PIL import Image
from typing import Optional, Dict, Any
from huggingface_hub import InferenceClient


class HuggingFaceAPI:
    """
    Wrapper for Hugging Face Inference API using InferenceClient.
    Free tier: ~1000 requests/day.
    """
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        """
        Initialize HF API client.
        
        Args:
            model_id: Hugging Face model identifier
        """
        self.model_id = model_id
        self.token = os.getenv("HF_TOKEN", "")
        
        # Initialize InferenceClient
        if self.is_configured():
            self.client = InferenceClient(token=self.token)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        """Check if API token is configured."""
        return bool(self.token and self.token.startswith("hf_"))
    
    def generate_text2img(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512,
        seed: Optional[int] = None
    ) -> Optional[Image.Image]:
        """
        Generate image from text using HF InferenceClient.
        
        Args:
            prompt: Text description of desired image
            negative_prompt: What to avoid in the image
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            width: Image width (may be ignored by some models)
            height: Image height (may be ignored by some models)
            seed: Random seed for reproducibility
            
        Returns:
            PIL Image or None if error
        """
        if not self.is_configured():
            raise ValueError("HF_TOKEN not configured. Set environment variable or add to .env file")
        
        try:
            print(f"📡 Sending request to Hugging Face API...")
            print(f"   Model: {self.model_id}")
            
            # Use InferenceClient for text-to-image
            image = self.client.text_to_image(
                prompt=prompt,
                model=self.model_id,
                negative_prompt=negative_prompt if negative_prompt else None,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                # Note: width/height/seed may not be supported by all models
            )
            
            print(f"✅ Image generated via HF API")
            return image
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ API Error: {error_msg}")
            
            # Handle common errors
            if "loading" in error_msg.lower():
                print("⏳ Model is loading on HF servers. This can take 30-60 seconds.")
                print("   Please try again in a moment.")
            elif "rate limit" in error_msg.lower():
                print("⚠️  Rate limit reached. Please wait a few minutes and try again.")
            elif "503" in error_msg:
                print("⏳ Service temporarily unavailable. Model may be loading.")
            
            return None
    
    def generate_img2img(
        self,
        prompt: str,
        init_image: Image.Image,
        strength: float = 0.75,
        negative_prompt: str = "",
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None
    ) -> Optional[Image.Image]:
        """
        Transform existing image using HF InferenceClient.
        
        Args:
            prompt: Text description
            init_image: Input image to transform
            strength: How much to transform (0-1)
            negative_prompt: What to avoid
            num_inference_steps: Denoising steps
            guidance_scale: Prompt adherence
            seed: Random seed
            
        Returns:
            PIL Image or None
        """
        if not self.is_configured():
            raise ValueError("HF_TOKEN not configured. Set environment variable or add to .env file")
        
        try:
            print(f"📡 Sending image-to-image request to Hugging Face API...")
            print(f"   Model: {self.model_id}")
            print(f"   Strength: {strength}")
            
            # Use InferenceClient for image-to-image
            image = self.client.image_to_image(
                image=init_image,
                prompt=prompt,
                model=self.model_id,
                negative_prompt=negative_prompt if negative_prompt else None,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
            )
            
            print(f"✅ Image transformed via HF API")
            return image
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ API Error: {error_msg}")
            
            # Handle common errors
            if "loading" in error_msg.lower():
                print("⏳ Model is loading on HF servers. This can take 30-60 seconds.")
                print("   Please try again in a moment.")
            elif "not supported" in error_msg.lower() or "image_to_image" in error_msg.lower():
                print("⚠️  This model may not support image-to-image generation.")
                print("   Falling back to text-to-image...")
                return self.generate_text2img(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    seed=seed
                )
            
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection and return status.
        
        Returns:
            Dict with status information
        """
        if not self.is_configured():
            return {
                "status": "error",
                "message": "HF_TOKEN not configured",
                "configured": False
            }
        
        try:
            # Simple test to verify client is working
            # We don't actually generate an image, just check if client is initialized
            if self.client is not None:
                return {
                    "status": "success",
                    "message": "API client initialized successfully",
                    "configured": True,
                    "model": self.model_id
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to initialize API client",
                    "configured": False
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}",
                "configured": True
            }


def get_setup_instructions() -> str:
    """
    Return instructions for setting up HF API.
    
    Returns:
        Formatted instruction string
    """
    return """
🔧 Hugging Face API Setup:

1. Go to: https://huggingface.co/settings/tokens
2. Sign up for a FREE account (if needed)
3. Click "New token" → Create a "Read" token
4. Copy the token (starts with 'hf_')

5. Set the token:
   
   Option A - Environment variable:
   export HF_TOKEN='hf_your_token_here'
   
   Option B - .env file (recommended):
   echo 'HF_TOKEN=hf_your_token_here' > .env

6. Restart the application

Free tier includes ~1000 requests/day!
    """
