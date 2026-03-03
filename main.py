from signals import *
from signal_plots import *

def main():
    t, signal = uniform_noise(1, 1, 2000)
    # print("Czas (t):", t)
    # print("Sygnał:", signal)
    # plot_signal(t, signal, title="Sygnał o rozkładzie jednostajnym")
    # t, signal = gaussian_noise(1, 1, 2000)
    # plot_signal(t, signal, title="Sygnał o rozkładzie normalnym")
    t, signal = sinusoidal_signal(1, 15, 20, 2000)
    plot_signal(t, signal, title="Sygnał sinusoidalny")

if __name__ == "__main__":    main()