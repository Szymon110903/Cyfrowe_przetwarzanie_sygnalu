import numpy as np
from src.logic.Signal import Signal
from src.logic.operations import convolution

def generate_low_pass_filter(M, K, fs):
   if M % 2 == 0:
      raise ValueError('M must be an odd integer')

   h = np.zeros(M)
   center = (M - 1) // 2

   for n in range(M):
      if n == center:
         h[n] = 2.0 / K
      else:
         numerator = np.sin(2 * np.pi * (n - center) / K)
         denominator = np.pi * (n - center)
         h[n] = numerator / denominator

   t = np.arange(M) / fs
   sig = Signal(A=1, d=M/fs, fs=fs, t1=0, t=t, signal=h)
   sig.name_override = f"Filtr DP (M={M}, K={K})"

   return sig

def apply_blackman_window(filter_signal):
   M = len(filter_signal.signal)
   n = np.arange(M)

   window = 0.42 - 0.5 * np.cos(2 * np.pi * n / M) + 0.08 * np.cos(4 * np.pi * n / M)
   windowed_h = filter_signal.signal * window

   sig = Signal(A=1, d=filter_signal.d, fs=filter_signal.fs, t1=filter_signal.t1, t=filter_signal.t, signal=windowed_h)
   sig.name_override = filter_signal.name_override + "[Blackman]"
   return sig

def transform_to_band_pass(filter_signal):
   M = len(filter_signal.signal)
   n = np.arange(M)

   s = 2 * np.sin(np.pi * n / 2)
   bp_h = filter_signal.signal * s

   sig = Signal(A=1, d=filter_signal.d, fs=filter_signal.fs, t1=filter_signal.t1, t=filter_signal.t, signal=bp_h)
   sig.name_override = filter_signal.name_override.replace("DP", "ŚP")
   return sig

def filter_signal_with_fir(input_signal, filter_impulse_response):
   filtered_signal = convolution(filter_impulse_response, input_signal)
   filtered_signal.name_override = f"Sygnał przefiltrowany: {getattr(input_signal, 'name_override', 'x')}"
   return filtered_signal