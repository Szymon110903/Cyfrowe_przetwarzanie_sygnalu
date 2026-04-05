import numpy as np

def calculate_MSE(original: np.ndarray, reconstructed: np.ndarray) -> float:
    return np.mean((original - reconstructed) ** 2)

def calculate_SNR(original: np.ndarray, reconstructed: np.ndarray) -> float:
    denominator = np.sum((original - reconstructed) ** 2)
    if denominator == 0:
        return float('inf')
    numerator = np.sum(original ** 2)
    return 10 * np.log10(np.divide(numerator, denominator))

def calculate_PSNR(original: np.ndarray, reconstructed: np.ndarray) -> float:
    denominator = calculate_MSE(original, reconstructed)
    if denominator == 0:
        return float('inf')
    numerator = np.abs(np.max(original))
    return 10 * np.log10(np.divide(numerator, denominator))

def calculate_MD(original: np.ndarray, reconstructed: np.ndarray) -> float:
    return np.max(np.abs(original - reconstructed))

def calculate_ENOB(original: np.ndarray, reconstructed: np.ndarray) -> float:
    snr = calculate_SNR(original, reconstructed)
    if snr == float('inf') or np.isinf(snr):
        return float('inf')

    return (snr - 1.76) / 6.02