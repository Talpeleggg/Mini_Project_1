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
