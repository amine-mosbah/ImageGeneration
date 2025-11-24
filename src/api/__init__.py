"""
API package for cloud-based image generation.
"""
from .huggingface import HuggingFaceAPI, get_setup_instructions

__all__ = ['HuggingFaceAPI', 'get_setup_instructions']
