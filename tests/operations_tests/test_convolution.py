import unittest
import numpy as np
from src.logic.Signal import Signal
from src.logic.operations import convolution


class TestConvolution(unittest.TestCase):
   def setUp(self):
      self.fs = 1.0
      self.sig_h = Signal(A=1, d=4, fs=self.fs, t1=0, t=np.array([0, 1, 2, 3]), signal=np.array([1, 2, 3, 4]))
      self.sig_x = Signal(A=1, d=3, fs=self.fs, t1=0, t=np.array([0, 1, 2]), signal=np.array([5, 6, 7]))

   def test_convolution_values(self):
      expected_values = np.array([5, 16, 34, 52, 45, 28])
      result_sig = convolution(self.sig_h, self.sig_x)
      np.testing.assert_array_equal(expected_values, result_sig.signal)

   def test_convolution_length(self):
      M = len(self.sig_h.signal)
      N = len(self.sig_x.signal)
      result_sig = convolution(self.sig_h, self.sig_x)

      self.assertEqual(len(result_sig.signal), M + N - 1)

   def test_convolution_time_axis(self):
      # t1_h = 0, t1_x = 0 -> t1_res = 0
      result_sig = convolution(self.sig_h, self.sig_x)
      self.assertEqual(result_sig.t[0], 0)

      # Test z przesunięciem
      sig_h_shifted = Signal(A=1, d=4, fs=self.fs, t1=2, t=np.array([2, 3, 4, 5]), signal=np.array([1, 2, 3, 4]))
      result_shifted = convolution(sig_h_shifted, self.sig_x)
      self.assertEqual(result_shifted.t1, 2)  # 2 + 0

if __name__ == '__main__':
   unittest.main()
