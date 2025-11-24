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
from core.styles import list_styles, get_style_description, apply_style
from core.generation import generate_text2img, generate_img2img
from core.history import save_image, list_recent_images, get_image_count
from utils.system_utils import generate_random_seed
from api.huggingface import HuggingFaceAPI


def create_text2img_interface(pipelines: Dict):
    """
    Create the text-to-image generation interface.
    Supports both local and API modes with dynamic switching.
    
    Args:
        pipelines: Dictionary containing loaded SD pipelines or API client
        
    Returns:
        Function for text-to-image generation
    """
    device = pipelines["device"]
    
    def generate_wrapper(
        prompt: str,
        style: str,
        steps: int,
        guidance: float,
        height: int,
        width: int,
        seed: int,
        use_random_seed: bool,
        use_api: bool
    ) -> Tuple[Image.Image, str]:
        """Wrapper function for text-to-image generation with UI feedback."""
        try:
            # Handle random seed
            if use_random_seed:
                seed = generate_random_seed()
            
            # Apply style to prompt
            styled_prompt = apply_style(prompt, style)
            
            # Determine mode based on toggle
            current_mode = "api" if use_api else "local"
            
            if current_mode == "api":
                # Use Hugging Face API
                api_client = pipelines["api_client"]
                image = api_client.generate_text2img(
                    prompt=styled_prompt,
                    num_inference_steps=steps,
                    guidance_scale=guidance,
                    width=width,
                    height=height,
                    seed=seed
                )
                
                if image is None:
                    return None, "❌ API request failed. Check your token or try again."
                
                # Create metadata
                metadata = {
                    "prompt": prompt,
                    "styled_prompt": styled_prompt,
                    "style": style,
                    "steps": steps,
                    "guidance_scale": guidance,
                    "width": image.size[0],
                    "height": image.size[1],
                    "seed": seed,
                    "mode": "api",
                    "generation_type": "text2img"
                }
            else:
                # Use local pipeline
                pipe = pipelines["text2img"]
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
            mode_indicator = "☁️ API" if current_mode == "api" else "💻 Local"
            info = f"""
**Generation Complete!** ({mode_indicator})
- **Prompt:** {prompt}
- **Style:** {style}
- **Size:** {metadata['width']}x{metadata['height']}
- **Steps:** {metadata['steps']}
- **Guidance Scale:** {metadata['guidance_scale']}
- **Seed:** {metadata['seed']}
- **Saved to:** {filepath}
            """
            
            return image, info.strip()
            
        except Exception as e:
            error_msg = f"❌ **Error:** {str(e)}"
            return None, error_msg
    
    return generate_wrapper


