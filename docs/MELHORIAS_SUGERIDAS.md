# Melhorias e adições sugeridas — Stock Tracker

Documento de referência com ideias para evolução do projeto.  
Gerado a partir da análise do estado atual da app (Components, Equipments, Excel, APIs, Qt Designer).

---

## 1. Cache local de imagens de componentes — **implementado**

### Comportamento actual

- Pasta: `data/component_image_cache/`
- Módulo: `src/core/component_image_cache.py` + integração em `component_images.py`
- **Só grava quando abres um componente** — nunca percorre o Excel inteiro
- Carregamento em **background** (`QThread`) para não bloquear a GUI com inventários grandes

### Limites automáticos (inventário grande)

| Limite | Valor |
|--------|-------|
| Entradas máximas | 800 imagens |
| Espaço máximo | 150 MB |
| Validade do ficheiro | 90 dias |
| URL em cache (evita API) | 30 dias |

Quando os limites são ultrapassados, as entradas **menos usadas** são apagadas primeiro (LRU).

### Fluxo

```text
Selecionar componente
    │
    ▼
Imagem em cache válida? ──SIM──► carregar do disco (rápido; sem API)
    │
    NÃO
    ▼
URL em cache (< 30 dias)? ──SIM──► download só da imagem
    │
    NÃO
    ▼
API distribuidor → download → guardar (com eviction se necessário)
```

### Desvantagens aceites e mitigação

| Risco | Mitigação |
|-------|-----------|
| Disco a crescer | Teto 150 MB / 800 ficheiros |
| Imagem desatualizada | TTL 90 dias; URL renovada ao fim de 30 dias |
| Cache só neste PC | Esperado; não vai para GitHub |
| 1.ª vez lenta | Normal; seguintes rápidas |
| Ficheiro corrompido | Re-download automático |

### Manutenção manual

Apagar a pasta `data/component_image_cache/` (exceto se quiseres manter) ou chamar `ComponentImageCache().clear_all()` num script — opcional para UI futura.

---

## 1b. ~~Cache local~~ (texto de planeamento original)

<details>
<summary>Notas de planeamento (pré-implementação)</summary>

### Problema que motivou o cache

Ao pesquisar ou selecionar um componente, a app:

1. Chama a API do distribuidor (ex.: Mouser) para obter o URL da imagem
2. Descarrega a imagem em alta resolução (`/lrg/`, ~500×500) via `curl_cffi`
3. Mostra o preview interativo (`catalog_image_preview.py`)

Isto pode demorar **10–20 segundos** por componente, sempre que mudas de peça — mesmo que já tenhas visto essa imagem antes na mesma sessão ou noutro dia.

### O que seria o cache

Guardar localmente, em disco, uma cópia da imagem já descarregada, associada à referência do componente (ex.: `594-B0207ZFYY` ou MPN `UXB0207ZFYY`).

**Pasta sugerida:** `data/component_image_cache/`

**Exemplo de ficheiros:**

```text
data/component_image_cache/
├── README.txt
├── 594-B0207ZFYY.webp
├── 511-LRS-150-24.webp
└── ...
```

O nome do ficheiro seria a referência normalizada (`StockTracker.normalize_ref()`), com extensão real (`.webp`, `.jpg`, `.png`).

### Fluxo proposto

```text
Pesquisar componente
    │
    ▼
Existe ficheiro em component_image_cache/ ?
    │
    ├─ SIM → carregar do disco (rápido, ~ms)
    │
    └─ NÃO → API Mouser → download → guardar em cache → mostrar
```

### Vantagens

| Benefício | Descrição |
|-----------|-----------|
| **Velocidade** | Segunda visualização do mesmo componente é quase instantânea |
| **Menos API** | Menos chamadas à Mouser (rate limits, quotas) |
| **Offline parcial** | Imagens já vistas funcionam sem rede |
| **Consistência** | Mesma imagem entre sessões |

### Detalhes técnicos a considerar

| Aspeto | Sugestão |
|--------|----------|
| **Módulo** | `src/core/component_image_cache.py` ou extensão de `component_images.py` |
| **Chave** | `normalize_ref(supplier_ref)` ou `manufacturer_ref` se supplier vazio |
| **Invalidação** | Opcional: TTL (ex. 30 dias) ou botão “Refresh image” na GUI |
| **Git** | Ignorar `data/component_image_cache/*` exceto `README.txt` (como `equipment_images/`) |
| **Tamanho** | ~50–200 KB por imagem; 500 componentes ≈ 25–100 MB — aceitável |
| **Thread** | Download em `QThread` para não bloquear a UI na primeira vez |
| **Fallback** | Se cache corrompido, apagar ficheiro e voltar a descarregar |

### Esforço estimado

