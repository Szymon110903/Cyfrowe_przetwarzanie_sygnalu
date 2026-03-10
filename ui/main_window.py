from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
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

      self.generate_btn = QPushButton("Generuj sygnał")
      self.generate_btn.clicked.connect(self.generate_plot)
      parameters_form_layout.addRow(self.generate_btn)

      signal_settings.setLayout(parameters_form_layout)
      signal_settings.setFixedWidth(350)
      self.layout.addWidget(signal_settings)

      right_side_box = QWidget()
      right_side_layout = QVBoxLayout()

      self.plot_title_label = QLabel("Tutaj będzie tytuł wykresu")
      right_side_layout.addWidget(self.plot_title_label)

      self.sc = MplCanvas(self, width=5, height=4, dpi=100)
      right_side_layout.addWidget(self.sc)

      right_side_box.setLayout(right_side_layout)
      self.layout.addWidget(right_side_box)

   def get_input_value(self, line_edit):
      text=line_edit.text().strip()
      if not text:
         return None
      try:
         return float(text)
      except ValueError:
         raise ValueError(f"Nieprawidłowa wartość w jednym z pól: '{text}'")

   def generate_plot(self):
      try:
         A = self.get_input_value(self.a_input)
         d = self.get_input_value(self.d_input)
         fs = self.get_input_value(self.fs_input)
         t1 = self.get_input_value(self.t1_input)
         T = self.get_input_value(self.T_input)
         kw = self.get_input_value(self.kw_input)
         ts = self.get_input_value(self.ts_input)
         p = self.get_input_value(self.p_input)

         func_idx = self.function_input.currentIndex()
         selected_function = self.functions_map[func_idx]
         signal_name = self.function_input.currentText()

         if A is None or d is None or fs is None or t1 is None:
            raise ValueError("Parametry A, d, fs oraz t1 są wymagane!")

         signal = Signal(A=A, d=d, fs=fs, t1=t1, function=selected_function, T=T, kw=kw, ts=ts, p=p)

         self.sc.axes.cla()

         discrete_signals = [unit_impulse_signal, impulse_noise]
         if selected_function in discrete_signals:
            self.sc.axes.stem(signal.t, signal.signal, basefmt=" ")
         else:
            self.sc.axes.plot(signal.t, signal.signal)

         self.sc.axes.set_title(signal_name)
         self.sc.axes.set_xlabel("Czas (s)")
         self.sc.axes.set_ylabel("Amplituda")
         self.sc.axes.grid(True)
         self.sc.draw()
         self.plot_title_label.setText(f"Wyświetlam: {signal_name}")

      except ValueError as e:
         QMessageBox.warning(self, "Błąd wejścia", str(e))
      except Exception as e:
         QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas generowania sygnału:\n{str(e)}")
