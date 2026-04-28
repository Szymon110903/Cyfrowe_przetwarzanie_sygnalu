import unittest
from src.logic.filters import *


class TestFilters(unittest.TestCase):
   def setUp(self):
      self.M = 15
      self.K = 8
      self.fs = 1000

   def test_generate_low_pass_filter_throws(self):
      with self.assertRaises(ValueError):
         generate_low_pass_filter(10, self.K, self.fs)

   def test_generate_low_pass_filter(self):
      filter_sig = generate_low_pass_filter(self.M, self.K, self.fs)

      self.assertEqual(len(filter_sig.signal), self.M)
      self.assertEqual(filter_sig.fs, self.fs)

      center = (self.M - 1) // 2
      self.assertAlmostEqual(filter_sig.signal[center], 2.0 / self.K)
      self.assertAlmostEqual(filter_sig.signal[center - 1], filter_sig.signal[center + 1])
      self.assertAlmostEqual(filter_sig.signal[center - 2], filter_sig.signal[center + 2])

   def test_apply_blackman_window(self):
      filter_sig = generate_low_pass_filter(self.M, self.K, self.fs)
      windowed_sig = apply_blackman_window(filter_sig)

      self.assertEqual(len(windowed_sig.signal), self.M)
      self.assertTrue(abs(windowed_sig.signal[0]) < abs(filter_sig.signal[0]))
      self.assertTrue(abs(windowed_sig.signal[-1]) < abs(filter_sig.signal[-1]))

   def test_transform_to_band_pass(self):
      filter_sig = generate_low_pass_filter(self.M, self.K, self.fs)
      bp_sig = transform_to_band_pass(filter_sig)

      self.assertEqual(len(bp_sig.signal), self.M)
      self.assertAlmostEqual(bp_sig.signal[0], 0.0)
      center = (self.M - 1) // 2
      expected_multiplier = 2 * np.sin(np.pi * center / 2)
      expected_center_val = filter_sig.signal[center] * expected_multiplier
      self.assertAlmostEqual(bp_sig.signal[center], expected_center_val)

   def test_filter_signal_with_fir(self):
      x_signal = np.ones(10)
      input_sig = Signal(A=1, d=10/self.fs, fs=self.fs, t1=0, t=np.arange(10)/self.fs, signal=x_signal)
      filter_sig = generate_low_pass_filter(self.M, self.K, self.fs)

      filtered_sig = filter_signal_with_fir(input_sig, filter_sig)

      expected_length = len(x_signal) + self.M - 1
      self.assertEqual(len(filtered_sig.signal), expected_length)

if __name__ == '__main__':
   unittest.main()
