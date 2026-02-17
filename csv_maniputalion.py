CSV_FILE_PATH = "month_budgets.csv"


def change_budget(month_name_or_number: str, amount) -> float | None:
    month_budgets = get_monthly_budgets()
    if not month_name_or_number.isdigit():
        month_names = [
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
        ]
        with open(CSV_FILE_PATH, "w") as file:
            i = month_names.index(month_name_or_number)

            month_budgets[i] = amount
            file.write(",".join([f"{budget}" for budget in month_budgets]))
    else:
        with open(CSV_FILE_PATH, "w") as file:

            month_budgets[int(month_name_or_number) - 1] = amount
            file.write(",".join([f"{budget}" for budget in month_budgets]))


def get_monthly_budgets() -> list[float]:
    with open(CSV_FILE_PATH) as file:
        return [float(budget) for budget in file.read().split(",")]


def create_budget_file():
    import os

    if os.path.exists(CSV_FILE_PATH):
        return
    with open(CSV_FILE_PATH, "x") as file:
        file.write(",".join(["-1"] * 12))
