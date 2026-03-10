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

def plot_histogram(signal_values, bins=10, title="Histogram"):
    plt.figure(figsize=(10, 5))
    plt.hist(signal_values, bins=bins)
    plt.title(title)
    plt.xlabel("Wartość Amplitudy")
    plt.ylabel("Liczba wystąpień próbki")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
