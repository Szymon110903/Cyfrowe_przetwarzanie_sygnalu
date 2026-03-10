import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QFileDialog, QListWidget
from .canvas_window import MplCanvas
from logic.Signal import Signal
from logic.signals_generator import *
from utils.file_manager import save_to_binary, save_to_text, load_from_binary, load_from_text

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Signal Generator")
      # self.resize(600, 450)
      main_widget = QWidget()
      self.setCentralWidget(main_widget)
      self.layout = QHBoxLayout(main_widget)

      self.signals_history = []
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

      left_panel = QWidget()
      left_panel.setFixedWidth(360)
      left_panel_layout = QVBoxLayout(left_panel)
      left_panel_layout.setContentsMargins(0, 0, 0, 0)

      signal_settings = QGroupBox('Ustawienia sygnału')
      parameters_form_layout = QFormLayout()

      self.function_input = QComboBox()
      self.function_input.addItems(names)
      self.a_input = QLineEdit("1")
      self.d_input = QLineEdit("2")
      self.fs_input = QLineEdit("1000")
      self.t1_input = QLineEdit("0")
      self.T_input = QLineEdit("0.5")
      self.kw_input = QLineEdit("0.5")
      self.ts_input = QLineEdit("1.0")
      self.p_input = QLineEdit("0.1")
      self.bins = QLineEdit("10")

      parameters_form_layout.addRow(QLabel('Funkcja generująca'))
      parameters_form_layout.addRow(self.function_input)
      parameters_form_layout.addRow('Amplituda: ', self.a_input)
      parameters_form_layout.addRow('Czas trwania: ', self.d_input)
      parameters_form_layout.addRow('Częstotliwość próbkowania: ', self.fs_input)
      parameters_form_layout.addRow('Czas początkowy: ', self.t1_input)
      parameters_form_layout.addRow('Okres: ', self.T_input)
      parameters_form_layout.addRow('Wspołczynnik wypełnienia: ', self.kw_input)
      parameters_form_layout.addRow('Czas skoku jednostkowego: ', self.ts_input)
      parameters_form_layout.addRow('Prawdopodobieństwo: ', self.p_input)
      parameters_form_layout.addRow('Ilość przedziałów dla histogramu: ', self.bins)

      buttons_layout = QHBoxLayout()
      self.generate_btn = QPushButton("Generuj sygnał")
      self.generate_btn.clicked.connect(self.generate_plot)
      buttons_layout.addWidget(self.generate_btn)

      self.save_btn = QPushButton("Zapisz sygnał")
      self.save_btn.clicked.connect(self.save_signal)
      buttons_layout.addWidget(self.save_btn)

      parameters_form_layout.addRow(buttons_layout)

      self.load_btn = QPushButton("Wczytaj sygnał")
      self.load_btn.clicked.connect(self.load_signal)
      parameters_form_layout.addRow(self.load_btn)

      signal_settings.setLayout(parameters_form_layout)
      left_panel_layout.addWidget(signal_settings)

      left_panel_layout.addWidget(QLabel("Historia sygnałów:"))
      self.signals_list_widget = QListWidget()
      self.signals_list_widget.currentRowChanged.connect(self.on_signal_selected)
      left_panel_layout.addWidget(self.signals_list_widget)

      self.layout.addWidget(left_panel)

      right_side_box = QWidget()
      right_side_layout = QVBoxLayout()

      self.plot_title_label = QLabel()
      right_side_layout.addWidget(self.plot_title_label)
      self.canvas_signal = MplCanvas(self, width=6, height=4, dpi=100)
      right_side_layout.addWidget(self.canvas_signal)

      self.hist_title_label = QLabel()
      right_side_layout.addWidget(self.hist_title_label)
      self.canvas_histogram = MplCanvas(self, width=6, height=4, dpi=100)
      right_side_layout.addWidget(self.canvas_histogram)

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

   def update_plots(self, current_signal, index):
      if not self.signals_history:
         return

      signal_name = current_signal.get_signal_name()

      self.canvas_signal.axes.cla()

      discrete_signals = [unit_impulse_signal, impulse_noise]
      if current_signal.function in discrete_signals:
         self.canvas_signal.axes.stem(current_signal.t, current_signal.signal, basefmt=" ")
      else:
         self.canvas_signal.axes.plot(current_signal.t, current_signal.signal)

      self.canvas_signal.axes.set_title(signal_name)
      self.canvas_signal.axes.set_xlabel("Czas (s)")
      self.canvas_signal.axes.set_ylabel("Amplituda")
      self.canvas_signal.axes.grid(True)
      self.canvas_signal.draw()
      self.plot_title_label.setText(f"Wyświetlam: {signal_name}, Sygnał #{index + 1}")

      self.canvas_histogram.axes.cla()
      signal_values = current_signal.get_full_periods()
      bins = int(self.get_input_value(self.bins))

      self.canvas_histogram.axes.hist(signal_values, bins=bins, edgecolor="black")
      self.canvas_histogram.axes.set_title(f"Histogram - {signal_name}")
      self.canvas_histogram.axes.set_xlabel("Wartość Amplitudy")
      self.canvas_histogram.axes.set_ylabel("Liczba wystąpień")
      self.canvas_histogram.axes.grid(axis='y', linestyle='--', alpha=0.7)
      self.canvas_histogram.draw()

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
         bins = int(self.get_input_value(self.bins))

         func_idx = self.function_input.currentIndex()
         selected_function = self.functions_map[func_idx]

         if A is None or d is None or fs is None or t1 is None:
            raise ValueError("Parametry A, d, fs oraz t1 są wymagane!")

         signal = Signal(A=A, d=d, fs=fs, t1=t1, function=selected_function, T=T, kw=kw, ts=ts, p=p)
         self.signals_history.append(signal)

         signal_name = signal.get_signal_name()
         self.signals_list_widget.addItem(f"#{len(self.signals_history)} - {signal_name}")
         self.signals_list_widget.setCurrentRow(len(self.signals_history) - 1)

      except ValueError as e:
         QMessageBox.warning(self, "Błąd wejścia", str(e))
      except Exception as e:
         QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas generowania sygnału:\n{str(e)}")

