from fastapi import FastAPI, UploadFile
import subprocess
import json
import os
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "venv/lib/python3.12/site-packages")))
from .agent import get_mood_map_from_metrics
from .test_agent import get_mood_map_from_metrics as get_mock_mood_map
from .music_gen import generate_music_from_mood_map
from loguru import logger
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# resolve output path from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8080"] for stricter policy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    ".logs/api.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
)


@app.post("/analyze/")
async def analyze_code(file: UploadFile):
    filepath = f"/tmp/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(await file.read())

    result = subprocess.run(
        ["code_parser/.build/code_parser", filepath], capture_output=True, text=True
    )
    if result.returncode != 0:
        return {"error": "C++ parser failed"}

    logger.debug(f"Results from code parser: {result.stdout}")
    metrics = json.loads(result.stdout)

    if os.environ.get("TESTING"):
        mood_map = get_mock_mood_map(metrics)
    else:
        mood_map = get_mood_map_from_metrics(metrics)

    output_path = generate_music_from_mood_map(mood_map)
    logger.info(f"SUCCESS. Check {output_path}")

    return {"metrics": metrics, "mood_map": mood_map, "music_path": output_path}
