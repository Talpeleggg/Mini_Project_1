"""TEMPORARY helper module. Owner: Part 2.

Will hold: load_raw, clean (returns a new table, never changes the input), load_clean.

Other parts import from here. Do not write code here until the related decisions are made on the board.
At integration the functions are copied into the final notebook and this file is deleted.
"""
# HE: --------------------------------------------------------------------------
# HE: מה הקובץ הזה עושה: הוא מחזיק פונקציות עזר לעבודה על נתוני המחשבים. כרגע יש בו
# HE: פונקציה אחת, load_raw, שרק קוראת את קובץ הנתונים. בהמשך (Q2 ב׳) נוסיף כאן את
# HE: clean (ניקוי) ו-load_clean (קריאה + ניקוי יחד), שאוהד ישתמש בהן.
# HE: --------------------------------------------------------------------------
from pathlib import Path

import pandas as pd

# HE: Path הוא כלי של פייתון לעבודה עם נתיבי קבצים בלי לטעות בלוכסנים.
# HE: __file__ הוא הנתיב של הקובץ הנוכחי (q2_clean.py). .parent.parent עולה שתי תיקיות למעלה,
# HE: מתיקיית parts אל שורש המאגר, ומשם נכנסים אל data/laptop_price_dataset.csv.
# HE: הנתיב יחסי (לא כתוב בו שם המשתמש שלך), ולכן הוא יעבוד אצל כל אחד ואצל הבודק.
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "laptop_price_dataset.csv"


def load_raw(path=None):
    """Read the laptop dataset exactly as it is in the file.

    The raw file is never modified. Every cleaning step lives in `clean()` and works on a copy.
    """
    # HE: הפונקציה מקבלת נתיב אופציונלי. אם לא נתנו נתיב (path הוא None), משתמשים ב-DATA_PATH.
    # HE: pd.read_csv קורא קובץ CSV (טבלה בטקסט, עמודות מופרדות בפסיקים) ומחזיר טבלה (DataFrame).
    # HE: בכוונה לא משנים כלום בקריאה: לא מוחקים שורות ולא מתקנים ערכים. הנתונים הגולמיים
    # HE: נשארים כמו שהם, כדי שנוכל תמיד להשוות מול המקור.
    return pd.read_csv(path or DATA_PATH)


# HE: --------------------------------------------------------------------------
# HE: ניקוי מערכת ההפעלה (החלטה os_map): מאחדים רק כינויים של אותה מערכת, ומוסיפים עמודת "משפחה".
# HE: --------------------------------------------------------------------------
# HE: מילון כינויים: "Mac OS X" ו-"macOS" הן אותה מערכת בשני שמות, ולכן ממפים אחת לשנייה.
OS_ALIASES = {"Mac OS X": "macOS"}

# HE: מילון משפחות: Windows 10, Windows 7 ו-Windows 10 S הן גרסאות שונות (מוצרים שונים), ולכן נשארות נפרדות
# HE: בעמודה OpSys_clean, אבל מקובצות יחד לעמודה OS_family כשצריך קבוצות גדולות.
OS_FAMILY = {
    "Windows 10": "Windows", "Windows 7": "Windows", "Windows 10 S": "Windows",
    "macOS": "macOS", "Linux": "Linux", "Chrome OS": "Chrome OS", "Android": "Android", "No OS": "No OS",
}


def clean_opsys(opsys):
    """Unify aliases of the same operating system and add the OS family.

    Returns (OpSys_clean, OS_family) as two Series with the same index as the input.
    Only true aliases are merged: Windows versions are different products and stay separate.
    """
    # HE: replace מחליפה ערכים לפי המילון. ערכים שלא במילון נשארים כמו שהם.
    clean = opsys.replace(OS_ALIASES)
    # HE: map מחליפה כל ערך בערך המתאים לו במילון. ערך שחסר במילון הופך ל-NaN.
    family = clean.map(OS_FAMILY)
    # HE: אם יש NaN במשפחה, פירושו שמצאנו שם מערכת חדש שלא הכרנו. עוצרים במקום להמשיך בשקט.
    unmapped = sorted(clean[family.isna()].unique())
    assert not unmapped, f"operating systems without a family: {unmapped}"
    return clean, family


