"""
Gradio UI application for Stable Diffusion image generation.
Provides text-to-image and image-to-image interfaces.
"""
import gradio as gr
from PIL import Image
from typing import Dict, Optional, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    APP_TITLE,
    APP_DESCRIPTION,
    DEFAULT_NUM_INFERENCE_STEPS,
    DEFAULT_GUIDANCE_SCALE,
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    DEFAULT_STRENGTH,
    MIN_STEPS,
    MAX_STEPS,
    MIN_GUIDANCE_SCALE,
    MAX_GUIDANCE_SCALE,
    MIN_RESOLUTION,
    MAX_HEIGHT,
    MAX_WIDTH,
    OUTPUT_DIR
)
from core.styles import list_styles, get_style_description
from core.generation import generate_text2img, generate_img2img
from core.history import save_image, list_recent_images, get_image_count
from utils.system_utils import generate_random_seed


def create_text2img_interface(pipelines: Dict) -> gr.Interface:
    """
    Create the text-to-image generation interface.
    
    Args:
        pipelines: Dictionary containing loaded SD pipelines
        
    Returns:
        gr.Interface: Gradio interface for text-to-image
    """
    pipe = pipelines["text2img"]
    device = pipelines["device"]
    
    def generate_wrapper(
        prompt: str,
        style: str,
        steps: int,
        guidance: float,
        height: int,
        width: int,
        seed: int,
        use_random_seed: bool
    ) -> Tuple[Image.Image, str, list]:
        """Wrapper function for text-to-image generation with UI feedback."""
        try:
            # Handle random seed
            if use_random_seed:
                seed = generate_random_seed()
            
            # Generate image
            image, metadata = generate_text2img(
                pipe=pipe,
                prompt=prompt,
                style=style,
                num_inference_steps=steps,
                guidance_scale=guidance,
                height=height,
                width=width,
                seed=seed,
                device=device
            )
            
            # Save image
            filepath = save_image(image, metadata, OUTPUT_DIR)
            
            # Prepare info text
            info = f"""
**Generation Complete!**
- **Prompt:** {prompt}
- **Style:** {style}
- **Size:** {metadata['width']}x{metadata['height']}
- **Steps:** {metadata['steps']}
- **Guidance Scale:** {metadata['guidance_scale']}
- **Seed:** {metadata['seed']}
- **Saved to:** {filepath}
            """
            
            # Get recent images for gallery
            recent_images = list_recent_images(OUTPUT_DIR, limit=6)
            
            return image, info.strip(), recent_images
            
        except Exception as e:
            error_msg = f"❌ **Error:** {str(e)}"
            return None, error_msg, []
    
    return generate_wrapper


def create_img2img_interface(pipelines: Dict) -> gr.Interface:
    """
    Create the image-to-image transformation interface.
    
    Args:
        pipelines: Dictionary containing loaded SD pipelines
        
    Returns:
        gr.Interface: Gradio interface for image-to-image
    """
    pipe = pipelines["img2img"]
    device = pipelines["device"]
    
    def transform_wrapper(
        input_image: Image.Image,
        prompt: str,
        style: str,
        strength: float,
        steps: int,
        guidance: float,
        seed: int,
        use_random_seed: bool
    ) -> Tuple[Optional[Image.Image], str]:
        """Wrapper function for image-to-image transformation with UI feedback."""
        try:
            # Validate input
            if input_image is None:
                return None, "❌ **Error:** Please upload an input image"
            
            # Handle random seed
            if use_random_seed:
                seed = generate_random_seed()
            
            # Transform image
            image, metadata = generate_img2img(
                pipe=pipe,
                prompt=prompt,
                init_image=input_image,
                strength=strength,
                style=style,
                num_inference_steps=steps,
                guidance_scale=guidance,
                seed=seed,
                device=device
            )
            
            # Save image
            filepath = save_image(image, metadata, OUTPUT_DIR)
            
            # Prepare info text
            info = f"""
**Transformation Complete!**
- **Prompt:** {prompt}
- **Style:** {style}
- **Strength:** {metadata['strength']}
- **Steps:** {metadata['steps']}
- **Guidance Scale:** {metadata['guidance_scale']}
- **Seed:** {metadata['seed']}
- **Saved to:** {filepath}
            """
            
            return image, info.strip()
            
        except Exception as e:
            error_msg = f"❌ **Error:** {str(e)}"
            return None, error_msg
    
    return transform_wrapper


