import numpy as np

# Sygnał o rozkładzie jednostajnym
# przyjmuje losowe wartości z przedziału <A1, A2> - jednakowe prawdopodobieństwo wystąpienia każdej wartości
# A - amplituda sygnału
# t1 - początek sygnału - czas w którym rozpoczyna się sygnał okresowy
# t2, n2 - koniec sygnału,
# d - czas trwania sygnału okresowego
# T - okres sygnału okresowego
# fs - częstotliwość próbkowania sygnału okresowego

"""fukcja zwracająca próbki i czas dla każdej"""
def samples_count(d, fs, t1 =0, **kwargs):
    """obliczenie ilości próbek sygnału - czas trwania sygnału * częstotliwość próbkowania """
    samples = int(np.round(d * fs))
    """ obliczenie czasu dla każdej próbki """
    n = np.arange(samples)
    t = t1 + n / fs
    return samples, t

def uniform_noise(A, d, fs, t1 =0, **kwargs):
    samples, t = samples_count(d, fs, t1, **kwargs)
    signal = np.random.uniform(-A, A, size=samples)
    return t, signal

def gaussian_noise(A, d, fs, t1 =0, **kwargs):
    samples, t = samples_count(d, fs, t1)
    signal =np.random.normal(0, A, size=samples)
    return t, signal

def sinusoidal_signal(A, f, d, fs, t1=0, **kwargs):
    _ , t = samples_count(d, fs, t1)
    # Wzór: x(t) = A * sin( (2 * PI / T) * (t - t1) )
    signal = A * np.sin((2 * np.pi * f) * (t - t1))
    return t, signal

def sinusoidal_signal_onehalf_rectified(A, f, d, fs, t1=0, **kwargs):
    _ , t = samples_count(d, fs, t1)
    signal = 0.5 * A * (np.sin((2 * np.pi * f) * (t - t1)) + np.abs(np.sin((2 * np.pi * f) * (t - t1))))
    return t, signal

def sinusoidal_signal_twohalf_rectified(A, f, d, fs, t1=0, **kwargs):
    _ , t = samples_count(d, fs, t1)
    # Wzór: x(t) = A * sin( (2 * PI / T) * (t - t1) )
    signal = A * np.abs(np.sin((2 * np.pi * f) * (t - t1)))
    return t, signal

def square_wave_signal(A, f, d, kw, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)

    # Jeśli czas wewnątrz okresu jest mniejszy niż (kw * T), dajemy A, w przeciwnym razie 0
    # (t-t1) % T czas wewnątrz okresu - do określenia czy faza wysoka czy niska
    T = 1.0 / f
    signal = np.where((t - t1) % T < (kw * T), A, 0.0)
    return t, signal

def square_wave_signal_symetrical(A, f, d, kw, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)

    # jeśli czas okresu < (kw * T), to stan A, w przeciwnym razie -A
    # (t-t1) % T czas wewnątrz okresu - do określenia czy faza wysoka czy niska
    T = 1.0 / f
    signal = np.where((t - t1) % T < (kw * T), A, -A)
    return t, signal

def triangle_wave_signal(A, f, d, kw, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)
    T = 1.0 / f
    time_in_period = (t - t1) % T
    denom_rise = max(kw * T, 1e-10)
    denom_fall = max((1 - kw) * T, 1e-10)

    signal = np.where(
        time_in_period < (kw * T), 
        A / denom_rise * time_in_period, 
        -A / denom_fall * (time_in_period - kw * T) + A
)
    return t, signal

def unit_step_signal(A, ts, d, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)
    conditions = [t < ts, t == ts, t > ts]
    choices = [0.0, A/2, A]
    
    # np.select dobiera wartości z choices na podstawie warunków w conditions
    # wybiera w kolejności - pierwszy warunek, który jest spełniony, decyduje o wartości sygnału w danym punkcie czasu
    signal = np.select(conditions, choices)
    return t, signal

def unit_impulse_signal(A, ts, d, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)
    signal = np.where(np.isclose(t, ts, atol=1/(2*fs)), A, 0.0)

    return t, signal

def impulse_noise(A, d, fs, p, t1=0, **kwargs):
    samples, t = samples_count(d, fs, t1)
    random_values = np.random.uniform(0,1, size=samples)
    signal = np.where(random_values < p, A, 0)
    return t, signal

# Zadanie 4 pomocnicze generowanie funkcji S3
# Wazne w zadaniu fs = 16
def S3_signal(A, f, d=1.0, fs=16.0, t1=0, **kwargs):
   samples, t = samples_count(d, fs, t1)
   signal = 5 * np.sin(2 * np.pi * t * 0.5) + np.sin(2 * np.pi * t * 4) * fs
   return t, signal