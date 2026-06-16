# Agent install guide — REAPER Producer skill

This file tells a coding agent (Codex, Claude Code, …) how to install this skill
from scratch. Follow the steps in order.

Steps marked **[ask the user]** require a manual action you cannot perform
yourself — pause, ask the user, and confirm before continuing.

## What this is

A Codex **skill** that layers a cautious REAPER music-production workflow on top
of an already-configured `reaper` MCP server. It is NOT the MCP server itself
and does not control REAPER on its own.

## Prerequisite (install this FIRST)

This skill requires the `reaper` MCP server from
**https://github.com/AnqiPinku/reaper-mcp-v2**, already installed and registered
as `reaper`. If it is not present, install that project first by reading its
`AGENTS.md`, then come back here.

## Install steps

1. Clone:
   ```bash
   git clone https://github.com/AnqiPinku/reaper-producer-skill
   cd reaper-producer-skill
   ```
2. Run the installer for the user's OS:
   - **Windows (PowerShell):** `./install/install_skill.ps1`
   - **macOS / Linux:** `bash install/install_skill.sh`

   It copies `skills/reaper-producer` into `~/.codex/skills/reaper-producer`.
3. **[ask the user]** Restart Codex or start a new thread so the skill is loaded.
4. Verify: the `reaper-producer` skill should now be available in Codex, and
   asking it to use `reaper_status` should reach REAPER (via the prerequisite
   MCP server).

## Notes

- Keep the IPC mailbox at the default `%APPDATA%\reaper-mcp-ipc`, or set
  `REAPER_MCP_IPC_DIR` on both the server and bridge sides.
- Requires REAPER and Codex with skills enabled.
- Skill behavior and safety rules are in `skills/reaper-producer/SKILL.md`;
  deeper references live under `skills/reaper-producer/references/`.