# HE: --------------------------------------------------------------------------
# HE: פירוק עמודת Memory (החלטות st_type ו-st_extra): מחרוזת כמו "128GB SSD +  1TB HDD" מכילה כונן אחד או שניים,
# HE: ולכל כונן יש קיבולת (GB או TB) וסוג (SSD, HDD, Flash Storage, Hybrid). אנחנו מחלצים מהמחרוזת:
# HE: Storage_type (תווית שילוב), Storage_GB_total (קיבולת כוללת) ו-has_SSD (האם יש SSD).
# HE: --------------------------------------------------------------------------
import re

# HE: ביטוי רגולרי (regex) שמתאר כונן אחד: מספר (אולי עם נקודה עשרונית), יחידה (GB או TB), רווח, וסוג כונן.
# HE: \d+ = ספרה אחת או יותר. (?:\.\d+)? = אולי נקודה וספרות. \s* = אפס רווחים או יותר. (GB|TB) = אחת משתי היחידות.
DRIVE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(GB|TB)\s+(SSD|HDD|Flash Storage|Hybrid)")

# HE: סדר קבוע לתווית: כך "SSD + HDD" תמיד נכתב באותו סדר, ולא פעם "HDD + SSD".
STORAGE_ORDER = ["SSD", "HDD", "Flash Storage", "Hybrid"]

# HE: הנחה שלנו (החלטה st_extra): 1 TB = 1000 GB (כך משווקים כוננים), ולא 1024.
GB_PER_TB = 1000


def parse_memory(memory):
    """Parse one `Memory` string.

    Returns (storage_type, total_gb, has_ssd). The storage type is a canonical label of the drive types
    that are present, in a fixed order, for example "SSD + HDD". Two drives of the same type give one type
    ("SSD") and their capacities are added. Raises AssertionError for text it does not understand.
    """
    # HE: findall מחזירה רשימה של כל הכוננים שנמצאו, כל כונן כשלישייה (מספר, יחידה, סוג).
    drives = DRIVE_PATTERN.findall(memory)
    assert drives, f"cannot parse Memory string: {memory!r}"
    # HE: בודקים שלא נשאר בטקסט שום דבר שלא הבנו: מוחקים את הכוננים שנמצאו, ואת סימן ה-+ ואת הרווחים,
    # HE: ומה שנשאר חייב להיות ריק. כך נתפוס פורמט חדש שלא צפינו.
    leftover = DRIVE_PATTERN.sub("", memory).replace("+", "").strip()
    assert leftover == "", f"unrecognised text {leftover!r} in Memory string: {memory!r}"

    # HE: קבוצה (set) של סוגי הכוננים שמופיעים. אם יש שני SSD, הסוג SSD מופיע פעם אחת בקבוצה.
    types = {drive_type for _, _, drive_type in drives}
    # HE: בונים את התווית לפי הסדר הקבוע, ומחברים עם " + ".
    storage_type = " + ".join(t for t in STORAGE_ORDER if t in types)
    # HE: קיבולת כוללת: מחברים את כל הכוננים, ומכפילים ב-1000 כשהיחידה היא TB.
    total_gb = sum(float(value) * (GB_PER_TB if unit == "TB" else 1) for value, unit, _ in drives)
    return storage_type, total_gb, "SSD" in types


def parse_memory_series(memory):
    """Apply `parse_memory` to a whole column. Returns a DataFrame with Storage_type, Storage_GB_total, has_SSD."""
    # HE: apply מפעילה את הפונקציה על כל ערך בעמודה. התוצאה היא רשימה של שלישיות, שהופכות לטבלה בת שלוש עמודות.
    parsed = [parse_memory(m) for m in memory]
    return pd.DataFrame(parsed, columns=["Storage_type", "Storage_GB_total", "has_SSD"], index=memory.index)


