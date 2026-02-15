import argparse

if __name__ == "__main__":
    argparser: argparse.ArgumentParser = argparse.ArgumentParser(
        "expense tracker", description="tracker de gastos"
    )
    subparsers = argparser.add_subparsers(dest="acción", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", "-d")
    add_parser.add_argument("--amount", "-a", type=int)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", required=True, type=int)

    delete_parser = subparsers.add_parser("summary")
    delete_parser.add_argument("--month", type=int)

    delete_parser = subparsers.add_parser("list")

    args = argparser.parse_args()
    print(args)
