from pathlib import Path
import yaml

def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")

    with path.open("r") as f:
        return yaml.safe_load(f)
