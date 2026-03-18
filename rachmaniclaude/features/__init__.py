"""Feature extraction from MusicXML files."""

from rachmaniclaude.features.harmonic import extract_harmonic_features
from rachmaniclaude.features.melodic import extract_melodic_features
from rachmaniclaude.features.structural import extract_structural_features
from rachmaniclaude.features.orchestration import extract_orchestration_features
from rachmaniclaude.features.extract import extract_features_from_file, extract_features_from_directory

__all__ = [
    "extract_harmonic_features",
    "extract_melodic_features",
    "extract_structural_features",
    "extract_orchestration_features",
    "extract_features_from_file",
    "extract_features_from_directory",
]
