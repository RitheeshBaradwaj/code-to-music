from mingus.core import scales

def get_scale_notes(key: str, scale_type: str) -> list[str]:
    """
    Returns the notes of a given scale.
    """
    scale_type = scale_type.lower()
    if scale_type == "major":
        return scales.Major(key).ascending()
    elif scale_type == "minor":
        return scales.NaturalMinor(key).ascending()
    elif scale_type == "dorian":
        return scales.Dorian(key).ascending()
    elif scale_type == "phrygian":
        return scales.Phrygian(key).ascending()
    elif scale_type == "lydian":
        return scales.Lydian(key).ascending()
    elif scale_type == "mixolydian":
        return scales.Mixolydian(key).ascending()
    elif scale_type == "locrian":
        return scales.Locrian(key).ascending()
    else:
        return scales.Major(key).ascending()
