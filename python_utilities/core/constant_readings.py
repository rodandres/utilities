from pathlib import Path
from .core_utilities import load_yaml


_BASE_DIR = Path(__file__).parents[2]

_DATA_DIR = _BASE_DIR / "general"
#_DATA_DIR = Path("/general")

_constants_data = load_yaml(_DATA_DIR / "physical_constants.yaml")
_conversions_data = load_yaml(_DATA_DIR / "physical_conversions.yaml")


class Constants:
    """Read-only access to physical and mathematical constants."""

    @staticmethod
    def get(*keys):
        node = _constants_data
        for k in keys:
            node = node[k]
        return node["value"]


class Conversions:
    """Unit conversion utilities."""

    @staticmethod
    def factor(*keys):
        node = _conversions_data
        for k in keys:
            node = node[k]
        return node["factor"]

    @staticmethod
    def convert(value, *keys):
        node = _conversions_data
        for k in keys:
            node = node[k]

        factor = node["factor"]
        offset = node.get("offset", 0.0)

        return value * factor + offset