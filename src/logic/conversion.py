import numpy as np

# def sampling(t: np.ndarray, signal: np.ndarray, fs_new: float) -> tuple[np.ndarray, np.ndarray]:
#     Ts = 1 / fs_new
#     t_sampled = np.arange(t[0], stop=t[-1], step=Ts)
#     signal_sampled = np.interp(t_sampled, t, signal)
#     return t_sampled, signal_sampled

def quantization_with_clipping(signal_sampled: np.ndarray, bit_depth: int = 8) -> np.ndarray:
    levels = 2 ** bit_depth
    min_val = np.min(signal_sampled)
    max_val = np.max(signal_sampled)
    if max_val == min_val:
        return signal_sampled
    step = (np.subtract(max_val, min_val)) / (levels - 1)
    quantized_signal = np.floor((signal_sampled - min_val) / step) * step + min_val
    return quantized_signal

def get_reconstruction_time(t_sampled: np.ndarray, f_rec: float) -> np.ndarray:
   T_rec = 1 / f_rec
   return np.arange(t_sampled[0], t_sampled[-1], T_rec)

def first_order_hold_reconstruction(signal_sampled: np.ndarray, t_sampled: np.ndarray, f_rec: float) -> tuple[np.ndarray, np.ndarray]:
    t_rec = get_reconstruction_time(t_sampled, f_rec)
    reconstructed = np.zeros(len(t_rec))

    for i, t in enumerate(t_rec):
        if t <= t_sampled[0]:
            reconstructed[i] = signal_sampled[0]
        elif t >= t_sampled[-1]:
            reconstructed[i] = signal_sampled[-1]
        else:
            idx = np.searchsorted(t_sampled, t)
            t0,t1 = t_sampled[idx - 1], t_sampled[idx]
            y0,y1 = signal_sampled[idx - 1], signal_sampled[idx]

            reconstructed[i] = y0 + (y1 - y0) * (t - t0) / (t1 - t0)
    return t_rec, reconstructed

def sinc_reconstruction(signal_sampled: np.ndarray, t_sampled: np.ndarray, f_rec: float, num_neighbours: int = None) -> tuple[np.ndarray, np.ndarray]:
    if len(t_sampled) < 2:
        return t_sampled, signal_sampled

    t_rec = get_reconstruction_time(t_sampled, f_rec)
    Ts = t_sampled[1] - t_sampled[0]
    reconstructed = np.zeros_like(t_rec)
    if num_neighbours is None:
        for n, x_n in enumerate(signal_sampled):
            t = (t_rec - t_sampled[n]) / Ts
            sinc_values = np.where(t == 0, 1.0, np.sin(np.pi * t) / (np.pi * t))
            reconstructed += x_n * sinc_values
    else :
        for i, t in enumerate(t_rec):
            idx = np.searchsorted(t_sampled, t)
            start_idx = max(0, int(idx - num_neighbours))
            end_idx = min(len(t_sampled), int(idx + num_neighbours))

            t_window = t_sampled[start_idx:end_idx]
            sig_window = signal_sampled[start_idx:end_idx]

            t_arg = (t - t_window) / Ts
            sinc_values = np.where(t_arg == 0, 1.0, np.sin(np.pi * t_arg) / (np.pi * t_arg))
            reconstructed[i] = np.sum(sig_window * sinc_values)

    return t_rec, reconstructed