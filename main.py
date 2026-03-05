from signals_generator import *
from plots import *
import Signal 
from file_manager import save_to_binary, load_from_binary
# TODO: spytać o działania na sygnałach różniących sie czasem trwania, częstotliwością próbkowania, czasem początkowym

def main():
#   signal = signal_class.Signal(A=1, d=1, fs=1000, t1=0, function=sinusoidal_signal, T=0.2)
#   signal.visualize()
#     signal2 = signal_class.Signal(A=1, d=1, fs=1000, t1=0, function=sinusoidal_signal, T=0.3, kw=0.5)
#     signal2.visualize()

    # signal2 = Signal.Signal(A=5, d=20, fs=1, ts=1.0, t1=-10, function=unit_impulse_signal)
    # signal2.visualize()

    signal_test = Signal.Signal(A=1, d=1, fs=1000, t1=0, function=sinusoidal_signal, T=0.2)
    signal_test.visualize()
    save_to_binary("test_signal.bin", signal_test)
    loaded_signal = load_from_binary("test_signal.bin")
    loaded_signal.visualize()


if __name__ == "__main__":    main()