## DO zastanowienia czy nie lepiej w przyszlosci nazwe pliku oprzecz o parametry sygnalu aby latwiej sie do niego potem dostac w folderze
   def save_signal(self):
      row = self.signals_list_widget.currentRow()
      if row < 0:
         QMessageBox.warning(self, "Brak sygnału", "Wybierz sygnał z historii do zapisania!")
         return

      try:
         selected_signal = self.signals_history[row]
         file_name = f"signal_{row+1}"
         save_to_binary(f"{file_name}.bin", selected_signal)
         save_to_text(f"{file_name}.txt", selected_signal)
         QMessageBox.information(self, "Sukces", "Sygnał został pomyślnie zapisany do plików (bin i txt).")
      except Exception as e:
         QMessageBox.critical(self, "Błąd zapisu", f"Wystąpił błąd podczas zapisywania sygnału:\n{str(e)}")

   def load_signal(self):
      file_path, _ = QFileDialog.getOpenFileName(
         self,
         "Wczytaj plik sygnału",
         "signals",
         "Sygnały (*.bin *.txt)"
      )

      if not file_path:
         return

      try:
         file_name = os.path.basename(file_path)

         if file_name.endswith('.bin'):
            loaded_signal = load_from_binary(file_name)
         elif file_name.endswith('.txt'):
            loaded_signal = load_from_text(file_name)
         else:
            QMessageBox.warning(self, "Błąd", "Wskazany format pliku nie jest obsługiwany.")
            return
         self.signals_history.append(loaded_signal)

         signal_name = loaded_signal.get_signal_name()
         self.signals_list_widget.addItem(f"#{len(self.signals_history)} - {signal_name}")
         self.signals_list_widget.setCurrentRow(len(self.signals_history) - 1)
         QMessageBox.information(self, "Sukces", f"Pomyślnie wczytano sygnał z pliku {file_name}.")

      except Exception as e:
         QMessageBox.critical(self, "Błąd wczytywania", f"Wystąpił błąd podczas odczytu pliku:\n{str(e)}")

   def on_signal_selected(self, row):
      if row < 0 or row >= len(self.signals_history):
         return

      selected_signal = self.signals_history[row]

      self.a_input.setText(str(selected_signal.A))
      self.d_input.setText(str(selected_signal.d))
      self.fs_input.setText(str(selected_signal.fs))
      self.t1_input.setText(str(selected_signal.t1))

      self.T_input.setText(str(selected_signal.T) if selected_signal.T is not None else "")
      self.kw_input.setText(str(selected_signal.kw) if selected_signal.kw is not None else "")
      self.ts_input.setText(str(selected_signal.ts) if selected_signal.ts is not None else "")
      self.p_input.setText(str(selected_signal.p) if selected_signal.p is not None else "")

      if selected_signal.function in self.functions_map:
         idx = self.functions_map.index(selected_signal.function)
         self.function_input.setCurrentIndex(idx)

      self.update_plots(selected_signal, row)
