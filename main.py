import argparse
from dataclasses import fields
from datetime import date
from ExpenseRecord import ExpenseRecord
from csv_maniputalion import change_budget, create_budget_file, get_monthly_budgets
from type_validators import date_format, positive_float
from tabulate import tabulate
from ArgsSchema import ArgsSchema
from json_manipulation import (
    create_json_file,
    update_expense_records_json,
    get_expense_records_from_json,
)

MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def filter_by_month_in_last_year(expense_records: list) -> list[ExpenseRecord]:

    def _(expense: ExpenseRecord):
        return (
            expense.date.month == args.month and expense.date.year == date.today().year
        )

    return list(filter(_, expense_records))


def filter_by_category(expense_records: list) -> list[ExpenseRecord]:

    def _(expense: ExpenseRecord):
        return expense.category == args.category

    return list(filter(_, expense_records))


if __name__ == "__main__":
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        "expense tracker", description="tracker de gastos"
    )
    subparsers = argparser.add_subparsers(dest="action", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", "-d", required=True)
    add_parser.add_argument("--amount", "-a", type=positive_float, required=True)
    add_parser.add_argument("--category", "-c")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", required=True, type=int)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument(
        "--month", "-m", choices=[*[f"{i}" for i in range(1, 12 + 1)], *MONTH_NAMES]
    )

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--category", "-c")

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True, type=int)
    update_parser.add_argument("--description", "-d")
    update_parser.add_argument("--amount", "-a", type=positive_float)
    update_parser.add_argument("--category", "-c")
    update_parser.add_argument("--date", "-dt", type=date_format, dest="date_made")

    budget_parser = subparsers.add_parser("budget")
    budget_parser.add_argument(
        "--month",
        "-m",
        choices=[*MONTH_NAMES, *[f"{i}" for i in range(1, 12 + 1)]],
    )
    budget_parser.add_argument("--amount", "-a", type=positive_float)
    budget_parser.add_argument("--list", "-l", action="store_true")

    args = ArgsSchema(**vars(argparser.parse_args()))
    create_json_file()
    create_budget_file()
    expense_records = get_expense_records_from_json()
    print(args)
    match args.action:

        case "list":
            headers = [field.name for field in fields(ExpenseRecord)]
            expense_records = (
                filter_by_category(expense_records)
                if args.category
                else expense_records
            )
            data = [vars(expense) for expense in expense_records]
            for i in range(len(data)):
                data[i]["category"] = f"{data[i]["category"] or "-"}"
                data[i]["amount"] = f"${data[i]["amount"]:.2f}"

            print(
                tabulate(
                    data,
                    headers="keys",
                )
            )
            if len(expense_records) == 0:
                print("There's no expenses made")
        case "summary":
            if args.month:
                expenses_filtered_by_month_for_last_year = filter_by_month_in_last_year(
                    expense_records
                )
                expense_summary = sum(
                    [
                        expense.amount.__round__(2)
                        for expense in expenses_filtered_by_month_for_last_year
                    ]
                )
                month = (
                    MONTH_NAMES[int(args.month) - 1]
                    if args.month.isdigit()
                    else args.month
                )
                print(f"expense summary for {month}: ${expense_summary:.2f}")
            else:
                expense_summary = sum(
                    [expense.amount.__round__(2) for expense in expense_records]
                )
                print(f"expense summary total: ${expense_summary:.2f}")
        case "add":
            if args.amount == None or args.description == None:
                raise AttributeError
            biggest_id = (
                max([expense.id for expense in expense_records])
                if len(expense_records) > 0
                else 0
            )
            new_expense = ExpenseRecord(
                id=biggest_id + 1,
                amount=args.amount,
                description=args.description,
                category=args.category,
            )
            expense_records.append(new_expense)
            update_expense_records_json(expense_records)
            print("expense added succesfully")
        case "delete":
            for expense in expense_records:
                if expense.id == args.id:
                    expense_records.remove(expense)
                    update_expense_records_json(expense_records)
                    print(f'Expense with description "{expense.description}" deleted')
                    exit(0)
            print(f"Expense with id {args.id} not found")
        case "update":
            for i in range(len(expense_records)):
                current_id = expense_records[i].id
                if current_id == args.id:
                    print(
                        f'Expense with description "{expense_records[i].description}" modified'
                    )
                    expense_records[i] = ExpenseRecord(
                        current_id,
                        amount=(
                            args.amount if args.amount else expense_records[i].amount
                        ),
                        description=(
                            args.description
                            if args.description
                            else expense_records[i].description
                        ),
                        date=(
                            args.date_made
                            if args.date_made
                            else expense_records[i].date
                        ),
                        category=(
                            args.category
                            if args.category
                            else expense_records[i].category
                        ),
                    )
                    update_expense_records_json(expense_records)
                    exit(0)
                # In case not found any expense
                print(f"Expense with id {args.id} not found")
        case "budget":
            if args.list:
                monthly_budgets = [
                    budget if budget >= 0 else "-" for budget in get_monthly_budgets()
                ]

                print(tabulate([monthly_budgets], headers=MONTH_NAMES))
            if args.amount and args.month:
                change_budget(args.month, args.amount)
                print("budget added succesfully")
