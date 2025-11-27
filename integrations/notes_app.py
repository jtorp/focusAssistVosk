import subprocess
from utils.logger import logger

def open_notes_app():
    try:
        subprocess.run(["open", "-a", "Notes.app"])
        logger.info("Notes app opened.")
    except subprocess.CalledProcessError as e:
        logger.error("Error opening Notes app: %s", e)