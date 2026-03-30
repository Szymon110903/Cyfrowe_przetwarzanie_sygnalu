import unittest
import numpy as np
import os
from src.logic.signals_generator import sinusoidal_signal
from src.logic.conversion import *
import matplotlib.pyplot as plt


class TestConversionPipeline(unittest.TestCase):
    def setUp(self):
        self.f_continous = 1000
        self.A = 1
        self.d = 1
        self.T = 0.5
        self.fs = 20
        self.bit_depth = 8

        self.output_dir = "test_outputs"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_full_conversion(self):
        t_c, sig_c = sinusoidal_signal(self.A, self.T, self.d, self.f_continous)
        t_s, sig_s = sampling(t_c, sig_c, self.fs)
        sig_q = quantization_with_clipping(sig_s, self.bit_depth)
        sig_r2 = first_order_hold_reconstruction(sig_q, t_s, t_c)
        sig_r3 = sinc_reconstruction(sig_q, t_s, t_c)

        fig, axs = plt.subplots(3, 1, sharex=True)
        axs[0].plot(t_c, sig_c, 'b-', label="sygnal oryginalny")
        axs[0].stem(t_s, sig_s, linefmt='r-', markerfmt='ro', basefmt=' ', label='Probki')
        axs[0].title.set_text(f"Probkowanie - f{self.fs}Hz")
        axs[0].legend(loc='upper right')
        axs[0].grid(True)

        axs[1].plot(t_c, sig_c, 'b-', label="sygnal oryginalny")
        axs[1].plot(t_c, sig_r2, 'g-', label="Sygnal po rekonstrukcji")
        axs[1].title.set_text("Rekonsturkcja pierwszego rzedu")
        axs[1].grid(True)

        axs[2].plot(t_c, sig_c, 'b-', label="sygnal oryginalny")
        axs[2].plot(t_c, sig_r3, 'g-', label="Sygnal po rekonstrukcji")
        axs[2].title.set_text("Rekonsturkcja sinc")
        axs[2].grid(True)

        file_path = os.path.join(self.output_dir, "split_pipeline_test.png")
        plt.savefig(file_path)
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
