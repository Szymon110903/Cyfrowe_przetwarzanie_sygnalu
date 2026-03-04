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

# TODO: Spytać sie o znaczenie Amplitudy w sygnale o rozkładzie normalnym 
    # jako maksymalna wartość sygnału czy jako mnożnik 
def gaussian_noise(A, d, fs, t1 =0, **kwargs):
    samples, t = samples_count(d, fs, t1)
    signal =A* np.random.normal(0, 1, size=samples)
    return t, signal


# TODO: Sptytać o to czy brać pod uwage tylko pełne okresy sygnału
# TODO: uwzględnnić tylko pełne okresy do póżniejszej analizy sygnału - zwracać je w osobnej zmiennej

def sinusoidal_signal(A, T, d, fs, t1=0, **kwargs):
    _ , t = samples_count(d, fs, t1)
    # Wzór: x(t) = A * sin( (2 * PI / T) * (t - t1) )
    signal = A * np.sin((2 * np.pi / T) * (t - t1))
    return t, signal

def sinusoidal_signal_onehalf_rectified(A, T, d, fs, t1=0, **kwargs):
    _ , t = samples_count(d, fs, t1)
    # Wzór: x(t) = A * sin( (2 * PI / T) * (t - t1) )
    signal = 0.5* A * (np.sin((2 * np.pi / T) * (t - t1)) + np.abs(np.sin((2 * np.pi / T) * (t - t1))))
    return t, signal

def sinusoidal_signal_twohalf_rectified(A, T, d, fs, t1=0, **kwargs):
    _ , t = samples_count(d, fs, t1)
    # Wzór: x(t) = A * sin( (2 * PI / T) * (t - t1) )
    signal = A * np.abs(np.sin((2 * np.pi / T) * (t - t1)))
    return t, signal

def square_wave_signal(A, T, d, kw, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)

    # Jeśli czas wewnątrz okresu jest mniejszy niż (kw * T), dajemy A, w przeciwnym razie 0
    # (t-t1) % T czas wewnątrz okresu - do określenia czy faza wysoka czy niska
    signal = np.where((t - t1) % T < (kw * T), A, 0.0)
    return t, signal

def square_wave_signal_symetrical(A, T, d, kw, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)

    # jeśli czas okresu < (kw * T), to stan A, w przeciwnym razie -A
    # (t-t1) % T czas wewnątrz okresu - do określenia czy faza wysoka czy niska
    signal = np.where((t - t1) % T < (kw * T), A, -A)
    return t, signal

def triangle_wave_signal(A, T, d, kw, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)

    time_in_period = (t - t1) % T
    signal = np.where(time_in_period < (kw * T), A/(kw*T)*time_in_period, -A/((1-kw)*T)*(time_in_period - kw*T) + A)
    return t, signal

def unit_step_signal(A, ts, d, fs, t1=0, **kwargs):
    _, t = samples_count(d, fs, t1)
    conditions = [t < ts, t == ts, t > ts]
    choices = [0.0, A/2, A]

    signal = np.select(conditions, choices)
    return t, signal