"""
Stock Tracker — consola de testes (desenvolvimento).

Execucao: python -m src.test_terminal
"""
from src.core.stock import StockTracker


def print_header(tracker: StockTracker, user: str) -> None:
    print("\n" + "=" * 50)
    print("  STOCK TRACKER - Teste no terminal")
    print("=" * 50)
    print(f"  Utilizador: {user}")
    print(f"  Excel: {tracker.excel_file}")
    mouser = "definida" if tracker.api_key else "NAO definida (opcoes 5 e 6)"
    print(f"  API Mouser: {mouser}")
    configured = tracker.configured_suppliers()
    print(f"  Fornecedores com chave: {', '.join(configured) or '(nenhum)'}")
    print("=" * 50)


def print_menu() -> None:
    print("\n  1 - Pesquisar componente no Excel")
    print("  2 - Ver dados de um codigo (scan simulado)")
    print("  3 - Adicionar stock (IN)")
    print("  4 - Remover stock (OUT) [pede confirmacao]")
    print("  5 - Pesquisar na Mouser (so consulta)")
    print("  6 - Mouser -> Excel -> adicionar stock")
    print("  7 - Listar componentes no Excel")
    print("  8 - Ver ultimos 20 movimentos (historico)")
    print("  9 - Mudar nome de utilizador")
    print(" 10 - Pesquisar na TME (so consulta)")
    print("  0 - Sair")


def print_component(data: dict) -> None:
    print("  --- Componente ---")
    print(f"  Mouser:     {data['mouser']}")
    print(f"  Fabricante: {data['manufacturer']}")
    print(f"  Ref. fab.:  {data['manufacturer_ref']}")
    print(f"  Descricao:  {data['description']}")
    print(f"  Stock:      {data['stock']}")
    print("  ------------------")


def ask_positive_int(prompt: str) -> int | None:
    text = input(prompt).strip()
    try:
        value = int(text)
    except ValueError:
        print("Quantidade invalida (tem de ser numero inteiro).")
        return None
    if value <= 0:
        print("Quantidade tem de ser maior que 0.")
        return None
    return value


def confirm_out(code: str, qty: int, current: int) -> bool:
    new_stock = current - qty
    print("\n  Confirmar remocao de stock?")
    print(f"  Componente: {code}")
    print(f"  Quantidade: {qty}")
    print(f"  Stock atual: {current}")
    print(f"  Stock depois: {new_stock}")
    answer = input("  Escreve SIM para confirmar: ").strip().upper()
    return answer == "SIM"


def pause() -> None:
    input("\n  [Enter para voltar ao menu]")


def get_row_stock(tracker: StockTracker, sheet, code: str):
    part = tracker.extract_part_number(code)
    row = tracker.find_component_any(sheet, part, code)
    if row is None:
        print("Componente nao encontrado no Excel.")
        return None, part
    return row, part


