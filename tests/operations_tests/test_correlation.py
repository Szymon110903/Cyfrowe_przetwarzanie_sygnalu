import unittest
import numpy as np
from src.logic.Signal import Signal
from src.logic.operations import correlate_signals_direct, correlate_signals_convolution

class TestCorrelation(unittest.TestCase):
   def setUp(self):
      self.fs = 1.0
      self.sig_h = Signal(A=1, d=4, fs=self.fs, t1=0, t=np.array([0, 1, 2, 3]), signal=np.array([1, 2, 3, 4]))
      self.sig_x = Signal(A=1, d=3, fs=self.fs, t1=0, t=np.array([0, 1, 2]), signal=np.array([5, 6, 7]))
      self.expected_correlation = np.array([7, 20, 38, 56, 39, 20])

   def test_direct_correlation(self):
      result_sig = correlate_signals_direct(self.sig_h, self.sig_x)
      expected_length = len(self.sig_h.signal) + len(self.sig_x.signal) - 1
      self.assertEqual(len(result_sig.signal), expected_length)
      np.testing.assert_allclose(result_sig.signal, self.expected_correlation)

   def test_convolution_correlation(self):
      result_sig = correlate_signals_convolution(self.sig_h, self.sig_x)
      expected_length = len(self.sig_h.signal) + len(self.sig_x.signal) - 1
      self.assertEqual(len(result_sig.signal), expected_length)
      np.testing.assert_allclose(result_sig.signal, self.expected_correlation)

   def test_both_methods_equal(self):
      random_h = np.random.rand(15)
      random_x = np.random.rand(10)
      sig_rand_h = Signal(A=1, d=15, fs=1, t1=0, t=np.arange(15), signal=random_h)
      sig_rand_x = Signal(A=1, d=10, fs=1, t1=0, t=np.arange(10), signal=random_x)
      result_direct = correlate_signals_direct(sig_rand_h, sig_rand_x)
      result_convolution = correlate_signals_convolution(sig_rand_h, sig_rand_x)
      np.testing.assert_allclose(result_direct.signal, result_convolution.signal)


if __name__ == '__main__':
   unittest.main()
