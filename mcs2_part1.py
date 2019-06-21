import scipy
from scipy.fftpack import dctn
import numpy as np
import math
from datetime import datetime
import csv
import os

#DCT1 Function
def dct_1(arr):
    n = len(arr)
    c_k = np.zeros((n, n))
    
    for k in range(n):
        alfa = math.sqrt(1 / n) if k == 0 else math.sqrt(2 / n) #Alfa coefficient

        sum = 0
        for x,f_i in enumerate(arr):
            sum += f_i * math.cos((k * math.pi * (2 * x + 1)) / (2 * n)) #Summatory from 0 to N-1 of dct
        c_k[k] = sum * alfa
    
    return c_k

#DCT2 Function
def dct_2(mat):
    return dct_1(np.transpose(dct_1(np.transpose(mat))))

if __name__ == '__main__':
    dimensions_matrix = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000]
    if os.path.isfile('results/dct2_nostra.csv'):
        os.remove('results/dct2_nostra.csv')
    if os.path.isfile('results/dct2_fft.csv'):
        os.remove('results/dct2_fft.csv')

    for i in dimensions_matrix:
        print("***** Working on " + str(i) + "x" + str(i) + " Matrix *****")
        matrix = np.random.uniform(low=0.0, high=255.0, size=(i, i)) #Generates a random array, with values in an uniform distribution between 0 and 255

        #DCT2 - Homemade Version
        now = datetime.now()
        dct2_results = dct_2(matrix)
        t_dct2 = (datetime.now() - now).total_seconds()
        print("Time Our DCT: " + str(t_dct2))

        with open('results/dct2_nostra.csv', 'a') as csvFile:
            row = [i, t_dct2]
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        
        #DCT2 - FFT Version
        now = datetime.now()
        dct_fft = dctn(matrix, norm = 'ortho') #type = 2 is default.
        t_fft = (datetime.now() - now).total_seconds()
        print("Time FFT DCT: " + str(t_fft))

        with open('results/dct2_fft.csv', 'a') as csvFile:
            row = [i, t_fft]
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()