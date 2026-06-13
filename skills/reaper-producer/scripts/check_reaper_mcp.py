#!/usr/bin/env python3
"""Check the TwelveTake REAPER MCP file bridge without third-party packages."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


def default_bridge_dir() -> str:
    env_value = os.environ.get("REAPER_BRIDGE_DIR")
    if env_value:
        return env_value

    candidates = []
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(str(Path(appdata) / "REAPER" / "Scripts" / "mcp_bridge_data"))
    candidates.extend(
        [
            os.path.expanduser(r"~/Library/Application Support/REAPER/Scripts/mcp_bridge_data"),
            os.path.expanduser(r"~/.config/REAPER/Scripts/mcp_bridge_data"),
        ]
    )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return candidates[0] if candidates else "mcp_bridge_data"


def call_bridge(bridge_dir: Path, func: str, args: list, timeout: float) -> dict:
    bridge_dir.mkdir(parents=True, exist_ok=True)
    slot = (int(time.time() * 1000) + os.getpid()) % 999 + 1
    for offset in range(999):
        candidate = (slot + offset - 1) % 999 + 1
        request_file = bridge_dir / f"request_{candidate}.json"
        response_file = bridge_dir / f"response_{candidate}.json"
        if not request_file.exists() and not response_file.exists():
            break
    else:
        return {"ok": False, "error": "no_free_request_slot"}

    response_file.unlink(missing_ok=True)
    request_file.write_text(json.dumps({"func": func, "args": args}), encoding="utf-8")

    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            if response_file.exists():
                text = response_file.read_text(encoding="utf-8").strip()
                if text:
                    return json.loads(text)
            time.sleep(0.05)
        return {"ok": False, "error": "timeout"}
    finally:
        request_file.unlink(missing_ok=True)
        response_file.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check REAPER MCP bridge health.")
    parser.add_argument(
        "--bridge-dir",
        default=default_bridge_dir(),
        help="Bridge directory. Defaults to REAPER_BRIDGE_DIR, then common REAPER locations.",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    bridge_dir = Path(args.bridge_dir)
    print(f"Bridge dir: {bridge_dir}")

    checks = [
        ("CountTracks", [0], "track_count"),
        ("Master_GetTempo", [], "tempo"),
        ("GetUndoState", [], "undo_state"),
    ]

    ok = True
    for func, call_args, label in checks:
        result = call_bridge(bridge_dir, func, call_args, args.timeout)
        status = "PASS" if result.get("ok") else "FAIL"
        print(f"{status} {label}: {json.dumps(result, ensure_ascii=False)}")
        ok = ok and bool(result.get("ok"))

    if not ok:
        print("REAPER bridge is not responding. Open REAPER and run reaper_mcp_bridge.lua.")
        return 1

    print("REAPER MCP bridge is responding.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
