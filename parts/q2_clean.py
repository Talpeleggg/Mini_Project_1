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


OS_ALIASES = {"Mac OS X": "macOS"}

OS_FAMILY = {
    "Windows 10": "Windows", "Windows 7": "Windows", "Windows 10 S": "Windows",
    "macOS": "macOS", "Linux": "Linux", "Chrome OS": "Chrome OS", "Android": "Android", "No OS": "No OS",
}


def clean_opsys(opsys):
    """Unify aliases of the same operating system and add the OS family.

    Returns (OpSys_clean, OS_family) as two Series with the same index as the input.
    Only true aliases are merged: Windows versions are different products and stay separate.
    """
    clean = opsys.replace(OS_ALIASES)
    family = clean.map(OS_FAMILY)
    unmapped = sorted(clean[family.isna()].unique())
    assert not unmapped, f"operating systems without a family: {unmapped}"
    return clean, family


import re

DRIVE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(GB|TB)\s+(SSD|HDD|Flash Storage|Hybrid)")

STORAGE_ORDER = ["SSD", "HDD", "Flash Storage", "Hybrid"]

GB_PER_TB = 1000


def parse_memory(memory):
    """Parse one `Memory` string.

    Returns (storage_type, total_gb, has_ssd). The storage type is a canonical label of the drive types
    that are present, in a fixed order, for example "SSD + HDD". Two drives of the same type give one type
    ("SSD") and their capacities are added. Raises AssertionError for text it does not understand.
    """
    drives = DRIVE_PATTERN.findall(memory)
    assert drives, f"cannot parse Memory string: {memory!r}"
    leftover = DRIVE_PATTERN.sub("", memory).replace("+", "").strip()
    assert leftover == "", f"unrecognised text {leftover!r} in Memory string: {memory!r}"

    types = {drive_type for _, _, drive_type in drives}
    storage_type = " + ".join(t for t in STORAGE_ORDER if t in types)
    total_gb = sum(float(value) * (GB_PER_TB if unit == "TB" else 1) for value, unit, _ in drives)
    return storage_type, total_gb, "SSD" in types


def parse_memory_series(memory):
    """Apply `parse_memory` to a whole column. Returns a DataFrame with Storage_type, Storage_GB_total, has_SSD."""
    parsed = [parse_memory(m) for m in memory]
    return pd.DataFrame(parsed, columns=["Storage_type", "Storage_GB_total", "has_SSD"], index=memory.index)


import numpy as np

CPU_TIERS = ["Core i3", "Core i5", "Core i7", "Other"]
DEDICATED_GPU_COMPANIES = ["Nvidia", "AMD"]
KNOWN_GPU_COMPANIES = ["Intel", "Nvidia", "AMD", "ARM"]


def screen_pixels(resolution):
    """Number of pixels (width x height) taken from the end of the ScreenResolution text."""
    width_height = resolution.str.extract(r"(\d+)x(\d+)\s*$").astype(float)
    assert width_height.notna().all().all(), "a ScreenResolution without a WxH resolution at the end"
    return (width_height[0] * width_height[1]).astype(int)


def has_touchscreen(resolution):
    """True when the ScreenResolution text mentions a touchscreen."""
    return resolution.str.contains("Touchscreen", regex=False)


def cpu_tier(cpu_type):
    """Processor tier: Core i3 / Core i5 / Core i7, and Other for everything else."""
    tier = cpu_type.str.extract(r"^(Core i[3579])")[0].fillna("Other")
    unexpected = sorted(set(tier) - set(CPU_TIERS))
    assert not unexpected, f"unexpected CPU tiers: {unexpected}"
    return tier


# Processor families, matched against the start of CPU_Type (first match wins). Added 2026-11-28 because the
# CPU_tier value "Other" mixes many different processors (Celeron, Pentium, Atom, AMD...).
CPU_FAMILY_RULES = [
    (r"^Core i3", "Core i3"), (r"^Core i5", "Core i5"), (r"^Core i7", "Core i7"), (r"^Core M", "Core M"),
    (r"^Celeron", "Celeron"), (r"^Pentium", "Pentium"), (r"^Atom", "Atom"), (r"^Xeon", "Xeon"),
    (r"^A\d+-Series", "AMD A-Series"), (r"^E-Series", "AMD E-Series"), (r"^FX", "AMD FX"),
    (r"^Ryzen", "AMD Ryzen"), (r"^Cortex", "Samsung Cortex"),
]


def cpu_family(cpu_type):
    """Processor family from the start of CPU_Type: Core i3/i5/i7, Core M, Celeron, Pentium, Atom, Xeon, AMD..."""
    family = pd.Series(np.nan, index=cpu_type.index, dtype=object)
    for pattern, name in CPU_FAMILY_RULES:
        family = family.where(family.notna() | ~cpu_type.str.match(pattern), name)
    unknown = sorted(cpu_type[family.isna()].unique())
    assert not unknown, f"processors without a family: {unknown}"
    return family


def log_price(price):
    """Natural logarithm of the price in euro (the price must be positive)."""
    assert (price > 0).all(), "log needs positive prices"
    return np.log(price)


def dedicated_gpu(gpu_company):
    """True for a Nvidia or AMD graphics card, False for Intel or ARM (integrated graphics).

    This is an approximation by company: some AMD cards are integrated graphics. It is stated as a limitation.
    """
    unknown = sorted(set(gpu_company) - set(KNOWN_GPU_COMPANIES))
    assert not unknown, f"unknown GPU companies: {unknown}"
    return gpu_company.isin(DEDICATED_GPU_COMPANIES)


