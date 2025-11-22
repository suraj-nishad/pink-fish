"""
Main entry point for Vercel deployment
Vercel looks for app.py in the root directory
"""

from backend.app import app

# This is the FastAPI app instance that Vercel will use
# It's imported from backend/app.py where all the routes are defined
