import logic.Signal as Signal
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
        T=None,
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
        T=None,
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
        T=None,
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
        T=None,
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
        T=None,
        kw=None,
        ts=None,
        t=signal1.t,
        
        # TODO: Spytać o to jak zrobić dzielenie przez 0 - czy ustwaiać na 0 czy brać bliskie przybliżenie (co powoduje duże wartości)
        signal=np.where(signal2.signal != 0, signal1.signal / signal2.signal, 0)
    )
    return new_signal