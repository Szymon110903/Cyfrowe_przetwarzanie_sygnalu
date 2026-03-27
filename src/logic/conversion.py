import numpy as np

# Spytać o tą funkcję, ponieważ w tresci Z.2 jest aby utworzyc próbkowanie rownomierne
# ale niby przy generowaniu to robimy. Więc dopytać czy tamto traktujemy jako ciągły sygnał
# i tutaj próbkujemy jeszcze raz, jako faktycznie próbkowanie.
def sampling(t: np.ndarray, signal: np.ndarray, fs_new: float) -> tuple[np.ndarray, np.ndarray]:
    Ts = 1 / fs_new
    t_sampled = np.arange(t[0], stop=t[-1], step=Ts)
    signal_sampled = np.interp(t_sampled, t, signal)
    return t_sampled, signal_sampled

def quantization_with_clipping(signal_sampled: np.ndarray, bit_depth: int = 8) -> np.ndarray:
    levels = 2 ** bit_depth
    min_val = np.min(signal_sampled)
    max_val = np.max(signal_sampled)
    if max_val == min_val:
        return signal_sampled
    step = (np.subtract(max_val, min_val)) / (levels - 1)
    quantized_signal = np.floor((signal_sampled - min_val) / step) * step + min_val
    return quantized_signal
