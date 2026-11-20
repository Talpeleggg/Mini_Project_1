"""TEMPORARY helper module. Owner: Part 2.

Will hold: load_raw, clean (returns a new table, never changes the input), load_clean.

Other parts import from here. Do not write code here until the related decisions are made on the board.
At integration the functions are copied into the final notebook and this file is deleted.
"""
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "laptop_price_dataset.csv"


def load_raw(path=None):
    """Read the laptop dataset exactly as it is in the file.

    The raw file is never modified. Every cleaning step lives in `clean()` and works on a copy.
    """
    return pd.read_csv(path or DATA_PATH)
