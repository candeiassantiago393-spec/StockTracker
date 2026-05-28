# Popups Siemens (Qt Designer)

Ficheiros gerados a partir de `siemens_template/gui_popup.ui` (template oficial Siemens).

| Ficheiro | Uso na app |
|----------|------------|
| `gui_popup_manual.ui` | ADD MANUAL COMPONENT |
| `gui_popup_history.ui` | HISTORY |
| `gui_popup_search.ui` | Resultados de pesquisa Excel |

**Em execução** a app usa `siemens_template/gui_popup.py` via `popup_shell.py` (mesmo layout).

Regenerar após alterar o template base:

```text
python tools/generate_popup_uis.py
```

Copiar para o Ambiente de Trabalho: `tools\sincronizar-desktop.ps1`
