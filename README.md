# REAPER Producer Skill

A Codex skill for using REAPER through MCP as a cautious music-production assistant.

This repository does not train a music model and does not replace REAPER. It gives Codex a practical workflow for controlling an already configured REAPER MCP server: inspect the project, plan safe edits, call REAPER tools, verify results, and keep destructive operations behind confirmation.

## What It Does

- Guides Codex to use the configured `reaper` MCP server safely.
- Encourages `get_project_summary()` before write operations.
- Resolves track names to current track indices before index-based edits.
- Requires confirmation for deletion, overwrite, render, record, and large batch edits.
- Maps common music-production feedback to proportional REAPER actions.
- Provides an on-demand instrument-template workflow for Kontakt, samplers, and VSTi libraries.
- Includes simple eval scenarios for checking whether the assistant is behaving safely.

## What It Does Not Do

- It does not include Kontakt instruments, samples, presets, or commercial content.
- It does not directly load `.nki` files inside Kontakt through fragile plugin UI automation.
- It does not require users to convert an entire instrument library into templates.
- It does not replace TwelveTake REAPER MCP; it is a workflow layer on top of a REAPER MCP server.

## Requirements

- REAPER.
- A working REAPER MCP server named `reaper`.
- Recommended: [TwelveTake-Studios/reaper-mcp](https://github.com/TwelveTake-Studios/reaper-mcp).
- Codex with skills enabled.

The skill assumes a `reaper` MCP server is available. With TwelveTake REAPER MCP, the usual path is:

1. Run `reaper_mcp_bridge.lua` inside REAPER.
2. Configure Codex MCP with the TwelveTake Python server.
3. Set `REAPER_COMM_MODE=file`.
4. Set `REAPER_BRIDGE_DIR` to the bridge directory used by the REAPER bridge.

## Install

### Windows

From this repository root:

```powershell
.\install\install_skill.ps1
```

### macOS / Linux

From this repository root:

```bash
bash install/install_skill.sh
```

The installer copies `skills/reaper-producer` into:

```text
~/.codex/skills/reaper-producer
```

Restart Codex or start a new thread after installation.

## Quick Test

Ask Codex:

```text
Use $reaper-producer to inspect the current REAPER project. Read-only only.
```

Expected behavior:

- Codex should use the `reaper` MCP server.
- It should inspect the project first.
- It should not modify the project.

If the bridge is not responding, run:

```bash
python ~/.codex/skills/reaper-producer/scripts/check_reaper_mcp.py --bridge-dir PATH_TO_MCP_BRIDGE_DATA
```

On Windows PowerShell, for example:

```powershell
python -X utf8 "$env:USERPROFILE\.codex\skills\reaper-producer\scripts\check_reaper_mcp.py" --bridge-dir "REDACTED"
```

## Instrument Loading

Kontakt and many sampler plugins do not reliably expose "load this instrument" as a normal REAPER FX parameter. The stable workflow is:

```text
requested instrument
-> registered REAPER track template
-> insert template
-> write MIDI / mix / arrange
```

Users do not need to template their whole library. Register instruments on demand:

1. Ask for an instrument, for example "Grand Piano".
2. If no template exists, create a track and load that one instrument manually in Kontakt or another plugin.
3. Save that track as a REAPER track template.
4. Add it to the instrument registry.
5. Next time, Codex can insert the template directly.

See:

- `skills/reaper-producer/references/instrument-loading.md`
- `examples/instruments.example.json`
- `schemas/instrument-registry.schema.json`

## Instrument Registry Helpers

Scan a directory of `.RTrackTemplate` files and generate a starter registry:

```bash
python skills/reaper-producer/scripts/scan_reaper_templates.py --templates-root "/path/to/REAPER/TrackTemplates" --output instruments.generated.json
```

Validate a registry:

```bash
python skills/reaper-producer/scripts/validate_instrument_registry.py examples/instruments.example.json
```

Insert a registered track template into the live REAPER project:

```bash
python skills/reaper-producer/scripts/insert_instrument_template.py grand_piano --registry instruments.json --bridge-dir PATH_TO_MCP_BRIDGE_DATA
```

`insert_instrument_template.py` modifies the open REAPER project by inserting a `.RTrackTemplate`. Use it only when REAPER is open and the bridge is running.

## Safety Model

The skill tells Codex to:

- read state before writes,
- verify after writes,
- avoid raw scripting when MCP tools can do the job,
- keep edits targeted,
- confirm destructive operations,
- avoid fragile plugin browser UI automation,
- prefer reversible DAW-native operations.

## Repository Layout

```text
skills/reaper-producer/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
examples/
schemas/
install/
```

## License

MIT. This repository contains workflow instructions and helper scripts only. It does not include third-party instrument content.

