import unittest
import numpy as np
from src.logic.transformations import wavelet_transform

class TestWaveletTransform(unittest.TestCase):
   def test_wavelet_lengths(self):
      x = np.ones(8)
      x1, x2 = wavelet_transform(x)
      self.assertEqual(len(x1), 6)
      self.assertEqual(len(x2), 5)

   def test_wavelet_impulse_response(self):
      x = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
      h0 = (1 + np.sqrt(3)) / (4 * np.sqrt(2))
      h1 = (3 + np.sqrt(3)) / (4 * np.sqrt(2))
      h2 = (3 - np.sqrt(3)) / (4 * np.sqrt(2))
      h3 = (1 - np.sqrt(3)) / (4 * np.sqrt(2))

      x1, x2 = wavelet_transform(x)
      expected_x1_start = np.array([h0, h2, 0.0])
      expected_x2_start = np.array([-h2, -h0, 0.0])
      np.testing.assert_allclose(x1[:3], expected_x1_start, atol=1e-10)
      np.testing.assert_allclose(x2[:3], expected_x2_start, atol=1e-10)

if __name__ == '__main__':
   unittest.main()
