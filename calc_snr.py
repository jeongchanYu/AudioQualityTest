import numpy as np
from math import ceil, log10

"""
This code is made by https://github.com/dbwls553/SignalToNoise/blob/master/get_signal_to_noise.py

If file is not noisy then SNR and SSNR are about 100dB.
"""

def SSNR(noisy, clean, frame_size):
    clean_signal = np.array(clean)
    size_of_clean = clean_signal.size
    noisy_signal = np.array(noisy)
    size_of_noisy = noisy_signal.size

    if size_of_clean != size_of_noisy:
        raise Exception("ERROR: Input output size mismatch")

    number_of_frame_size = ceil(size_of_clean / frame_size)

    S_SNR = 0
    nonzero_frame_number = 0
    input, signal, noise = [], [], []
    for i in range(number_of_frame_size):
        input.append(noisy_signal[frame_size * i:frame_size * (i + 1)])
        signal.append(clean_signal[frame_size * i:frame_size * (i + 1)])
        noise.append(input[i] - signal[i])

        segmental_signal_power = 0
        segmental_noise_power = 0
        for n in range(len(signal[i])):
            segmental_signal_power += pow(signal[i][n], 2)
            segmental_noise_power += pow(noise[i][n], 2)

        if segmental_noise_power == 0:
            segmental_noise_power = pow(0.1, 10)

        if segmental_signal_power != 0:
            nonzero_frame_number += 1
            S_SNR += 10 * log10(segmental_signal_power / segmental_noise_power)

    S_SNR /= nonzero_frame_number
    return S_SNR

def SNR(noisy, clean):
    clean_signal = np.array(clean)
    size_of_clean = clean_signal.size
    noisy_signal = np.array(noisy)
    size_of_noisy = noisy_signal.size

    if size_of_clean != size_of_noisy:
        raise Exception("ERROR: Input output size mismatch")

    signal_power = 0
    noise_power = 0
    signal, noise = [], []
    signal.extend(clean_signal[:])
    noise.extend(noisy_signal - clean_signal)

    for i in range(size_of_noisy):
        signal_power += pow(signal[i], 2)
        noise_power += pow(noise[i], 2)

    if noise_power == 0:
        noise_power = pow(0.1, 10)
        # raise Exception("ERROR: Not noisy")
    snr = 10 * log10(signal_power / noise_power)
    return snr
