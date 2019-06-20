import scipy
from scipy.fftpack import dct
import numpy as np
import math

# cell dct evaluation of the input image
def dct_cells(image, F, d):
    compressed_image = image #copy to store the original image

    # cycle the image in step of F
    for x in range(0,image.shape[0],F):
        for y in range(0,image.shape[1],F):
            cell = compressed_image[x:x+F, y:y+F]   # width of cell = F, height of cell = F
            cell = dct(cell,type = 2, norm = 'ortho') # discrete cosine transform of the selected cell

            # delete the frequencies in the cell making reference to d parameter
            for x in range(cell.shape[0]):
                for y in range(cell.shape[1]):
                    if x+y > d:
                        cell[i,j] = 0 

            # compute the inverse dct of the cell
            cell = dct(cell, type = 3, norm = 'ortho')

            #round of ff at the nearest integer, put to 0 negative values, put to 255 bigger values
            for x in range(cell.shape[0]):
                for y in range(cell.shape[1]):
                    value = round(cell[x,y])
                    if value < 0:
                        value = 0
                    elif value > 255:
                        value = 255
                    cell[x,y] = value
            compressed_image[x:x+F, y:y+F] = cell
    
    return compressed_image
