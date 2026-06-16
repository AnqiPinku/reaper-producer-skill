# REAPER Producer Skill

[![CI](https://github.com/AnqiPinku/reaper-producer-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/AnqiPinku/reaper-producer-skill/actions/workflows/ci.yml)

A Codex skill for using REAPER through MCP as a cautious music-production assistant.

This repository does not train a music model and does not replace REAPER. It gives Codex a practical workflow for controlling an already configured REAPER MCP server: inspect the project, plan safe edits, call REAPER tools, verify results, and keep destructive operations behind confirmation.

## What It Does

- Guides Codex to use the configured `reaper` MCP server safely.
- Encourages `reaper_status()` before write operations.
- Resolves track names to current track indices before index-based edits.
- Requires confirmation for deletion, overwrite, render, record, and large batch edits.
- Maps common music-production feedback to proportional REAPER actions.
- Provides an on-demand instrument-template workflow for Kontakt, samplers, and VSTi libraries.
- Includes simple eval scenarios for checking whether the assistant is behaving safely.

## What It Does Not Do

- It does not include Kontakt instruments, samples, presets, or commercial content.
- It does not directly load `.nki` files inside Kontakt through fragile plugin UI automation.
- It does not require users to convert an entire instrument library into templates.
- It does not replace the REAPER MCP server; it is a workflow layer on top of a configured REAPER MCP server.

## Requirements

- REAPER.
- [REAPER MCP v2](https://github.com/AnqiPinku/reaper-mcp-v2), registered as `reaper`.
- Codex with skills enabled.

The skill assumes a `reaper` MCP server is available. With [REAPER MCP v2](https://github.com/AnqiPinku/reaper-mcp-v2), the usual path is:

1. Run `reaper_mcp_bridge.lua` inside REAPER.
2. Configure Codex MCP with `server/reaper_mcp_server.py`.
3. Use an ASCII path for the MCP server command/cwd on Windows when possible.
4. Keep the default IPC mailbox at `%APPDATA%\reaper-mcp-ipc`, or set `REAPER_MCP_IPC_DIR` on both sides.

## 🤖 Install with your coding agent

Tell your agent (Codex, Claude Code, …):

> Install the REAPER Producer skill from https://github.com/AnqiPinku/reaper-producer-skill — read AGENTS.md and follow it.

It will clone the repo and run the installer. Note this skill needs the [REAPER MCP v2](https://github.com/AnqiPinku/reaper-mcp-v2) server installed first. See [AGENTS.md](AGENTS.md), or follow the manual steps below.

## Install

### Windows

Clone the repository and run the installer:

```powershell
git clone https://github.com/AnqiPinku/reaper-producer-skill.git
Set-Location -LiteralPath .\reaper-producer-skill
.\install\install_skill.ps1
```

If you already cloned the repository, run this from the repository root:

```powershell
.\install\install_skill.ps1
```

### macOS / Linux

Clone the repository and run the installer:

```bash
git clone https://github.com/AnqiPinku/reaper-producer-skill.git
cd reaper-producer-skill
bash install/install_skill.sh
```

If you already cloned the repository, run this from the repository root:

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
python ~/.codex/skills/reaper-producer/scripts/check_reaper_mcp.py
```

On Windows PowerShell, for example:

```powershell
python -X utf8 "$env:USERPROFILE\.codex\skills\reaper-producer\scripts\check_reaper_mcp.py"
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
python skills/reaper-producer/scripts/insert_instrument_template.py grand_piano --registry instruments.json
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

## Credits

Designed to work with [REAPER MCP v2](https://github.com/AnqiPinku/reaper-mcp-v2), whose bridge design derives from [TwelveTake-Studios/reaper-mcp](https://github.com/TwelveTake-Studios/reaper-mcp) (MIT). REAPER is a trademark of Cockos Incorporated; this is an independent, unofficial project, not affiliated with or endorsed by Cockos Incorporated or TwelveTake Studios.

## License

MIT. This repository contains workflow instructions and helper scripts only. It does not include third-party instrument content.
