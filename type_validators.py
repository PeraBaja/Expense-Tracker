import argparse


def positive_float(value: str):
    try:
        v: float = float(value)
    except:
        raise argparse.ArgumentTypeError
    if v < 0:
        raise argparse.ArgumentTypeError("Can't assing a negative value")
    return v
