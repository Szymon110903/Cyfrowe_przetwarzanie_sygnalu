import numpy as np
from plots import *
from signals_generator import *

""""
Klasa reprezentująca sygnał, która przechowuje jego parametry, generuje sygnał.
W przyszłości może być rozszerzona o dodatkowe metody, próbkowanie i kwantowanie, analiza sygnału itp.
"""

class Signal:
    def __init__(self, A, d, fs, t1=0, function=None, T=None, kw=None, ts=None, t = None, signal=None, p=None):
        self.A = A # amplituda sygnału
        self.d = d # czas trwania sygnału
        self.fs = fs # częstotliwość próbkowania
        self.t1 = t1 # czas początkowy sygnału
        self.function = function # funkcja generująca sygnał

        """" Bazowo None - tylko dla sygnałów okresowych i skokowych """
        self.T = T # okres sygnału
        self.kw = kw # współczynnik wypełnienia dla sygnałów prostokątnych i trójkątnych
        self.ts = ts # czas skoku jednostkowego dla sygnału skokowego
        """" Parametr wykorzystywany w szumie impulsowym standardowo None"""
        self.p = p
        print(f"Tworzenie sygnału: A={A}, d={d}, fs={fs}, t1={t1}, function={function.__name__ if function else None}, T={T}, kw={kw}, ts={ts}")

        # obsługa sytuacji, gdy sygnał jest już wygenerowany - wczytanie pliku
        if t is not None and signal is not None:
            self.t = t
            self.signal = signal
        elif function is not None:
            self.t, self.signal = self.generate_signal()
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
                'T': self.T,
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
            impulse_noise: "Szum impulsowy"
        }
        return names.get(self.function)

    def get_full_periods(self):
        periodic_signals = [
            sinusoidal_signal, sinusoidal_signal_onehalf_rectified,
            sinusoidal_signal_twohalf_rectified, square_wave_signal,
            square_wave_signal_symetrical, triangle_wave_signal
        ]
        if self.T is not None and self.function in periodic_signals:
            full_periods = int(self.d // self.T)
            if full_periods > 0:
                time_to_keep = full_periods * self.T
                samples_to_keep = int(np.round(time_to_keep * self.fs))
                return self.signal[:samples_to_keep]
            else:
                return self.signal

        return self.signal

    """" Rozbicie funkcji visualise na visualise i visualise histogram"""
    def visualize(self):
        discrete_signals = [unit_impulse_signal, impulse_noise]
        is_discrete = self.function in discrete_signals
        plot_signal(self.t, self.signal, title=self.get_signal_name(), discrete=is_discrete)

    def visualize_histogram(self, bins=10):
        title = f"{self.get_signal_name()} - Histogram"
        signal_values = self.get_full_periods()
        plot_histogram(signal_values, bins=bins, title=title)

    def calculate_parameters(self):
        signal = self.get_full_periods()
        if len(signal) == 0:
            return None

        mean_val = np.mean(signal)
        absoulute_mean_val = np.mean(np.abs(signal))
        avg_power = np.mean(signal ** 2)
        variance = np.var(signal)
        effective_value = np.sqrt(avg_power)

        return {
            "Wartosc srednia": mean_val,
            "Wartosc srednia bezwzgledna": absoulute_mean_val,
            "Wartosc skuteczna": effective_value,
            "Wariancja": variance,
            "Moc srednia": effective_value,
        }

    def print_parameters(self):
        parameters = self.calculate_parameters()

        if parameters is not None:
            print(f"--- Wyliczone parametry dla: {self.get_signal_name()} ---")
            for name, value in parameters.items():
                print(f"{name}: {value:.4f}")
        else:
            print("Sygnał jest pusty")