# Popups Siemens (Qt Designer)

Ficheiros **completos** para ver e editar no Qt Designer (formulário, tabela, botões).

| Ficheiro | Conteúdo visível no Designer |
|----------|----------------------------|
| `gui_popup_manual.ui` | Formulário (refs, stock) + Save/Cancel |
| `gui_popup_history.ui` | Tabela de histórico + Close |
| `gui_popup_search.ui` | Tabela de resultados + Ok/Cancel |
| `gui_popup_template.ui` | Template Siemens original (só título + descrição) |

**Em execução** a app usa `popup_shell.py` + `gui_popup.ui` (widgets extra em Python).

Regenerar:

```text
python tools/generate_popup_uis.py
powershell -File tools\prepare-designer-desktop.ps1
```

Abrir: `Desktop\StockTracker-Designer\DESIGNER.bat` → opções 2–5.
