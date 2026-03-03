import matplotlib.pyplot as plt

def plot_signal(t, signal, title="Sygnał", xlabel="Czas (s)", ylabel="Amplituda"):
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal, label='Sygnał')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend()
    plt.show()