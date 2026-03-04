import matplotlib.pyplot as plt

def plot_signal(t, signal, title="Sygnał", xlabel="Czas (s)", ylabel="Amplituda", discrete=False):
    plt.figure(figsize=(10, 4))
    if discrete:
        plt.stem(t, signal, label='Sygnał (dyskretny)', basefmt=" ")
    else:
        plt.plot(t, signal, label='Sygnał (ciągły)')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend()
    plt.show()