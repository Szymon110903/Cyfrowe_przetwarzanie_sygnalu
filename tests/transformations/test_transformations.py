import unittest
import numpy as np
from src.logic.transfomations import dft, reverse_bits, fft_dit

class TestTransformations(unittest.TestCase):

   def test_reverse_bits_4(self):
      # input array
      x = np.array([0, 1, 2, 3])
      expected = np.array([0, 2, 1, 3], dtype=complex)
      results = reverse_bits(x)
      np.testing.assert_array_equal(results, expected)

   def test_reverse_bits_8(self):
      x = np.array([0, 1, 2, 3, 4, 5, 6, 7])
      expected = np.array([0, 4, 2, 6, 1, 5, 3, 7], dtype=complex)
      results = reverse_bits(x)
      np.testing.assert_array_equal(results, expected)

   def test_dft_constant_signal(self):
      x = np.array([2.0, 2.0, 2.0, 2.0])
      expected = np.array([2.0+0j, 0.0+0j, 0.0+0j, 0.0+0j], dtype=complex)
      results = dft(x)
      np.testing.assert_allclose(results, expected, atol=1e-10)

   def test_dft_impulse_signal(self):
      x = np.array([1.0, 0.0, 0.0, 0.0])
      expected = np.array([0.25+0j, 0.25+0j, 0.25+0j, 0.25+0j], dtype=complex)
      results = dft(x)
      np.testing.assert_allclose(results, expected, atol=1e-10)

   def test_dft_versus_numpy_dft(self):
      np.random.seed(42)
      x = np.random.rand(8)
      result = dft(x)
      expected = np.fft.fft(x) / len(x)
      np.testing.assert_allclose(result, expected, atol=1e-10)

   def test_fft_dit_constant_signal(self):
      x = np.array([2.0, 2.0, 2.0, 2.0])
      expected = np.array([2.0+0j, 0.0+0j, 0.0+0j, 0.0+0j], dtype=complex)
      results = fft_dit(x)
      np.testing.assert_allclose(results, expected, atol=1e-10)

   def test_fft_dit_impulse_signal(self):
      x = np.array([1.0, 0.0, 0.0, 0.0])
      expected = np.array([0.25+0j, 0.25+0j, 0.25+0j, 0.25+0j], dtype=complex)
      results = fft_dit(x)
      np.testing.assert_allclose(results, expected, atol=1e-10)

   def test_fft_dit_versus_numpy_dft(self):
      np.random.seed(42)
      x = np.random.rand(8)
      result = fft_dit(x)
      expected = np.fft.fft(x) / len(x)
      np.testing.assert_allclose(result, expected, atol=1e-10)



if __name__ == '__main__':
   unittest.main()
