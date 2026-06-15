import unittest
import sys
import six
# rozwiązuje problem z bibliteka six
if not hasattr(six._SixMetaPathImporter, '_path'):
    six._SixMetaPathImporter._path = []

import numpy as np
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.logic.Signal import Signal
from src.logic.signals_generator import sinusoidal_signal

class TestGUIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize QApplication once
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    def test_transformations_list_sync_and_plots(self):
        window = MainWindow()
        
        # Początkowo historia jest pusta
        self.assertEqual(len(window.signals_history), 0)
        
        # Tworzenie sygnału testowego (1024 próbek - potęga 2 dla FFT)
        signal = Signal(A=1, d=2, fs=512, t1=0, function=sinusoidal_signal, f=2.0)
        window.signals_history.append(signal)
        window.add_signal_to_lists(window.get_sig_name(signal))
        
        # Powinniśmy mieć 1 sygnał w historii i na listach
        self.assertEqual(len(window.signals_history), 1)
        self.assertEqual(window.signals_list_widget.count(), 1)
        self.assertEqual(window.transform_signals_list.count(), 1)
        
        # Wybór pierwszego rzędu w liście transformacji
        window.transform_signals_list.setCurrentRow(0)
        self.assertEqual(window.signals_list_widget.currentRow(), 0)
        self.assertEqual(window.conversion_signals_list.currentRow(), 0)
        self.assertEqual(window.transform_signals_list.currentRow(), 0)
        
        # Wykonanie transformacji FFT (indeks 1 w transform_type_combo)
        window.transform_type_combo.setCurrentIndex(1)
        window.perform_transformation()
        
        # Powinien pojawić się nowy sygnał FFT w historii
        self.assertEqual(len(window.signals_history), 2)
        self.assertEqual(window.transform_signals_list.count(), 2)
        
        # Weryfikacja nowo wygenerowanego sygnału FFT
        fft_signal = window.signals_history[1]
        self.assertTrue(fft_signal.name_override.startswith("FFT"))
        self.assertTrue(hasattr(fft_signal, 'transform_plots_info'))
        self.assertEqual(fft_signal.transform_plots_info['type'], 'fourier')
        
        # Wybór oryginalnego sygnału
        window.transform_signals_list.setCurrentRow(0)
        
        # Wybór sygnału FFT
        window.transform_signals_list.setCurrentRow(1)

if __name__ == '__main__':
    unittest.main()
