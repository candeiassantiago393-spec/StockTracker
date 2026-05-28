"""
Stock Tracker — terminal test console (development).

Run: python -m src.test_terminal
"""
from src.core.stock import StockTracker
from src.core.suppliers import supplier_label
from src.core.suppliers.base import SupplierId
from src.core.suppliers.credentials import is_configured


def print_header(tracker: StockTracker, user: str) -> None:
    print("\n" + "=" * 50)
    print("  STOCK TRACKER - Terminal test")
    print("=" * 50)
    print(f"  User: {user}")
    print(f"  Excel: {tracker.excel_file}")
    configured = tracker.configured_suppliers()
    if configured:
        names = ", ".join(supplier_label(s) for s in configured)
        print(f"  Distributor APIs: {names}")
    else:
        print("  Distributor APIs: (none configured)")
    print("=" * 50)


def print_menu() -> None:
    print("\n  1 - Search component in Excel")
    print("  2 - View component by code (simulated scan)")
    print("  3 - Add stock (IN)")
    print("  4 - Remove stock (OUT) [confirmation]")
    print("  5 - Search distributor catalog (lookup only)")
    print("  6 - Distributor -> Excel -> add stock")
    print("  7 - List components in Excel")
    print("  8 - View last 20 history entries")
    print("  9 - Change user name")
    print(" 10 - Add manual component (no reference required)")
    print("  0 - Exit")


def print_component(data: dict) -> None:
    print("  --- Component ---")
    print(f"  Supplier ref: {data['mouser']}")
    print(f"  Manufacturer: {data['manufacturer']}")
    print(f"  Mfr. ref:     {data['manufacturer_ref']}")
    print(f"  Description:  {data['description']}")
    print(f"  Stock:        {data['stock']}")
    print("  ------------------")


def pick_supplier(tracker: StockTracker) -> SupplierId | None:
    configured = tracker.configured_suppliers()
    if not configured:
        print("No distributor API configured. Edit config/secrets.py.")
        return None
    if len(configured) == 1:
        return configured[0]
    print("\n  Select distributor:")
    for index, supplier_id in enumerate(configured, start=1):
        print(f"    {index} - {supplier_label(supplier_id)}")
    choice = input("  Number: ").strip()
    try:
        position = int(choice) - 1
        return configured[position]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None


def print_supplier_part(supplier_id: SupplierId, result: dict) -> None:
    print(f"  --- {supplier_label(supplier_id)} ---")
    print(
        f"  Part: {StockTracker.part_supplier_reference(result)}"
    )
    print(f"  Manufacturer: {StockTracker.part_manufacturer(result)}")
    print(f"  Mfr. ref:     {StockTracker.part_manufacturer_reference(result)}")
    print(f"  Description:  {StockTracker.part_description(result)}")


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


def add_manual_component_terminal(tracker: StockTracker, user: str) -> None:
    print("\n  Add manual component")
    print("  Leave Supplier Reference empty if not available.")
    supplier_ref = input("  Supplier Reference (optional): ").strip()
    manufacturer = input("  Manufacturer: ").strip()
    manufacturer_ref = input("  Manufacturer Reference: ").strip()
    description = input("  Description: ").strip()
    initial_stock_text = input("  Initial Stock [0]: ").strip()

    if not initial_stock_text:
        initial_stock = 0
    else:
        try:
            initial_stock = int(initial_stock_text)
        except ValueError:
            print("  Initial stock must be an integer.")
            return

    ok, message = tracker.add_manual_component(
        user=user,
        supplier_reference=supplier_ref,
        manufacturer=manufacturer,
        manufacturer_reference=manufacturer_ref,
        description=description,
        initial_stock=initial_stock,
    )
    print(f"  {message}")
    if ok:
        wb = tracker.get_workbook()
        sheet = tracker.get_components_sheet(wb)
        row = tracker.find_component_any(sheet, supplier_ref, manufacturer_ref, manufacturer)
        if row:
            print_component(tracker.row_to_dict(row))


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

        elif opcao == "10":
            add_manual_component_terminal(tracker, user)
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
            supplier = pick_supplier(tracker)
            if supplier and is_configured(supplier, tracker._secrets):
                part = input("Part number or keyword: ").strip()
                if part:
                    result = tracker.search_supplier(supplier, part)
                    if result:
                        print_supplier_part(supplier, result)
                    else:
                        print("No result or connection error.")
            pause()

        elif opcao == "6":
            supplier = pick_supplier(tracker)
            if supplier and is_configured(supplier, tracker._secrets):
                code = input("Part reference (new or existing): ").strip()
                qty = ask_positive_int("Quantity to add: ")
                if code and qty is not None:
                    tracker.add_from_supplier_and_stock_in(
                        user, code, qty, supplier
                    )
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
