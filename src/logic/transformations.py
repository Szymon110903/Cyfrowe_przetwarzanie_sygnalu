import numpy as np
from src.logic.operations import custom_convolution
import time

# DFT F-1 z instrukcji
def dft(x):
   N = len(x)
   X = np.zeros(N, dtype=complex)
   for m in range(N):
      for n in range(N):
         X[m] += x[n] * np.exp(-2j * np.pi * m * n / N)
   return X / N

def idft(X):
   N = len(X)
   x = np.zeros(N, dtype=complex)
   for n in range(N):
      for m in range(N):
         x[n] += X[m] * np.exp(2j * np.pi * m * n / N)
   return x

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

def ifft_dit(X):
   N = len(X)
   if (N & (N - 1)) != 0 or N == 0:
      raise ValueError("Liczba próbek musi być potęgą liczby 2.")
   x = reverse_bits(X)
   step = 2
   while step <= N:
      half_step = step // 2
      for k in range(0, N, step):
         for m in range(half_step):
            W = np.exp(2j * np.pi * m / step)
            even_idx = k + m
            odd_idx = k + m + half_step
            temp = x[even_idx]
            x[even_idx] = temp + x[odd_idx] * W
            x[odd_idx] = temp - x[odd_idx] * W
      step *= 2
   return x

# Przekształcenie falkowe rzędu czwartego
def wavelet_transform(x):
   h0 = (1 + np.sqrt(3)) / (4*np.sqrt(2))
   h1 = (3 + np.sqrt(3)) / (4*np.sqrt(2))
   h2 = (3 - np.sqrt(3)) / (4*np.sqrt(2))
   h3 = (1 - np.sqrt(3)) / (4*np.sqrt(2))
   H = np.array([h0, h1, h2, h3])
   G = np.array([h3, -h2, h1, -h0])
   xh = custom_convolution(x, H)
   xg = custom_convolution(x, G)
   return xh[0::2], xg[1::2]

def inverse_wavelet_transform(x1, x2, N=None):
   if N is None:
      N = 2 * (len(x1) - 2)

   h0 = (1 + np.sqrt(3)) / (4*np.sqrt(2))
   h1 = (3 + np.sqrt(3)) / (4*np.sqrt(2))
   h2 = (3 - np.sqrt(3)) / (4*np.sqrt(2))
   h3 = (1 - np.sqrt(3)) / (4*np.sqrt(2))
   H = np.array([h0, h1, h2, h3])
   G = np.array([h3, -h2, h1, -h0])

   # Budujemy macierz A przekształcenia falkowego o kształcie (len(x1) + len(x2), N)
   A = []
   for j in range(len(x1)):
      row = np.zeros(N)
      idx = 2 * j
      for k in range(4):
         x_idx = idx - k
         if 0 <= x_idx < N:
            row[x_idx] = H[k]
      A.append(row)

   for j in range(len(x2)):
      row = np.zeros(N)
      idx = 2 * j + 1
      for k in range(4):
         x_idx = idx - k
         if 0 <= x_idx < N:
            row[x_idx] = G[k]
      A.append(row)

   A = np.array(A)
   A_pinv = np.linalg.pinv(A)

   y = np.concatenate([x1, x2])
   x_rec = A_pinv @ y
   return x_rec


def measure_transform_time(func, x):
   start_time = time.perf_counter()
   result = func(x)
   end_time = time.perf_counter()
   return result, end_time - start_time
