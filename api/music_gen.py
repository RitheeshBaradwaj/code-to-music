import os
import pretty_midi
import random
import subprocess
from mingus.core import scales, chords
from .scale_info import get_scale_notes

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SOUNDFONT_PATH = os.path.join(PROJECT_ROOT, "soundfonts", "FluidR3_GM.sf2")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_music_from_mood_map(mood_map: dict) -> str:
    """
    Generates a MIDI and WAV file from a musical mood map.
    """
    tempo = mood_map.get("tempo", 120)
    scale_name = mood_map.get("scale", "C major")
    instruments = mood_map.get("instruments", ["Acoustic Grand Piano"])

    # Get the notes in the scale
    try:
        key, scale_type = scale_name.split()
        notes_in_scale = get_scale_notes(key, scale_type)
    except ValueError:
        notes_in_scale = get_scale_notes("C", "major")

    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)

    for instrument_name in instruments:
        instrument_program = pretty_midi.instrument_name_to_program(instrument_name)
        instrument = pretty_midi.Instrument(program=instrument_program)

        # Generate a simple melody
        current_time = 0.0
        for _ in range(32):
            note_name = random.choice(notes_in_scale)
            note_number = pretty_midi.note_name_to_number(note_name)
            note = pretty_midi.Note(
                velocity=random.randint(80, 110),
                pitch=note_number,
                start=current_time,
                end=current_time + 0.5,
            )
            instrument.notes.append(note)
            current_time += 0.5

        midi.instruments.append(instrument)

    midi_path = os.path.join(OUTPUT_DIR, "result.mid")
    wav_path = os.path.join(OUTPUT_DIR, "result.wav")

    midi.write(midi_path)
    return convert_midi_to_wav(midi_path, wav_path)


def convert_midi_to_wav(midi_path: str, wav_path: str) -> str:
    """
    Converts a MIDI file to a WAV file using fluidsynth.
    """
    if not os.path.exists(SOUNDFONT_PATH):
        raise FileNotFoundError(f"Soundfont not found at: {SOUNDFONT_PATH}")

    result = subprocess.run(
        ["fluidsynth", "-ni", SOUNDFONT_PATH, midi_path, "-F", wav_path, "-r", "44100"],
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"fluidsynth failed:\n{result.stderr.decode()}")

    return f"output/{os.path.basename(wav_path)}"
