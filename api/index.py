"""
Vercel serverless function entry point for Digital Twin Dashboard
This file is required for Vercel Python runtime
"""

from backend.app import app

# Vercel expects a FastAPI 'app' instance
# The app is already created in backend.app, so we just import it
# This exposes it at the api/index.py location that Vercel expects

# Note: The 'app' variable name is required by Vercel
__all__ = ['app']
