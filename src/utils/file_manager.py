# struct - wysoka wydajność, tworzenie nagłowków,
import struct

import numpy as np

import src.logic.Signal as Signal
import os
from src.logic.signals_generator import *

DIR = "signals/"
ID_TO_FUNC = {
    1: uniform_noise,
    2: gaussian_noise,
    3: sinusoidal_signal,
    4: sinusoidal_signal_onehalf_rectified,
    5: sinusoidal_signal_twohalf_rectified,
    6: square_wave_signal,
    7: square_wave_signal_symetrical,
    8: triangle_wave_signal,
    9: unit_step_signal,
    10: unit_impulse_signal,
    11: impulse_noise,
    12: S3_signal,
    13: exponential_signal
}
# wymiana numeru i nazwy funkcji miejscami - obsługa mapowania w obie strony - przy zapisie i odczycie sygnału
FUNC_TO_ID = {v: k for k, v in ID_TO_FUNC.items()}

def ensure_dir():
    """Tworzy folder, jeśli nie istnieje."""
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def get_path(filename):
    """Łączenie folderu z nazwą pliku."""
    return os.path.join(DIR, filename)

def save_to_binary(filename, signal):
    """Zapis sygnału do pliku binarnego"""
    ensure_dir()
    path = get_path(filename)
    function_id = FUNC_TO_ID.get(signal.function, 0)

    is_complex = 1.0 if np.iscomplexobj(signal.signal) else 0.0

    # 8 wartości double - każdy po 8 bajtów, 64 bajty nagłówka
    header = [
        float(signal.A) if signal.A is not None else -1.0,
        float(signal.d),
        float(signal.fs),
        float(signal.t1),
        float(signal.f) if signal.f is not None else -1.0,
        float(signal.kw) if signal.kw is not None else -1.0,
        float(signal.ts) if signal.ts is not None else -1.0,
        float(signal.p) if signal.p is not None else -1.0,
        float(function_id),
        float(is_complex)
    ]
    # działanie
    with open(path, 'wb') as f:
        # zapis nagłowka
        f.write(struct.pack('dddddddddd', *header))
        if is_complex:
           f.write(signal.signal.astype(np.complex128).tobytes())
        else:
           # zapis danych sygnału - konwersja do float64 i zapis jako bajty
           f.write(signal.signal.astype(np.float64).tobytes())


def load_from_binary(filename):
    """Wczytanie sygnału z pliku binarnego."""
    ensure_dir()
    path = get_path(filename)
    with open(path, 'rb') as f:
        # odczyt nagłówka - 80 bajtow
        header_data = f.read(80)
        # rozpakowanie nagłówka
        A, d, fs, t1, f_val, kw, ts, p, function_id, is_complex = struct.unpack('dddddddddd', header_data)

        data = f.read() # doczyt surowego ciągu bajtów danych sygnału
        if is_complex:
           signal_values = np.frombuffer(data, dtype=np.complex128)
        else:
           signal_values = np.frombuffer(data, dtype=np.float64) # konwersja bajtów na tablice, dzielenie na 8 bajtów, - odczyt jako float64

        # tworzenie tablicy czasu
        num_samples = len(signal_values)
        t = t1 + np.arange(num_samples) / fs

        # konwersja wartości None w sygnale
        A = A if A != -1.0 else None
        f_val = f_val if f_val != -1.0 else None
        kw = kw if kw != -1.0 else None
        ts = ts if ts != -1.0 else None
        p = p if p != -1.0 else None

        # mapowanie function_id na funkcję generującą sygnał
        function = ID_TO_FUNC.get(int(function_id))
        signal = Signal.Signal(A, d, fs, t1, function=function, f=f_val, kw=kw, ts=ts, p=p, t=t, signal=signal_values)

    return signal

def save_to_text(filename, signal):
    """Zapis sygnału do pliku tekstowego."""
    ensure_dir()
    path = get_path(filename)
    function_id = FUNC_TO_ID.get(signal.function, 0)
    is_complex = 1.0 if np.iscomplexobj(signal.signal) else 0.0

    header = [
        float(signal.A) if signal.A is not None else -1.0,
        float(signal.d),
        float(signal.fs),
        float(signal.t1),
        float(signal.f) if signal.f is not None else -1.0,
        float(signal.kw) if signal.kw is not None else -1.0,
        float(signal.ts) if signal.ts is not None else -1.0,
        float(signal.p) if signal.p is not None else -1.0,
        float(function_id),
        float(is_complex)
    ]
    with open(path, 'w') as f:
        f.write(' '.join(map(str, header)) + '\n')
        if is_complex:
           for t_val, s_val in zip(signal.t, signal.signal):
              f.write(f"{t_val} {s_val.real} {s_val.imag}\n")
        else:
           for t_val, s_val in zip(signal.t, signal.signal):
              f.write(f"{t_val} {s_val}\n")

def load_from_text(filename):
    """Wczytanie sygnału z pliku tekstowego."""
    ensure_dir()
    path = get_path(filename)
    with open(path, 'r') as f:
        header_line = f.readline().strip().split()
        A, d, fs, t1, f_val, kw, ts, p, function_id, is_complex = map(float, header_line[:10])

        signal_values = []
        t_values = []
        for line in f:
            parts = line.strip().split()
            if not parts:
               continue
            t_values.append(float(parts[0]))
            if is_complex:
               signal_values.append(complex(float(parts[1]), float(parts[2])))
            else:
               signal_values.append(float(parts[1]))

        A = A if A != -1.0 else None
        f_val = f_val if f_val != -1.0 else None
        kw = kw if kw != -1.0 else None
        ts = ts if ts != -1.0 else None
        p = p if p != -1.0 else None

        function = ID_TO_FUNC.get(int(function_id))
        signal = Signal.Signal(A, d, fs, t1, function=function, f=f_val, kw=kw, ts=ts, p=p, t=np.array(t_values), signal=np.array(signal_values))

    return signal

