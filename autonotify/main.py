import asyncio
import signal
import sys
from pathlib import Path
from .config import load_config
from .logger import get_logger
from .monitor import run_checks
from .notifier import build_notifiers, alert

log = get_logger(__name__)

class AutoNotifyApp:
    def __init__(self, cfg_path: Path = None):
        self.cfg_path = cfg_path or Path(__file__).parent.parent / "config" / "config.yaml"
        self.cfg = load_config(self.cfg_path)
        self.notifiers = build_notifiers(self.cfg)
        self.interval = self.cfg.get("monitor", {}).get("interval_seconds", 30)
        self.checks = self.cfg.get("monitor", {}).get("checks", [])
        self.shutdown = asyncio.Event()
        signal.signal(signal.SIGHUP, self.handle_reload)
        signal.signal(signal.SIGINT, self.handle_stop)
        signal.signal(signal.SIGTERM, self.handle_stop)

    def handle_reload(self, *_):
        log.info("Reloading configuration due to SIGHUP")
        try:
            self.cfg = load_config(self.cfg_path)
            self.notifiers = build_notifiers(self.cfg)
            self.interval = self.cfg.get("monitor", {}).get("interval_seconds", 30)
            self.checks = self.cfg.get("monitor", {}).get("checks", [])
            log.info("Configuration reloaded successfully")
        except Exception as exc:
            log.error("Failed to reload configuration: %s", exc)

    def handle_stop(self, *_):
        log.info("Shutdown signal received, stopping…")
        self.shutdown.set()

    async def monitor_loop(self):
        while not self.shutdown.is_set():
            try:
                results = await run_checks(self.checks)
                failures = [r for r in results if not r["healthy"]]
                if failures:
                    log.warning("%d check(s) failed", len(failures))
                    alert(self.notifiers, failures)
                else:
                    log.info("All checks passed")
            except Exception as exc:
                log.exception("Unexpected error during monitoring loop: %s", exc)
            await asyncio.wait([self.shutdown.wait()], timeout=self.interval)

    async def run(self):
        await self.monitor_loop()

def main():
    app = AutoNotifyApp()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        log.info("Interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
