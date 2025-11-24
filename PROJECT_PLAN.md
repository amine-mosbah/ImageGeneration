# Project Plan: Local Image Generation App - Stable Diffusion Mini UI

## 1. Project Overview

### 1.1 Project Title

**Local Image Generation App – Stable Diffusion Mini UI**

### 1.2 Description

A local web application that allows users to:

- Generate images from text prompts (text → image)
- Transform existing images using prompts (image → image)
- Choose between different styles (e.g. realistic, anime, 3D)
- Control key generation parameters (steps, guidance scale, resolution, seed)
- Download generated images and view a small history

All of this runs entirely locally using Stable Diffusion 1.5 (or similar open models) via the Diffusers library and a Gradio web UI. No paid APIs, no online inference.

---

## 2. High-Level Architecture

### 2.1 Components

#### Model Layer

- Stable Diffusion text-to-image pipeline
- Stable Diffusion image-to-image pipeline
- Optional safety checker (can be disabled)

#### Core Logic Layer

- Image generation utilities
- Style preset system
- Parameter validation
- Image saving & history management

#### UI Layer (Gradio)

- Tabs / sections for:
  - Text → Image
  - Image → Image
- Controls: prompt input, style dropdown, sliders (steps, CFG, etc.), seed, resolution
- Output gallery and download buttons

#### Configuration & Utilities

- Config file for:
  - model names
  - default parameters
  - paths (model cache, output dir)
- Logging utilities
- Simple error handling and graceful fallbacks (CPU vs GPU)

### 2.2 File / Folder Structure

```
ImageGeneration/
├── src/
│   ├── main.py                    # Entry point – launches Gradio app
│   ├── config.py                  # Global configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sd_loader.py           # Functions to load SD pipelines
│   ├── core/
│   │   ├── __init__.py
│   │   ├── generation.py          # Core generate_text2img / generate_img2img
│   │   ├── styles.py              # Style presets and prompt modifiers
│   │   ├── history.py             # Save images + metadata, list history
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py                 # Gradio layout, event handlers
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py         # Image loading, resizing, conversions
│   │   ├── system_utils.py        # Device selection, seed helpers
│
├── outputs/
│   ├── generated/                 # Saved generated images
│   └── logs/                      # (Optional) Log files
│
├── models_cache/                  # Local cache for models
│
├── requirements.txt
├── PROJECT_PLAN.md
├── README.md
└── .gitignore
```

---

## 3. Implementation Details

### 3.1 Technology Stack

**Core Libraries:**

- `torch` - PyTorch deep learning framework
- `diffusers` - HuggingFace Diffusers for Stable Diffusion
- `transformers` - Text encoding models
- `accelerate` - Model optimization
- `gradio` - Web UI framework
- `Pillow` - Image processing
- `numpy` - Numerical operations

**Model:**

- Stable Diffusion 1.5 (`runwayml/stable-diffusion-v1-5`)
- Downloaded from HuggingFace Hub (~4GB)

### 3.2 Key Modules

#### config.py

Centralized configuration including:

- Model ID and paths
- Device selection (CUDA/CPU)
- Default generation parameters
- Safety limits for parameters
- Output directories

#### models/sd_loader.py

Functions to:

- Detect device (GPU/CPU)
- Load text-to-image pipeline
- Load image-to-image pipeline
- Apply memory optimizations
- Initialize both pipelines at startup

#### core/styles.py

Style preset system with 10 presets:

- None, Realistic Photography, Anime, 3D Render
- Oil Painting, Watercolor, Cyberpunk
- Fantasy Art, Pixel Art, Comic Book

Each style has:

- Prompt prefix
- Prompt suffix
- Optional extra parameters
- Description

#### core/generation.py

Core generation logic:

- `generate_text2img()` - Text to image generation
- `generate_img2img()` - Image to image transformation
- Parameter validation and clamping
- Style application
- Seed handling
- Error handling

#### core/history.py

Image management:

- Save images with metadata
- Generate unique filenames
- Save JSON sidecar files
- List recent images
- Get image count

#### ui/app.py

Gradio interface with:

- Two tabs (Text→Image, Image→Image)
- Input controls for all parameters
- Output image display
- Info panel with generation details
- Recent images gallery
- Tips and instructions

#### main.py

Application entry point:

- Directory setup
- Pipeline initialization
- UI creation
- Server launch with proper configuration

### 3.3 Features Implemented

✅ **Text-to-Image Generation**

- Custom prompts
- 10 style presets
- Configurable steps, guidance, resolution
- Seed control for reproducibility
- Recent images gallery

✅ **Image-to-Image Transformation**

- Upload existing images
- Transform with prompts and styles
- Strength control (how much to change)
- All standard parameters

✅ **Parameter Control**

- Steps: 1-100 (default 30)
- Guidance Scale: 1-20 (default 7.5)
- Resolution: 256-768 (default 512)
- Seed: random or specific value
- Strength: 0.0-1.0 for img2img

✅ **Memory Management**

- Automatic device detection
- FP16 on GPU, FP32 on CPU
- Attention slicing for memory efficiency
- Graceful degradation to CPU if needed

