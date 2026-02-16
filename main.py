import argparse
from dataclasses import dataclass, field, Field
import json
from ExpenseRecord import ExpenseRecord
from json_extensions import DateTimeDecoder, DateTimeEncoder


@dataclass
class ArgsSchema:
    action: str
    description: str | None = field(default=None)
    id: int | None = field(default=None)
    amount: int | None = field(default=None)
    month: int | None = field(default=None)


def get_expense_records_from_json() -> list[ExpenseRecord]:
    with open("expense-records.json") as file:
        data = json.load(file, cls=DateTimeDecoder)
    return [ExpenseRecord(**expense) for expense in data]


def update_expense_records_json(expense_records: list[ExpenseRecord]):
    with open("expense-records.json", "w") as file:
        json.dump(
            [vars(expense) for expense in expense_records], file, cls=DateTimeEncoder
        )


def create_json_file():
    import os

    FILE_PATH = "expense-records.json"
    if not os.path.exists(
        FILE_PATH,
    ):
        open(FILE_PATH, "x")


if __name__ == "__main__":
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        "expense tracker", description="tracker de gastos"
    )
    subparsers = argparser.add_subparsers(dest="action", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", "-d", required=True)
    add_parser.add_argument("--amount", "-a", type=int, required=True)
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", required=True, type=int)

    delete_parser = subparsers.add_parser("summary")
    delete_parser.add_argument("--month", type=int)

    delete_parser = subparsers.add_parser("list")

    args = ArgsSchema(**vars(argparser.parse_args()))
    create_json_file()
    expense_records = get_expense_records_from_json()
    print(args)
    match args.action:

        case "list":
            for expense in expense_records:
                print(expense)
        case "summary":
            expense_summary = sum([expense.amount for expense in expense_records])
            print(expense_summary)
        case "add":
            if args.amount == None or args.description == None:
                raise AttributeError
            expense_records.append(
                ExpenseRecord(amount=args.amount, description=args.description)
            )
            update_expense_records_json(expense_records)
