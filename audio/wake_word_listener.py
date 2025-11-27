#Tiny & stupid -> wake word listener: tiny, fast, stupidly narrow near-exact match
# Billingual chaos -> i mix both languages and  don’t want false triggers.
# JOB: ignore chatter and look for separate, isolated triggers.
# Use words that I don’t use naturally blend into your normal speech aka dedicated wake words you never say casually.

# My brain is mixing EN + RU mid-sentence, so you need to isolate
# does not decode chatter or sentences that are not wake words 
# reads FROM  two streams, each recognizer gets its own audio feed and won’t interfere.
from vosk import Model, KaldiRecognizer
from config.settings import MODEL_EN_PATH, AUDIO_SAMPLE_RATE, WAKE_WORDS, TEXT_LIMIT, AUDIO_FRAME_SIZE
from utils.logger import logger
import json
import pyaudio




def init_recognizer_en() -> KaldiRecognizer:
    """
    Initialize the Vosk RU model and create a recognizer.

    :return: A KaldiRecognizer object
    :rtype: KaldiRecognizer
    """
    try:
        model = Model(str(MODEL_EN_PATH))
        recognizer_ru = KaldiRecognizer(model, AUDIO_SAMPLE_RATE)
        if not model:
            raise ValueError("Model is null")
    except Exception as e:
        logger.error("Error loading Vosk RU model: %s", e)
        raise e

    return recognizer_ru
            
recognizer= init_recognizer_en()

def listen_for_wake_word(recognizer, stream: pyaudio.Stream, WAKE_WORDS):
     while True:
        data = stream.read(AUDIO_FRAME_SIZE, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result_text = json.loads(recognizer.FinalResult()).get("text", "")
            logger.info(f"Just heard: {result_text}")
            if any(wake_word in result_text.lower() for wake_word in WAKE_WORDS):
                return
        partial_result: str = recognizer.PartialResult()
        if partial_result and len(partial_result) > TEXT_LIMIT:
            recognizer.Reset()
