import argparse
from dataclasses import dataclass, field, Field


@dataclass
class ArgsSchema:
    action: str
    description: str | None = field(default=None)
    id: int | None = field(default=None)
    amount: int | None = field(default=None)


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
    print(args)
