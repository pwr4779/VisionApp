import errno
from random import randint

import matplotlib
import numpy as np
import os
import glob
import cv2

def targetPixelList(image):
    x = len(image[0])
    y = len(image)
    pointlist = []
    for i in range(y):
        for j in range(x):
            if(image[i][j] < 100):
                pointlist.append([i,j])
    return pointlist


def createPointLabel(TPL, image):
    y = len(image)
    x = len(image[0])
    patch = np.zeros((y,x))
    # pointpatch = pointPatch
    temp = np.full(( 21 , 21 ), 255 )
    if(len(TPL)>0):
        index = randint(0,len(TPL)-1)
        kernel1d = cv2.getGaussianKernel(21, 5)
        kernel2d = np.outer(kernel1d, kernel1d.transpose())

        gaussianPath = temp * kernel2d
        k = 255 / gaussianPath[10][10]
        gaussianPath = k*gaussianPath
        patchY = TPL[index][0]
        patchX = TPL[index][1]
        for j in range(patchY-10, patchY+11):
            for k in range(patchX-10, patchX+11):
                if(j<0 or k<0 or j > y-1 or k>x-1):
                    continue
                patch[j][k] = gaussianPath[j-(patchY-10)][k-(patchX-10)]
    return patch


if __name__ == "__main__":
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_ 0"] = "4"
    maskdirNames = '/home/su_j615/out_focusing/trainmasks'
    # maskdirNames = '/home/su_j615/out_focusing/valmasks'
    dirName = glob.glob(maskdirNames + "/*")
    k=0
    for j in range(len(dirName)):
        fileNames = glob.glob(dirName[j] + "/*")
        print(len(fileNames))
        for i in range(len(fileNames)):
            # print(str(i))
            image = cv2.imread(fileNames[i], cv2.IMREAD_GRAYSCALE)
            print(fileNames[i])
            TPL = targetPixelList(image)
            patch = createPointLabel(TPL, image)
            dirpath = dirName[j].replace('trainmasks', 'trainbackpoints') + '/point' + str(k)
            # dirpath = dirName[j].replace('valmasks', 'valbackpoints') + '/point' + str(k)
            print(dirpath)
            if not (os.path.isdir(dirpath)):
                os.makedirs(os.path.join(dirpath))
            path = fileNames[i][fileNames[i].rfind('/') + 1:]
            path = dirpath + '/' + path
            print(path)
            cv2.imwrite(path, patch)


