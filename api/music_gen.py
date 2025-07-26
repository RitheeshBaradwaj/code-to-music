import subprocess
import os
from mingus.containers import Note, Bar, Track
from mingus.midi import midi_file_out

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --- Configuration ---
MOOD_CONFIG = {
    "tense": {"meter": (7, 8), "notes": ["C", "D", "Eb", "F"]},
    "chaotic": {"meter": (5, 4), "notes": ["C", "E", "G#", "B"]},
    "calm": {"meter": (4, 4), "notes": ["C", "E", "G"]},
}

DEFAULT_MOOD = "calm"
MIDI_OUTPUT = os.path.join(PROJECT_ROOT, "output", "result.mid")
WAV_OUTPUT = os.path.join(PROJECT_ROOT, "output", "result.wav")
SOUNDFONT_PATH = os.path.join(PROJECT_ROOT, "soundfonts", "FluidR3_GM.sf2")


# --- Generate MIDI from mood ---
def generate_music(mood: str) -> str:
    config = MOOD_CONFIG.get(mood.lower(), MOOD_CONFIG[DEFAULT_MOOD])

    os.makedirs("output", exist_ok=True)

    bar = Bar()
    bar.set_meter(config["meter"])

    for note in config["notes"]:
        bar.place_notes(Note(note), 4)

    track = Track()
    track.add_bar(bar)

    midi_file_out.write_Track(MIDI_OUTPUT, track)

    return convert_midi_to_wav(MIDI_OUTPUT, WAV_OUTPUT)


# --- Convert MIDI to WAV using FluidSynth ---
def convert_midi_to_wav(midi_path: str, wav_path: str) -> str:
    if not os.path.exists(SOUNDFONT_PATH):
        raise FileNotFoundError(f"Soundfont not found at: {SOUNDFONT_PATH}")

    result = subprocess.run(
        ["fluidsynth", "-ni", SOUNDFONT_PATH, midi_path, "-F", wav_path, "-r", "44100"],
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"fluidsynth failed:\n{result.stderr.decode()}")

    return f"output/{os.path.basename(wav_path)}"
