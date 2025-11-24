#!/usr/bin/env python3
"""
Test script to verify installation and basic functionality.
Run this after installing dependencies to check if everything works.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import diffusers
        print(f"✅ Diffusers: {diffusers.__version__}")
    except ImportError as e:
        print(f"❌ Diffusers import failed: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import gradio
        print(f"✅ Gradio: {gradio.__version__}")
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ Pillow (PIL)")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy: {numpy.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True


def test_cuda():
    """Test CUDA availability."""
    print("\nTesting CUDA availability...")
    
    import torch
    
    if torch.cuda.is_available():
        print(f"✅ CUDA is available")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print(f"   CUDA Version: {torch.version.cuda}")
        return True
    else:
        print("⚠️  CUDA is not available - will use CPU (slower)")
        print("   This is fine for testing, but GPU is recommended for regular use")
        return False


def test_project_structure():
    """Test if project structure is correct."""
    print("\nTesting project structure...")
    
    required_dirs = [
        'src',
        'src/models',
        'src/core',
        'src/ui',
        'src/utils',
        'outputs',
        'outputs/generated',
        'models_cache'
    ]
    
    required_files = [
        'src/main.py',
        'src/config.py',
        'src/models/sd_loader.py',
        'src/core/generation.py',
        'src/core/styles.py',
        'src/core/history.py',
        'src/ui/app.py',
        'src/utils/image_utils.py',
        'src/utils/system_utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    base_dir = os.path.dirname(__file__)
    
    all_good = True
    
    for dir_path in required_dirs:
        full_path = os.path.join(base_dir, dir_path)
        if os.path.isdir(full_path):
            print(f"✅ Directory: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
    
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.isfile(full_path):
            print(f"✅ File: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good


def test_module_imports():
    """Test if project modules can be imported."""
    print("\nTesting project module imports...")
    
    try:
        from config import SD_MODEL_ID, DEVICE
        print(f"✅ Config module")
        print(f"   Model: {SD_MODEL_ID}")
        print(f"   Device: {DEVICE}")
    except ImportError as e:
        print(f"❌ Config module failed: {e}")
        return False
    
    try:
        from utils.system_utils import get_device
        print(f"✅ System utils module")
    except ImportError as e:
        print(f"❌ System utils import failed: {e}")
        return False
    
    try:
        from utils.image_utils import validate_dimensions
        print(f"✅ Image utils module")
    except ImportError as e:
        print(f"❌ Image utils import failed: {e}")
        return False
    
    try:
        from core.styles import list_styles
        styles = list_styles()
        print(f"✅ Styles module ({len(styles)} styles available)")
    except ImportError as e:
        print(f"❌ Styles module import failed: {e}")
        return False
    
    try:
        from core.generation import generate_text2img
        print(f"✅ Generation module")
    except ImportError as e:
        print(f"❌ Generation module import failed: {e}")
        return False
    
    try:
        from core.history import save_image
        print(f"✅ History module")
    except ImportError as e:
        print(f"❌ History module import failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 INSTALLATION TEST SUITE")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test 1: Package imports
    if not test_imports():
        print("\n❌ Package import test failed!")
        print("   Run: pip install -r requirements.txt")
        all_passed = False
    else:
        print("\n✅ All required packages are installed")
    
    # Test 2: CUDA
    has_cuda = test_cuda()
    
    # Test 3: Project structure
    if not test_project_structure():
        print("\n❌ Project structure test failed!")
        print("   Some files or directories are missing")
        all_passed = False
    else:
        print("\n✅ Project structure is correct")
    
    # Test 4: Module imports
    if not test_module_imports():
        print("\n❌ Module import test failed!")
        print("   Check Python path and module structure")
        all_passed = False
    else:
        print("\n✅ All project modules can be imported")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if all_passed:
        print("✅ All tests passed!")
        print()
        print("🚀 You're ready to run the application:")
        print("   python src/main.py")
        print()
        if not has_cuda:
            print("⚠️  Note: Running on CPU will be slow (2-5 min per image)")
            print("   Consider using a GPU for better performance")
    else:
        print("❌ Some tests failed")
        print()
        print("📝 Next steps:")
        print("   1. Make sure you're in the virtual environment")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Check that all files are present")
        print("   4. Run this test script again")
    
    print()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
