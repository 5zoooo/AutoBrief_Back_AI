"""
AutoBrief Backend API

This module initializes the FastAPI application and makes it available for ASGI servers.
"""

from app.main import app
from app.config import settings

__all__ = ["app", "settings"]