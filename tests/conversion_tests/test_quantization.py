import unittest
import numpy as np
from src.logic.conversion import quantization_with_clipping


class TestQuantization(unittest.TestCase):
    def test_constant_signal(self):
        signal = np.array([1.0,1.0,1.0,1.0,1.0])

        quantized = quantization_with_clipping(signal, bit_depth=3)
        np.testing.assert_array_equal(quantized, signal)

    def test_two_bit_quantization(self):
        signal = np.array([0, 0.8, 1.5, 2.1, 3, 3.9, 5.1, 9])
        expected_signal = np.array([0, 0, 0, 0, 3, 3, 3, 9])

        quantized = quantization_with_clipping(signal, bit_depth=2)
        np.testing.assert_allclose(quantized, expected_signal)

    def test_negative_and_positive_values(self):
        signal = np.array([-1, -0.1, 0.1, 0.99, 1])
        expected_signal = np.array([-1, -1, -1, -1, 1])
        quantized = quantization_with_clipping(signal, bit_depth=1)
        np.testing.assert_allclose(quantized, expected_signal)

    def test_number_of_unique_levels(self):
        t = np.linspace(0, 2 * np.pi, 1000)
        sig = np.sin(t)
        bit_depth = 3
        max_levels = 2 ** bit_depth

        quantized = quantization_with_clipping(sig, bit_depth=bit_depth)
        unique_values = np.unique(quantized)
        self.assertLessEqual(len(unique_values), max_levels)

if __name__ == '__main__':
    unittest.main()
