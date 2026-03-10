from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QLineEdit, QComboBox
from .canvas_window import MplCanvas
from logic.Signal import Signal
from logic.signals_generator import *

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Signal Generator")
      # self.resize(600, 450)
      main_widget = QWidget()
      self.setCentralWidget(main_widget)
      self.layout = QHBoxLayout(main_widget)

      self.functions_map = [
            uniform_noise, gaussian_noise, sinusoidal_signal,
            sinusoidal_signal_onehalf_rectified, sinusoidal_signal_twohalf_rectified,
            square_wave_signal, square_wave_signal_symetrical, triangle_wave_signal,
            unit_step_signal, unit_impulse_signal, impulse_noise
        ]

      self.createWidgets()


   def createWidgets(self):
      names = ["Sygnał o rozkładzie jednostajnym", "Sygnał o rozkładzie normalnym", "Sygnał sinusoidalny", "Sygnał sinusoidalny z dodatnią częścią", "Sygnał sinusoidalny z dodatnią częścią prostowaną", "Sygnał prostokątny",
               "Sygnał prostokątny symetryczny", "Sygnał trójkątny", "Sygnał skok jednostkowy", "Impuls jednostkowy", "Szum impulsowy"]

      signal_settings = QGroupBox('Ustawienia sygnału')
      parameters_form_layout = QFormLayout()

      self.a_input = QLineEdit("1")
      self.d_input = QLineEdit("2")
      self.fs_input = QLineEdit("1")
      self.t1_input = QLineEdit("0")
      self.T_input = QLineEdit("0.5")
      self.kw_input = QLineEdit("0.5")
      self.ts_input = QLineEdit("1.0")
      self.p_input = QLineEdit("0.1")
      self.function_input = QComboBox()
      self.function_input.addItems(names)

      parameters_form_layout.addRow('Funkcja generująca: ', self.function_input)
      parameters_form_layout.addRow('Amplituda: ', self.a_input)
      parameters_form_layout.addRow('Czas trwania: ', self.d_input)
      parameters_form_layout.addRow('Częstotliwość próbkowania: ', self.fs_input)
      parameters_form_layout.addRow('Czas początkowy: ', self.t1_input)
      parameters_form_layout.addRow('Okres: ', self.T_input)
      parameters_form_layout.addRow('Wspołczynnik wypełnienia: ', self.kw_input)
      parameters_form_layout.addRow('Czas skoku jednostkowego: ', self.ts_input)
      parameters_form_layout.addRow('Prawdopodobieństwo: ', self.p_input)



      signal_settings.setLayout(parameters_form_layout)

      self.layout.addWidget(signal_settings)

      right_side_box = QWidget()
      right_side_layout = QVBoxLayout()

      right_side_layout.addWidget(QLabel("Tutaj będzie tytuł wykresu"))

      right_side_box.setLayout(right_side_layout)

      self.layout.addWidget(right_side_box)

   def create_plot(self):
      return ""
