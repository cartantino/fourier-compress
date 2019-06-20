import scipy
from scipy.fftpack import dct
from scipy import misc
import numpy as np
import math
import os




# cell dct evaluation of the input image
def dct_compression(image, F, d):
    compressed_image = image #copy to store the original image
    h = image.shape[0]
    w = image.shape[1]
    # cycle the image in step of F
    for x in range(0,h,F):
        for y in range(0,w,F):
            cell = compressed_image[x:x+F, y:y+F]   # width of cell = F, height of cell = F
            cell = dct(cell,type = 2, norm = 'ortho') # discrete cosine transform of the selected cell

            c_h = cell.shape[0]
            c_w = cell.shape[1]
            # delete the frequencies in the cell making reference to d parameter
            for x in range(c_h):
                for y in range(c_w):
                    if x+y > d:
                        cell[x,y] = 0 

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



            print(compressed_image)
            dio  = input("mannaggia a cristo")
            
    return compressed_image

if __name__ ==  '__main__':
    F = int(input("insert F parameter:"))
    d = int(input("\ninsert d parameter"))
    
    images = ["artificial.bmp","big_building.bmp","big_tree","bridge.bmp","cathedral.bmp","deer.bmp","fireworks.bmp","flower_foveon.bmp","hdr.bmp"]
    path = 'images/'
    print("dio")
    for image in images:
        image = misc.imread(os.path.join(path,image), flatten = 0)
        image_compressed = dct_compression(image, F, d)
        