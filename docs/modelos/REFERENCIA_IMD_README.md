# Product README layout (reference)

Structure used for embedded products (example: Insulation Monitoring Device firmware).

Typical top-level sections:

1. `# Firmware` — one-line product purpose  
2. `# Specifications` — bullet list of capabilities and standards  
3. `# Communication Protocol` — bus defaults, tables (baud, parity, unit ID)  
4. `## Registers` — address map with permissions (`r`, `w`, `s`)  
5. `## Modes` / `## Status` — bit masks or mode codes  
6. `# Versions` / `## Current changes` / `# TODO`

Stock Tracker equivalent: [`../PROJETO_STOCKTRACKER.md`](../PROJETO_STOCKTRACKER.md)  
(Excel columns instead of Modbus registers; REST APIs instead of RS-485.)
