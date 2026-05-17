import yaml
import os
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.yaml"


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """Load YAML configuration, merging environment overrides.

    Environment variables can override any scalar value using the syntax
    `AUTONOTIFY_<SECTION>_<KEY>`. Example: `AUTONOTIFY_NOTIFICATIONS_TELEGRAM_TOKEN`.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    # Apply env overrides
    prefix = "AUTONOTIFY_"
    for env_key, env_val in os.environ.items():
        if not env_key.startswith(prefix):
            continue
        # Transform ``AUTONOTIFY_NOTIFICATIONS_TELEGRAM_TOKEN`` -> cfg['notifications']['telegram']['token']
        parts = env_key[len(prefix):].lower().split("_")
        sub_cfg = cfg
        for part in parts[:-1]:
            sub_cfg = sub_cfg.setdefault(part, {})
        sub_cfg[parts[-1]] = env_val
    return cfg
