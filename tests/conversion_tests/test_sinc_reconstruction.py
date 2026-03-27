import unittest
import numpy as np
from src.logic.conversion import sinc_reconstruction

class TestSincReconstruction(unittest.TestCase):
    def setUp(self):
        self.fs = 10
        self.t_sampled = np.arange(0,1, 1/self.fs)
        self.signal_sampled = np.array([0.0, 1.5, 2.0, -1.0, -2.5, 0.5, 1.0, 3.0, 0.0, -1.0])

    def test_exact_sample_points(self):
        reconstructed = sinc_reconstruction(self.signal_sampled, self.t_sampled, self.t_sampled)
        np.testing.assert_allclose(reconstructed, self.signal_sampled, atol=1e-9)

    def test_single_sample(self):
        sig_samp = np.array([1.0])
        t_samp = np.array([0.0])
        t_continous = np.array([0.0, 1.0, 2.0])
        reconstructed = sinc_reconstruction(sig_samp, t_samp, t_continous)
        np.testing.assert_array_equal(reconstructed, sig_samp)

    def test_num_neighbours(self):
        t_continous = np.array([0.45])

        reconstructed_full = sinc_reconstruction(self.signal_sampled, self.t_sampled, t_continous)
        reconstructed_window = sinc_reconstruction(self.signal_sampled, self.t_sampled, t_continous, num_neighbours=1)
        self.assertEqual(len(reconstructed_full), 1)
        self.assertEqual(len(reconstructed_window), 1)
        self.assertNotEqual(reconstructed_full[0], reconstructed_window[0])

if __name__ == '__main__':
    unittest.main()