RARE_MIN_COUNT = 10   # a category with fewer than 10 laptops counts as rare (same threshold as in the audit)


def group_rare(series, min_count=RARE_MIN_COUNT, label="Other"):
    """Replace categories with fewer than `min_count` rows by `label`. Returns a new Series; no row is removed."""
    counts = series.value_counts()
    rare = counts[counts < min_count].index
    assert label not in set(series.unique()), f"{label!r} is already a category of this column"
    return series.where(~series.isin(rare), label)


def flag_near_duplicates(df, key_cols):
    """True for every row that shares all of `key_cols` with another row (here: every column except the price)."""
    return df.duplicated(subset=key_cols, keep=False)


SUSPICIOUS_RULES = {
    "small screen (<=13.3 in) but heavy (>2.5 kg)": lambda d: (d["Inches"] <= 13.3) & (d["Weight (kg)"] > 2.5),
    "large screen (>=17 in) but light (<1.5 kg)": lambda d: (d["Inches"] >= 17) & (d["Weight (kg)"] < 1.5),
    "Netbook with 16 GB RAM or more": lambda d: (d["TypeName"] == "Netbook") & (d["RAM (GB)"] >= 16),
    "Gaming/Workstation under 500 euro": lambda d: d["TypeName"].isin(["Gaming", "Workstation"]) & (d["Price (Euro)"] < 500),
    "32 GB RAM or more under 1000 euro": lambda d: (d["RAM (GB)"] >= 32) & (d["Price (Euro)"] < 1000),
}


def flag_suspicious(df):
    """Flag rows that break a physical or price plausibility rule. Rows are flagged, never removed.

    Returns (any_rule, per_rule) where `any_rule` is a Series of True/False and `per_rule` has a column per rule.
    """
    per_rule = pd.DataFrame({name: rule(df) for name, rule in SUSPICIOUS_RULES.items()})
    return per_rule.any(axis=1), per_rule


def clean(df):
    """Return a new, cleaned table. The input table is never changed.

    The cleaned table has all the original columns, unchanged, followed by the new columns listed in
    `COLUMN_DICTIONARY`. No row is removed.
    """
    out = df.copy()
    original_columns = list(df.columns)

    out["OpSys_clean"], out["OS_family"] = clean_opsys(out["OpSys"])
    out = pd.concat([out, parse_memory_series(out["Memory"])], axis=1)
    out["Screen_pixels"] = screen_pixels(out["ScreenResolution"])
    out["Touchscreen"] = has_touchscreen(out["ScreenResolution"])
    out["CPU_tier"] = cpu_tier(out["CPU_Type"])
    out["CPU_family"] = cpu_family(out["CPU_Type"])
    out["log_price"] = log_price(out["Price (Euro)"])
    out["Dedicated_GPU"] = dedicated_gpu(out["GPU_Company"])
    out["Company_grouped"] = group_rare(out["Company"])
    out["OpSys_grouped"] = group_rare(out["OpSys_clean"])
    out["CPU_Company_grouped"] = group_rare(out["CPU_Company"])
    out["GPU_Company_grouped"] = group_rare(out["GPU_Company"])
    out["Storage_type_grouped"] = group_rare(out["Storage_type"], label="Other storage")
    key_cols = [c for c in original_columns if c != "Price (Euro)"]
    out["near_duplicate"] = flag_near_duplicates(out, key_cols)
    out["suspicious"], _ = flag_suspicious(out)
    return out


def load_clean(path=None):
    """Read the dataset and return the cleaned table in one call."""
    return clean(load_raw(path))


COLUMN_DICTIONARY = {
    "OpSys_clean": ("operating system with aliases merged (Mac OS X is macOS)", "os_map"),
    "OS_family": ("operating system family (Windows, macOS, Linux, Chrome OS, Android, No OS)", "os_map"),
    "Storage_type": ("combination of drive types, for example SSD + HDD", "st_type"),
    "Storage_GB_total": ("total storage capacity in GB (1 TB = 1000 GB)", "st_extra"),
    "has_SSD": ("True when the laptop has an SSD (Flash Storage does not count)", "st_extra"),
    "Screen_pixels": ("screen width times height in pixels", "st_extra"),
    "Touchscreen": ("True when the screen is a touchscreen", "st_extra"),
    "CPU_tier": ("Core i3, Core i5, Core i7 or Other", "st_extra"),
    "CPU_family": ("processor family (Core i3/i5/i7, Core M, Celeron, Pentium, Atom, Xeon, AMD A/E-Series, FX, Ryzen, Samsung Cortex); splits the mixed Other group of CPU_tier", "st_extra"),
    "log_price": ("natural logarithm of the price in euro", "st_extra, tr"),
    "Dedicated_GPU": ("True for a Nvidia or AMD graphics card (approximation by company)", "st_extra"),
    "Company_grouped": ("company, with companies below 10 laptops grouped as Other", "rare"),
    "OpSys_grouped": ("operating system, rare ones grouped as Other", "rare"),
    "CPU_Company_grouped": ("processor company, rare ones grouped as Other", "rare"),
    "GPU_Company_grouped": ("graphics company, rare ones grouped as Other", "rare"),
    "Storage_type_grouped": ("storage type, rare combinations grouped as Other storage", "st_type, rare"),
    "near_duplicate": ("True when another row has the same configuration with a different price", "q_dups"),
    "suspicious": ("True when a row breaks a plausibility rule (flagged, never removed)", "q_issues"),
}
