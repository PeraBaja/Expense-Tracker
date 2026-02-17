from ExpenseRecord import ExpenseRecord
import json
from json_extensions import DateTimeDecoder, DateTimeEncoder


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
        with open(FILE_PATH, "x") as file:
            file.write("[]")
