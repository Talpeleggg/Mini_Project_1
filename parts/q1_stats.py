"""TEMPORARY helper module. Owner: Part 2.

Will hold: isi, cv, lv, fano, short_isi_fraction, next_interval_corr (each returns nan when undefined).

Other parts import from here. Do not write code here until the related decisions are made on the board.
At integration the functions are copied into the final notebook and this file is deleted.
"""

import numpy as np

# HE: ----------------------------------------------------------------------------
# HE: פונקציות הסטטיסטיקה של Q1 ב׳ (החלטות b_stats, b_thr, b_fano, b_bin).
# HE: קלט: spikes = מערך זמני פעימות בשניות (עולה), T = אורך ההקלטה בשניות.
# HE: כלל: מדד שאי אפשר לחשב (מעט מדי פעימות, חלוקה באפס) מחזיר np.nan, ולא שגיאה.
# HE: ----------------------------------------------------------------------------


def isi(spikes):
    """Inter-spike intervals in seconds: the gaps between consecutive spikes."""
    # HE: diff מחסרת כל זמן מהקודם לו, וכך מתקבלים המרווחים. n פעימות נותנות n-1 מרווחים.
    return np.diff(np.asarray(spikes, dtype=float))


def mean_rate(spikes, T):
    """Mean firing rate in Hz: number of spikes divided by the recording length."""
    return len(spikes) / T


def mean_isi(spikes):
    """Mean interval in seconds (nan when there is no interval)."""
    x = isi(spikes)
    return float(x.mean()) if len(x) >= 1 else np.nan


def cv(spikes):
    """Coefficient of variation of the intervals: std / mean (sample std, ddof=1). Needs at least 2 intervals."""
    x = isi(spikes)
    # HE: מחשבים סטיית תקן רק אם יש לפחות שני מרווחים, והממוצע לא אפס.
    if len(x) < 2 or x.mean() == 0:
        return np.nan
    return float(x.std(ddof=1) / x.mean())


def lv(spikes):
    """Local variation (Shinomoto): compares only neighbouring intervals, so it ignores slow rate changes."""
    x = isi(spikes)
    if len(x) < 2:
        return np.nan
    a, b = x[:-1], x[1:]
    # HE: לכל זוג מרווחים שכנים: ((a-b)/(a+b))^2. מכפילים ב-3 וממצעים (חלקי מספר המרווחים פחות 1).
    s = a + b
    if np.any(s == 0):
        return np.nan
    return float(3.0 * np.mean(((a - b) / s) ** 2))


def next_interval_corr(spikes):
    """Serial correlation between each interval and the next one (does a short one follow a long one?)."""
    x = isi(spikes)
    if len(x) < 3:
        return np.nan
    a, b = x[:-1], x[1:]
    # HE: אם כל המרווחים זהים אין שונות ולכן אין מתאם (חלוקה באפס). מחזירים nan.
    # HE: בגלל שגיאות עיגול של מספרים עשרוניים, "זהים" פירושו שהשונות זעירה ביחס לממוצע, ולא בדיוק אפס.
    if a.std() <= 1e-9 * x.mean() or b.std() <= 1e-9 * x.mean():
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def short_isi_fraction(spikes, threshold=0.010):
    """Fraction of intervals shorter than `threshold` seconds (default 10 ms): the share of 'burst-like' intervals."""
    x = isi(spikes)
    if len(x) == 0:
        return np.nan
    return float(np.mean(x < threshold))


def short_isi_curve(spikes, thresholds):
    """Decision b_thr: the short-interval fraction for every threshold in `thresholds` (seconds)."""
    return np.array([short_isi_fraction(spikes, t) for t in thresholds])


def window_counts(spikes, T, window):
    """Spike counts in consecutive non-overlapping windows of `window` seconds (the last partial window is dropped)."""
    n_windows = int(np.floor(T / window + 1e-9))
    if n_windows < 1:
        return np.array([], dtype=int)
    # HE: histogram סופר כמה פעימות נופלות בכל חלון. edges הם קצוות החלונות.
    edges = np.arange(n_windows + 1) * window
    counts, _ = np.histogram(spikes, bins=edges)
    return counts


def fano(spikes, T, window):
    """Fano factor: variance / mean of the spike counts in windows of `window` seconds (needs 2 windows)."""
    c = window_counts(spikes, T, window)
    if len(c) < 2 or c.mean() == 0:
        return np.nan
    return float(c.var(ddof=1) / c.mean())


def fano_curve(spikes, T, windows):
    """Decision b_fano: the Fano factor for every window size in `windows` (seconds)."""
    return np.array([fano(spikes, T, w) for w in windows])


def rate_over_time(spikes, T, bin_size=0.100):
    """Decision b_bin: firing rate in Hz in consecutive bins of `bin_size` seconds (default 100 ms)."""
    c = window_counts(spikes, T, bin_size)
    return c / bin_size
