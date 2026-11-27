# Agent Plugins schemas

Snapshots obtained on 2026-11-27 from the official Agent Plugins 1.0.0 specification:

| File | Source | SHA-256 |
|---|---|---|
| plugin.schema.json | https://agent-plugins.org/schemas/1.0.0/plugin.schema.json | 0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883 |
| mcp.schema.json | https://agent-plugins.org/schemas/1.0.0/mcp.schema.json | 6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb |

They are stored unchanged to make PR checks independent of the schema host.
`package.py` validates the manifest and the standard MCP projection against these snapshots.
The published MCP configuration has one explicit OpenAI extension and is **not** claimed to pass the strict MCP schema.
Only that exact extension is allowed by the source checker; the Vibe artifact removes it and passes the strict schema.

