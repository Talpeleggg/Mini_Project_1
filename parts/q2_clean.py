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
