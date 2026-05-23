import src.logic.Signal as Signal
import numpy as np

def check_compatibility(signal1, signal2):
    if signal1.fs != signal2.fs:
        raise ValueError("Sygnały mają różne częstotliwości próbkowania.")
    if signal1.t1 != signal2.t1:
        raise ValueError("Sygnały mają różne czasy początkowe.")
    if signal1.d != signal2.d:
        raise ValueError("Sygnały mają różne czasy trwania.")
    
def add_signals(signal1, signal2):
    check_compatibility(signal1, signal2)
    new_signal = Signal.Signal(
        A=None,
        d=signal1.d,
        fs=signal1.fs,
        t1=signal1.t1,
        function=None,
        f=None,
        kw=None,
        ts=None,
        t=signal1.t,  
        signal=signal1.signal + signal2.signal  
    )
    return new_signal

def subtraction_signals(signal1, signal2):
    check_compatibility(signal1, signal2)
    new_signal = Signal.Signal(
        A=None,
        d=signal1.d,
        fs=signal1.fs,
        t1=signal1.t1,
        function=None,
        f=None,
        kw=None,
        ts=None,
        t=signal1.t,  
        signal=signal1.signal - signal2.signal  
    )
    return new_signal

def multiplication_signals(signal1, signal2):
    check_compatibility(signal1, signal2)
    new_signal = Signal.Signal(
        A=None,
        d=signal1.d,
        fs=signal1.fs,
        t1=signal1.t1,
        function=None,
        f=None,
        kw=None,
        ts=None,
        t=signal1.t,  
        signal=signal1.signal * signal2.signal  
    )
    return new_signal

def division_signals_with_epsilon(signal1, signal2, epsilon=1e-10):
    check_compatibility(signal1, signal2)
    # zwraca true, keidy wartość sygnału jest większa niż epsilon
    safe_condition = np.abs(signal2.signal) > epsilon
    
    # dzielenie sygnałów z zabezpieczeniem przed dzieleniem przez zero - tam gdzie signal2 jest bliskie 0, wynik będzie ustawiony na 0
    divided_values = np.divide(
        signal1.signal, 
        signal2.signal, 
        out=np.zeros_like(signal1.signal), 
        where=safe_condition
    )
    new_signal = Signal.Signal(
        A=None,
        d=signal1.d,
        fs=signal1.fs,
        t1=signal1.t1,
        function=None,
        f=None,
        kw=None,
        ts=None,
        t=signal1.t,

        # TODO: Spytać o to jak zrobić dzielenie przez 0 - czy ustwaiać na 0 czy brać bliskie przybliżenie (co powoduje duże wartości)
        signal=divided_values
    )
    return new_signal

def division_signals(signal1, signal2):
    check_compatibility(signal1, signal2)
    new_signal = Signal.Signal(
        A=None,
        d=signal1.d,
        fs=signal1.fs,
        t1=signal1.t1,
        function=None,
        f=None,
        kw=None,
        ts=None,
        t=signal1.t,
        
        # TODO: Spytać o to jak zrobić dzielenie przez 0 - czy ustwaiać na 0 czy brać bliskie przybliżenie (co powoduje duże wartości)
        signal=np.where(signal2.signal != 0, signal1.signal / signal2.signal, 0)
    )
    return new_signal

def convolution(discrete1 , discrete2):
   h = discrete1.signal
   x = discrete2.signal
   M = len(h)
   N = len(x)
   new_length = M + N - 1
   result_signal = np.zeros(new_length)

   for n in range(new_length):
      for k in range(M):
         if 0 <= n-k < N:
            result_signal[n] += h[k] * x[n-k]

   fs = discrete1.fs
   t1_new = discrete1.t1 + discrete2.t1
   t_new = t1_new + np.arange(new_length) / fs

   new_signal = Signal.Signal(
      A=None,
      d=new_length / fs,
      fs=fs,
      t1=t1_new,
      t=t_new,
      signal=result_signal
   )
   new_signal.name_override = f"Splot ({getattr(discrete1, 'name_override', 'h')} * {getattr(discrete2, 'name_override', 'x')})"

   return new_signal

def correlate_signals_direct(signal_h, signal_x):
   h = signal_h.signal
   x = signal_x.signal

   M = len(h)
   N = len(x)
   output_length = M + N - 1
   result_signal = np.zeros(output_length)
   for i in range(output_length):
      shift = i - (N - 1)
      for k in range(M):
         if 0 <= k-shift < N:
            result_signal[i] += h[k] * x[k-shift]
   fs = signal_h.fs
   t_new = np.arange(output_length) / fs
   new_signal = Signal.Signal(A=None, d=output_length / fs, fs=fs, t1=0, t=t_new, signal=result_signal)
   new_signal.name_override = f"Korelacja bezpośrednia ({getattr(signal_h, 'name_override', 'h')}, {getattr(signal_x, 'name_override', 'x')})"
   return new_signal

def correlate_signals_convolution(signal_h, signal_x):
   x_reversed = signal_x.signal[::-1]
   sig_x_reversed = Signal.Signal(A=signal_x.A, d=signal_x.d, fs=signal_x.fs, t1=signal_x.t1, t=signal_x.t, signal=x_reversed)

   result_signal = convolution(signal_h, sig_x_reversed)
   result_signal.t = np.arange(len(result_signal.signal)) / result_signal.fs
   result_signal.name_override = f"Korelacja splotem ({getattr(signal_h, 'name_override', 'h')}, {getattr(signal_x, 'name_override', 'x')})"
   return result_signal