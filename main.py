from dotenv import load_dotenv
import os
from vosk import Model, KaldiRecognizer
import spotipy
import pyaudio
from spotipy.oauth2 import SpotifyOAuth
import json
import tempfile
import wave
import time
import webbrowser
from utils.logger import logger
from audio.wake_word_listener import init_recognizer_en, listen_for_wake_word
from config.settings import (
    AUDIO_SAMPLE_RATE,
    AUDIO_FRAME_SIZE,
    AUDIO_CHANNELS,
    MODEL_EN_PATH,
    WAKE_WORDS,
)
from config.secrets import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPE,
    SPOTIFY_API_DELAY,
)


def record_command(stream: pyaudio.Stream, duration_seconds: float = 10) -> bytes:
    """
    Record audio from the given stream for the specified duration.
    """
    frames = []
    for _ in range(int(duration_seconds * AUDIO_SAMPLE_RATE / AUDIO_FRAME_SIZE)):
        frame = stream.read(AUDIO_FRAME_SIZE, exception_on_overflow=False)
        frames.append(frame)
    return b"".join(frames)


def transcribe_with_vosk(data: bytes) -> str:
    """Offline transcription using Vosk."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file_name = temp_file.name
        wf = wave.open(temp_file_name, "wb")
    try:
        wf.setnchannels(AUDIO_CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(AUDIO_SAMPLE_RATE)
        wf.writeframes(data)
    finally:
        wf.close()

    wf = wave.open(temp_file_name, "rb")
    model = Model(str(MODEL_EN_PATH))
    rec = KaldiRecognizer(model, wf.getframerate())
    transcript = []

    while True:
        buf = wf.readframes(AUDIO_FRAME_SIZE)
        if len(buf) == 0:
            break
        if rec.AcceptWaveform(buf):
            result = json.loads(rec.Result())
            transcript.append(result.get("text", ""))
    result = json.loads(rec.FinalResult())
    transcript.append(result.get("text", ""))
    logger.debug("Raw transcription data: %s", transcript)

    wf.close()
    os.unlink(temp_file_name)
    return " ".join(transcript).strip()


def init_spotify() -> spotipy.Spotify | None:
    """
    Initialize Spotify client with debug logs.
    """
    logger.debug("Initializing Spotify client...")
    # Check if credentials exist
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        logger.error("Spotify client ID or secret missing!")
        logger.info(f"SPOTIFY_CLIENT_ID={SPOTIFY_CLIENT_ID}")

        return None
    try:
        sp = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope=SPOTIFY_SCOPE,
                cache_path=".spotify_token_cache",
            )
        )
        logger.debug("SUCCESS: Spotify client initialized.")
        return sp

    except Exception as e:
        logger.error(f"Error: {e}")
        return None


def search_spotify_and_play(sp: spotipy.Spotify, query: str):
    """
    Search Spotify and open the track URL in browser/app
    """

    try:
        results = sp.search(q=query, type="track", limit=1)
        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            track_url = track["external_urls"]["spotify"]
            logger.info(f"Opening: {track['name']} by {track['artists'][0]['name']}")
            webbrowser.open(track_url)
            return True
        else:
            logger.warning("Could not find track")
            return False
    except Exception as e:
        logger.error(f"Error searching Spotify: {e})")
        return False


# refactor this


def main() -> None:
    """
    main for billingal models
    """
    # Init Vosk models
    try:
        recognizer = init_recognizer_en()

    except Exception as e:
        logger.error("Error loading Vosk models: %s", e)
        raise e

    # Init Spotify client
    spotify_client = init_spotify()
    if not spotify_client:
        logger.error("ERROR initializing Spotify client")

    # --- Init PyAudio stream
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=AUDIO_CHANNELS,
            rate=AUDIO_SAMPLE_RATE,
            input=True,
            frames_per_buffer=AUDIO_FRAME_SIZE,
        )
    except Exception as e:
        logger.error("Error initializing PyAudio stream: %s", e)
        raise e

    # --- Main loop
    try:
        while True:
            # Listen for wake words in EN and RU
            listen_for_wake_word(recognizer, stream, WAKE_WORDS)
            logger.info("COMMAND MODE: listening for command...")

            # ACTIVE MODE: listen for command
            # Record audio command
            data = record_command(stream)
            if not data:
                logger.warning("No audio recorded")
                continue

            text = transcribe_with_vosk(data)
            if not text or text.strip() == "":
                logger.warning("Could not transcribe audio")
                continue

            logger.info(f"You said: {text}")
            search_spotify_and_play(spotify_client, text)

    except KeyboardInterrupt:
        logger.warning("...bye...")
    finally:
        # Clean up audio
        if stream:
            stream.stop_stream()
            stream.close()
        if audio:
            audio.terminate()


if __name__ == "__main__":
    main()  # Call the main function
