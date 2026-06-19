# Equipments — especificação da caixa de imagem

Documento formatado a partir do **anexo com retângulo vermelho** que enviaste.  
Esta é a versão **original do que pediste**, antes das tentativas de implementação no código.

---

## Objetivo

A área tracejada (`equipment_image_preview`) deve ser exactamente o retângulo que desenhaste a vermelho — não maior, não deslocada para baixo da janela inteira.

---

## Alinhamento (coluna direita como referência)

| Borda da caixa | Alinha com |
|----------------|------------|
| **Topo** | Primeira linha de **Equipment Details** → **Supplier Reference** |
| **Fundo** | Última linha de **Support Documentation** → **Add** / botão **ADD DOC** |

```
  DIREITA                          ESQUERDA (Operations)
  ─────────────────────────────────────────────────────────
  Equipment Details
  Supplier Reference  ───────────► TOPO da caixa de imagem
  Serial Number
  Description
  ...
  Support Documentation
  Search doc
  Link
  Folder
  Add / ADD DOC       ───────────► FUNDO da caixa de imagem
```

---

## Posição na coluna esquerda

- Mantém-se **abaixo** de Search Equipment e Scan Barcode / Supplier Ref.
- Ocupa a **largura útil** da coluna Operations (margens normais do painel).
- O texto **"Drop image here"** ou a foto fica **dentro** do bordo tracejado.
- Botões **Add** e **Delete** da imagem ficam **logo abaixo** da caixa tracejada (como no layout inicial).

---

## Comportamento da imagem

1. Sem equipamento seleccionado → placeholder `Drop image here`.
2. Com equipamento com imagem → foto **redimensionada para caber dentro** da caixa (proporção mantida).
3. A caixa **não deve crescer** quando chega uma foto grande.
4. Drag & drop e botões Add/Delete mantêm-se como estavam.

---

## O que **não** deve acontecer

- Caixa a esticar até ao fundo da janela.
- A mesma imagem para componentes diferentes (Components).
- Texto parcial no campo Search (ex.: `re`) a substituir a referência real do componente.
- Campo Scan com ≤4 caracteres a disparar pesquisa (ruído de etiquetas Mouser).

---

## Referência visual

Screenshot anotado pelo utilizador (retângulo vermelho no ecrã **Inventory — Equipments**).

---

## Estado do código

| Item | Situação |
|------|----------|
| Layout caixa imagem (este anexo) | **Pendente** — código revertido ao grid original (300×260) |
| Remover Copy no Scan (Operations) | **Feito** — Components e Equipments |
| Crash threads catálogo | **Corrigido** |
| Imagem errada ao pesquisar | **Corrigido** (cache por ref. do componente) |
| Ignorar scan ≤4 caracteres | **Feito** |

---

## Ficheiros relacionados

| Ficheiro | Função |
|----------|--------|
| `src/gui/designer/gui_equipments.ui` | Layout Qt Designer |
| `src/gui/equipments_page.py` | Imagem, drag & drop, botões |
| `tools/generate_equipments_ui.py` | Regenerar `.ui` |

---

## Estado actual (código)

- Caixa de imagem: **300×320 px** mínimo (`EQUIPMENT_IMAGE_PREVIEW_*` em `styles.py`).
- Alinhamento vertical com a coluna direita pode ainda diferir ligeiramente do desenho original; ver `src/gui/equipments_page.py` e `equipment_image_panel_xml()` em `gui_ui_builder.py`.
