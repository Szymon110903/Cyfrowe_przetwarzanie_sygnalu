import numpy as np
import time

# DFT F-1 z instrukcji
def dft(x):
   N = len(x)
   X = np.zeros(N, dtype=complex)
   for m in range(N):
      for n in range(N):
         X[m] += x[n] * np.exp(-2j * np.pi * m * n / N)
   return X / N

# Funkcja pomocnicza do przestawienia kolejności próbek
def reverse_bits(x):
   N = len(x)
   num_bits = int(np.log2(N))
   x_rev = np.zeros(N, dtype=complex)
   for i in range(N):
      i_rev = int(f"{i:0{num_bits}b}"[::-1], 2)
      x_rev[i_rev] = x[i]
   return x_rev

# Szybka transormata Fouriera z decymacją w dziedzinie czasu
def fft_dit(x):
   N = len(x)
   if (N & (N - 1)) != 0 or N == 0:
      raise ValueError("Liczba próbek musi być potęgą liczby 2.")
   X = reverse_bits(x)
   step = 2
   while step <= N:
      half_step = step // 2
      for k in range(0, N, step):
         for m in range(half_step):
            W = np.exp(-2j * np.pi * m / step)
            even_idx = k + m
            odd_idx = k + m + half_step
            temp = X[even_idx]
            X[even_idx] = temp + X[odd_idx] * W
            X[odd_idx] = temp - X[odd_idx] * W
      step *= 2
   return X/N

