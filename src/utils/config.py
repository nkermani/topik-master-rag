"""Configuration loader for TOPIK Master RAG."""
import yaml
from pathlib import Path


class Config:
    """Load and manage configuration settings."""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config_path = Path(config_path)
        self._config = self._load()

    def _load(self) -> dict:
        """Load YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default=None):
        """Get configuration value by dot notation key."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value
