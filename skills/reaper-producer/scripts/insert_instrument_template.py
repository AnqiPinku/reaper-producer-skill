#!/usr/bin/env python3
"""Insert a registered REAPER track template through the TwelveTake file bridge."""

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


def expand_path(value: str, variables: dict[str, str]) -> Path:
    expanded = value
    for key, replacement in variables.items():
        expanded = expanded.replace("${" + key + "}", replacement)
    return Path(expanded).expanduser()


def find_instrument(registry: dict, instrument_id: str) -> dict | None:
    query = instrument_id.strip().lower()
    for inst in registry.get("instruments", []):
        if inst.get("id", "").lower() == query:
            return inst
        aliases = [str(alias).lower() for alias in inst.get("aliases", [])]
        if query in aliases:
            return inst
    return None


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
    try:
        deadline = time.time() + timeout
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
    parser = argparse.ArgumentParser(description="Insert a registered REAPER instrument track template.")
    parser.add_argument("instrument", help="Instrument id or alias from the registry.")
    parser.add_argument("--registry", default="instruments.json", help="Instrument registry path.")
    parser.add_argument("--bridge-dir", default=default_bridge_dir(), help="TwelveTake file bridge directory.")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        help="Variable expansion KEY=VALUE, e.g. REAPER_RESOURCE_PATH=C:\\Users\\me\\AppData\\Roaming\\REAPER",
    )
    args = parser.parse_args()

    registry_path = Path(args.registry)
    if not registry_path.exists():
        print(f"Registry not found: {registry_path}", file=sys.stderr)
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    variables = {}
    for item in args.var:
        if "=" not in item:
            print(f"--var must be KEY=VALUE, got: {item}", file=sys.stderr)
            return 1
        key, value = item.split("=", 1)
        variables[key] = value

    inst = find_instrument(registry, args.instrument)
    if not inst:
        print(f"Instrument not found in registry: {args.instrument}", file=sys.stderr)
        return 1

    template_path = expand_path(inst["template_path"], variables)
    if template_path.suffix != ".RTrackTemplate":
        print(f"Refusing non-track-template path: {template_path}", file=sys.stderr)
        return 1
    if not template_path.exists():
        print(f"Track template not found: {template_path}", file=sys.stderr)
        return 1

    result = call_bridge(Path(args.bridge_dir), "Main_openProject", [str(template_path)], args.timeout)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
