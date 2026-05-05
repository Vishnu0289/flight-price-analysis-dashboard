import logging
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def ensure_directory(path):
    """
    Ensures directory exists safely.
    Handles Windows file/folder conflicts.
    """
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f"{path} exists but is not a directory.")
    else:
        os.makedirs(path, exist_ok=True)