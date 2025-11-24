"""
Main entry point for the Stable Diffusion Image Generation App.
Initializes pipelines and launches the Gradio UI.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SD_MODEL_ID, OUTPUT_DIR, LOG_DIR, MODEL_CACHE_DIR
from models.sd_loader import init_pipelines
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
    
    # Initialize Stable Diffusion pipelines
    print("🚀 Loading Stable Diffusion models...")
    print(f"   Model: {SD_MODEL_ID}")
    print("   (This may take a few minutes on first run)")
    print()
    
    try:
        pipelines = init_pipelines()
        print()
    except Exception as e:
        print(f"❌ Failed to load models: {e}")
        print()
        print("💡 Tips:")
        print("   - Ensure you have enough disk space (model is ~4GB)")
        print("   - Check your internet connection for first-time download")
        print("   - Make sure PyTorch and diffusers are properly installed")
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
