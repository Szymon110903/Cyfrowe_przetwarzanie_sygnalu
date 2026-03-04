from signals import *
from plots import *
import signal_class 
# TODO: spytać o działania na sygnałach różniących sie czasem trwania, częstotliwością próbkowania, czasem początkowym

def main():
  signal = signal_class.Signal(A=1, d=1, fs=1000, t1=0, function=sinusoidal_signal, T=0.2)
  signal.visualize()

if __name__ == "__main__":    main()