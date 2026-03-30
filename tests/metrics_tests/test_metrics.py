import unittest
from src.logic.metrics import *


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.original = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
        self.processed_perfect = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
        self.processed_noisy = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_mse(self):
        mse_perfect = calculate_MSE(self.original, self.processed_perfect)
        self.assertEqual(mse_perfect, 0)
        mse_noisy = calculate_MSE(self.original, self.processed_noisy)
        self.assertEqual(mse_noisy, 100)

    def test_snr(self):
        snr_perfect = calculate_SNR(self.original, self.processed_perfect)
        self.assertEqual(snr_perfect, float('inf'))
        snr_noisy = calculate_SNR(self.original, self.processed_noisy)
        self.assertEqual(snr_noisy, 0)

    def test_psnr(self):
        psnr_perfect = calculate_PSNR(self.original, self.processed_perfect)
        self.assertEqual(psnr_perfect, float('inf'))
        psnr_noisy = calculate_PSNR(self.original, self.processed_noisy)
        self.assertEqual(psnr_noisy, -10)

    def test_md(self):
        md_perfect = calculate_MD(self.original, self.processed_perfect)
        self.assertEqual(md_perfect, 0)
        md_noisy = calculate_MD(self.original, self.processed_noisy)
        self.assertEqual(md_noisy, 10)
        processed = np.array([2, 2, 7, 2, 3, 5, 1, 2, 4, 0])
        md = calculate_MD(self.original, processed)
        self.assertEqual(md, 10)

    def test_enob(self):
        enob_perfect = calculate_ENOB(self.original, self.processed_perfect)
        self.assertEqual(enob_perfect, float('inf'))

        enob_noisy = calculate_ENOB(self.original, self.processed_noisy)
        expected_enob = (0 - 1.76) / 6.02
        self.assertAlmostEqual(enob_noisy, expected_enob, places=5)

if __name__ == '__main__':
    unittest.main()
