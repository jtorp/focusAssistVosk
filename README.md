# focusAssistVosk

Lightweight Vosk model assistant for offline/online voice recognition in English.

## Setup

### Download Vosk Models

The project uses offline Vosk models for speech recognition. You need to download them locally:

#### English Model
Using `wget`:
```bash
cd models/model_en
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip
cd ../..
```

Or using `curl`:
```bash
cd models/model_en
curl -L -O https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip
cd ../..
```

## Structure

- `main.py` - Main application entry point
- `config/secrets.py` - Centralized configuration for constants, paths, and API keys
- `models/` - Local Vosk model directories (ignored in git, download separately)

## Features

- Offline speech recognition using Vosk
- Spotify web api integration for music search and playback
- Free Vosk transcription
- Colored logging for easy debugging

