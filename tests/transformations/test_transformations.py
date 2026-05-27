import unittest
import numpy as np
from src.logic.transfomations import reverse_bits

class TestTransformations(unittest.TestCase):

   def test_reverse_bits_4(self):
      x = np.array([0, 1, 2, 3])
      expected = np.array([0, 2, 1, 3], dtype=complex)
      results = reverse_bits(x)
      np.testing.assert_array_equal(results, expected)

   def test_reverse_bits_8(self):
      x = np.array([0, 1, 2, 3, 4, 5, 6, 7])
      expected = np.array([0, 4, 2, 6, 1, 5, 3, 7], dtype=complex)
      results = reverse_bits(x)
      np.testing.assert_array_equal(results, expected)



if __name__ == '__main__':
   unittest.main()
