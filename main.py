import sys
from PySide6.QtWidgets import QApplication

from logic.signals_generator import *
from utils.plots import *
import logic.Signal as Signal
from ui.main_window import MainWindow
import logic.operations as operations

def main():
    # signal2 = Signal.Signal(A=5, d=10, fs=100, t1=0, function=sinusoidal_signal, T=1)
    # signal2.visualize()
    # signal2.print_parameters()
    # # signal2.visualize_histogram()
    # signal2.print_parameters()
    # # save_to_text("signal2.txt", signal2)
    # # loaded_signal2_text = load_from_text("signal2.txt")
    # # loaded_signal2_text.visualize()
    # # loaded_signal2_text.print_variables()

    # signal3 = Signal.Signal(A=1, d=10, fs=100, t1=0, function=square_wave_signal, T=1, kw=0.5)
    # signal3.visualize()
    # signal3.print_parameters()

    # signal_div = operations.subtraction_signals(signal2, signal3)
    # signal_div.visualize()
    # signal_div.print_parameters()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":    main()
