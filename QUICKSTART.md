# 🚀 Quick Start Guide

## Get Started in 3 Minutes

### Step 1: Setup Environment (1 minute)

```bash
# Navigate to project directory
cd /home/hama/Desktop/PS/ImageGeneration

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies (2-3 minutes)

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note:** This installs PyTorch, Diffusers, Gradio, and other dependencies. May take a few minutes.

### Step 3: Launch the App

```bash
# Start the application
python src/main.py
```

**First launch will:**

1. Download Stable Diffusion model (~4GB) - takes 3-5 minutes
2. Initialize pipelines
3. Open web browser at `http://127.0.0.1:7860`

---

## 🎨 Your First Image

### Text-to-Image (Easiest)

1. Open the **Text → Image** tab
2. Enter prompt: `a beautiful sunset over mountains`
3. Click **Generate Image** (keep all default settings)
4. Wait 5-30 seconds (depending on GPU/CPU)
5. Your image appears and is saved to `outputs/generated/`

### Try Different Styles

1. Same prompt: `a beautiful sunset over mountains`
2. Change **Style** to: `Oil Painting`
3. Click **Generate Image**
4. Compare with previous image!

---

## ⚙️ Quick Settings Guide

**For Good Quality (Recommended):**

- Steps: 30
- Guidance Scale: 7.5
- Resolution: 512x512
- Use these for your first few images

**For Fast Testing:**

- Steps: 15
- Guidance Scale: 7
- Resolution: 384x384
- Good for experimenting quickly

**For Best Quality (Slow):**

- Steps: 50
- Guidance Scale: 10
- Resolution: 768x768
- Requires good GPU

---

## 🐛 Quick Troubleshooting

### "CUDA out of memory"

```bash
# Reduce resolution to 384x384 or 256x256
# Or reduce steps to 20
```

### "Module not found"

```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### App won't open in browser

```
# Manually open: http://127.0.0.1:7860
# Or try: http://localhost:7860
```

---

## 📁 Where Are My Images?

All generated images are saved to:

```
outputs/generated/
```

Each image has:

- PNG image file
- JSON metadata file (same name, .json extension)

---

## 🛑 Stopping the App

Press `Ctrl+C` in the terminal where the app is running.

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [PROJECT_PLAN.md](PROJECT_PLAN.md) for architecture details
- Experiment with different styles and prompts!

---

**Happy generating! 🎨✨**
