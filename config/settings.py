from pathlib import Path
# ============================================================================
# VOICE RECOGNITION CONFIGURATION
# ============================================================================
WAKE_WORDS = ["wake up torp", "wake up", "hello torp"]

# Audio recording parameters
AUDIO_SAMPLE_RATE = 16000
AUDIO_FRAME_SIZE = 4000
AUDIO_CHANNELS = 1
AUDIO_RECORD_DURATION = 10  # seconds

# Text processing thresholds
TEXT_LIMIT = 100
SILENCE_THRESHOLD = 1500  # Adjusted for better sensitivity

# ============================================================================
# PROJECT PATHS
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
MODEL_EN_PATH = MODELS_DIR / "model_en" / "vosk-model-small-en-us-0.15"
