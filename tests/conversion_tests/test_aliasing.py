import unittest
import os
from src.logic.signals_generator import sinusoidal_signal
from src.logic.conversion import *
import matplotlib.pyplot as plt


class TestAliasing(unittest.TestCase):
    def setUp(self):
        self.f0 = 100
        self.fs = 1000
        self.fd = 1100
        self.A0 = 1
        self.Ad = 0.5
        self.T0 = 1/self.f0
        self.Td = 1/self.fd
        self.d = 0.04
        self.f_rec = 10000
        self.bit_depth = 8

        self.output_dir = "test_outputs"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_full_conversion(self):
        t_cont, sig0_cont = sinusoidal_signal(self.A0, self.T0,self.d, self.f_rec)
        _, sigd_cont = sinusoidal_signal(self.Ad, self.Td, self.d, self.f_rec)
        sig_cont = sig0_cont + sigd_cont

        t_s, sig0_s = sinusoidal_signal(self.A0, self.T0, self.d, self.fs)
        _, sigd_s = sinusoidal_signal(self.Ad, self.Td, self.d, self.fs)
        sig_s = sig0_s + sigd_s
        sig_q = quantization_with_clipping(sig_s, self.bit_depth)

        t_rec, sig_r2 = first_order_hold_reconstruction(sig_q, t_s, self.f_rec)
        t_rec_sinc, sig_r3 = sinc_reconstruction(sig_q, t_s, self.f_rec)

        fig, axs = plt.subplots(3, 1, sharex=True)
        axs[0].plot(t_cont, sig_cont, 'b-', label="sygnal oryginalny")
        axs[0].stem(t_s, sig_s, linefmt='r-', markerfmt='ro', basefmt=' ', label='Probki')
        axs[0].title.set_text(f"Probkowanie - f{self.fs}Hz")
        axs[0].legend(loc='upper right')
        axs[0].grid(True)

        axs[1].plot(t_cont, sig_cont, 'b-', label="sygnal oryginalny")
        axs[1].plot(t_rec, sig_r2, 'g-', label="Sygnal po rekonstrukcji")
        axs[1].title.set_text("Rekonsturkcja pierwszego rzedu")
        axs[1].grid(True)

        axs[2].plot(t_cont, sig_cont, 'b-', label="sygnal oryginalny")
        axs[2].plot(t_rec_sinc, sig_r3, 'g-', label="Sygnal po rekonstrukcji")
        axs[2].title.set_text("Rekonsturkcja sinc")
        axs[2].grid(True)

        file_path = os.path.join(self.output_dir, "split_pipeline_test.png")
        plt.savefig(file_path)
        plt.close(fig)

if __name__ == '__main__':
    unittest.main()