**Baixo–médio** (meio dia): lógica de leitura/escrita + integração em `fetch_pixmap_from_url` ou `_show_component_image_url`.

### Riscos / limitações

- Imagem em cache pode ficar desatualizada se o fornecedor mudar a foto (raro)
- Primeira vez continua lenta até existir cache
- Não resolve APIs em falha (DigiKey/TME 403) — só evita repetir o que já funcionou

</details>

---

## 2. Stock mínimo e alertas

### Ideia

Nova coluna **`Min Stock`** na folha `Components`. Quando `Current Stock < Min Stock`, destacar na GUI (cor, ícone ou lista “Stock baixo”).

### Valor

Saberes de relance o que precisa de reposição, sem abrir o Excel.

### Esforço

**Médio** — migração Excel + UI + opcional relatório.

---

## 3. Editar equipamento ao clicar nos detalhes

### Ideia

Em **Equipments**, clicar num campo de detalhe **preenchido** abre o diálogo **Edit** (hoje só campos vazios abrem Add).

### Valor

Comportamento igual ao de Components; menos cliques.

### Esforço

**Baixo** — lógica em `equipments_page.py`.

---

## 4. Loading assíncrono (API e imagens)

### Ideia

Operações lentas (SCAN, lookup catálogo, download imagem) em `QThread` ou `QRunnable`, com indicador “A carregar…” na barra de estado ou no preview.

### Valor

A janela deixa de parecer bloqueada.

### Esforço

**Médio** — refatorar chamadas bloqueantes na GUI.

---

## 5. Backup automático do Excel — **implementado**

### Comportamento actual

- Antes de cada gravação de `data/stock.xlsx`, cópia para `data/backups/stock_YYYYMMDD_HHMMSS.xlsx`
- Mantém apenas os **20** ficheiros mais recentes (os mais antigos são apagados)
- Módulo: `src/core/excel_backups.py`, integrado em `StockTracker.save_workbook()`
- Se o backup falhar (disco cheio, etc.), a gravação **continua** — o inventário não fica bloqueado

### Restaurar manualmente

1. Fechar o Excel  
2. Copiar um ficheiro de `data/backups/` para `data/stock.xlsx`

---

## 5b. ~~Backup automático~~ (planeamento original)

<details>
<summary>Notas de planeamento (pré-implementação)</summary>

### Ideia

Antes de gravar `data/stock.xlsx`, copiar para `data/backups/stock_YYYYMMDD_HHMMSS.xlsx`. Manter os últimos N ficheiros (ex. 20).

### Valor

Proteção contra corrupção, gravação a meio ou erro humano.

### Esforço

**Baixo** — função em `stock.py` antes de `save`.

</details>

---

## 6. Exportar relatórios

### Ideia

- Stock abaixo do mínimo → Excel/PDF  
- Equipamentos com calibração a expirar (30/60 dias)  
- Histórico filtrado por componente ou utilizador  

### Valor

Partilha com equipa/gestão sem copiar manualmente do Excel.

### Esforço

**Médio–alto** — depende de PDF e filtros.

---

## 7. Pesquisa global

### Ideia

Uma pesquisa que encontre componentes **e** equipamentos ao mesmo tempo, com resultados agrupados.

### Valor

Menos navegação entre páginas COMPONENTS / EQUIPMENTS.

### Esforço

**Médio** — novo diálogo ou barra no header.

---

## 8. Duplicar componente / equipamento

### Ideia

Botão “Duplicate” para criar entrada nova baseada na selecionada (refs e descrição copiadas, stock a zero).

### Valor

Entrada rápida de variantes parecidas.

### Esforço

**Baixo–médio**.

---

## 9. Atalhos de teclado

### Ideia

| Atalho | Ação |
|--------|------|
| `Ctrl+F` | Foco na pesquisa |
| `Enter` | SCAN / confirmar |
| `Ctrl+S` ou `+` | Add stock |
| `Ctrl+D` ou `-` | Remove stock |
| `Esc` | Clear |

### Valor

Mais rápido para utilizadores frequentes.

### Esforço

**Baixo** — `keyPressEvent` / `QShortcut` na janela principal.

---

## 10. Últimos itens consultados

### Ideia

Lista dos 5–10 últimos componentes/equipamentos abertos, acessível na barra inferior ou menu.

### Valor

Voltar rapidamente ao que estavas a tratar.

### Esforço

**Baixo** — lista em memória na sessão; opcional persistência.

---

## 11. Resolver DigiKey / TME

### Ideia

Corrigir autenticação e permissões (DigiKey sandbox 403, TME 403) para ter mais fontes de catálogo e imagens.

### Valor

Menos dependência só da Mouser; SCAN mais robusto.

### Esforço

**Variável** — muitas vezes depende do portal do fornecedor / tickets de suporte.

