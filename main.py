import custom_function as cf
import calc_snr as cs
from pypesq import pesq
import os
import wav
import sys
sys.setrecursionlimit(10**9)

clean_file_path = "C:/Users/YJC/Desktop/DenoiseWavenetCond/test_result/DWC_22_16_22_100/result"
noisy_file_path = "C:/Users/YJC/Desktop/DenoiseWavenetCond/test_result/DWC_22_16_22_100/noise"
csv_file_path   = "./22_16_22.csv"
ssnr_frame_size = 1600


# frame_size check
if type(ssnr_frame_size) != int:
    raise Exception("E: ssnr_frame_size must be int")
if ssnr_frame_size < 1:
    raise Exception("E: ssnr_frame_size must larger than 0")


# clean and noisy_file_path_path is path or file?
clean_path_isdir = os.path.isdir(clean_file_path)
noisy_path_isdir = os.path.isdir(noisy_file_path)
if clean_path_isdir != noisy_path_isdir:
    raise Exception("E: Clean and noisy path is incorrect")
if clean_path_isdir:
    if not cf.compare_path_list(clean_file_path, noisy_file_path, 'wav'):
        raise Exception("E: Clean and noisy file list is not same")
    clean_file_list = cf.read_path_list(clean_file_path, "wav")
    noisy_file_list = cf.read_path_list(noisy_file_path, "wav")
else:
    clean_file_list = [clean_file_path]
    noisy_file_list = [noisy_file_path]

cf.clear_csv_file(csv_file_path)
cf.write_csv_file(csv_file_path, "file name", "SNR,SSNR,PESQ")

for i in range(len(clean_file_list)):
    if clean_path_isdir:
        file_name = clean_file_list[i].replace(clean_file_path, "")
    else:
        file_name = os.path.basename(clean_file_path)
    print("({}/{}){} /".format(i+1, len(clean_file_list), file_name), end="")

    # read train data file
    clean_signal, clean_sample_rate = wav.read_wav(clean_file_list[i])
    noisy_signal, noisy_sample_rate = wav.read_wav(noisy_file_list[i])

    # different sample rate detect
    if clean_sample_rate != noisy_sample_rate:
        raise Exception("E: Different sample rate detected. clean({})/noisy({})".format(clean_sample_rate, noisy_sample_rate))

    SNR = cs.SNR(noisy_signal, clean_signal)
    SSNR = cs.SSNR(noisy_signal, clean_signal, ssnr_frame_size)
    PESQ = pesq(clean_signal, noisy_signal, clean_sample_rate)

    print(" SNR:{} | SSNR:{} | PESQ:{}".format(SNR, SSNR, PESQ))
    cf.write_csv_file(csv_file_path, file_name, "{},{},{}".format(SNR, SSNR, PESQ))