"""
Config file for environment variables, API keys, paths, and constants.
"""

import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
# Logger
from utils.logger import logger

try:
    load_dotenv()
except ImportError as e:
    logger.error("Error loading environment variables: %s", e)
    exit(1)



# ============================================================================
# SPOTIFY CONFIGURATION
# =======a=====================================================================
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPE = "user-read-playback-state, user-modify-playback-state, user-read-currently-playing"

# ============================================================================
# OPENAI CONFIGURATION
# ============================================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "whisper-1"
OPENAI_RESPONSE_FORMAT = "text"


# ============================================================================
# SPOTIFY API TIMING
# ============================================================================
SPOTIFY_API_DELAY = 1  # seconds between Spotify API calls
