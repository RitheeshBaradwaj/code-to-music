import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_mood_map_from_metrics(metrics: dict) -> dict:
    """
    Generates a musical mood map from C++ code metrics using an AI agent.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = _create_prompt(metrics)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative musical expert."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        mood_map = json.loads(response.choices[0].message.content)
        return mood_map

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {
            "mood": "Error",
            "tempo": 120,
            "scale": "C major",
            "instruments": ["piano"],
            "tags": ["error"],
        }


def _create_prompt(metrics: dict) -> str:
    """
    Creates a detailed prompt for the AI agent based on aggregated C++ metrics.
    """
    prompt = f"""
    Analyze the following C++ code metrics to generate a 'musical mood map'.
    Your response must be a JSON object with the following keys:
    - "mood": A single, evocative word (e.g., "chaotic", "serene", "mysterious").
    - "tempo": A suggested BPM (e.g., 80, 120, 160).
    - "scale": A musical scale (e.g., "C# minor", "F major", "G Dorian").
    - "instruments": A list of 2-4 instruments (e.g., ["violin", "piano", "drums"]).
    - "tags": A list of descriptive tags (e.g., ["suspenseful", "minimalist", "aggressive"]).

    Metrics:
    - Total Lines: {metrics.get('total_lines', 0)}
    - Total Files: {metrics.get('total_files', 0)}
    - Functions: {metrics.get('functions', 0)}
    - Classes: {metrics.get('classes', 0)}
    - Structs: {metrics.get('structs', 0)}
    - Loops: {metrics.get('loops', 0)}
    - Conditionals: {metrics.get('conditionals', 0)}
    - Cyclomatic Complexity: {metrics.get('cyclomatic_complexity', 0)}

    Based on these metrics, generate a musical mood map that reflects the code's structure and complexity.
    For example, high complexity might suggest a "chaotic" mood, faster tempo, and a minor key.
    Low complexity might suggest a "calm" mood, slower tempo, and a major key.
    Be creative and consistent.
    """
    return prompt
