# focusAssistVosk

Lightweight Vosk model assistant for offline/online voice recognition in English.

## VOSK
Used for offline speech recognition.

### Wake Word Detection 

Continuous listening for "hey you", "okay you", etc.
Fast, always-on, zero latency
### Command Transcription 

Records audio after wake word is detected
Transcribes full commands entirely offline using Vosk
No API calls, no costs, complete privacy
**Advantages:**
- ✅ 100% Offline – Everything runs locally, no cloud dependency
- ✅ Zero API Costs – No external service charges
- ✅ Privacy – Audio never leaves your device
- ✅ Low Latency – No network round-trips
- ✅ Bilingual Support – English & Russian models

**Best For:**
- Straightforward, routine commands (e.g., "play white noise ", "shuffle rock")
- Short, predictable user utterances
- Always-on voice assistants with consistent command patterns

**Trade-offs:**
- ❌ Lower accuracy on complex/ambiguous speech
- ❌ Weak with heavy background noise
- ❌ Limited context understanding (no semantic awareness)
- ❌ No punctuation/capitalization in output
- ❌ Static model – cannot improve over time

### Download Vosk Models
List of Vosk models: https://alphacephei.com/vosk/models

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

