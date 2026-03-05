import numpy as np
from plots import *
from signals_generator import *

""""
Klasa reprezentująca sygnał, która przechowuje jego parametry, generuje sygnał.
W przyszłości może być rozszerzona o dodatkowe metody, próbkowanie i kwantowanie, analiza sygnału itp.
"""

class Signal:
    def __init__(self, A, d, fs, t1=0, function=None, T=None, kw=None, ts=None, t = None, signal=None):
        self.A = A # amplituda sygnału
        self.d = d # czas trwania sygnału
        self.fs = fs # częstotliwość próbkowania
        self.t1 = t1 # czas początkowy sygnału
        self.function = function # funkcja generująca sygnał

        """" Bazowo None - tylko dla sygnałów okresowych i skokowych """
        self.T = T # okres sygnału
        self.kw = kw # współczynnik wypełnienia dla sygnałów prostokątnych i trójkątnych
        self.ts = ts # czas skoku jednostkowego dla sygnału skokowego
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
                'ts': self.ts
            }
            # k - klucz, 
            # v - wartość, 
            # filtruje parametry, które są różne od None, aby uniknąć przekazywania niepotrzebnych argumentów do funkcji generującej sygnał

            filtered_params = {k: v for k, v in params.items() if v is not None}
            return self.function(**filtered_params)
        
    def visualize(self):
        discrete_signals = [unit_impulse_signal]

        is_discrete = self.function in discrete_signals

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
            unit_impulse_signal: "Impuls jednostkowy"
        }
        plot_signal(self.t, self.signal, title=names.get(self.function), discrete=is_discrete)