def main():
    tracker = StockTracker()
    user = input("Nome de utilizador: ").strip()
    if not user:
        print("Utilizador obrigatorio.")
        return

    while True:
        print_header(tracker, user)
        print_menu()
        opcao = input("\nOpcao: ").strip()

        if opcao == "0":
            print("A sair.")
            break

        elif opcao == "9":
            new_user = input("Novo nome de utilizador: ").strip()
            if new_user:
                user = new_user
                print(f"Utilizador alterado para: {user}")
            else:
                print("Nome vazio — mantido o anterior.")
            pause()
            continue

        elif opcao == "1":
            query = input("Texto a pesquisar: ").strip()
            if not query:
                print("Escreve algo para pesquisar.")
            else:
                wb = tracker.get_workbook()
                sheet = tracker.get_components_sheet(wb)
                matches = tracker.search_in_excel_all(sheet, query)
                if not matches:
                    print("Nao encontrado no Excel.")
                elif len(matches) == 1:
                    print_component(tracker.row_to_dict(matches[0]))
                else:
                    print(f"\n  {len(matches)} resultado(s):\n")
                    for i, row in enumerate(matches, 1):
                        d = tracker.row_to_dict(row)
                        print(
                            f"  {i:2}. {str(d['mouser']):<22} "
                            f"stock={d['stock']}  {str(d['description'])[:40]}"
                        )
                    pick = input("\n  Escolhe numero (Enter=1): ").strip()
                    try:
                        idx = int(pick) - 1 if pick else 0
                    except ValueError:
                        idx = 0
                    if 0 <= idx < len(matches):
                        print_component(tracker.row_to_dict(matches[idx]))
                    else:
                        print("  Numero invalido.")
            pause()

        elif opcao == "2":
            code = input("Codigo / referencia / scan: ").strip()
            if len(code) < 5:
                print("Referencia demasiado curta (minimo 5 caracteres).")
            elif code:
                wb = tracker.get_workbook()
                sheet = tracker.get_components_sheet(wb)
                row, _ = get_row_stock(tracker, sheet, code)
                if row:
                    print_component(tracker.row_to_dict(row))
            pause()

        elif opcao == "3":
            code = input("Referencia do componente: ").strip()
            qty = ask_positive_int("Quantidade a adicionar: ")
            if code and qty is not None:
                if len(code) < 5:
                    print("Referencia demasiado curta.")
                else:
                    ok = tracker.update_stock(user, code, qty, "IN")
                    print("Guardado com sucesso." if ok else "Nao guardado (ver mensagens acima).")
            pause()

        elif opcao == "4":
            code = input("Referencia do componente: ").strip()
            qty = ask_positive_int("Quantidade a remover: ")
            if code and qty is not None:
                if len(code) < 5:
                    print("Referencia demasiado curta.")
                else:
                    wb = tracker.get_workbook()
                    sheet = tracker.get_components_sheet(wb)
                    row, _ = get_row_stock(tracker, sheet, code)
                    if row:
                        current = int(row[6].value or 0)
                        if current < qty:
                            print("Stock insuficiente.")
                        elif confirm_out(str(row[1].value or code), qty, current):
                            ok = tracker.update_stock(user, code, qty, "OUT")
                            print(
                                "Guardado com sucesso." if ok else "Nao guardado."
                            )
                        else:
                            print("Remocao cancelada.")
            pause()

        elif opcao == "5":
            if not tracker.api_key:
                print("Defina MOUSER_API_KEY em config/secrets.py.")
            else:
                part = input("Referencia Mouser: ").strip()
                if part:
                    result = tracker.search_mouser(part)
                    if result:
                        print("  --- Mouser ---")
                        print(f"  Part: {result.get('MouserPartNumber')}")
                        print(f"  Fabricante: {result.get('Manufacturer')}")
                        print(f"  Descricao: {result.get('Description')}")
                    else:
                        print("Sem resultado ou erro de ligacao.")
            pause()

        elif opcao == "6":
            if not tracker.api_key:
                print("Defina MOUSER_API_KEY em config/secrets.py.")
            else:
                code = input("Referencia Mouser (nova ou existente): ").strip()
                qty = ask_positive_int("Quantidade a adicionar: ")
                if code and qty is not None:
                    tracker.add_from_mouser_and_stock_in(user, code, qty)
            pause()

        elif opcao == "7":
            wb = tracker.get_workbook()
            sheet = tracker.get_components_sheet(wb)
            items = tracker.list_components(sheet)
            print(f"\nTotal: {len(items)} componente(s)\n")
            if not items:
                print("  (Excel vazio ou so cabecalhos)")
            for i, item in enumerate(items, 1):
                print(
                    f"  {i:3}. {item['mouser']:<28} stock={item['stock']}"
                )
            pause()

        elif opcao == "10":
            from src.core.suppliers.credentials import is_configured

            if not is_configured("tme", tracker._secrets):
                print(
                    "Defina TME_API_TOKEN e TME_APP_SECRET em config/secrets.py "
                    "e guarde o ficheiro (Ctrl+S)."
                )
            else:
                part = input("Referencia TME (simbolo ou texto): ").strip()
                if part:
                    result = tracker.search_tme(part)
                    if result:
                        print("  --- TME ---")
                        print(
                            f"  Symbol: {result.get('supplier_part_number') or result.get('MouserPartNumber')}"
                        )
                        print(f"  Fabricante: {result.get('Manufacturer')}")
                        print(f"  Ref. fab.:  {result.get('ManufacturerPartNumber')}")
                        print(f"  Descricao:  {result.get('Description')}")
                    else:
                        print("Sem resultado ou erro de ligacao (ver mensagens acima).")
            pause()

        elif opcao == "8":
            wb = tracker.get_workbook()
            rows = tracker.get_history_rows(wb, component_only=False)
            print(f"\nUltimos movimentos (max. 20):\n")
            if not rows:
                print("  (Sem historico)")
            else:
                print(
                    f"  {'Data':<20} {'User':<12} {'Ref.':<22} "
                    f"{'Mov':<4} {'Qtd':<5} {'Stock':<5}"
                )
                print("  " + "-" * 72)
                for row in rows:
                    date, u, ref, mov, qtd, after = row[:6]
                    print(
                        f"  {str(date):<20} {str(u):<12} {str(ref):<22} "
                        f"{str(mov):<4} {str(qtd):<5} {str(after):<5}"
                    )
            pause()

        else:
            print("Opcao invalida.")
            pause()


if __name__ == "__main__":
    main()