# HE: --------------------------------------------------------------------------
# HE: עמודות המסך, המעבד, המחיר וכרטיס המסך (החלטה st_extra). כל פונקציה מקבלת עמודה (Series) ומחזירה עמודה חדשה.
# HE: --------------------------------------------------------------------------
import numpy as np

CPU_TIERS = ["Core i3", "Core i5", "Core i7", "Other"]
DEDICATED_GPU_COMPANIES = ["Nvidia", "AMD"]
KNOWN_GPU_COMPANIES = ["Intel", "Nvidia", "AMD", "ARM"]


def screen_pixels(resolution):
    """Number of pixels (width x height) taken from the end of the ScreenResolution text."""
    # HE: הרזולוציה (למשל 1920x1080) נמצאת תמיד בסוף המחרוזת. \s*$ אומר "אולי רווחים ואז סוף המחרוזת".
    # HE: extract שולפת את שני המספרים (רוחב וגובה) לשתי עמודות.
    width_height = resolution.str.extract(r"(\d+)x(\d+)\s*$").astype(float)
    assert width_height.notna().all().all(), "a ScreenResolution without a WxH resolution at the end"
    # HE: פיקסלים = רוחב כפול גובה.
    return (width_height[0] * width_height[1]).astype(int)


def has_touchscreen(resolution):
    """True when the ScreenResolution text mentions a touchscreen."""
    # HE: regex=False אומר "חפש את הטקסט כמו שהוא".
    return resolution.str.contains("Touchscreen", regex=False)


def cpu_tier(cpu_type):
    """Processor tier: Core i3 / Core i5 / Core i7, and Other for everything else."""
    # HE: לוקחים את תחילת השם אם הוא "Core i" ואחריו 3, 5, 7 או 9. מה שלא מתחיל כך (Celeron, Pentium, AMD...) הופך ל-Other.
    tier = cpu_type.str.extract(r"^(Core i[3579])")[0].fillna("Other")
    # HE: אם יופיע Core i9, הוא לא ברשימה המותרת וניעצר, כדי שנחליט במפורש מה עושים איתו.
    unexpected = sorted(set(tier) - set(CPU_TIERS))
    assert not unexpected, f"unexpected CPU tiers: {unexpected}"
    return tier


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


# HE: --------------------------------------------------------------------------
# HE: קטגוריות נדירות וסימונים (החלטות rare, q_dups, q_issues). לא מוחקים אף שורה: רק מוסיפים עמודות עזר.
# HE: --------------------------------------------------------------------------
RARE_MIN_COUNT = 10   # HE: קטגוריה עם פחות מ-10 מחשבים נחשבת נדירה (אותו סף כמו בביקורת)


def group_rare(series, min_count=RARE_MIN_COUNT, label="Other"):
    """Replace categories with fewer than `min_count` rows by `label`. Returns a new Series; no row is removed."""
    # HE: value_counts סופרת כמה מחשבים בכל קטגוריה. rare היא רשימת הקטגוריות שמתחת לסף.
    counts = series.value_counts()
    rare = counts[counts < min_count].index
    # HE: אם התווית "Other" כבר קיימת כקטגוריה אמיתית, הקיבוץ היה מערבב אותה איתה. עוצרים.
    assert label not in set(series.unique()), f"{label!r} is already a category of this column"
    # HE: where משאירה את הערך כשהתנאי נכון, ומחליפה בתווית כשהוא לא. כאן: משאירים קטגוריות שאינן נדירות.
    return series.where(~series.isin(rare), label)


def flag_near_duplicates(df, key_cols):
    """True for every row that shares all of `key_cols` with another row (here: every column except the price)."""
    # HE: keep=False מסמנת את כל השורות בקבוצה, ולא רק את הכפולה.
    return df.duplicated(subset=key_cols, keep=False)


