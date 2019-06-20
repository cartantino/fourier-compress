import scipy
from scipy.fftpack import dct
import numpy as np
import math
from datetime import datetime
import csv
import os

## DCT1 FUNCTION; returns frequency coefficients  array
def dct_1(arr):
    n = arr.size
    c_k = np.zeros(n)
    
    for k in range(n):
        if k == 0:
            alfa = math.sqrt(1/n)
        else:
            alfa = math.sqrt(2/n)
        sum = 0
        for x,f_i in enumerate(arr):
            sum += f_i * math.cos((k * math.pi * (2 * x + 1)) / (2 * n)) #summatory from 0 to N-1 of dct
        c_k[k] = sum * alfa
    
    return c_k

def dct_2(mat, dimension):
    result_matrix = np.zeros(mat.shape)
    result_matrix = np.apply_along_axis(dct_1, 1, mat) #iteration of the rows of the array
    result_matrix = np.apply_along_axis(dct_1, 0, result_matrix) #iteration of the transposed array evaluated at the previous step
    return result_matrix
    

if __name__ == '__main__':
    dimensions_matrix = [10,20,50,70,90, 100, 130, 200, 250, 300, 400, 500,700, 750, 800, 900, 1000]
    if os.path.isfile('results/dct2_nostra.csv'):
        os.remove('results/dct2_nostra.csv')
    if os.path.isfile('results/dct2_fft.csv'):
        os.remove('results/dct2_fft.csv')

    for i in dimensions_matrix:

        print("Working on " + str(i) + "*" + str(i) + " Matrix\n")
        matrix = np.random.uniform(low=0.0, high=255.0, size=(i, i)) #generate a random array, with values in an uniform distribution between 0 and 255
        
        now = datetime.now()
        dct2_results = dct_2(matrix, i)
        t_dct2 = (datetime.now() - now).total_seconds()
        print("our dct time: " + str(t_dct2) + "\n")
        print("Writing results on CSV of our dct\n")
        with open('results/dct2_nostra.csv', 'a') as csvFile:
            row = [i, t_dct2]
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        
        ####   DCT2 FFT    ######
        print("\n\nStarting evaluation of fft dct2")
        
        now = datetime.now()
        dct_fft = dct(matrix,type = 2, norm = 'ortho')
        t_fft = (datetime.now() - now).total_seconds()
        print("time fft: " + str(t_fft) + "\n")

        print("Writing results on CSV of fft dct\n")
        with open('results/dct2_fft.csv', 'a') as csvFile:
            row = [i, t_fft]
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()