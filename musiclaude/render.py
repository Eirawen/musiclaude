"""
MusicXML → audio renderer with soundfont voice selection.

Decoupled from composition: the MusicXML just has instrument names,
this module picks the actual sound (soundfont + preset) per part and
renders via FluidSynth.

Usage:
    # With a voice map (agent-picked):
    render("output/score.musicxml", "output/score.mp3",
           voice_map={"Clarinet": "warm_expressive", "Piano": "warm_grand"})

    # With default voices (auto-picks from catalog):
    render("output/score.musicxml", "output/score.mp3")
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import music21

SOUNDFONTS_DIR = Path(__file__).parent.parent / "soundfonts"
CATALOG_PATH = SOUNDFONTS_DIR / "catalog.json"


def load_catalog() -> dict:
    """Load the soundfont catalog."""
    with open(CATALOG_PATH) as f:
        return json.load(f)


def _normalize_instrument_name(name: str) -> str:
    """Normalize a MusicXML part/instrument name to a catalog key.

    E.g. 'Clarinet in Bb' -> 'clarinet', 'Acoustic Grand Piano' -> 'piano'
    """
    name_lower = name.lower().strip()

    # Direct matches first
    direct_map = {
        "piano": "piano",
        "clarinet": "clarinet",
        "flute": "flute",
        "oboe": "oboe",
        "violin": "violin",
        "viola": "viola",
        "cello": "cello",
        "trumpet": "trumpet",
        "trombone": "trombone",
        "french horn": "french_horn",
        "horn": "french_horn",
        "harp": "harp",
        "celesta": "celesta",
        "timpani": "timpani",
        "harpsichord": "harpsichord",
        "organ": "organ",
        "guitar": "acoustic_guitar",
    }

    # Check substring matches
    for keyword, catalog_key in direct_map.items():
        if keyword in name_lower:
            return catalog_key

    # String ensemble detection
    if "string" in name_lower and ("ensemble" in name_lower or "section" in name_lower):
        return "strings_ensemble"

    return None


def _resolve_soundfont_path(sf_ref: str, catalog: dict) -> str:
    """Resolve a soundfont reference to an absolute path."""
    sf_info = catalog["soundfonts"][sf_ref]
    sf_file = sf_info["file"]

    # Absolute path (e.g. system-installed soundfonts)
    if os.path.isabs(sf_file):
        return sf_file

    return str(SOUNDFONTS_DIR / sf_file)


def _get_voice_config(instrument_name: str, voice_name: str | None, catalog: dict) -> dict | None:
    """Get the soundfont/bank/preset config for an instrument voice."""
    catalog_key = _normalize_instrument_name(instrument_name)
    if catalog_key is None:
        return None

    voices = catalog.get("voices", {}).get(catalog_key, {})
    if not voices:
        return None

    if voice_name and voice_name in voices:
        return voices[voice_name]

    # Default: pick the first voice
    return next(iter(voices.values()))


def get_part_names(musicxml_path: str) -> list[str]:
    """Extract part/instrument names from a MusicXML file."""
    score = music21.converter.parse(musicxml_path)
    names = []
    for part in score.parts:
        name = part.partName or f"Part {len(names) + 1}"
        names.append(name)
    return names


def list_voices(instrument: str | None = None) -> dict:
    """List available voices, optionally filtered by instrument.

    Returns dict of {instrument: {voice_name: description}}.
    """
    catalog = load_catalog()
    voices = catalog.get("voices", {})

    if instrument:
        key = _normalize_instrument_name(instrument)
        if key and key in voices:
            return {key: {k: v["description"] for k, v in voices[key].items()}}
        return {}

    return {
        inst: {k: v["description"] for k, v in inst_voices.items()}
        for inst, inst_voices in voices.items()
    }


def render(
    musicxml_path: str,
    output_path: str,
    voice_map: dict[str, str] | None = None,
    sample_rate: int = 44100,
    gain: float = 1.0,
) -> bool:
    """Render MusicXML to audio using FluidSynth with voice selection.

    Args:
        musicxml_path: Path to MusicXML file.
        output_path: Output path (.mp3 or .wav).
        voice_map: Dict mapping part names to voice names from catalog.
                   E.g. {"Clarinet in Bb": "warm_expressive", "Piano": "warm_grand"}
                   If None, uses first available voice for each instrument.
        sample_rate: Audio sample rate (default 44100).
        gain: FluidSynth gain multiplier (default 1.0).

    Returns:
        True if rendering succeeded.
    """
    voice_map = voice_map or {}
    catalog = load_catalog()

    # Parse MusicXML and get part info
    score = music21.converter.parse(musicxml_path)
    parts = list(score.parts)

    # Build per-channel voice assignments
    # MIDI channels 0-15, channel 9 is percussion (skip it)
    channel_assignments = []  # [(channel, soundfont_path, bank, preset)]
    available_channels = [c for c in range(16) if c != 9]

    for i, part in enumerate(parts):
        if i >= len(available_channels):
            print(f"Warning: too many parts ({len(parts)}), max 15 non-percussion. Skipping extra parts.")
            break

        channel = available_channels[i]
        part_name = part.partName or f"Part {i + 1}"

        # Look up voice from map
        voice_name = voice_map.get(part_name)

        # Also try fuzzy matching on the voice_map keys
        if voice_name is None:
            for map_key, map_voice in voice_map.items():
                if map_key.lower() in part_name.lower() or part_name.lower() in map_key.lower():
                    voice_name = map_voice
                    break

        voice_config = _get_voice_config(part_name, voice_name, catalog)

        if voice_config:
            sf_path = _resolve_soundfont_path(voice_config["soundfont"], catalog)
            bank = voice_config["bank"]
            preset = voice_config["preset"]
            print(f"  Part '{part_name}' → ch{channel}: {voice_config.get('description', voice_name)}")
        else:
            # Fallback to FluidR3 GM with standard GM program
            sf_path = _resolve_soundfont_path("FluidR3_GM", catalog)
            bank = 0
            # Try to get GM preset from instrument
            preset = _guess_gm_preset(part_name, catalog)
            print(f"  Part '{part_name}' → ch{channel}: FluidR3 GM preset {preset} (auto)")

        channel_assignments.append((channel, sf_path, bank, preset))

        # Set the MIDI channel on the part so the MIDI export uses it
        for el in part.recurse():
            if hasattr(el, 'channel'):
                el.channel = channel

    # Export MIDI
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp_midi:
        midi_path = tmp_midi.name

    mf = music21.midi.translate.streamToMidiFile(score)

    # Remap channels in the MIDI data
    for i, part in enumerate(parts):
        if i >= len(available_channels):
            break
        channel = available_channels[i]
        track_idx = i + 1  # Track 0 is typically metadata
        if track_idx < len(mf.tracks):
            for event in mf.tracks[track_idx].events:
                if hasattr(event, 'channel') and event.channel is not None:
                    event.channel = channel

    mf.open(midi_path, 'wb')
    mf.write()
    mf.close()

    # Render with FluidSynth
    wants_mp3 = output_path.lower().endswith('.mp3')
    wav_path = output_path if not wants_mp3 else output_path.rsplit('.', 1)[0] + '.wav'

    try:
        # Build FluidSynth command
        # Collect unique soundfonts needed
        unique_sfs = list(dict.fromkeys(sf for _, sf, _, _ in channel_assignments))

        # Use the primary soundfont (first one) for FluidSynth,
        # then use config commands to set up banks/presets per channel
        config_lines = []
        for channel, sf_path, bank, preset in channel_assignments:
            # Find which sfont ID this will be (1-indexed, in load order)
            sf_id = unique_sfs.index(sf_path) + 1
            config_lines.append(f"select {channel} {sf_id} {bank} {preset}")

        # Write FluidSynth config
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as cfg_file:
            cfg_path = cfg_file.name
            for line in config_lines:
                cfg_file.write(line + '\n')

        # Build command: load all soundfonts, apply config, render
        cmd = [
            "fluidsynth",
            "-ni",  # non-interactive, no MIDI input
            "-g", str(gain),
            "-r", str(sample_rate),
            "-F", wav_path,  # render to file
        ]

        # Add all unique soundfonts
        for sf in unique_sfs:
            cmd.append(sf)

        # Add MIDI file and config
        cmd.append(midi_path)

        print(f"  Rendering with {len(unique_sfs)} soundfont(s)...")

        # FluidSynth doesn't have a config file flag for `select` commands,
        # so we pipe them via stdin before the MIDI plays
        # Actually, we use -f for loading config
        # Let's use the approach of loading config via -f
        # But -f runs commands, not selects...
        # The cleanest way: use fluidsynth with stdin

        result = subprocess.run(
            cmd,
            input='\n'.join(config_lines) + '\n',
            capture_output=True,
            text=True,
            timeout=120,
        )

        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            print(f"  FluidSynth error: {result.stderr[:500]}")
            return False

        # Convert to MP3 if needed
        if wants_mp3:
            mp3_result = subprocess.run(
                ["lame", "--quiet", "-V2", wav_path, output_path],
                capture_output=True,
                text=True,
                timeout=60,
            )
            os.unlink(wav_path)
            if not os.path.exists(output_path):
                print(f"  LAME error: {mp3_result.stderr[:500]}")
                return False

        print(f"  Done: {output_path}")
        return True

    finally:
        # Cleanup temp files
        if os.path.exists(midi_path):
            os.unlink(midi_path)
        if 'cfg_path' in locals() and os.path.exists(cfg_path):
            os.unlink(cfg_path)


def _guess_gm_preset(part_name: str, catalog: dict) -> int:
    """Guess a General MIDI preset number from a part name."""
    gm_map = catalog.get("gm_instrument_map", {})

    # Try exact match first
    if part_name in gm_map:
        return gm_map[part_name]

    # Try substring match
    name_lower = part_name.lower()
    for gm_name, preset in gm_map.items():
        if gm_name.lower() in name_lower or name_lower in gm_name.lower():
            return preset

    # Common keyword fallbacks
    keyword_presets = {
        "piano": 0, "clarinet": 71, "flute": 73, "oboe": 68,
        "violin": 40, "viola": 41, "cello": 42, "bass": 43,
        "trumpet": 56, "trombone": 57, "horn": 60, "tuba": 58,
        "guitar": 24, "harp": 46, "organ": 19, "timpani": 47,
    }
    for keyword, preset in keyword_presets.items():
        if keyword in name_lower:
            return preset

    return 0  # Default to piano


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python -m musiclaude.render <input.musicxml> <output.mp3> [voice_map.json]")
        print("\nAvailable voices:")
        for inst, voices in list_voices().items():
            print(f"\n  {inst}:")
            for name, desc in voices.items():
                print(f"    {name}: {desc}")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    vm = None
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            vm = json.load(f)

    print(f"Parts in {input_path}:")
    for name in get_part_names(input_path):
        print(f"  - {name}")
    print()

    success = render(input_path, output_path, voice_map=vm)
    sys.exit(0 if success else 1)