def create_app(pipelines: Dict) -> gr.Blocks:
    """
    Create the complete Gradio application with all tabs.
    
    Args:
        pipelines: Dictionary containing loaded SD pipelines
        
    Returns:
        gr.Blocks: Complete Gradio application
    """
    # Get available styles
    styles = list_styles()
    
    # Create generation functions
    text2img_fn = create_text2img_interface(pipelines)
    img2img_fn = create_img2img_interface(pipelines)
    
    # Build the UI
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft()) as app:
        gr.Markdown(f"# {APP_TITLE}")
        gr.Markdown(APP_DESCRIPTION)
        
        # Show image count
        image_count = get_image_count(OUTPUT_DIR)
        gr.Markdown(f"*Generated images: {image_count}*")
        
        with gr.Tabs():
            # ========== TEXT TO IMAGE TAB ==========
            with gr.Tab("📝 Text → Image"):
                gr.Markdown("Generate images from text prompts")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        txt_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="Describe the image you want to generate...",
                            lines=3
                        )
                        
                        txt_style = gr.Dropdown(
                            label="Style",
                            choices=styles,
                            value="None",
                            info="Choose a style preset"
                        )
                        
                        with gr.Row():
                            txt_steps = gr.Slider(
                                label="Steps",
                                minimum=MIN_STEPS,
                                maximum=MAX_STEPS,
                                value=DEFAULT_NUM_INFERENCE_STEPS,
                                step=1,
                                info="More steps = higher quality but slower"
                            )
                            
                            txt_guidance = gr.Slider(
                                label="Guidance Scale",
                                minimum=MIN_GUIDANCE_SCALE,
                                maximum=MAX_GUIDANCE_SCALE,
                                value=DEFAULT_GUIDANCE_SCALE,
                                step=0.5,
                                info="How closely to follow the prompt"
                            )
                        
                        with gr.Row():
                            txt_width = gr.Slider(
                                label="Width",
                                minimum=MIN_RESOLUTION,
                                maximum=MAX_WIDTH,
                                value=DEFAULT_WIDTH,
                                step=64,
                                info="Image width (must be multiple of 8)"
                            )
                            
                            txt_height = gr.Slider(
                                label="Height",
                                minimum=MIN_RESOLUTION,
                                maximum=MAX_HEIGHT,
                                value=DEFAULT_HEIGHT,
                                step=64,
                                info="Image height (must be multiple of 8)"
                            )
                        
                        with gr.Row():
                            txt_seed = gr.Number(
                                label="Seed",
                                value=-1,
                                precision=0,
                                info="Seed for reproducibility (-1 = random)"
                            )
                            
                            txt_random_seed = gr.Checkbox(
                                label="Use Random Seed",
                                value=True,
                                info="Generate new random seed each time"
                            )
                        
                        txt_generate_btn = gr.Button("🎨 Generate Image", variant="primary", size="lg")
                    
                    with gr.Column(scale=1):
                        txt_output = gr.Image(label="Generated Image", type="pil")
                        txt_info = gr.Markdown("*Output info will appear here*")
                
                # Gallery of recent images
                with gr.Row():
                    txt_gallery = gr.Gallery(
                        label="Recent Generations",
                        columns=3,
                        rows=2,
                        height="auto"
                    )
                
                # Connect the generate button
                txt_generate_btn.click(
                    fn=text2img_fn,
                    inputs=[
                        txt_prompt,
                        txt_style,
                        txt_steps,
                        txt_guidance,
                        txt_height,
                        txt_width,
                        txt_seed,
                        txt_random_seed
                    ],
                    outputs=[txt_output, txt_info, txt_gallery]
                )
            
            # ========== IMAGE TO IMAGE TAB ==========
            with gr.Tab("🖼️ Image → Image"):
                gr.Markdown("Transform existing images with text prompts")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        img_input = gr.Image(
                            label="Input Image",
                            type="pil",
                            sources=["upload", "clipboard"]
                        )
                        
                        img_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="Describe how you want to transform the image...",
                            lines=3
                        )
                        
                        img_style = gr.Dropdown(
                            label="Style",
                            choices=styles,
                            value="None",
                            info="Choose a style preset"
                        )
                        
                        img_strength = gr.Slider(
                            label="Strength",
                            minimum=0.0,
                            maximum=1.0,
                            value=DEFAULT_STRENGTH,
                            step=0.05,
                            info="How much to transform (0=keep original, 1=full change)"
                        )
                        
                        with gr.Row():
                            img_steps = gr.Slider(
                                label="Steps",
                                minimum=MIN_STEPS,
                                maximum=MAX_STEPS,
                                value=DEFAULT_NUM_INFERENCE_STEPS,
                                step=1
                            )
                            
                            img_guidance = gr.Slider(
                                label="Guidance Scale",
                                minimum=MIN_GUIDANCE_SCALE,
                                maximum=MAX_GUIDANCE_SCALE,
                                value=DEFAULT_GUIDANCE_SCALE,
                                step=0.5
                            )
                        
                        with gr.Row():
                            img_seed = gr.Number(
                                label="Seed",
                                value=-1,
                                precision=0,
                                info="Seed for reproducibility (-1 = random)"
                            )
                            
                            img_random_seed = gr.Checkbox(
                                label="Use Random Seed",
                                value=True,
                                info="Generate new random seed each time"
                            )
                        
                        img_generate_btn = gr.Button("🎨 Transform Image", variant="primary", size="lg")
                    
                    with gr.Column(scale=1):
                        img_output = gr.Image(label="Transformed Image", type="pil")
                        img_info = gr.Markdown("*Output info will appear here*")
                
                # Connect the transform button
                img_generate_btn.click(
                    fn=img2img_fn,
                    inputs=[
                        img_input,
                        img_prompt,
                        img_style,
                        img_strength,
                        img_steps,
                        img_guidance,
                        img_seed,
                        img_random_seed
                    ],
                    outputs=[img_output, img_info]
                )
        
        # Footer
        gr.Markdown("""
---
### 💡 Tips
- **Text → Image**: Start with simple prompts and adjust style/parameters
- **Image → Image**: Lower strength values preserve more of the original image
- **Quality**: More steps = better quality but slower generation
- **Memory**: If you run out of VRAM, reduce resolution or close other GPU applications
- **Seeds**: Use the same seed to recreate similar images

### 📁 Output
All generated images are saved to: `outputs/generated/`
        """)
    
    return app
