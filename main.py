import sys
from PySide6.QtWidgets import QApplication

from logic.signals_generator import *
from utils.plots import *
import logic.Signal as Signal
from utils.file_manager import save_to_binary, load_from_binary, save_to_text, load_from_text
from ui.main_window import MainWindow
# TODO: spytać o działania na sygnałach różniących sie czasem trwania, częstotliwością próbkowania, czasem początkowym


def main():
   #  signal2 = Signal.Signal(A=5, d=10, fs=1000, t1=0, function=uniform_noise)
   #  signal2.visualize()
   #  signal2.visualize_histogram()
   #  signal2.print_parameters()
   #  save_to_text("signal2.txt", signal2)
   #  loaded_signal2_text = load_from_text("signal2.txt")
   #  loaded_signal2_text.visualize()
   #  loaded_signal2_text.print_variables()

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()

if __name__ == "__main__":    main()
