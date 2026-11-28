"""TEMPORARY helper module. Owner: Part 1 (Q1 A: the three neuron models).

Contract used by the other parts:
    make_rngs(seed, n)                      -> list of n independent random generators
    simulate_regular(T, rng, rate_hz=10)    -> spike times (s), strictly increasing, inside [0, T)
    simulate_irregular(T, rng, rate_hz=10)  -> same
    simulate_bursting(T, rng, rate_hz=10)   -> same (an empty array if no spike falls in [0, T))

The explanations and the reasons for every decision are in Q1_part1_models_validation.ipynb.
At integration the functions are copied into the final notebook and this file is deleted.
"""
import numpy as np

# ---- Parameters shared by all three neurons (times in seconds) ----
# refractory period: no two spikes closer than 2 ms
DEAD_TIME = 0.002

# warm-up: every neuron starts firing 2 s before the recording begins (spikes before t = 0 are dropped)
BURN_IN = 2.0

# ---- Regular and irregular neurons ----
# Gamma shape of the regular neuron (large k = low variability)
K_REGULAR = 400
# Gamma shape of the irregular neuron (k = 1 -> exponential ISIs, Poisson-like)
K_IRREGULAR = 1

# ---- Bursting neuron ----
# spikes per burst = MIN_SPIKES + Poisson(EXTRA_SPIKES_MEAN)  -> mean 4
MIN_SPIKES = 2
EXTRA_SPIKES_MEAN = 2
MEAN_SPIKES_PER_BURST = MIN_SPIKES + EXTRA_SPIKES_MEAN

# ISI inside a burst: mean 5 ms, minimum 2 ms, Gamma shape 9 -> CV = 0.2
INTRA_MEAN = 0.005
INTRA_K = 9

# quiet period between bursts: at least 50 ms, Gamma shape 4
QUIET_MIN = 0.050
QUIET_K = 4


def make_rngs(seed, n=3):
    """Return n independent random generators derived from one master seed."""
    # split the master seed into n child seeds, one random stream per neuron
    child_seeds = np.random.SeedSequence(seed).spawn(n)
    return [np.random.default_rng(s) for s in child_seeds]


# ---- Building block 1: drawing ISIs ----
def draw_isis(n, k, mean_isi, rng):
    """Draw n random inter-spike intervals (in seconds) = DEAD_TIME + Gamma(k), with mean `mean_isi`."""
    # scale, so that the mean is exactly mean_isi
    theta = (mean_isi - DEAD_TIME) / k
    # n random Gamma numbers
    random_part = rng.gamma(shape=k, scale=theta, size=n)
    # shift every interval by the dead time
    return DEAD_TIME + random_part


# ---- Building block 2: from ISIs to spike times ----
def isis_to_spike_times(k, T, rng, rate_hz=10.0):
    """Spike times (in seconds) of a Gamma renewal process inside [0, T)."""
    mean_isi = 1 / rate_hz

    # random time of the first spike, BURN_IN seconds before the recording starts
    first_spike = rng.uniform(0, mean_isi) - BURN_IN

    # draw more ISIs than needed (about 2x, for the burn-in + the recording)
    n_isis = int(2 * rate_hz * (BURN_IN + T)) + 20
    isis = draw_isis(n_isis, k, mean_isi, rng)

    # running total of ISIs
    spike_times = first_spike + np.concatenate([[0], np.cumsum(isis)])
    # make sure we covered the whole recording
    assert spike_times[-1] >= T, "not enough ISIs were drawn"

    # keep only spikes inside the recording [0, T)
    return spike_times[(spike_times >= 0) & (spike_times < T)]


# ---- Building block 3: checking that spike times are valid ----
def check_spike_times(spike_times, T):
    """Stop with an error if the spike times break the model's rules."""
    # intervals between consecutive spikes
    isis = np.diff(spike_times)

    assert np.all(spike_times >= 0),          "a spike is before time 0"
    assert np.all(spike_times < T),           "a spike is after the end of the recording"
    assert np.all(isis > 0),                  "spike times are not in increasing order"
    assert np.all(isis >= DEAD_TIME - 1e-12), "two spikes are closer than the dead time"


# ---- The regular and irregular neurons ----
def simulate_regular(T, rng, rate_hz=10.0, k=K_REGULAR):
    """Spike times of the regular neuron (Gamma renewal process with a large shape k)."""
    # building blocks 1 + 2
    spike_times = isis_to_spike_times(k, T, rng, rate_hz)
    # building block 3
    check_spike_times(spike_times, T)
    return spike_times


def simulate_irregular(T, rng, rate_hz=10.0):
    """Spike times of the irregular neuron (k = 1: exponential ISIs, Poisson-like)."""
    # building blocks 1 + 2
    spike_times = isis_to_spike_times(K_IRREGULAR, T, rng, rate_hz)
    # building block 3
    check_spike_times(spike_times, T)
    return spike_times


# ---- The bursting neuron ----
def draw_shifted_gamma(n, mean, k, minimum, rng):
    """Draw n values = minimum + Gamma(k, theta), with overall mean `mean`."""
    # scale, so that the overall mean is exactly `mean`
    theta = (mean - minimum) / k
    return minimum + rng.gamma(shape=k, scale=theta, size=n)


def bursting_timing(rate_hz=10.0):
    """Mean burst cycle and mean quiet period (s) that give the requested mean rate."""
    # one burst every MEAN_SPIKES_PER_BURST / rate seconds on average (400 ms at 10 Hz)
    mean_cycle = MEAN_SPIKES_PER_BURST / rate_hz
    # mean quiet = mean cycle minus the mean burst length (3 intervals of 5 ms)
    quiet_mean = mean_cycle - (MEAN_SPIKES_PER_BURST - 1) * INTRA_MEAN
    assert quiet_mean > QUIET_MIN, "rate too high: no room for the minimum quiet period"
    return mean_cycle, quiet_mean


def simulate_bursting(T, rng, rate_hz=10.0):
    """Spike times of the bursting neuron."""
    mean_cycle, quiet_mean = bursting_timing(rate_hz)
    spike_times = []

    # 1. random start time of the first burst, BURN_IN seconds before the recording
    burst_start = rng.uniform(0, mean_cycle) - BURN_IN

    while burst_start < T:
        # 2. number of spikes in this burst (at least 2)
        n_spikes = MIN_SPIKES + rng.poisson(EXTRA_SPIKES_MEAN)
        # intervals inside the burst (one less than the number of spikes)
        intra_isis = draw_shifted_gamma(n_spikes - 1, INTRA_MEAN, INTRA_K, DEAD_TIME, rng)
        # spike times of this burst
        burst = burst_start + np.concatenate([[0], np.cumsum(intra_isis)])
        spike_times.extend(burst)

        # 3. quiet period, measured from the last spike of the burst
        quiet = draw_shifted_gamma(1, quiet_mean, QUIET_K, QUIET_MIN, rng)[0]
        burst_start = burst[-1] + quiet

    # 4. keep only spikes inside the recording, then check them (building block 3)
    spike_times = np.array(spike_times, dtype=float)
    spike_times = spike_times[(spike_times >= 0) & (spike_times < T)]
    check_spike_times(spike_times, T)
    return spike_times
