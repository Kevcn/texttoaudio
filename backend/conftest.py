import os
import sys
from pathlib import Path

# Get the absolute path of the backend directory
backend_dir = Path(__file__).parent.absolute()

# Add the backend directory to Python path if not already there
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from app.main import app 