# HE: כללי הגיון (אותם חמישה כללים מהביקורת): כל כלל הוא פונקציה שמקבלת את הטבלה ומחזירה True/False לכל שורה.
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


# HE: --------------------------------------------------------------------------
# HE: הפונקציה הראשית: clean מחברת את כל הצעדים שבנינו (B1 עד B4) לקריאה אחת, ו-load_clean קוראת ומנקה יחד.
# HE: אוהד (חלק 3) משתמש רק ב-load_clean. שמות העמודות החדשות הם "חוזה" מולו: לא משנים בלי להודיע.
# HE: --------------------------------------------------------------------------
def clean(df):
    """Return a new, cleaned table. The input table is never changed.

    The cleaned table has all the original columns, unchanged, followed by the new columns listed in
    `COLUMN_DICTIONARY`. No row is removed.
    """
    # HE: מתחילים בעותק, כדי שהטבלה שקיבלנו לא תשתנה. את רשימת העמודות המקוריות שומרים לפני שמוסיפים חדשות.
    out = df.copy()
    original_columns = list(df.columns)

    # HE: B1: מערכת הפעלה
    out["OpSys_clean"], out["OS_family"] = clean_opsys(out["OpSys"])
    # HE: B2: אחסון (שלוש עמודות בבת אחת)
    out = pd.concat([out, parse_memory_series(out["Memory"])], axis=1)
    # HE: B3: מסך, מעבד, מחיר וכרטיס מסך
    out["Screen_pixels"] = screen_pixels(out["ScreenResolution"])
    out["Touchscreen"] = has_touchscreen(out["ScreenResolution"])
    out["CPU_tier"] = cpu_tier(out["CPU_Type"])
    out["log_price"] = log_price(out["Price (Euro)"])
    out["Dedicated_GPU"] = dedicated_gpu(out["GPU_Company"])
    # HE: B4: קיבוץ נדירים בעמודות עזר
    out["Company_grouped"] = group_rare(out["Company"])
    out["OpSys_grouped"] = group_rare(out["OpSys_clean"])
    out["CPU_Company_grouped"] = group_rare(out["CPU_Company"])
    out["GPU_Company_grouped"] = group_rare(out["GPU_Company"])
    out["Storage_type_grouped"] = group_rare(out["Storage_type"], label="Other storage")
    # HE: B4: סימונים. key_cols הם רק העמודות המקוריות חוץ מהמחיר (log_price נגזר מהמחיר, ולכן לא נכלל).
    key_cols = [c for c in original_columns if c != "Price (Euro)"]
    out["near_duplicate"] = flag_near_duplicates(out, key_cols)
    out["suspicious"], _ = flag_suspicious(out)
    return out


def load_clean(path=None):
    """Read the dataset and return the cleaned table in one call."""
    return clean(load_raw(path))


# HE: מילון העמודות החדשות: לכל עמודה, מה היא ואיזו החלטה בלוח יצרה אותה.
COLUMN_DICTIONARY = {
    "OpSys_clean": ("operating system with aliases merged (Mac OS X is macOS)", "os_map"),
    "OS_family": ("operating system family (Windows, macOS, Linux, Chrome OS, Android, No OS)", "os_map"),
    "Storage_type": ("combination of drive types, for example SSD + HDD", "st_type"),
    "Storage_GB_total": ("total storage capacity in GB (1 TB = 1000 GB)", "st_extra"),
    "has_SSD": ("True when the laptop has an SSD (Flash Storage does not count)", "st_extra"),
    "Screen_pixels": ("screen width times height in pixels", "st_extra"),
    "Touchscreen": ("True when the screen is a touchscreen", "st_extra"),
    "CPU_tier": ("Core i3, Core i5, Core i7 or Other", "st_extra"),
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
