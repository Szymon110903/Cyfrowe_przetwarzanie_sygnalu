from signals import *
from signal_plots import *

# TODO: spytać o działania na sygnałach różniących sie czasem trwania, częstotliwością próbkowania, czasem początkowym

def main():
    t, signal = uniform_noise(1, 1, 2000)
    # print("Czas (t):", t)
    # print("Sygnał:", signal)
    # plot_signal(t, signal, title="Sygnał o rozkładzie jednostajnym")
    # t, signal = gaussian_noise(1, 1, 2000)
    # plot_signal(t, signal, title="Sygnał o rozkładzie normalnym")
    # t, signal = sinusoidal_signal(1, 15, 20, 2000)
    # plot_signal(t, signal, title="Sygnał sinusoidalny")
    # t, signal = sinusoidal_signal_onehalf_rectified(1, 15, 20, 2000)
    # plot_signal(t, signal, title="Sygnał sinusoidalny z dodatnią częścią")
    # t, signal = sinusoidal_signal_twohalf_rectified(1, 15, 20, 2000)
    # plot_signal(t, signal, title="Sygnał sinusoidalny z dodatnią częścią prostowaną")
    # t, signal = square_wave_signal(1, 10, 20, 0.75, 2000)
    # plot_signal(t, signal, title="Sygnał prostokątny")
    # t, signal = square_wave_signal_symetrical(1, 5, 20, 0.75, 2000)
    # plot_signal(t, signal, title="Sygnał prostokątny symetryczny")
    # t, signal = triangle_wave_signal(1, 10, 20, 0.5, 2000)
    # plot_signal(t, signal, title="Sygnał trójkątny")
    t, signal = unit_step_signal(1, 2, 5, 2000)
    plot_signal(t, signal, title="Sygnał skok jednostkowy")

if __name__ == "__main__":    main()