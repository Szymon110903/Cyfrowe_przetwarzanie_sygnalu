from signals_generator import *
from plots import *
import Signal
from file_manager import save_to_binary, load_from_binary
# TODO: spytać o działania na sygnałach różniących sie czasem trwania, częstotliwością próbkowania, czasem początkowym

def main():
  # signal = Signal.Signal(A=10, d=10, fs=1000, t1=0, function=sinusoidal_signal, T=6)
  # signal.visualize()
  # signal.visualize_histogram()
  # signal.print_parameters()

    signal2 = Signal.Signal(A=5, d=50, fs=1, p=0.2, t1=0, function=impulse_noise)
    signal2.visualize()
    signal2.visualize_histogram()
    signal2.print_parameters()

    # signal_test = Signal.Signal(A=1, d=1, fs=1000, t1=0, function=sinusoidal_signal, T=0.2)
    # signal_test.visualize()
    # save_to_binary("test_signal.bin", signal_test)
    # loaded_signal = load_from_binary("test_signal.bin")
    # loaded_signal.visualize()


if __name__ == "__main__":    main()