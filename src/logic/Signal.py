from src.logic.signals_generator import *
""""
Klasa reprezentująca sygnał, która przechowuje jego parametry, generuje sygnał.
W przyszłości może być rozszerzona o dodatkowe metody, próbkowanie i kwantowanie, analiza sygnału itp.
"""
class Signal:
    def __init__(self, A, d, fs=1, t1=0, function=None, f=None, kw=None, ts=None, t = None, signal=None, p=None):
        self.A = A # amplituda sygnału
        self.d = d # czas trwania sygnału
        self.fs = fs # częstotliwość próbkowania
        self.t1 = t1 # czas początkowy sygnału
        self.function = function # funkcja generująca sygnał

        """" Bazowo None - tylko dla sygnałów okresowych i skokowych """
        self.f = f # częstotliwość sygnału
        self.kw = kw # współczynnik wypełnienia dla sygnałów prostokątnych i trójkątnych
        self.ts = ts # czas skoku jednostkowego dla sygnału skokowego
        """" Parametr wykorzystywany w szumie impulsowym standardowo None"""
        self.p = p

        """ Parametry sygnału - wartość średnia, wartość średnia bezwzględna, wartość skuteczna, wariancja, moc średnia """
        self.mean_val = None
        self.absolute_mean_val = None
        self.avg_power = None
        self.variance = None
        self.effective_value = None

        # obsługa sytuacji, gdy sygnał jest już wygenerowany - wczytanie pliku
        if t is not None and signal is not None:
            self.t = t
            self.signal = signal
        elif function is not None:
            self.t, self.signal = self.generate_signal()
            self.calculate_parameters()
        else:
            raise ValueError("Niepoprawne parametry sygnału.")

    def generate_signal(self):
        if self.function is None:
            raise ValueError("Funkcja generująca sygnał nie została zdefiniowana.")
        else:
            params = {
                'A': self.A,
                'd': self.d,
                'fs': self.fs,
                't1': self.t1,
                'f': self.f,
                'kw': self.kw,
                'ts': self.ts,
                'p': self.p
            }
            # k - klucz,
            # v - wartość,
            # filtruje parametry, które są różne od None, aby uniknąć przekazywania niepotrzebnych argumentów do funkcji generującej sygnał

            filtered_params = {k: v for k, v in params.items() if v is not None}
            return self.function(**filtered_params)

    def get_signal_name(self):
        names = {
            uniform_noise: "Sygnał o rozkładzie jednostajnym",
            gaussian_noise: "Sygnał o rozkładzie normalnym",
            sinusoidal_signal: "Sygnał sinusoidalny",
            sinusoidal_signal_onehalf_rectified: "Sygnał sinusoidalny z dodatnią częścią",
            sinusoidal_signal_twohalf_rectified: "Sygnał sinusoidalny z dodatnią częścią prostowaną",
            square_wave_signal: "Sygnał prostokątny",
            square_wave_signal_symetrical: "Sygnał prostokątny symetryczny",
            triangle_wave_signal: "Sygnał trójkątny",
            unit_step_signal: "Sygnał skok jednostkowy",
            unit_impulse_signal: "Impuls jednostkowy",
            impulse_noise: "Szum impulsowy",
            S3_signal: "Sygnał testowy S3",
            exponential_signal: "Sygnał wykładniczy"
        }
        return names.get(self.function)

    def get_full_periods(self):
        periodic_signals = [
            sinusoidal_signal, sinusoidal_signal_onehalf_rectified,
            sinusoidal_signal_twohalf_rectified, square_wave_signal,
            square_wave_signal_symetrical, triangle_wave_signal
        ]
        if self.f is not None and self.function in periodic_signals:
            T = 1.0 / self.f
            full_periods = int(self.d // T)
            if full_periods > 0:
                time_to_keep = full_periods * T
                samples_to_keep = int(np.round(time_to_keep * self.fs))
                return self.signal[:samples_to_keep]
            else:
                return self.signal

        return self.signal

    def calculate_parameters(self):
        signal = self.get_full_periods()
        if len(signal) == 0:
            return None

        mean_val = np.mean(signal)
        absoulute_mean_val = np.mean(np.abs(signal))
        avg_power = np.mean(signal ** 2)
        variance = np.var(signal)
        effective_value = np.sqrt(avg_power)

        self.mean_val = mean_val
        self.absolute_mean_val = absoulute_mean_val
        self.avg_power = avg_power
        self.variance = variance
        self.effective_value = effective_value

        return {
            "Wartosc srednia": mean_val,
            "Wartosc srednia bezwzgledna": absoulute_mean_val,
            "Wartosc skuteczna": effective_value,
            "Wariancja": variance,
            "Moc srednia": avg_power,
        }
