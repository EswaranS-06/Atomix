import yaml
from pathlib import Path


PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles"


def load_profile(profile_name: str) -> dict:
    profile_path = PROFILES_DIR / f"{profile_name}.yaml"

    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_name}")

    with open(profile_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
