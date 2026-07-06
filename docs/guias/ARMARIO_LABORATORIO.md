# Armário SMD do laboratório

O armário físico do lab está organizado em **Stock 1**, **Stock 2**, **Stock 3** e em **boxes** com etiquetas. Essa organização está reflectida na coluna **Location** do Excel (`Components` e `Generic`).

## Onde consultar

A lista completa de localizações e que peças estão em cada sítio está no **backup mais recente** de `data/stock.xlsx`:

```
data/backups/stock_YYYYMMDD_HHMMSS.xlsx
```

O ficheiro com data mais recente é o que reflecte o estado actual do armário. A app grava um backup automático antes de cada gravação (mantém os últimos 20).

Para ver no Excel: abrir o backup, folhas `Components` e `Generic`, coluna **Location**.

Na aplicação: página **Statistics** mostra contagens por localização; **Ctrl+G** permite pesquisar uma peça e ver onde está.

---

## Organização actual (referência)

Nomes usados na coluna Location — correspondem ao armário físico:


| Localização no Excel           | O que é no lab                                              |
| ------------------------------ | ----------------------------------------------------------- |
| `smd stock 1`                  | Gaveta / zona **Stock 1** — maior volume de componentes SMD |
| `smd stock 2`                  | Gaveta / zona **Stock 2**                                   |
| `SMD STOCK 3`                  | Gaveta / zona **Stock 3**                                   |
| `SMD STOCK BOX 1`              | Box etiquetada **Stock Box 1**                              |
| `SMD STOCK BOX 2`              | Box etiquetada **Stock Box 2**                              |
| `SMD CABINET`                  | Armário SMD (zona geral)                                    |
| `CERAMIC CHIP CAPACITORS 0603` | Box de condensadores cerâmicos 0603                         |
| `ELECTROLYTIC CAPACITORES`     | Box de condensadores electrolíticos SMD                     |
| `RESISTORES 0805/1206`         | Box de resistores 0805 e 1206                               |


Algumas localizações antigas (`SMD STOCK BOX 3`, `4`, `5`) foram renomeadas no Excel para os nomes descritivos acima (electrolíticos, cerâmicos, resistores).

Uma peça pode ter mais do que uma localização separada por `;` (ex.: `smd stock 1;SMD STOCK 3`) quando existe stock em dois sítios.

---

## Notas

- Ao adicionar stock novo, usar o mesmo nome de Location que está no armário para manter a correspondência física ↔ Excel.
- O autocomplete de Location na app sugere nomes já usados no inventário.
- Se restaurares um backup antigo, copia-o sobre `data/stock.xlsx` com o Excel fechado.

Ver também: [data/README.md](../../data/README.md) · [MANUAL_UTILIZADOR.md](MANUAL_UTILIZADOR.md)