---

## 12. Link direto ao fornecedor

### Ideia

Botões “Open in Mouser” / “Open datasheet” nos detalhes do componente (URL da API: `ProductDetailUrl`, `DataSheetUrl`).

### Valor

Um clique para ficha técnica ou página do distribuidor.

### Esforço

**Baixo** — `QDesktopServices.openUrl()`.

---

## 13. Importação em massa

### Ideia

Importar CSV/Excel com lista de componentes ou stock inicial (mapeamento de colunas).

### Valor

Arranque rápido de inventário grande.

### Esforço

**Médio–alto**.

---

## 14. Leitor de código de barras USB

### Ideia

Validar e documentar fluxo com leitor HID (simula teclado + Enter no campo SCAN).

### Valor

Entrada de stock em armazém sem digitar refs.

### Esforço

**Baixo** (teste + docs) se o leitor já envia Enter; **médio** se for preciso protocolo serial.

---

## 15. Testes automáticos (pytest)

### Ideia

Testes para `stock.py`: normalização de refs, IN/OUT, migração de colunas, `equipment_row_to_dict`, etc.

### Valor

Menos regressões ao alterar core ou Excel.

### Esforço

**Médio** — setup inicial; depois manutenção baixa.

---

## 16. Log de erros

### Ideia

`data/logs/app.log` com falhas de API, Excel bloqueado, imagens indisponíveis, exceções.

### Valor

Diagnóstico sem depender só da consola.

### Esforço

**Baixo** — `logging` no core e GUI.

---

## 17. Versão visível na app

### Ideia

Mostrar versão (ex. `v2.1`) no canto, About ou título da janela; alinhar com tags Git.

### Valor

Saber que build está instalado ao reportar problemas.

### Esforço

**Muito baixo**.

---

## 18. Instalador Windows (.exe)

### Ideia

Empacotar com PyInstaller ou instalador para utilizadores sem Python.

### Valor

Distribuição interna mais simples.

### Esforço

**Médio** — ícones, dependências (`curl_cffi`, PySide6), updates.

---

## 19. Tema claro / escuro

### Ideia

Alternar entre tema Siemens escuro atual e variante clara (`styles.py`).

### Valor

Conforto visual; acessibilidade.

### Esforço

**Médio** — rever todos os estilos.

---

## 20. Campos de detalhe mais legíveis

### Ideia

Description e outros campos com texto cortado: alargar, elipsis + tooltip com texto completo (como `val_datasheet` em Equipments).

### Valor

Ler descrições completas sem copiar para Excel.

### Esforço

**Baixo** — padrão já existe em Equipments.

---

## 21. Página Materials / Consumíveis

### Ideia

Terceira secção para material não eletrónico (consumíveis, EPI, etc.) com folha Excel própria.

### Valor

Um só programa para todo o inventário de laboratório.

### Esforço

**Alto** — nova página, folha, migração, Designer.

---

## 22. Dashboard inicial

### Ideia

Ecrã ao abrir: stock baixo, calibrações a expirar, últimos movimentos, atalhos.

### Valor

Visão de gestão num relance.

### Esforço

**Alto** — novo layout e agregação de dados.

---

## Priorização sugerida

| Ordem | Item | Estado |
|-------|------|--------|
| 1 | Cache imagens componentes | **Feito** |
| 2 | Backup automático Excel | **Feito** |
| 3 | Stock mínimo + alertas | Pendente |
| 4 | Loading assíncrono (imagens) | **Feito** (QThread) |
| 5 | Link fornecedor / datasheet | Pendente |
| 6 | Atalhos de teclado | Pendente |
| 7 | Log de erros | Pendente |
| 8 | Testes pytest | Pendente |
| 9 | Relatórios export | Pendente |
| 10 | Instalador .exe | Pendente |

---

## Relação com o código atual

| Funcionalidade existente | Ficheiros principais |
|--------------------------|----------------------|
| Imagem catálogo componentes | `src/core/component_images.py`, `src/core/component_image_cache.py`, `src/gui/catalog_image_preview.py` |
| Imagem equipamentos (local) | `src/core/equipment_images.py`, `data/equipment_images/` |
| Excel / stock | `src/core/stock.py`, `data/stock.xlsx` |
| GUI Components | `src/gui/stock_tracker_window.py` |
| GUI Equipments | `src/gui/equipments_page.py` |
| APIs fornecedores | `src/core/suppliers/` |

---

## Notas

- Este documento é **planeamento**, não compromisso de implementação.
- Prioridades podem mudar consoante uso real (armazém vs escritório vs calibração).
- Para implementar um item: criar issue no GitHub ou pedir desenvolvimento com o número da secção (ex. “implementar secção 1”).

*Última atualização: junho 2026*