✅ **History & Persistence**

- Auto-save all generations
- Metadata in JSON format
- Timestamped filenames
- Recent images display

✅ **User Experience**

- Clean, intuitive UI
- Real-time generation info
- Error messages
- Tips and guidance
- Automatic browser launch

---

## 4. Step-by-Step Execution Plan (COMPLETED ✅)

### 4.1 Setup & Boilerplate ✅

- [x] Create project folder structure
- [x] Initialize git repository
- [x] Create .gitignore
- [x] Create virtual environment setup
- [x] Create requirements.txt

### 4.2 Configuration & Utilities ✅

- [x] Implement config.py
- [x] Implement utils/system_utils.py
- [x] Implement utils/image_utils.py

### 4.3 Model Loading ✅

- [x] Create models/ package
- [x] Implement sd_loader.get_device
- [x] Implement load_text2img_pipeline
- [x] Implement load_img2img_pipeline
- [x] Implement init_pipelines

### 4.4 Core Logic ✅

- [x] Create core/ package
- [x] Implement core/styles.py with presets
- [x] Implement core/generation.py
- [x] Implement generate_text2img()
- [x] Implement generate_img2img()
- [x] Implement core/history.py
- [x] Implement save_image()
- [x] Implement list_recent_images()

### 4.5 UI Layer ✅

- [x] Create ui/ package
- [x] Design Gradio layout in app.py
- [x] Implement Text → Image tab
- [x] Implement Image → Image tab
- [x] Add parameter validation
- [x] Add info panels and galleries

### 4.6 Entry Point & Integration ✅

- [x] Implement src/main.py
- [x] Directory initialization
- [x] Pipeline loading
- [x] UI creation
- [x] Server launch

### 4.7 Documentation ✅

- [x] Write comprehensive README.md
- [x] Document installation steps
- [x] Document usage instructions
- [x] Add troubleshooting guide
- [x] Document architecture
- [x] Add parameter guide

---

## 5. Usage Instructions

### Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python src/main.py
```

The app will:

1. Load Stable Diffusion models (1-2 min first time)
2. Launch web UI at http://127.0.0.1:7860
3. Open automatically in browser

### Basic Usage

**Text to Image:**

1. Go to "Text → Image" tab
2. Enter prompt: "a serene mountain landscape"
3. Choose style (optional)
4. Adjust parameters as needed
5. Click "Generate Image"

**Image to Image:**

1. Go to "Image → Image" tab
2. Upload an image
3. Enter transformation prompt
4. Adjust strength (0.5-0.8 recommended)
5. Click "Transform Image"

---

## 6. Performance & Requirements

### System Requirements

- **Python**: 3.8+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: ~5GB for model cache
- **GPU**: Optional but recommended
  - NVIDIA GPU with CUDA
  - 6GB+ VRAM (8GB+ ideal)

### Performance Estimates

- **GPU (RTX 3060 12GB)**
  - 512x512: ~3-5 seconds
  - 768x768: ~8-12 seconds
- **CPU (Modern i7/Ryzen 7)**
  - 512x512: ~2-3 minutes
  - Not recommended for regular use

---

## 7. Future Enhancements

### Planned Features

- [ ] Batch generation (multiple images at once)
- [ ] Negative prompts
- [ ] More models (SD 2.x, SDXL)
- [ ] ControlNet support
- [ ] Inpainting (edit parts of images)
- [ ] LoRA model support
- [ ] Prompt history
- [ ] Better image browser
- [ ] CLI interface
- [ ] API endpoint mode

### Possible Optimizations

- [ ] xFormers for memory efficiency
- [ ] Model quantization
- [ ] Cached text encoders
- [ ] Progressive image previews

---

## 8. Troubleshooting

### Common Issues

**CUDA Out of Memory**

- Reduce resolution to 512x512 or lower
- Reduce number of steps
- Enable CPU offload in sd_loader.py

**Slow Generation**

- Normal on CPU (2-5 min per image)
- GPU recommended for regular use
- Reduce steps and resolution

**Model Download Fails**

- Check internet connection
- Ensure ~5GB free space
- May need to configure HuggingFace token for gated models

---

## 9. Architecture Diagram

```
User Browser
     ↓
Gradio Web UI (ui/app.py)
     ↓
Core Logic (core/generation.py)
     ↓
Style System (core/styles.py)
     ↓
SD Pipelines (models/sd_loader.py)
     ↓
[Text2Img Pipeline] [Img2Img Pipeline]
     ↓
Generated Image
     ↓
History Manager (core/history.py)
     ↓
Saved to outputs/generated/
```

---

## 10. Conclusion

This project provides a complete, production-ready local image generation application with:

- ✅ Clean architecture and modular design
- ✅ Comprehensive documentation
- ✅ User-friendly interface
- ✅ Robust error handling
- ✅ Memory optimizations
- ✅ Extensible codebase

The application is ready to use and can be extended with additional features as needed.

---

**Project Status: COMPLETE ✅**

**Created:** November 24, 2025
**Last Updated:** November 24, 2025
