import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from operator import xor
from matplotlib import pyplot as plt
import os
from numba import njit
import pydicom
from pydicom.data import get_testdata_files
from numba import jit
#pip install opencv-python pydicom

SZ=90
IN_DIR = 'C:\\_Denis\\dcm1\\'
OUT_DIR = "C:\\_Denis\\out\\"

FALSE_VAL=-2047
TRUE_VAL=0

INNER_FACTOR=1
BORDER_FACTOR=5
OUTER_FACTOR=2

start_xx = 240
start_yy = 240
zona_delta_r = 2
rmin = 12
rmax = 22
outnum=0
def read_dicom(fname):
    dataset = pydicom.dcmread( fname)
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)
    flat = np.array(dataset.pixel_array.flat)
    TR1=1900
    TR2=2250

    mn = -2047
    mx = 2047
    wl=0
    ww=20
    flat[flat <= wl - ww/2] = mn
    flat[flat >= wl + ww/2] = mx

    for i,value in enumerate(flat):
        if value <= wl - ww/2:
            flat[i] = FALSE_VAL
        elif value >= wl + ww/2:
            flat[i] = TRUE_VAL
        else:
            flat[i] = TRUE_VAL


    # flat += 2048
    # flat[flat<TR1]=0
    # flat[flat>TR2]=0
    # flat -= TR1
    mid = (TR2 - TR1)/2
    # for i,value in enumerate(flat):
    #     if value<mid:
    #         flat[i] = value *0.1
    #     else:
    #         flat[i] = value



    res=flat.reshape([cols, rows])

    res = res[start_yy:start_yy + SZ, start_xx:start_xx + SZ]
    # largest_idx = largest_indices(res, 5)
    # for i in range(5):
    #     print( str( largest_idx[0][i] )+' '+str(largest_idx[1][i])+'='+str(res[largest_idx[0][i]][largest_idx[1][i]]))




    return res

def largest_indices(ary, n):
    """Returns the n largest indices from a numpy array."""
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return np.unravel_index(indices, ary.shape)

def FIND_CIRCLE(jpeg_name, outprefix):
    # arr = np.zeros([SZ, SZ], np.int8)
    fname=jpeg_name #"IMG-0001-00027.jpg"
    image = read_dicom(IN_DIR+fname)
    arr = image
    # plt.imshow(image, cmap='gray')
    # plt.show()
    # plt.close()

    # wx = SZ
    # wy = SZ
    # img = image[start_yy:start_yy + wy, start_xx:start_xx + wx]
    # img[img > 200] = 0
    # edges =  cv2.Canny(img, 100, 400, 1)
    img_out = image.copy()

    haugh=np.zeros([SZ,SZ,100] , np.float)

    @jit
    def score(center_x,center_y,radii, delta_radii):
        result=0
        total_count=0
        max_r = radii+2*delta_radii

        radii2 = radii * radii

        if center_x-max_r <0: return 0
        if center_y-max_r <0: return 0
        if center_x+max_r >=SZ: return 0
        if center_y+max_r >=SZ: return 0

        # if center_x == 62 and center_y == 30:
        #     print(123)

        for x in range(center_x-max_r,center_x+max_r+1):
            for y in range(center_y-max_r,center_y+max_r+1):
                r2 =   (x-center_x)*(x-center_x) + (y-center_y)*(y-center_y)
                if(r2<radii2):
                    total_count+=1
                    if(arr[x][y]==TRUE_VAL):
                        result+=INNER_FACTOR
                if(r2 > (radii+delta_radii)*(radii+delta_radii) and r2 <= (radii+2*delta_radii)*(radii+2*delta_radii)):
                    total_count += 1
                    if(arr[x][y]==FALSE_VAL):
                        result+=OUTER_FACTOR


                # 8 neibour [+1 0 1]X[+1 0 1]
                true_val_count =0
                false_val_count =0
                border_count = 0
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        r2 = (x+dx - center_x) * (x+dx - center_x) + (y+dy - center_y) * (y+dy - center_y)
                        if(r2>=radii2 and r2<=(radii+delta_radii)*(radii+delta_radii)):
                            border_count += 1
                            if(arr[x+dx][y+dy]==TRUE_VAL):
                                true_val_count+=1
                            if(arr[x+dx][y+dy]==FALSE_VAL):
                                false_val_count+=1
                border_rate =  BORDER_FACTOR*(border_count-abs(false_val_count-true_val_count))/( 1 + abs(false_val_count-true_val_count))

                total_count+=1
                result+=border_rate
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



    def drw_circle(img,xx,yy,rr,clr):
        res=img.copy()
        r1 = np.random.sample()+0.7
        r2 = np.random.sample()+0.7
        r3 = np.random.sample()+0.7

        for x in range(SZ):
            for y in range(SZ):
                if (x - xx) ** 2 + (y - yy) ** 2 <= rr ** 2 :
                    res[x][y] =500 # img_out[x][y]+300
                    # img_out[x][y] = min(30+int(r1*img_out[x][y][0] ), 255)
                    # img_out[x][y] = min(30+int(r2*img_out[x][y][1] ), 255)
                    # img_out[x][y][2] = min(30+int(r3*img_out[x][y][2] ), 255)
        return res




    largest_index =  largest_indices(haugh, 20)
    print(largest_index)
    fig = plt.figure(figsize=(10, 10))

    fig.add_subplot(4, 4, 1)
    plt.imshow(image, cmap='gray')

    for i in range(15):
        x=largest_index[0][i]
        y=largest_index[1][i]
        r=largest_index[2][i]
        fig.add_subplot(4, 4, 2+ i)
        plt.imshow(drw_circle(img_out,x,y,r+1 , 100), cmap='gray')


    # x_score =max_score[0][0]
    # y_score =max_score[1][0]
    # r_score =max_score[2][0]

    # drw_circle(x_score,y_score,r_score,200)
    #plt.imshow(img)
    #plt.show()



    ##

    # fig.add_subplot(2, 2, 2)
    # plt.imshow(edges, cmap='gray')

    # fig.add_subplot(2, 2, 3)
    # plt.imshow(img_out, cmap='gray')
    # plt.title(f'r={r_score} {x_score},{y_score}')

    plt.savefig(OUT_DIR  + outprefix + fname+".png")
    #plt.show()
    plt.close()



def main():
    files = os.listdir(IN_DIR)
    outprefix=0
    for f in files:
        print(f)
        outprefix+=1
        if f.find('.dcm')>=0:
            FIND_CIRCLE(f,'out'+str(outprefix)+'_')

main()
#FIND_CIRCLE('IMG-0001-00031.jpg')
#read_dicom('1.2.392.200036.9116.2.6.1.48.1214242851.1571977503.267444.dcm')
#read_dicom('I:\\КТ для нейросети норма\\Брюшная полость\\1-50\\6\\1.2.392.200036.9116.2.6.1.48.1214242851.1572235470.185170.dcm')