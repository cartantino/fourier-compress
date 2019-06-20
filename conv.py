import scipy
from scipy.fftpack import dctn, idctn
from scipy import misc
import numpy as np
import math
import os
import matplotlib.pyplot as mplp




# cell dct evaluation of the input image
def dct_compression(image, F, d):
    compressed_image = image + 0 #copy to store the original image
    h = image.shape[0]
    print(h)
    w = image.shape[1]
    print(w)
    if(h%F != 0):
        h = int(h/F) * F
        print(h)
    if(w%F != 0):
        w = int(w/F) * F
        print(w)

    print(h)
    print(w)
    # cycle the image in step of F
    for x in range(0,h,F):
        for y in range(0,w,F):
            cell = compressed_image[x:x+F, y:y+F]   # width of cell = F, height of cell = F
            #print("first cell:\n")
            #print(cell)
            cell = dctn(cell, norm = 'ortho') # discrete cosine transform of the selected cell

            c_h = cell.shape[0]
            c_w = cell.shape[1]
            # delete the frequencies in the cell making reference to d parameter
            for x in range(0,c_h):
                for y in range(0,c_w):
                    if x+y >= d:
                        cell[x,y] = 0 

            # compute the inverse dct of the cell
            cell = idctn(cell, norm = 'ortho')

            #round of ff at the nearest integer, put to 0 negative values, put to 255 bigger values
            for x in range(0,c_h):
                for y in range(0,c_w):
                    value = round(cell[x,y])
                    if value < 0:
                        value = 0
                    elif value > 255:
                        value = 255
                    cell[x,y] = value
            compressed_image[x:x+F, y:y+F] = cell

    return compressed_image

if __name__ ==  '__main__':
    F = int(input("insert F parameter:"))
    d = int(input("\ninsert d parameter:"))
    
    images = ["flower_foveon.bmp"] #"hdr.bmp","artificial.bmp","big_building.bmp","big_tree","bridge.bmp","cathedral.bmp","deer.bmp","fireworks.bmp"
    path = 'images/'
    
    for image in images:
        print(image + "\n")
        image = misc.imread(os.path.join(path,image), flatten = 0)
        if (image.ndim >= 3):
            image = image[:,:,0]
        image_compressed = dct_compression(image, F, d)

    
    
    mplp.imshow(image_compressed, cmap='gray')
    
	
    mplp.show()   