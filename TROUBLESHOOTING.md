# Troubleshooting Guide

## Common Issues and Solutions

### 1. Gradio TypeError on Launch

**Error:**

```
TypeError: argument of type 'bool' is not iterable
```

**Solution:**
This is a known compatibility issue with Gradio 4.44+ and Python 3.9. The app now uses Gradio 4.36.1 which is stable.

If you encounter this, reinstall dependencies:

```bash
source .venv/bin/activate
pip install "gradio==4.36.1"
```

### 2. CUDA/GPU Not Detected

**Symptom:**
App runs on CPU instead of GPU, generation is very slow.

**Solution:**

1. Check CUDA installation:

   ```bash
   nvidia-smi
   python -c "import torch; print(torch.cuda.is_available())"
   ```

2. Reinstall PyTorch with CUDA support:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### 3. Out of Memory (VRAM)

**Error:**

```
CUDA out of memory
```

**Solutions:**

- Reduce image resolution (try 256x256 or 384x384)
- Reduce batch size to 1
- Close other GPU applications
- Use CPU mode (slower but works):
  - Edit `src/config.py` and set `FORCE_CPU = True`

### 4. Slow Generation on CPU

**Symptom:**
Takes several minutes to generate one image.

**Explanation:**
This is normal behavior on CPU. Stable Diffusion is GPU-intensive.

**Solutions:**

- Use a GPU if available
- Reduce inference steps (try 15-20 instead of 30-50)
- Reduce image resolution
- Be patient - CPU generation can take 2-10 minutes per image

### 5. Model Download Fails

**Error:**

```
HTTPError: 404 Client Error
```

**Solutions:**

1. Check internet connection
2. Try downloading model manually:
   ```bash
   python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
   ```
3. Use a different model by editing `src/config.py`

### 6. Import Errors

**Error:**

```
ModuleNotFoundError: No module named 'X'
```

**Solution:**
Reinstall all dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 7. Permission Errors

**Error:**

```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. Make scripts executable:

   ```bash
   chmod +x setup.sh run.sh
   ```

2. Check write permissions:
   ```bash
   chmod -R u+w outputs/ models_cache/
   ```

### 8. Port Already in Use

**Error:**

```
OSError: [Errno 98] Address already in use
```

**Solutions:**

1. Find and kill the process using port 7860:

   ```bash
   lsof -ti:7860 | xargs kill -9
   ```

2. Or use a different port by editing `src/main.py`:
   ```python
   app.launch(server_port=7861)
   ```

### 9. Low Quality Images

**Symptom:**
Generated images look blurry or low quality.

**Solutions:**

- Increase inference steps (try 30-50)
- Increase guidance scale (try 7.5-10)
- Use higher resolution (512x512 or 768x768)
- Write more detailed prompts
- Try different style presets

### 10. Browser Doesn't Open

**Symptom:**
App launches but browser doesn't open automatically.

**Solution:**
Manually open browser and navigate to the URL shown in terminal:

```
http://127.0.0.1:7860
```

### 11. Image Upload Fails (Image-to-Image)

**Symptom:**
"Error: Please upload an input image" even after uploading.

**Solutions:**

- Try a different image format (PNG, JPG)
- Reduce image file size (< 10MB)
- Check image isn't corrupted
- Try uploading from a different location

## Performance Tips

### For CPU Users:

- Use 15-20 steps instead of 30+
- Use 256x256 or 384x384 resolution
- Lower guidance scale slightly (6-7 instead of 7.5)

### For GPU Users:

- Monitor VRAM usage with `nvidia-smi`
- Close unnecessary applications
- Use FP16 precision (already enabled for GPU)

### For All Users:

- Be specific and detailed in prompts
- Experiment with different styles
- Save good seeds for reproducibility
- Start with lower settings and increase gradually

## Getting Help

If you continue to experience issues:

1. Check the logs in `outputs/logs/`
2. Review error messages carefully
3. Search for similar issues online
4. Check Gradio and Diffusers documentation

## Version Information

This app was tested with:

- Python 3.9+
- Gradio 4.36.1
- Diffusers (latest)
- PyTorch (latest with CUDA 11.8 or 12.1)

For best results, use these versions.
