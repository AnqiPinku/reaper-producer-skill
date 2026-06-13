# REAPER MCP Tool Map

Use this reference when selecting TwelveTake REAPER MCP tools. Prefer project-aware, reversible, high-level workflows over scattered low-level calls.

## First Call

Use `get_project_summary()` first for almost every production task. It should provide track count, names, volumes, pans, FX, markers, regions, tempo, and time signature.

Fallback read-only calls:

- `get_all_tracks`
- `get_track_count`
- `get_track`
- `get_master_track`
- `get_tempo`
- `get_time_signature`
- `get_markers`
- `get_regions`
- `get_selected_tracks`
- `get_selected_items`
- `get_undo_state`

## Track Operations

Preferred flow for creating a track:

1. `insert_track(index, name)`
2. `set_track_name(track_index, name)` if needed
3. `set_track_color(track_index, r, g, b)`
4. `set_track_volume(track_index, volume_db)`
5. `set_track_pan(track_index, pan)`

Use `get_all_tracks` after creation to confirm the index and name.

For edits, always resolve the current track index from state by track name. Do not assume indices from old context.

## MIDI Operations

Preferred flow for a new MIDI part:

1. Resolve track index by name.
2. `create_midi_item(track_index, position, length)`
3. `add_midi_notes_batch(track_index, item_index, notes)`
4. `get_midi_notes(track_index, item_index)` if verification is needed.

Use beat-based timing when available. Keep clips aligned to bar boundaries unless the user asks for loose timing.

Use `clear_midi_item` only after confirmation unless the user explicitly asked to replace that item.

## FX Operations

Preferred flow:

1. `track_fx_get_list(track_index)`
2. `track_fx_add_by_name(track_index, fx_name, position)` if missing
3. `track_fx_get_num_params`
4. `track_fx_get_param_name` to discover parameter indices
5. `track_fx_set_param` for targeted changes

For stock REAPER plugins, prefer:

- `ReaEQ`
- `ReaComp`
- `ReaDelay`
- `ReaVerbate`
- `ReaSynth`
- `ReaSamplOmatic5000`
- `JS: Saturation`

Do not use `track_fx_delete` or `take_fx_delete` without confirmation. Prefer bypassing with `track_fx_set_enabled(..., false)` when testing.

## Routing And Buses

Use high-level helpers when possible:

- `create_bus`
- `create_send`
- `set_send_volume`
- `setup_sidechain_send`
- `setup_sidechain_compression`
- `add_parallel_compression`

For sidechain compression, prefer `setup_sidechain_compression(trigger_track, target_track, compressor_fx_index, send_volume_db)` when a ReaComp exists on the target. If no compressor exists, add ReaComp first.

## Mixing Helpers

Use these when the request maps clearly to the helper:

- `add_eq`
- `add_compressor`
- `add_limiter`
- `add_mastering_chain`
- `add_parallel_compression`

Keep helper use transparent: summarize the created FX, sends, and likely parameters afterward.

## Audio Items

For importing audio:

1. Confirm the path if it is outside an obvious workspace/sample directory.
2. `insert_audio_file`
3. `set_item_position`
4. `set_item_length` or fade tools if needed.
5. `set_item_volume`

Do not assume automatic tempo warping. First versions should align start positions and report that advanced warping was not performed unless the tool explicitly supports it.

## Rendering

`render_project` can overwrite files depending on REAPER render settings. Confirm:

- output path
- time range
- whether overwrite is acceptable
- whether tails are needed

Use `render_region` cautiously: in the current TwelveTake code it may return an "not yet implemented" explanatory error.

## Dangerous Tools

Require explicit confirmation before these:

- `delete_track`
- `delete_item`
- `delete_selected_items`
- `delete_take`
- `delete_marker`
- `delete_region`
- `delete_send`
- `track_fx_delete`
- `take_fx_delete`
- `clear_midi_item`
- `clear_envelope`
- `clear_fx_envelope`
- `cut_selected_items`
- `save_project`
- `open_project`
- `render_project`
- `record`
- broad `run_action`
- broad `run_action_by_name`

## Safer Substitutions

- Delete track -> mute track or ask confirmation.
- Delete FX -> bypass FX first.
- Replace MIDI item -> duplicate or ask confirmation before clearing.
- Open different project -> ask confirmation and warn about unsaved work.
- Render -> ask for output path and overwrite confirmation.
- Broad action command -> describe exact REAPER action and ask confirmation.
