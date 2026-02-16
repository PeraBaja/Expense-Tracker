import argparse
from datetime import date


def positive_float(value: str):
    try:
        v: float = float(value)
    except:
        raise argparse.ArgumentTypeError
    if v < 0:
        raise argparse.ArgumentTypeError("Can't assing a negative value")
    return v


def date_format(value: str):
    try:
        date.fromisoformat(value)
    except:
        raise argparse.ArgumentTypeError("Invalid date. Valid format eg.: yyyy-MM-dd")
