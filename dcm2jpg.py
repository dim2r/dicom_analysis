import pydicom as dicom
import os
import cv2
import PIL # optional
# make it True if you want in PNG format
PNG = True
# Specify the .dcm folder path
folder_path = "C:\\_Denis\\dcm1\\"
# Specify the output jpg/png folder path
jpg_folder_path = "C:\\_Denis\\out"


images_path = os.listdir(folder_path)
for n, image in enumerate(images_path):
    ds = dicom.dcmread(os.path.join(folder_path, image))
    pixel_array_numpy = ds.pixel_array
    pixel_array_numpy+=200
    print(pixel_array_numpy.shape)
    if PNG == False:
        image = image.replace('.dcm', '.jpg')
    else:
        image = image.replace('.dcm', '.png')
    cv2.imwrite(os.path.join(jpg_folder_path, image), pixel_array_numpy)
    if n % 50 == 0:
        print('{} image converted'.format(n))