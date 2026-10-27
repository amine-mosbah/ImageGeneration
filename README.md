# ImageGeneration — Stable Diffusion / FLUX Image Studio

A Gradio web app for text-to-image and image-to-image generation. It can run Stable Diffusion 1.5 locally with Hugging Face `diffusers`, or send generation to the Hugging Face Inference API (FLUX.1-dev) when no GPU is available.

## What it does

- **Text → Image:** you enter a prompt, choose a style preset, and set steps, guidance scale, resolution (256–768 px) and seed (fixed or random).
- **Image → Image:** you upload an image and describe how it should change. A strength slider controls how far the result moves away from the original.
- **Two generation backends, chosen at startup:**
  - **API mode** (the default): uses `huggingface_hub.InferenceClient` with `black-forest-labs/FLUX.1-dev`. Needs a free `HF_TOKEN`; no GPU required.
  - **Local mode:** uses `runwayml/stable-diffusion-v1-5` through `StableDiffusionPipeline` / `StableDiffusionImg2ImgPipeline`. It picks CUDA (fp16) or CPU (fp32) automatically and enables attention slicing on GPU.
  - If API mode is selected but no token is set, the app falls back to local mode.
- **9 style presets plus "None":** Realistic Photography, Anime, 3D Render, Oil Painting, Watercolor, Cyberpunk, Fantasy Art, Pixel Art and Comic Book. Each one adds a prefix and a suffix to your prompt.
- **History on disk:** every image is saved to `outputs/generated/` as `YYYYMMDD_HHMMSS_<type>_<style>_<seed>.png`, with a JSON sidecar holding the prompt and all generation parameters. The header shows how many images you have generated.

## Tech stack

Python · PyTorch · Hugging Face `diffusers` / `transformers` / `accelerate` · `huggingface_hub` InferenceClient · Gradio 4 · Pillow · python-dotenv

## Architecture

```
main.py ── picks mode (config.GENERATION_MODE + HF_TOKEN)
   ├── api/huggingface.py   HuggingFaceAPI: text_to_image / image_to_image via InferenceClient
   ├── models/sd_loader.py  loads SD 1.5 text2img + img2img pipelines (local mode)
   └── ui/app.py            Gradio Blocks UI (two tabs) ──► core/
                                core/styles.py      style presets → prompt
                                core/generation.py  parameter clamping, seeding, local inference
                                core/history.py     save PNG + JSON metadata, list/count images
```

The UI layer only talks to `core/` and to the API client, so either backend can serve the same interface.

## Getting started

Requirements: Python 3.8+. For local mode, a CUDA GPU with 6 GB+ VRAM is recommended (the CPU works, but slowly), and the first run downloads about 4 GB of model weights.

```bash
git clone https://github.com/amine-mosbah/ImageGeneration.git
cd ImageGeneration

./setup.sh                 # creates .venv, installs requirements, runs test_installation.py

# API mode (default): add a free read token from https://huggingface.co/settings/tokens
echo 'HF_TOKEN=<your token>' > .env

./run.sh                   # or: source .venv/bin/activate && python src/main.py
```

The app opens at http://127.0.0.1:7860. To switch backends, set `GENERATION_MODE` in `src/config.py` to `"api"`, `"local"` or `"auto"` (`auto` uses the API when a token is present). The same file holds the model IDs, default parameters and limits.

## Project structure

```
src/
  main.py            entry point: mode selection, model/API init, launches Gradio
  config.py          mode, model IDs, defaults, limits, paths
  api/huggingface.py Hugging Face Inference API client
  models/sd_loader.py  local Stable Diffusion pipeline loading
  core/              generation.py, styles.py, history.py
  ui/app.py          Gradio interface
  utils/             image and device/seed helpers
test_installation.py checks dependencies, CUDA and project imports
setup.sh / run.sh    one-command setup and launch
```

## Further docs

- [API_SETUP.md](API_SETUP.md): getting a Hugging Face token and choosing a generation mode
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md): common install, CUDA and API errors

## Known limitations

- In API mode, width, height and seed are passed to the UI but not to the hosted model, so results aren't reproducible by seed.
- If the hosted model doesn't support image-to-image, the API client falls back to text-to-image and ignores the uploaded image.
- Local pipelines are loaded only when the app starts in local mode. The in-app "Use Cloud API" toggle therefore can't switch an API-mode session to local generation.
- The UI doesn't expose negative prompts yet.

## Author

Mohamed Amine Ben Mosbah, software engineering student at ENISo (Tunisia) · [github.com/amine-mosbah](https://github.com/amine-mosbah)
