import asyncio
import aiohttp
import socket
from typing import Dict, List, Any
from .logger import get_logger

log = get_logger(__name__)

async def http_check(url: str, expected_status: int = 200, timeout: int = 10) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as resp:
                ok = resp.status == expected_status
                if not ok:
                    log.debug("HTTP check failed: %s returned %s (expected %s)", url, resp.status, expected_status)
                return ok
    except Exception as exc:
        log.debug("HTTP check exception for %s: %s", url, exc)
        return False

def tcp_check(host: str, port: int, timeout: int = 5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception as exc:
        log.debug("TCP check failed for %s:%s – %s", host, port, exc)
        return False

CHECK_FUNCS = {
    "http": http_check,
    "tcp": tcp_check,
}

async def run_checks(checks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for chk in checks:
        name = chk.get("name", "unnamed")
        typ = chk.get("type")
        func = CHECK_FUNCS.get(typ)
        if func is None:
            log.warning("Unsupported check type %s for %s", typ, name)
            continue
        log.info("Running %s check: %s", typ, name)
        if typ == "http":
            ok = await func(
                url=chk["url"],
                expected_status=chk.get("expected_status", 200),
                timeout=chk.get("timeout", 10),
            )
        else:  # tcp
            ok = func(
                host=chk["host"],
                port=chk["port"],
                timeout=chk.get("timeout", 5),
            )
        results.append({"name": name, "type": typ, "healthy": ok})
    return results
