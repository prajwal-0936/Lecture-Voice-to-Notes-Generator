import os
import re
from datetime import datetime

# Utility functions for file handling and simple helpers

def get_project_root():
    """Return the absolute path to the project root (folder containing this file)."""
    return os.path.dirname(os.path.abspath(__file__))


def ensure_data_dirs():
    """Ensure `data/audio`, `data/transcripts`, and `data/notes` directories exist."""
    root = get_project_root()
    paths = [
        os.path.join(root, "data", "audio"),
        os.path.join(root, "data", "transcripts"),
        os.path.join(root, "data", "notes"),
    ]
    for p in paths:
        os.makedirs(p, exist_ok=True)
    return paths


def sanitize_filename(name: str) -> str:
    """Make a safe filename by removing unsafe characters."""
    name = os.path.splitext(name)[0]
    # Replace spaces and non-alphanumeric with underscores
    safe = re.sub(r"[^0-9A-Za-z._-]", "_", name)
    return safe


def timestamp():
    """Return a compact timestamp string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_text_file(dir_path: str, filename: str, text: str) -> str:
    """Save `text` to `dir_path/filename`. Ensure directory exists and return saved path."""
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path
