import numpy as np
import

# DFT F-1 z instrukcji
def dft(x):
   N = len(x)
   X = np.zeros(N)
   for m in range(N):
      for n in range(N):
         X[m] += x[n] * np.exp(-2j * np.pi * m * n / N)
   return X / N