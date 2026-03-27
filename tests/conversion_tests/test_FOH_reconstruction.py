import unittest
import numpy as np
from src.logic.conversion import first_order_hold_reconstruction

class TestFOH(unittest.TestCase):
    def setUp(self):
        self.t_sampled = np.array([0, 1, 2, 3])
        self.signal_sampled = np.array([10, 20, 0, -10])

    def test_exact_sample_points(self):
        t_continous = np.array([0, 1, 2, 3])
        expected = np.array([10, 20, 0, -10])

        reconstructed = first_order_hold_reconstruction(self.signal_sampled, self.t_sampled, t_continous)
        np.testing.assert_allclose(expected, reconstructed)

    def test_values_between_sample_points(self):
        t_continous = np.array([0.5, 1.5, 2.5])
        expected = np.array([15, 10, -5])

        reconstructed = first_order_hold_reconstruction(self.signal_sampled, self.t_sampled, t_continous)
        np.testing.assert_allclose(expected, reconstructed)

if __name__ == '__main__':
    unittest.main()
