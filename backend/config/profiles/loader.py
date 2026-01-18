import os
import yaml


PROFILES_DIR = os.getenv("PROFILES_DIR", "profiles")


class ProfileError(Exception):
    pass


def load_profile(profile_name: str) -> dict:
    profile_path = os.path.join(PROFILES_DIR, f"{profile_name}.yaml")

    if not os.path.exists(profile_path):
        raise ProfileError(f"Profile not found: {profile_name}")

    with open(profile_path, "r") as f:
        data = yaml.safe_load(f)

    _validate_profile(data)
    return data


def _validate_profile(profile: dict):
    required_top = {"profile", "desc", "type", "tools"}

    if not isinstance(profile, dict):
        raise ProfileError("Profile must be a YAML mapping")

    missing = required_top - profile.keys()
    if missing:
        raise ProfileError(f"Missing profile fields: {missing}")

    if not isinstance(profile["tools"], list):
        raise ProfileError("Profile tools must be a list")

    for tool in profile["tools"]:
        _validate_tool(tool)


def _validate_tool(tool: dict):
    required_tool = {"name", "enabled", "info", "args", "output", "regex"}

    missing = required_tool - tool.keys()
    if missing:
        raise ProfileError(f"Missing tool fields: {missing}")

    if not isinstance(tool["args"], list):
        raise ProfileError("Tool args must be a list")

    if "type" not in tool["output"]:
        raise ProfileError("Tool output.type is required")
