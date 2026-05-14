import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QLineEdit, \
   QComboBox, QPushButton, QMessageBox, QFileDialog, QListWidget, QGridLayout, QMenu, QTabWidget
from PySide6.QtCore import Qt
from .canvas_window import MplCanvas
from src.logic.Signal import Signal
from src.logic.signals_generator import *
from src.utils.file_manager import save_to_binary, save_to_text, load_from_binary, load_from_text
from src.logic.radar import RadarSimulator
import src.logic.operations as operations
import src.logic.conversion as conversion
import src.logic.metrics as metrics
from PySide6.QtWidgets import QTextEdit 

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Signal Generator")
      self.tabs = QTabWidget()
      self.setCentralWidget(self.tabs)

      self.signal1 = None
      self.signal2 = None
      self.combined_signal = None

      self.signals_history = []
      self.functions_map = [
            uniform_noise, gaussian_noise, sinusoidal_signal,
            sinusoidal_signal_onehalf_rectified, sinusoidal_signal_twohalf_rectified,
            square_wave_signal, square_wave_signal_symetrical, triangle_wave_signal,
            unit_step_signal, unit_impulse_signal, impulse_noise
        ]
      self.create_tabs()

   def create_tabs(self):
      self.tab_operations = QWidget()
      self.setup_operations_tab()
      self.tabs.addTab(self.tab_operations, "Generowanie i Operacje")

      self.tab_conversion = QWidget()
      self.setup_conversion_tab()
      self.tabs.addTab(self.tab_conversion, "Próbkowanie i Kwantyzacja")

      self.tab_radar = QWidget()
      self.setup_radar_tab()
      self.tabs.addTab(self.tab_radar, "Radar / Korelacja")

      self.signals_list_widget.currentRowChanged.connect(self.sync_lists)
      self.conversion_signals_list.currentRowChanged.connect(self.sync_lists)

   def sync_lists(self, row):
      if self.signals_list_widget.currentRow() != row:
         self.signals_list_widget.setCurrentRow(row)
      if self.conversion_signals_list.currentRow() != row:
         self.conversion_signals_list.setCurrentRow(row)

   def add_signal_to_lists(self, signal_name):
      display_text = f"#{len(self.signals_history)} - {signal_name}"
      self.signals_list_widget.addItem(display_text)
      self.conversion_signals_list.addItem(display_text)
      self.signals_list_widget.setCurrentRow(len(self.signals_history) - 1)

   def setup_operations_tab(self):
      names = ["Sygnał o rozkładzie jednostajnym", "Sygnał o rozkładzie normalnym", "Sygnał sinusoidalny", "Sygnał sinusoidalny z dodatnią częścią", "Sygnał sinusoidalny z dodatnią częścią prostowaną", "Sygnał prostokątny",
               "Sygnał prostokątny symetryczny", "Sygnał trójkątny", "Sygnał skok jednostkowy", "Impuls jednostkowy", "Szum impulsowy"]

      tab1_layout = QHBoxLayout(self.tab_operations)
      # Lewy panel dla ustawień parametrów sygnałow, historii sygnałów oraz operacji i ich wyników
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
      self.f_input = QLineEdit("2.0")
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
      parameters_form_layout.addRow('Częstotliwość sygnału: ', self.f_input)
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
      self.signals_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
      self.signals_list_widget.customContextMenuRequested.connect(self.show_context_menu)
      left_panel_layout.addWidget(self.signals_list_widget)

      assign_layout = QHBoxLayout()
      self.btn_set_sig1 = QPushButton("Wyświetl jako Sygnał 1")
      self.btn_set_sig1.clicked.connect(self.set_signal1)
      assign_layout.addWidget(self.btn_set_sig1)
      self.btn_set_sig2 = QPushButton("Wyświetl jako Sygnał 2")
      self.btn_set_sig2.clicked.connect(self.set_signal2)
      assign_layout.addWidget(self.btn_set_sig2)

      left_panel_layout.addLayout(assign_layout)
      operations_box = QGroupBox("Operacje na sygnałach")
      operations_layout = QHBoxLayout()
      self.add_signals_btn = QPushButton("Dodaj")
      self.add_signals_btn.clicked.connect(self.add_selected_signals)
      self.subtract_signals_btn = QPushButton("Odejmij")
      self.subtract_signals_btn.clicked.connect(self.subtract_selected_signals)
      self.multiply_signals_btn = QPushButton("Pomnóż")
      self.multiply_signals_btn.clicked.connect(self.multiply_selected_signals)
      self.divide_signals_btn = QPushButton("Podziel")
      self.divide_signals_btn.clicked.connect(self.divide_selected_signals)
      operations_layout.addWidget(self.add_signals_btn)
      operations_layout.addWidget(self.subtract_signals_btn)
      operations_layout.addWidget(self.multiply_signals_btn)
      operations_layout.addWidget(self.divide_signals_btn)
      operations_box.setLayout(operations_layout)
      left_panel_layout.addWidget(operations_box)

      # --- Panel parametrów ---
      left_panel_layout.addWidget(QLabel("Parametry wybranego sygnału:"))
      self.params_display = QTextEdit()
      self.params_display.setReadOnly(True) 
      self.params_display.setFixedHeight(150)
      self.params_display.setPlaceholderText("Wygeneruj sygnał, aby zobaczyć parametry...")
      left_panel_layout.addWidget(self.params_display)

      right_side_box = QWidget()
      right_side_layout = QGridLayout()

      self.canvas_sig1 = MplCanvas(self, width=5, height=4, dpi=100)
      self.canvas_hist1 = MplCanvas(self, width=5, height=4, dpi=100)

      right_side_layout.addWidget(self.canvas_sig1, 0, 0)
      right_side_layout.addWidget(self.canvas_hist1, 0, 1)

      self.canvas_sig2 = MplCanvas(self, width=5, height=4, dpi=100)
      self.canvas_hist2 = MplCanvas(self, width=5, height=4, dpi=100)

      right_side_layout.addWidget(self.canvas_sig2, 1, 0)
      right_side_layout.addWidget(self.canvas_hist2, 1, 1)

      self.canvas_sig3 = MplCanvas(self, width=5, height=4, dpi=100)
      self.canvas_hist3 = MplCanvas(self, width=5, height=4, dpi=100)

      right_side_layout.addWidget(self.canvas_sig3, 2, 0)
      right_side_layout.addWidget(self.canvas_hist3, 2, 1)

      right_side_box.setLayout(right_side_layout)

      tab1_layout.addWidget(left_panel)
      tab1_layout.addWidget(right_side_box)

   def setup_conversion_tab(self):
      layout = QHBoxLayout(self.tab_conversion)

      left_panel = QWidget()
      left_panel.setFixedWidth(360)
      left_layout = QVBoxLayout(left_panel)

      left_layout.addWidget(QLabel("Wybierz sygnał do konwersji:"))
      self.conversion_signals_list = QListWidget()
      self.conversion_signals_list.setFixedHeight(150)
      left_layout.addWidget(self.conversion_signals_list)

      settings_box = QGroupBox("Parametry Konwersji (A/C i C/A)")
      form = QFormLayout()

      self.conv_fs_input = QLineEdit("50")
      self.conv_bits_input = QLineEdit("8")
      self.conv_recon_method = QComboBox()
      self.conv_recon_method.addItems(["FOH - Pierwszego rzędu", "Sinc"])
      self.conv_sinc_n_input = QLineEdit("10")

      form.addRow("Częstotliwość próbkowania fs:", self.conv_fs_input)
      form.addRow("Liczba bitów kwantyzacji:", self.conv_bits_input)
      form.addRow("Metoda rekonstrukcji:", self.conv_recon_method)
      form.addRow("Liczba sąsiadów:", self.conv_sinc_n_input)

      self.convert_btn = QPushButton("Wykonaj konwersję")
      self.convert_btn.clicked.connect(self.perform_conversion)
      form.addRow(self.convert_btn)

      settings_box.setLayout(form)
      left_layout.addWidget(settings_box)

      left_layout.addWidget(QLabel("Błędy konwersji (Miary podobieństwa):"))
      self.metrics_display = QTextEdit()
      self.metrics_display.setReadOnly(True)
      left_layout.addWidget(self.metrics_display)
      layout.addWidget(left_panel)

      right_panel = QWidget()
      right_layout = QVBoxLayout(right_panel)

      self.canvas_ac = MplCanvas(self, width=5, height=4, dpi=100)
      right_layout.addWidget(self.canvas_ac)

      self.canvas_ca = MplCanvas(self, width=5, height=4, dpi=100)
      right_layout.addWidget(self.canvas_ca)

      layout.addWidget(right_panel)

   def setup_radar_tab(self):
      layout = QHBoxLayout(self.tab_radar)
      left_panel = QWidget()
      left_panel.setFixedWidth(360)
      left_layout = QVBoxLayout(left_panel)

      settings_box = QGroupBox("Parametry Radaru")
      form = QFormLayout()

      self.radar_v_input = QLineEdit("300")
      self.radar_target_v_input = QLineEdit("-15")
      self.radar_init_dist_input = QLineEdit("50")
      self.radar_fs_input = QLineEdit("1000")
      self.radar_buffer_input = QLineEdit("1000")
      self.radar_report_input = QLineEdit("1.0")

      form.addRow("Prędkość fali V [m/s]:", self.radar_v_input)
      form.addRow("Prędkość obiektu [m/s]:", self.radar_target_v_input)
      form.addRow("Początkowa odległość [m]:", self.radar_init_dist_input)
      form.addRow("Częstotliwość próbkowania fs:", self.radar_fs_input)
      form.addRow("Długość bufora (próbki):", self.radar_buffer_input)
      form.addRow("Okres raportowania [s]:", self.radar_report_input)

      self.radar_step_btn = QPushButton("Wykonaj krok symulacji")
      self.radar_step_btn.clicked.connect(lambda a: a)
      self.radar_reset_btn = QPushButton("Resetuj symulator")
      self.radar_reset_btn.clicked.connect(lambda a: a)

      form.addRow(self.radar_step_btn)
      form.addRow(self.radar_reset_btn)

      settings_box.setLayout(form)
      left_layout.addWidget(settings_box)

      left_layout.addWidget(QLabel("Wyniki pomiarów"))
      self.radar_log_display = QTextEdit()
      self.radar_log_display.setReadOnly(True)
      left_layout.addWidget(self.radar_log_display)

      layout.addWidget(left_panel)

      # Wykresy
      right_panel = QWidget()
      right_layout = QVBoxLayout(right_panel)

      self.canvas_radar_sent = MplCanvas(self, width=5, height=2, dpi=100)
      self.canvas_radar_recv = MplCanvas(self, width=5, height=2, dpi=100)
      self.canvas_radar_corr = MplCanvas(self, width=5, height=3, dpi=100)

      right_layout.addWidget(self.canvas_radar_sent)
      right_layout.addWidget(self.canvas_radar_recv)
      right_layout.addWidget(self.canvas_radar_corr)

      layout.addWidget(right_panel)
      self.radar_simulator = None

   def perform_conversion(self):
      row = self.signals_list_widget.currentRow()
      if row < 0:
         QMessageBox.warning(self, "Błąd", "Najpierw wygeneruj i wybierz sygnał")
         return

      original_singal = self.signals_history[row]
      t_c = original_singal.t
      sig_c = original_singal.signal

      try:
         fs_new = float(self.conv_fs_input.text().strip())
         bits = int(self.conv_bits_input.text().strip())
      except ValueError:
         QMessageBox.warning(self, "Błąd", "Podaj poprawne wartości dla fs oraz bitów")
         return

      t_s, sig_s = conversion.sampling(t_c, sig_c, fs_new)
      sig_q = conversion.quantization_with_clipping(sig_s, bits)

      r_method = self.conv_recon_method.currentIndex()
      if r_method == 0:
         sig_r = conversion.first_order_hold_reconstruction(sig_q, t_s, t_c)
      else:
         try:
            n_val = int(self.conv_sinc_n_input.text().strip())
            neighbours = n_val if n_val else None
         except ValueError:
            neighbours = None
         sig_r = conversion.sinc_reconstruction(sig_q, t_s, t_c, neighbours)

      self.canvas_ac.axes.cla()
      self.canvas_ac.axes.plot(t_c, sig_c, label="Oryginalny", color="blue")
      self.canvas_ac.axes.stem(t_s, sig_q, linefmt="r-", markerfmt="ro", basefmt=" ", label="Skwantowane próbki")
      self.canvas_ac.axes.set_title("Konwersja A/C")
      self.canvas_ac.axes.legend(loc="upper right")
      self.canvas_ac.axes.grid(True)
      self.canvas_ac.draw()

      self.canvas_ca.axes.cla()
      self.canvas_ca.axes.plot(t_c, sig_c, label="Oryginalny", color="blue")
      self.canvas_ca.axes.plot(t_c, sig_r,  label="Zrekonstruowany", color="green")
      self.canvas_ca.axes.set_title("Konwersja C/A")
      self.canvas_ca.axes.legend(loc="upper right")
      self.canvas_ca.axes.grid(True)
      self.canvas_ca.draw()

      text = "Błedy próbkowania i rekonstrukcji\n"
      text += f"MSE:  {metrics.calculate_MSE(sig_c, sig_r):.4f}\n"
      text += f"SNR:  {metrics.calculate_SNR(sig_c, sig_r):.4f} dB\n"
      text += f"PSNR: {metrics.calculate_PSNR(sig_c, sig_r):.4f} dB\n"
      text += f"MD:   {metrics.calculate_MD(sig_c, sig_r):.4f}\n"
      text += f"ENOB: {metrics.calculate_ENOB(sig_c, sig_r):.4f} bitów\n\n"

      text += "Błędy kwantyzacji\n"
      text += f"MSE:  {metrics.calculate_MSE(sig_s, sig_q):.4f}\n"
      text += f"SNR:  {metrics.calculate_SNR(sig_s, sig_q):.4f} dB\n"
      text += f"PSNR: {metrics.calculate_PSNR(sig_s, sig_q):.4f} dB\n"
      text += f"MD:   {metrics.calculate_MD(sig_s, sig_q):.4f}\n"
      text += f"ENOB: {metrics.calculate_ENOB(sig_s, sig_q):.4f} bitów\n"

      self.metrics_display.setText(text)

   def get_input_value(self, line_edit):
      text=line_edit.text().strip()
      if not text:
         return None
      try:
         return float(text)
      except ValueError:
         raise ValueError(f"Nieprawidłowa wartość w jednym z pól: '{text}'")

   def get_sig_name(self, signal):
      if hasattr(signal, 'name_override'):
         return signal.name_override
      name = signal.get_signal_name()
      return name if name else "Sygnał wynikowy"

   def generate_plot(self):
      try:
         A = self.get_input_value(self.a_input)
         d = self.get_input_value(self.d_input)
         fs = self.get_input_value(self.fs_input)
         t1 = self.get_input_value(self.t1_input)
         f = self.get_input_value(self.f_input)
         kw = self.get_input_value(self.kw_input)
         ts = self.get_input_value(self.ts_input)
         p = self.get_input_value(self.p_input)
         # bins = int(self.get_input_value(self.bins))

         func_idx = self.function_input.currentIndex()
         selected_function = self.functions_map[func_idx]

         if A is None or d is None or fs is None or t1 is None:
            raise ValueError("Parametry A, d, fs oraz t1 są wymagane!")

         signal = Signal(A=A, d=d, fs=fs, t1=t1, function=selected_function, f=f, kw=kw, ts=ts, p=p)
         self.signals_history.append(signal)

         signal_name = self.get_sig_name(signal)
         self.add_signal_to_lists(signal_name)

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

         signal_name = self.get_sig_name(loaded_signal)
         self.add_signal_to_lists(signal_name)
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

      self.f_input.setText(str(selected_signal.f) if selected_signal.f is not None else "")
      self.kw_input.setText(str(selected_signal.kw) if selected_signal.kw is not None else "")
      self.ts_input.setText(str(selected_signal.ts) if selected_signal.ts is not None else "")
      self.p_input.setText(str(selected_signal.p) if selected_signal.p is not None else "")

      if selected_signal.function in self.functions_map:
         idx = self.functions_map.index(selected_signal.function)
         self.function_input.setCurrentIndex(idx)
      if row == 0:
         self.set_signal1()
      else:
         self.set_signal2()

   def set_signal1(self):
      row = self.signals_list_widget.currentRow()
      if row < 0: return
      self.signal1 = self.signals_history[row]
      self.update_single_plot(self.signal1, self.canvas_sig1, self.canvas_hist1, row)

   def set_signal2(self):
      row = self.signals_list_widget.currentRow()
      if row < 0: return
      self.signal2 = self.signals_history[row]
      self.update_single_plot(self.signal2, self.canvas_sig2, self.canvas_hist2, row)

   def update_single_plot(self, signal, canvas_sig, canvas_hist, list_index):
    if not signal:
        return
    signal_name = self.get_sig_name(signal)
    canvas_sig.axes.cla()
    
    discrete_signals = [unit_impulse_signal, impulse_noise]

    if signal.function in discrete_signals:
        canvas_sig.axes.stem(signal.t, signal.signal, basefmt=" ")
    else:
        canvas_sig.axes.plot(signal.t, signal.signal)

    canvas_sig.axes.set_title(f"{signal_name} #{list_index+1}")
    canvas_sig.axes.set_xlabel("Czas (s)")
    canvas_sig.axes.set_ylabel("Amplituda")
    canvas_sig.axes.grid(True)
    canvas_sig.draw()

    canvas_hist.axes.cla()
    signal_values = signal.get_full_periods()
    
    try:
        bins = int(self.get_input_value(self.bins))
    except (ValueError, TypeError):
        bins = 10  

    canvas_hist.axes.hist(signal_values, bins=bins, edgecolor='black', alpha=0.7)
    canvas_hist.axes.set_title(f"Histogram")
    canvas_hist.axes.set_xlabel("Wartość Amplitudy")
    canvas_hist.axes.set_ylabel("Liczba wystąpień")
    canvas_hist.axes.grid(axis='y', linestyle='--', alpha=0.7)
    canvas_hist.draw()

    params = signal.calculate_parameters()
    
    if params and hasattr(self, 'params_display'):
        text = f"PARAMETRY STATYSTYCZNE SYGNAŁU #{list_index + 1}\n"
        text += f"Nazwa: {signal_name}\n"
        text += "=" * 35 + "\n"
        
        for key, value in params.items():
            text += f"{key:<28}: {value:.4f}\n"
        
        self.params_display.setText(text)

   def add_selected_signals(self):
      if self.signal1 is None or self.signal2 is None:
         QMessageBox.warning(self, "Błąd", "Najpierw ustaw Sygnał 1 i Sygnał 2 wybierając je z listy!")
         return

      try:
         new_signal = operations.add_signals(self.signal1, self.signal2)
         name1 = self.get_sig_name(self.signal1)
         name2 = self.get_sig_name(self.signal2)
         signal_name = f"Dodanie {name1} + {name2}"
         new_signal.name_override = signal_name

         self.signals_history.append(new_signal)
         self.add_signal_to_lists(signal_name)
         # self.signals_list_widget.addItem(f"#{len(self.signals_history)} - {signal_name}")

         QMessageBox.information(self, "Sukces", "Sygnały zostały pomyślnie dodane.")

         row = len(self.signals_history) - 1
         if row < 0: return
         self.combined_signal = self.signals_history[row]
         self.update_single_plot(self.combined_signal, self.canvas_sig3, self.canvas_hist3, row)

      except ValueError as e:
         QMessageBox.warning(self, "Błąd zgodności sygnałów", str(e))
      except Exception as e:
         QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas dodawania sygnałów:\n{str(e)}")

   def subtract_selected_signals(self):
      if self.signal1 is None or self.signal2 is None:
         QMessageBox.warning(self, "Błąd", "Najpierw ustaw Sygnał 1 i Sygnał 2 wybierając je z listy!")
         return

      try:
         new_signal = operations.subtraction_signals(self.signal1, self.signal2)
         self.signals_history.append(new_signal)
         signal_name = f"Odjęcie {self.signal1.get_signal_name()} + {self.signal2.get_signal_name()}"
         self.signals_list_widget.addItem(f"#{len(self.signals_history)} - {signal_name}")
         # self.signals_list_widget.setCurrentRow(len(self.signals_history) - 1)

         QMessageBox.information(self, "Sukces", "Sygnały zostały pomyślnie odjęte.")

         row = len(self.signals_history) - 1
         if row < 0: return
         self.combined_signal = self.signals_history[row]
         self.update_single_plot(self.combined_signal, self.canvas_sig3, self.canvas_hist3, row)

      except ValueError as e:
         QMessageBox.warning(self, "Błąd zgodności sygnałów", str(e))
      except Exception as e:
         QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas dodawania sygnałów:\n{str(e)}")

   def multiply_selected_signals(self):
      if self.signal1 is None or self.signal2 is None:
         QMessageBox.warning(self, "Błąd", "Najpierw ustaw Sygnał 1 i Sygnał 2 wybierając je z listy!")
         return

      try:
         new_signal = operations.multiplication_signals(self.signal1, self.signal2)
         self.signals_history.append(new_signal)
         signal_name = f"Mnożenie {self.signal1.get_signal_name()} + {self.signal2.get_signal_name()}"
         self.signals_list_widget.addItem(f"#{len(self.signals_history)} - {signal_name}")
         # self.signals_list_widget.setCurrentRow(len(self.signals_history) - 1)

         QMessageBox.information(self, "Sukces", "Sygnały zostały pomyślnie pomnożone.")

         row = len(self.signals_history) - 1
         if row < 0: return
         self.combined_signal = self.signals_history[row]
         self.update_single_plot(self.combined_signal, self.canvas_sig3, self.canvas_hist3, row)

      except ValueError as e:
         QMessageBox.warning(self, "Błąd zgodności sygnałów", str(e))
      except Exception as e:
         QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas dodawania sygnałów:\n{str(e)}")

   def divide_selected_signals(self):
      if self.signal1 is None or self.signal2 is None:
         QMessageBox.warning(self, "Błąd", "Najpierw ustaw Sygnał 1 i Sygnał 2 wybierając je z listy!")
         return

      try:
         new_signal = operations.division_signals_with_epsilon(self.signal1, self.signal2)
         self.signals_history.append(new_signal)
         signal_name = f"Dzielenie {self.signal1.get_signal_name()} + {self.signal2.get_signal_name()}"
         self.signals_list_widget.addItem(f"#{len(self.signals_history)} - {signal_name}")
         # self.signals_list_widget.setCurrentRow(len(self.signals_history) - 1)

         QMessageBox.information(self, "Sukces", "Sygnały zostały pomyślnie podzielone.")

         row = len(self.signals_history) - 1
         if row < 0: return
         self.combined_signal = self.signals_history[row]
         self.update_single_plot(self.combined_signal, self.canvas_sig3, self.canvas_hist3, row)

      except ValueError as e:
         QMessageBox.warning(self, "Błąd zgodności sygnałów", str(e))
      except Exception as e:
         QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas dodawania sygnałów:\n{str(e)}")

   def show_context_menu(self, pos):
      item = self.signals_list_widget.itemAt(pos)
      if item is None:
         return
      menu = QMenu(self)
      delete_action = menu.addAction("Usuń sygnał")
      action = menu.exec(self.signals_list_widget.mapToGlobal(pos))
      if action == delete_action:
         self.delete_signal(item)

   def delete_signal(self, item):
      row = self.signals_list_widget.row(item)
      deleted_signal = self.signals_history.pop(row)
      self.signals_list_widget.takeItem(row)
      self.conversion_signals_list.takeItem(row)

      if self.signal1 == deleted_signal:
         self.signal1 = None
         self.canvas_sig1.axes.cla()
         self.canvas_hist1.axes.cla()
         self.canvas_sig1.draw()
         self.canvas_hist1.draw()

      if self.signal2 == deleted_signal:
         self.signal2 = None
         self.canvas_sig2.axes.cla()
         self.canvas_hist2.axes.cla()
         self.canvas_sig2.draw()
         self.canvas_hist2.draw()

      if self.combined_signal == deleted_signal:
         self.combined_signal = None
         self.canvas_sig3.axes.cla()
         self.canvas_hist3.axes.cla()
         self.canvas_sig3.draw()
         self.canvas_hist3.draw()

      if row == 0:
         self.set_signal1()

      for i in range(self.signals_list_widget.count()):
         current_item = self.signals_list_widget.item(i)
         current_item_conv = self.conversion_signals_list.item(i)
         signal_name = self.get_sig_name(self.signals_history[i])
         text = f"#{i+1} - {signal_name}"
         current_item.setText(text)
         current_item_conv.setText(text)

