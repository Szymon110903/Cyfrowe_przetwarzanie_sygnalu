import unittest
from src.logic.radar import RadarSimulator


class TestRadarSimulator(unittest.TestCase):
   def setUp(self):
      self.radar = RadarSimulator(
         signal_speed=300.0,
         target_speed=-10.0,  # Obiekt zbliża się 10 m/s
         initial_distance=45.0,
         fs=1000.0,
         buffer_length=1000,  # Dłuższy bufor, żeby pomieścić 300 próbek opóźnienia
         reporting_period=1.0  # Raport co 1 sekundę
      )

   def test_initialization(self):
      """Sprawdza, czy parametry początkowe są prawidłowo ustawione."""
      self.assertEqual(self.radar.V, 300.0)
      self.assertEqual(self.radar.actual_distance, 45.0)
      self.assertEqual(self.radar.current_time, 0.0)

   def test_signal_generation(self):
      """Sprawdza własności sygnałów sondujących i zwrotnych."""
      sig_sent = self.radar.generate_sounding_signal()
      sig_recv = self.radar.generate_reflected_signal(delay=0.1)

      # Bufor musi mieć odpowiednią liczbę próbek
      self.assertEqual(len(sig_sent.signal), 1000)
      self.assertEqual(len(sig_recv.signal), 1000)
      self.assertEqual(sig_sent.fs, 1000.0)

   def test_simulate_step_distance_calculation(self):
      """Sprawdza rdzeń logiki - czy korelacja poprawnie wyznacza odległość."""
      result = self.radar.simulate_step()

      # W chwili t=0 odległość rzeczywista to 45m.
      self.assertEqual(result["actual_distance"], 45.0)
      self.assertAlmostEqual(result["measured_distance"], 45.0, delta=0.5)

   def test_simulate_step_updates_world_state(self):
      """Sprawdza, czy symulator poprawnie uaktualnia czas i pozycję obiektu."""
      # Krok 1 (czas: 0.0 -> 1.0)
      self.radar.simulate_step()
      self.assertEqual(self.radar.current_time, 1.0)
      self.assertEqual(self.radar.actual_distance, 35.0)

      # Krok 2 (czas: 1.0 -> 2.0)
      result2 = self.radar.simulate_step()
      self.assertEqual(result2["actual_distance"], 35.0)
      # Radar powinien teraz namierzyć odległość 35m
      self.assertAlmostEqual(result2["measured_distance"], 35.0, delta=0.5)
      self.assertEqual(self.radar.actual_distance, 25.0)



if __name__ == '__main__':
   unittest.main()