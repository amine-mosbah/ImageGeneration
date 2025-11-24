"""
Main entry point for the Stable Diffusion Image Generation App.
Supports both local model generation and cloud API generation.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    SD_MODEL_ID,
    API_MODEL_ID,
    OUTPUT_DIR, 
    LOG_DIR, 
    MODEL_CACHE_DIR,
    get_active_mode,
    HF_API_TOKEN
)
from models.sd_loader import init_pipelines
from api.huggingface import HuggingFaceAPI, get_setup_instructions
from utils.system_utils import ensure_directories
from ui.app import create_app


def main():
    """
    Main function to run the image generation application.
    """
    print("=" * 60)
    print("🎨 STABLE DIFFUSION IMAGE GENERATION APP")
    print("=" * 60)
    print()
    
    # Ensure required directories exist
    print("📁 Setting up directories...")
    ensure_directories([OUTPUT_DIR, LOG_DIR, MODEL_CACHE_DIR])
    print()
    
    # Determine generation mode
    mode = get_active_mode()
    print(f"🔧 Generation Mode: {mode.upper()}")
    
    pipelines = {}
    
    if mode == "api":
        print("📡 Using Hugging Face API (cloud-based generation)")
        print(f"   Model: {API_MODEL_ID}")
        print()
        
        # Initialize API client
        api_client = HuggingFaceAPI(model_id=API_MODEL_ID)
        
        if not api_client.is_configured():
            print("⚠️  WARNING: HF_TOKEN not configured!")
            print()
            print(get_setup_instructions())
            print()
            print("Falling back to LOCAL mode...")
            print()
            mode = "local"
        else:
            print("✅ API token configured")
            # Test connection
            status = api_client.test_connection()
            if status["status"] == "error":
                print(f"⚠️  API Warning: {status['message']}")
                print("   Attempting to continue anyway...")
            else:
                print(f"✅ {status['message']}")
            print()
            
            pipelines = {
                "mode": "api",
                "api_client": api_client,
                "text2img": None,  # Not needed for API mode
                "img2img": None,
                "device": "cloud"
            }
    
    if mode == "local":
        print("💻 Using Local Models (GPU/CPU generation)")
        print(f"   Model: {SD_MODEL_ID}")
        print("   (This may take a few minutes on first run)")
        print()
        
        try:
            pipelines = init_pipelines()
            pipelines["mode"] = "local"
            print()
        except Exception as e:
            print(f"❌ Failed to load models: {e}")
            print()
            print("💡 Tips:")
            print("   - Ensure you have enough disk space (model is ~4GB)")
            print("   - Check your internet connection for first-time download")
            print("   - Make sure PyTorch and diffusers are properly installed")
            print()
            print("🔄 Alternative: Use API mode instead!")
            print(get_setup_instructions())
            sys.exit(1)
    
    # Create Gradio app
    print("🎨 Building UI...")
    try:
        app = create_app(pipelines)
        print("✅ UI ready!")
        print()
    except Exception as e:
        print(f"❌ Failed to create UI: {e}")
        sys.exit(1)
    
    # Launch the app
    print("=" * 60)
    print("🌐 LAUNCHING WEB APPLICATION")
    print("=" * 60)
    print()
    print("The app will open in your browser automatically.")
    print("If it doesn't, copy and paste the URL shown below.")
    print()
    print("To stop the server, press Ctrl+C in this terminal.")
    print()
    
    try:
        app.launch(
            server_name="127.0.0.1",  # Localhost only
            server_port=7860,          # Default Gradio port
            share=False,               # Don't create public link
            inbrowser=True,            # Open browser automatically
            show_error=True            # Show detailed errors in UI
        )
    except KeyboardInterrupt:
        print()
        print("👋 Shutting down gracefully...")
        print("Goodbye!")
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
