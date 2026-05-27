import unittest
import numpy as np
from src.logic.transfomations import dft, fft_dit


class TestDFT(unittest.TestCase):
   def test_dft_constant_signal(self):
      x = np.array([2.0, 2.0, 2.0, 2.0])
      expected = np.array([2.0 + 0j, 0.0 + 0j, 0.0 + 0j, 0.0 + 0j], dtype=complex)
      results = dft(x)
      np.testing.assert_allclose(results, expected, atol=1e-10)

   def test_dft_impulse_signal(self):
      x = np.array([1.0, 0.0, 0.0, 0.0])
      expected = np.array([0.25 + 0j, 0.25 + 0j, 0.25 + 0j, 0.25 + 0j], dtype=complex)
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
      expected = np.array([2.0 + 0j, 0.0 + 0j, 0.0 + 0j, 0.0 + 0j], dtype=complex)
      results = fft_dit(x)
      np.testing.assert_allclose(results, expected, atol=1e-10)

   def test_fft_dit_impulse_signal(self):
      x = np.array([1.0, 0.0, 0.0, 0.0])
      expected = np.array([0.25 + 0j, 0.25 + 0j, 0.25 + 0j, 0.25 + 0j], dtype=complex)
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
