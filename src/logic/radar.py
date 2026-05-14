import numpy as np

from src.logic.Signal import Signal
from src.logic.operations import correlate_signals_convolution


class RadarSimulator:
   def __init__(self, signal_speed=300.0, target_speed=10.0, initial_distance=50.0, fs=1000.0, buffer_length=500, reporting_period=0.5):
      # Parametry środowiska
      self.V = signal_speed
      self.target_speed = target_speed
      self.actual_distance = initial_distance
      # Parametry radaru
      self.fs = fs
      self.buffer_length = buffer_length
      self.reporting_period = reporting_period
      # Zegar symulacji
      self.current_time = 0.0

   def generate_composite_signal(self, t):
      f1 = 2.0
      f2 = 5.0
      return np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

   def generate_sounding_signal(self):
      t = self.current_time + np.arange(self.buffer_length) / self.fs
      sig_values = self.generate_composite_signal(t)
      sig = Signal(A=1.5, d=self.buffer_length/self.fs, fs=self.fs, t1=self.current_time, t=t, signal=sig_values)
      sig.name_override = "Sygnał sondujący (wysłany)"
      return sig

   def generate_reflected_signal(self, delay):
      t = self.current_time + np.arange(self.buffer_length) / self.fs
      t_delayed = t - delay
      sig_values = self.generate_composite_signal(t_delayed)
      sig = Signal(A=1.5, d=self.buffer_length/self.fs, fs=self.fs, t1=self.current_time, t=t, signal=sig_values)
      sig.name_override = "Sygnał zwrotny (odebrany)"
      return sig

   def simulate_step(self):
      actual_delay = (2.0 * self.actual_distance) / self.V
      sig_sent = self.generate_sounding_signal()
      sig_recv = self.generate_reflected_signal(delay=actual_delay)

      correlation = correlate_signals_convolution(sig_recv, sig_sent)
      correlation.name_override = "Korelacja wzajemna R_yx"

      center_idx = self.buffer_length - 1
      right_half = correlation.signal[center_idx:]
      max_idx_relative = np.argmax(right_half)
      measured_delay = max_idx_relative / self.fs
      measured_distance = (self.V * measured_delay) / 2.0
      dist_at_moment = self.actual_distance
      self.current_time += self.reporting_period
      self.actual_distance += self.target_speed * self.reporting_period
      return {
         "time": self.current_time - self.reporting_period,
         "actual_distance": dist_at_moment,
         "measured_distance": measured_distance,
         "error": abs(dist_at_moment - measured_distance),
         "sig_sent": sig_sent,
         "sig_recv": sig_recv,
         "correlation": correlation,
      }
