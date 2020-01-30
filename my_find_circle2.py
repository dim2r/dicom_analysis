import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from operator import xor
from matplotlib import pyplot as plt
import os
from numba import njit
''' read .jpg
    extract countours
    find circle
'''
SZ=90
IN_DIR = 'C:\\_Denis\\img\\'
OUT_DIR = "C:\\_Denis\\out\\"

start_xx = 240
start_yy = 240
zona_delta_r = 1
rmin = 12
rmax = 19


def largest_indices(ary, n):
    """Returns the n largest indices from a numpy array."""
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return np.unravel_index(indices, ary.shape)

def FIND_CIRCLE(jpeg_name):
    arr = np.zeros([SZ, SZ], np.int8)
    fname=jpeg_name #"IMG-0001-00027.jpg"
    image = cv2.imread(IN_DIR+fname)

    wx = SZ
    wy = SZ
    img = image[start_yy:start_yy + wy, start_xx:start_xx + wx]
    img[img > 200] = 0
    edges =  cv2.Canny(img, 100, 400, 1)
    img_out = img.copy()


    for x in range(SZ):
        for y in range(SZ):
            if edges[x,y]>111:
                arr[x][y]=100
    #plt.imshow(arr)
    #plt.show()


    haugh=np.zeros([SZ,SZ,100] , np.float)

    def score(center_x,center_y,radii, delta_radii):
        result=0
        total_count=0
        max_r = radii+2*delta_radii
        if center_x-max_r <0: return 0
        if center_y-max_r <0: return 0
        if center_x+max_r >=SZ: return 0
        if center_y+max_r >=SZ: return 0

        for x in range(center_x-max_r,center_x+max_r+1):
            for y in range(center_y-max_r,center_y+max_r+1):
                r2 =   (x-center_x)*(x-center_x) + (y-center_y)*(y-center_y)
                radii2=radii*radii

                if(r2<radii2):
                    total_count+=1
                    if(arr[x][y]==0):
                        result+=1
                if(r2>(radii+delta_radii)*(radii+delta_radii) and r2<=(radii+2*delta_radii)*(radii+2*delta_radii)):
                    total_count += 1
                    if(arr[x][y]==0):
                        result+=1


                # 8 neibour [+1 0 1]X[+1 0 1]
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        r2 = (x+dx - center_x) * (x+dx - center_x) + (y+dy - center_y) * (y+dy - center_y)
                        if(r2>=radii2 and r2<=(radii+delta_radii)*(radii+delta_radii)):
                            total_count += 1
                            if(arr[x+dx][y+dy]==100):
                                result+=1
                #OK!
                #if(r2>=radii2 and r2<=(radii+delta_radii)*(radii+delta_radii)):
                #    total_count += 5
                #    if(arr[x][y]==100):
                #        result+=5


        return result/total_count


    for r in range(rmin, rmax + 1):
        print(f'\nr={r}')
        for x in range(r, SZ-r):
            print('.', end='')
            for y in range(r, SZ-r):
                haugh[x,y,r] = score(x,y,r,zona_delta_r)

    haugh_max=haugh.max()
    max_score = np.where(haugh == haugh_max)
    print(f'haugh_max={haugh_max}')
    print(max_score)


    largest_index =  largest_indices(haugh, 20)


    def drw_circle(xx,yy,rr,clr):
        r1 = np.random.sample()+0.7
        r2 = np.random.sample()+0.7
        r3 = np.random.sample()+0.7

        for x in range(SZ):
            for y in range(SZ):
                if (x - xx) ** 2 + (y - yy) ** 2 <= rr ** 2:
                    #arr[x][y] = xor(clr,arr[x][y])
                    img_out[x][y][0] = min(30+int(r1*img_out[x][y][0] ), 255)
                    img_out[x][y][1] = min(30+int(r2*img_out[x][y][1] ), 255)
                    img_out[x][y][2] = min(30+int(r3*img_out[x][y][2] ), 255)

    print(largest_index)
    for i in range(20):
        x=largest_index[0][i]
        y=largest_index[1][i]
        r=largest_index[2][i]
        drw_circle(x,y,r , 100)

    x_score =max_score[0][0]
    y_score =max_score[1][0]
    r_score =max_score[2][0]
    drw_circle(x_score,y_score,r_score,200)
    #plt.imshow(img)
    #plt.show()



    ##
    fig = plt.figure(figsize=(10, 10))
    fig.add_subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')

    fig.add_subplot(2, 2, 2)
    plt.imshow(edges, cmap='gray')

    fig.add_subplot(2, 2, 3)
    plt.imshow(img_out)
    plt.title(f'r={r_score} {x_score},{y_score}')
    plt.savefig(OUT_DIR  + 'out' + fname)
    #plt.show()
    plt.close()



def main():
    files = os.listdir(IN_DIR)
    for f in files:
        print(f)
        if f.find('IMG')==0:
            FIND_CIRCLE(f)


#main()
FIND_CIRCLE('IMG-0001-00031.jpg')