def create_img2img_interface(pipelines: Dict):
    """
    Create the image-to-image transformation interface.
    Supports both local and API modes with dynamic switching.
    
    Args:
        pipelines: Dictionary containing loaded SD pipelines
        
    Returns:
        Function for image-to-image transformation
    """
    device = pipelines["device"]
    
    def transform_wrapper(
        input_image: Image.Image,
        prompt: str,
        style: str,
        strength: float,
        steps: int,
        guidance: float,
        seed: int,
        use_random_seed: bool,
        use_api: bool
    ) -> Tuple[Optional[Image.Image], str]:
        """Wrapper function for image-to-image transformation with UI feedback."""
        try:
            # Validate input
            if input_image is None:
                return None, "❌ **Error:** Please upload an input image"
            
            # Handle random seed
            if use_random_seed:
                seed = generate_random_seed()
            
            # Apply style
            styled_prompt = apply_style(prompt, style)
            
            # Determine mode based on toggle
            current_mode = "api" if use_api else "local"
            
            if current_mode == "api":
                # Use Hugging Face API (note: basic API may not support img2img)
                api_client = pipelines["api_client"]
                image = api_client.generate_img2img(
                    prompt=styled_prompt,
                    init_image=input_image,
                    strength=strength,
                    num_inference_steps=steps,
                    guidance_scale=guidance,
                    seed=seed
                )
                
                if image is None:
                    return None, "❌ API request failed or img2img not supported by API"
                
                # Create metadata
                metadata = {
                    "prompt": prompt,
                    "styled_prompt": styled_prompt,
                    "style": style,
                    "strength": strength,
                    "steps": steps,
                    "guidance_scale": guidance,
                    "seed": seed,
                    "mode": "api",
                    "generation_type": "img2img"
                }
            else:
                # Use local pipeline
                pipe = pipelines["img2img"]
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
            mode_indicator = "☁️ API" if current_mode == "api" else "💻 Local"
            info = f"""
**Transformation Complete!** ({mode_indicator})
- **Prompt:** {prompt}
- **Style:** {style}
- **Strength:** {metadata.get('strength', strength)}
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
    # Get mode and available styles
    mode = pipelines.get("mode", "local")
    styles = list_styles()
    
    # Create generation functions
    text2img_fn = create_text2img_interface(pipelines)
    img2img_fn = create_img2img_interface(pipelines)
    
    # Custom CSS for premium look
    custom_css = """
    .gradio-container {
        font-family: 'Inter', sans-serif !important;
    }
    
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
    }
    
    .app-header h1 {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .app-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
    }
    
    .mode-toggle {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        margin-top: 1rem;
    }
    
    .stats-badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
    }
    
    .generate-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    """
    
    # Build the UI
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft(), css=custom_css) as app:
        # Premium Header
        with gr.Row(elem_classes="app-header"):
            with gr.Column():
                gr.Markdown("# 🎨 AI Image Generation Studio")
                gr.Markdown("Powered by Stable Diffusion & FLUX • Professional Quality • Lightning Fast")
                
                with gr.Row():
                    # Mode toggle in header
                    api_toggle = gr.Checkbox(
                        label="☁️ Use Cloud API (Fast & Free)",
                        value=(mode == "api"),
                        interactive=True,
                        elem_classes="mode-toggle"
                    )
                    
                    # Stats
                    image_count = get_image_count(OUTPUT_DIR)
                    gr.Markdown(f'<span class="stats-badge">📸 {image_count} images generated</span>')
        
        with gr.Tabs() as tabs:
            # ========== TEXT TO IMAGE TAB ==========
            with gr.Tab("📝 Text → Image"):
                gr.Markdown("### Generate stunning images from your imagination")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        txt_prompt = gr.Textbox(
                            label="✨ Your Prompt",
                            placeholder="A majestic dragon soaring through storm clouds, cinematic lighting, highly detailed...",
                            lines=4
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
                        txt_output = gr.Image(label="✨ Generated Image", type="pil", height=500)
                        txt_info = gr.Markdown("*Click generate to create your image*")
                
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
                        txt_random_seed,
                        api_toggle  # Add API toggle to inputs
                    ],
                    outputs=[txt_output, txt_info]
                )
            
            # ========== IMAGE TO IMAGE TAB ==========
            with gr.Tab("🖼️ Image → Image"):
                gr.Markdown("### Transform and reimagine your images")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        img_input = gr.Image(
                            label="📤 Upload Image",
                            type="pil",
                            height=400
                        )
                        
                        img_prompt = gr.Textbox(
                            label="✨ Transformation Prompt",
                            placeholder="Transform into a watercolor painting, add magical atmosphere...",
                            lines=4
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
                        img_output = gr.Image(label="✨ Transformed Image", type="pil", height=500)
                        img_info = gr.Markdown("*Upload an image and click transform*")
                
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
                        img_random_seed,
                        api_toggle  # Add API toggle to inputs
                    ],
                    outputs=[img_output, img_info]
                )
        
        # Premium Footer
        gr.Markdown("""
---
### 💡 Pro Tips
        
**🎨 Crafting Better Prompts:**
- Be specific and descriptive (lighting, mood, style, details)
- Use artistic terms: "cinematic lighting", "highly detailed", "8k resolution"
- Combine styles: "oil painting in the style of Van Gogh"

**⚡ Mode Selection:**
- **☁️ Cloud API**: Fast generation (10-30s), no GPU needed, ~1000 free/day
- **💻 Local**: Unlimited use, requires GPU for speed, complete privacy

**🎯 Parameters Guide:**
- **Steps**: 20-30 for speed, 50+ for maximum quality
- **Guidance**: 7-8 for balanced, 10+ for strict prompt following
- **Strength** (img2img): 0.3-0.5 for subtle changes, 0.7-0.9 for major transformation

**🔐 Privacy & Storage:**
All images saved to `outputs/generated/` • Toggle API mode anytime • Your prompts stay private in local mode

---
<div style="text-align: center; color: #888; padding: 1rem;">
    Made with ❤️ using Stable Diffusion & FLUX • Powered by HuggingFace
</div>
        """)
    
    return app
