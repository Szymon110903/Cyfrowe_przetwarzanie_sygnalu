import numpy as np

# Sygnał o rozkładzie jednostajnym
# przyjmuje losowe wartości z przedziału <A1, A2> - jednakowe prawdopodobieństwo wystąpienia każdej wartości
# A - amplituda sygnału
# t1 - początek sygnału - czas w którym rozpoczyna się sygnał okresowy
# t2, n2 - koniec sygnału,
# d - czas trwania sygnału okresowego
# T - okres sygnału okresowego
# fs - częstotliwość próbkowania sygnału okresowego
"""fukcja zwracająca czas trwania sygnału i czas dla każdej próbki sygnału"""

def samples_count(d, fs, t1 =0):
    """obliczenie ilości próbek sygnału - czas trwania sygnału * częstotliwość próbkowania """
    samples = int(np.round(d * fs))
    """ obliczenie czasu dla każdej próbki """
    n = np.arange(samples)
    t = t1 + n / fs
    return samples, t

def uniform_noise(A, d, fs, t1 =0):
    samples, t = samples_count(d, fs, t1)
    signal = np.random.uniform(-A, A, size=samples)
    return t, signal

# TODO: Spytać sie o znaczenie Amplitudy w sygnale o rozkładzie normalnym 
    # jako maksymalna wartość sygnału czy jako mnożnik 
def gaussian_noise(A, d, fs, t1 =0):
    samples, t = samples_count(d, fs, t1)
    signal =A* np.random.normal(0, 1, size=samples)
    return t, signal


# TODO: Sptytać o to czy brać pod uwage tylko pełne okresy sygnału

# TODO: uwzględnnić tylko pełne okresy do póżniejszej analizy sygnału - zwracać je w osobnej zmiennej

def sinusoidal_signal(A, T, d, fs, t1=0):
    _ , t = samples_count(d, fs, t1)
    # Wzór: x(t) = A * sin( (2 * PI / T) * (t - t1) )
    signal_total = A * np.sin((2 * np.pi / T) * (t - t1))
    return t, signal_total