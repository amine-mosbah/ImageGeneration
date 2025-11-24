# 🎨 AI Image Generation App - Stable Diffusion

A flexible web application for generating images using Stable Diffusion 1.5. Generate images from text prompts or transform existing images with various style presets. **Supports both local generation (GPU/CPU) and free cloud API mode.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Modes](https://img.shields.io/badge/modes-local%20%7C%20cloud-green.svg)

## ✨ Features

- **Hybrid Generation**: Choose between local (GPU/CPU) or cloud API (free) generation
- **Text-to-Image**: Create images from descriptive text prompts
- **Image-to-Image**: Transform existing images using prompts
- **10 Style Presets**: Realistic, Anime, 3D Render, Oil Painting, Watercolor, Cyberpunk, Fantasy, Pixel Art, Comic Book, Sketch
- **Full Control**: Adjust steps, guidance scale, resolution, strength, and seed
- **History Management**: Automatic saving with metadata and generation history
- **Flexible Deployment**: Works on any computer (API mode) or local GPU/CPU
- **100% Free**: No paid APIs required

## 📋 Table of Contents

- [Generation Modes](#generation-modes)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Features Overview](#features-overview)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## 🔄 Generation Modes

This app supports two generation modes:

### 💻 Local Mode (Default)

- Runs Stable Diffusion on your GPU/CPU
- **Pros**: Unlimited generations, complete privacy, works offline
- **Cons**: Requires GPU for speed (or patience with CPU), 3.4GB model download
- **Best for**: Users with GPU, unlimited use, privacy-conscious users

### ☁️ API Mode (Free Cloud)

- Uses HuggingFace Inference API (free tier)
- **Pros**: No GPU needed, 10-30 sec generation, works on any computer
- **Cons**: Requires internet, ~1000 requests/day limit
- **Best for**: CPU-only users, testing, cheap VPS deployment

**See [API_SETUP.md](API_SETUP.md) for instructions on enabling API mode.**

## 🔧 Requirements

### System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: ~5GB for model cache
- **GPU** (optional but recommended):
  - NVIDIA GPU with CUDA support
  - 6GB+ VRAM (8GB+ recommended)
  - Compatible with CUDA 11.8 or higher

### Software Requirements

All dependencies are listed in `requirements.txt`:

- `torch` - PyTorch for deep learning
- `diffusers` - HuggingFace Diffusers library for Stable Diffusion
- `transformers` - Text encoding models
- `accelerate` - Model optimization
- `gradio` - Web UI framework
- `Pillow` - Image processing
- `numpy` - Numerical operations

## 📦 Installation

### 1. Clone or Download

```bash
# Navigate to your desired directory
cd ~/Desktop/PS/ImageGeneration
```

### 2. Create Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Note**: First run will download the Stable Diffusion model (~4GB). Ensure you have a stable internet connection.

### 4. GPU Setup (Optional)

If you have an NVIDIA GPU:

```bash
# Verify CUDA availability
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
```

If CUDA is not detected, you may need to reinstall PyTorch with CUDA support:

```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## 🚀 Usage

### Starting the Application

```bash
# From the project root directory
python src/main.py
```

The application will:

1. Load the Stable Diffusion models (takes 1-2 minutes on first run)
2. Launch a web interface at `http://127.0.0.1:7860`
3. Automatically open in your default browser

### Text-to-Image Generation

1. Navigate to the **📝 Text → Image** tab
2. Enter your prompt (e.g., "a serene mountain landscape at sunset")
3. Choose a style preset (optional)
4. Adjust parameters:
   - **Steps**: 20-50 for good quality (more = slower but better)
   - **Guidance Scale**: 7-12 for balanced results
   - **Resolution**: 512x512 is standard, higher = more VRAM needed
   - **Seed**: Use specific seed for reproducibility or random for variety
5. Click **🎨 Generate Image**
6. Image will be displayed and saved to `outputs/generated/`

### Image-to-Image Transformation

1. Navigate to the **🖼️ Image → Image** tab
2. Upload an image
3. Enter transformation prompt (e.g., "turn into a watercolor painting")
4. Choose a style preset
5. Adjust **Strength**:
   - 0.3-0.5: Subtle changes, preserves original
   - 0.6-0.8: Moderate transformation
   - 0.9-1.0: Heavy transformation, almost like new image
6. Adjust other parameters as needed
7. Click **🎨 Transform Image**

### Parameter Guide

| Parameter              | Range   | Recommended | Description                                                      |
| ---------------------- | ------- | ----------- | ---------------------------------------------------------------- |
| **Steps**              | 1-100   | 25-40       | Number of denoising iterations. More = better quality but slower |
| **Guidance Scale**     | 1-20    | 7-12        | How strictly to follow the prompt. Higher = more literal         |
| **Resolution**         | 256-768 | 512         | Output dimensions. Higher needs more VRAM                        |
| **Strength** (img2img) | 0.0-1.0 | 0.75        | Transformation intensity. Lower = keep more of original          |
| **Seed**               | any int | -1 (random) | Reproducibility. Same seed + prompt = similar image              |

## 📂 Features Overview

### Style Presets

The app includes 10 built-in style presets:

1. **None**: Raw prompt without modifications
2. **Realistic Photography**: Professional, photorealistic images
3. **Anime**: Japanese anime/manga style illustrations
4. **3D Render**: Pixar-style CGI renders
5. **Oil Painting**: Classical art style with brush strokes
6. **Watercolor**: Soft, flowing watercolor paintings
7. **Cyberpunk**: Neon-lit futuristic aesthetic
8. **Fantasy Art**: Magical, ethereal artwork
9. **Pixel Art**: Retro 8-bit gaming style
10. **Comic Book**: Bold superhero comic style

### History & Saving

- **Automatic Saving**: All generated images are saved to `outputs/generated/`
- **Metadata**: Each image has a JSON sidecar with generation parameters
- **Naming Convention**: `YYYYMMDD_HHMMSS_type_style_seed.png`
- **Recent Gallery**: Text-to-image tab shows 6 most recent generations

### Memory Optimizations

The app automatically applies optimizations based on your hardware:

- **Attention Slicing**: Reduces VRAM usage
- **Mixed Precision**: FP16 on GPU, FP32 on CPU
- **Automatic Device Selection**: Uses GPU if available, falls back to CPU

## 🏗️ Architecture

### Project Structure

```
ImageGeneration/
├── src/
│   ├── main.py                 # Entry point
│   ├── config.py               # Global configuration
│   ├── models/
│   │   ├── sd_loader.py        # Pipeline loading
│   ├── core/
│   │   ├── generation.py       # Core generation logic
│   │   ├── styles.py           # Style presets
│   │   ├── history.py          # Image saving/loading
│   ├── ui/
│   │   ├── app.py              # Gradio interface
│   ├── utils/
│   │   ├── image_utils.py      # Image processing helpers
│   │   ├── system_utils.py     # System utilities
│
├── outputs/
│   ├── generated/              # Saved images
│   └── logs/                   # Log files
│
├── models_cache/               # HuggingFace model cache
├── requirements.txt
├── README.md
└── .gitignore
```

### Component Overview

1. **Model Layer** (`models/`): Loads and manages Stable Diffusion pipelines
2. **Core Logic** (`core/`): Generation, styles, history management
3. **UI Layer** (`ui/`): Gradio web interface
4. **Utilities** (`utils/`): Helper functions for images and system operations
5. **Configuration** (`config.py`): Centralized settings and defaults

## ⚙️ Configuration

Edit `src/config.py` to customize:

```python
# Model selection
SD_MODEL_ID = "runwayml/stable-diffusion-v1-5"

# Generation defaults
DEFAULT_NUM_INFERENCE_STEPS = 30
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_HEIGHT = 512
DEFAULT_WIDTH = 512

# Safety limits
MAX_STEPS = 100
MAX_HEIGHT = 768
MAX_WIDTH = 768

# Paths
OUTPUT_DIR = "outputs/generated"
MODEL_CACHE_DIR = "models_cache"

# Safety checker (content filtering)
ENABLE_SAFETY_CHECKER = False
```

### Using Different Models

To use a different Stable Diffusion model:

1. Find a model on [HuggingFace](https://huggingface.co/models?pipeline_tag=text-to-image)
2. Update `SD_MODEL_ID` in `config.py`:
   ```python
   SD_MODEL_ID = "stabilityai/stable-diffusion-2-1"
   # or any other compatible model
   ```

## 🔧 Troubleshooting

### Common Issues

#### 1. CUDA Out of Memory

**Problem**: `RuntimeError: CUDA out of memory`

**Solutions**:

- Reduce resolution (try 512x512 or 384x384)
- Lower number of steps
- Close other GPU applications
- Use CPU mode by setting `DEVICE = "cpu"` in `config.py`

#### 2. Slow Generation

**Problem**: Generation takes very long

**Reasons & Solutions**:

- **CPU Mode**: Normal, 2-5 minutes per image. Consider getting GPU access.
- **High Resolution**: Reduce to 512x512
- **Too Many Steps**: 30-40 steps is usually sufficient
- **First Run**: Model loading takes time initially

#### 3. Model Download Issues

**Problem**: Model fails to download

**Solutions**:

- Check internet connection
- Ensure ~5GB free disk space
- Try manual download:
  ```bash
  python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
  ```

#### 4. Import Errors

**Problem**: `ModuleNotFoundError`

**Solutions**:

- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.8+)

#### 5. Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**:

- Change port in `src/main.py`:
  ```python
  app.launch(server_port=7861)  # Use different port
  ```

### Performance Tips

**For Best Quality**:

- Use 30-50 steps
- Guidance scale 7-12
- 512x512 or higher resolution
- GPU with 8GB+ VRAM

**For Fastest Generation**:

- 15-20 steps
- 384x384 or 512x512
- Guidance scale 7-9

**For Low VRAM (<6GB)**:

- Enable CPU offload in `models/sd_loader.py`:
  ```python
  pipeline.enable_sequential_cpu_offload()
  ```

## 🚧 Future Enhancements

Planned features and improvements:

- [ ] **Batch Generation**: Generate multiple images at once
- [ ] **More Models**: Support for SD 2.x, SDXL, and custom checkpoints
- [ ] **Inpainting**: Edit specific parts of images
- [ ] **Prompt History**: Save and reuse previous prompts
- [ ] **ControlNet**: Advanced image guidance (pose, depth, edges)
- [ ] **Upscaling**: Enhance image resolution with AI upscalers
- [ ] **CLI Mode**: Command-line interface for scripting
- [ ] **Negative Prompts**: Specify what NOT to include
- [ ] **LoRA Support**: Load custom LoRA models
- [ ] **Image Browser**: Better gallery with filtering and search

## 📄 License

This project is released under the MIT License. See LICENSE file for details.

The Stable Diffusion model is subject to the CreativeML Open RAIL-M license. See [HuggingFace model card](https://huggingface.co/runwayml/stable-diffusion-v1-5) for details.

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) for Stable Diffusion
- [HuggingFace](https://huggingface.co/) for Diffusers library
- [Gradio](https://gradio.app/) for the UI framework

## 📞 Support

For issues and questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [HuggingFace Diffusers docs](https://huggingface.co/docs/diffusers/)
3. Check [Gradio documentation](https://gradio.app/docs/)

---

**Enjoy creating amazing images! 🎨✨**
