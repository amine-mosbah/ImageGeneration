# 🆓 Free API Mode Setup Guide

This guide shows you how to use **FREE** cloud-based generation instead of running locally.

## Why Use API Mode?

✅ **No GPU required** - Runs on HuggingFace servers  
✅ **Fast on any computer** - 10-30 seconds per image  
✅ **No 3.4GB model download** - Minimal disk space needed  
✅ **Works on cheap VPS** - Deploy for $5-10/month  
✅ **100% FREE** - ~1000 images/day free tier

---

## Step 1: Get Free HuggingFace Token

1. Go to **https://huggingface.co**
2. Click "Sign Up" (completely free, no credit card)
3. Verify your email
4. Go to **https://huggingface.co/settings/tokens**
5. Click "New token"
6. Name it (e.g., "image-gen")
7. Select **"Read"** permission
8. Click "Generate"
9. **Copy the token** (starts with `hf_`)

---

## Step 2: Configure Token

### Option A: Environment Variable (Quick)

```bash
export HF_TOKEN="hf_your_token_here"
```

### Option B: .env File (Recommended)

```bash
# Create .env file in project root
echo 'HF_TOKEN=hf_your_token_here' > .env
```

---

## Step 3: Enable API Mode

Edit `src/config.py` and change the `GENERATION_MODE`:

```python
# Set to "api" to always use API
GENERATION_MODE = "api"

# Or set to "auto" to use API if token exists, otherwise local
GENERATION_MODE = "auto"
```

---

## Step 4: Run the App

```bash
./run.sh
```

Or:

```bash
source .venv/bin/activate
python src/main.py
```

---

## Verification

When you start the app, you should see:

```
🔧 Generation Mode: API
📡 Using Hugging Face API (cloud-based generation)
✅ API token configured
✅ API connection successful
```

---

## Using the App

1. Open http://127.0.0.1:7860
2. Enter your prompt (e.g., "a beautiful sunset over mountains")
3. Click "Generate Image"
4. Wait 10-30 seconds (first request may take longer)
5. Done! Much faster than CPU generation

The UI will show: **☁️ API Mode (Cloud)**

---

## Switching Between Modes

### Method 1: Edit config.py

```python
GENERATION_MODE = "local"   # Use local GPU/CPU
GENERATION_MODE = "api"     # Use HuggingFace API
GENERATION_MODE = "auto"    # Auto-detect (recommended)
```

### Method 2: Environment Variable

```bash
# Unset token to force local mode
unset HF_TOKEN

# Set token to enable API mode
export HF_TOKEN="hf_your_token"
```

### Method 3: Remove .env File

```bash
# Force local mode
mv .env .env.backup

# Restore API mode
mv .env.backup .env
```

---

## Comparison

| Feature         | Local Mode        | API Mode           |
| --------------- | ----------------- | ------------------ |
| **Speed (CPU)** | 2-10 min          | 10-30 sec          |
| **Speed (GPU)** | 10-30 sec         | 10-30 sec          |
| **Cost**        | Free              | Free (~1000/day)   |
| **Setup**       | Complex           | Very easy          |
| **Downloads**   | 3.4GB             | None               |
| **GPU Needed**  | Yes (for speed)   | No                 |
| **Internet**    | Only for download | Required           |
| **Privacy**     | 100% private      | Prompts sent to HF |

---

## Rate Limits

### Free Tier (No Credit Card)

- **~1000 requests per day**
- **~1 request per second**
- **Automatic rate limiting**

If you hit limits:

- Wait a few minutes
- Requests reset after 24 hours
- Consider local mode for heavy use

---

## Troubleshooting

### "Model is loading"

**This is normal for the first request!**

The model needs to warm up on HF servers. Wait 30-60 seconds and the next request will be fast.

### "Invalid API token"

1. Check token starts with `hf_`
2. Verify it's a "Read" token
3. Generate a new token if needed
4. Make sure token is set correctly:
   ```bash
   echo $HF_TOKEN  # Should show your token
   ```

### "API request failed"

- Check your internet connection
- HF servers may be temporarily overloaded
- Try again in a few minutes
- Check HF status: https://status.huggingface.co

### App still using local mode

1. Check `GENERATION_MODE` in config.py
2. Verify token is set:
   ```bash
   echo $HF_TOKEN
   ```
3. Restart the application
4. Look for "API Mode" in startup logs

---

## Deploying to VPS with API Mode

Since API mode doesn't need GPU, you can deploy on cheap VPS:

### Minimum VPS Requirements:

- **CPU**: 1-2 cores
- **RAM**: 2GB (4GB recommended)
- **Storage**: 5GB
- **Cost**: $5-10/month

### Popular VPS Providers:

- DigitalOcean ($6/month)
- Linode ($5/month)
- Vultr ($5/month)
- AWS Lightsail ($5/month)

### Deployment Steps:

1. SSH into VPS:

   ```bash
   ssh user@your-vps-ip
   ```

2. Clone repo:

   ```bash
   git clone https://github.com/yourusername/ImageGeneration.git
   cd ImageGeneration
   ```

3. Setup:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

4. Configure token:

   ```bash
   echo 'HF_TOKEN=hf_your_token' > .env
   ```

5. Set to API mode in config.py:

   ```python
   GENERATION_MODE = "api"
   ```

6. Run:

   ```bash
   ./run.sh
   ```

7. Access remotely:
   - Edit `src/main.py` and change:
     ```python
     server_name="0.0.0.0"  # Listen on all interfaces
     ```
   - Access at: `http://your-vps-ip:7860`

---

## Security Tips for VPS

1. **Use firewall**:

   ```bash
   sudo ufw allow 22    # SSH
   sudo ufw allow 7860  # Gradio
   sudo ufw enable
   ```

2. **Add authentication** (edit main.py):

   ```python
   app.launch(
       server_name="0.0.0.0",
       auth=("username", "password")  # Add auth
   )
   ```

3. **Use HTTPS** with reverse proxy (nginx/caddy)

---

## Benefits Summary

### For CPU Users:

- **20x faster** than local CPU generation
- No more 5-10 minute waits
- Same quality as GPU

### For VPS Deployment:

- Deploy on $5/month VPS instead of $50-500/month GPU VPS
- 90-99% cost savings
- Same user experience

### For Everyone:

- Easy setup (just one token)
- Completely free for reasonable use
- No hardware requirements

---

## Getting Help

If you need assistance:

1. Check `TROUBLESHOOTING.md`
2. Verify token at https://huggingface.co/settings/tokens
3. Check app logs when starting
4. Test API connection manually:
   ```bash
   python -c "from src.api.huggingface import HuggingFaceAPI; api = HuggingFaceAPI(); print(api.test_connection())"
   ```

---

## Next Steps

1. Generate some test images
2. Try different styles and prompts
3. Compare speed with local mode (if you have GPU)
4. Consider deploying to VPS for remote access

Enjoy fast, free image generation! 🎨☁️
