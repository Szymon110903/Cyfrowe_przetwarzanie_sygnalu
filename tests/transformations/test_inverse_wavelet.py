import unittest
import numpy as np
from src.logic.transformations import wavelet_transform, inverse_wavelet_transform

class TestInverseWaveletTransform(unittest.TestCase):
   def test_reconstruction_even_lengths(self):
      for N in [8, 16, 32, 64, 128, 256]:
         # Generate a random signal
         x = np.random.randn(N)
         
         # Perform forward DWT
         x1, x2 = wavelet_transform(x)
         
         # Perform inverse DWT
         x_rec = inverse_wavelet_transform(x1, x2)
         
         # Assert perfect reconstruction
         np.testing.assert_allclose(x, x_rec, rtol=1e-10, atol=1e-10)

   def test_reconstruction_odd_lengths(self):
      for N in [7, 15, 33, 65, 127]:
         # Generate a random signal
         x = np.random.randn(N)
         
         # Perform forward DWT
         x1, x2 = wavelet_transform(x)
         
         # Perform inverse DWT, passing the exact N
         x_rec = inverse_wavelet_transform(x1, x2, N=N)
         
         # Assert perfect reconstruction
         np.testing.assert_allclose(x, x_rec, rtol=1e-10, atol=1e-10)

if __name__ == '__main__':
   unittest.main()
