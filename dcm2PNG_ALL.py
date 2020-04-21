# -*- coding: utf-8 -*-

import pydicom as dicom
import pathlib
import os
import numpy as np
import cv2
import PIL # optional
from numba import jit
from PIL import Image
from numba import jit


# path=u"I:\\Tomography\\set1"
path=u"I:\\Tomography\\set2"

#C:\_Denis\train_data\MarkSet1v2_original\set1
for curdir, subdirs, files in os.walk(path):
    # outdir = curdir.replace("I:\\Tomography","C:\\_Denis\\train_data\\MarkSet1v2_original")
    outdir = curdir.replace("I:\\Tomography","C:\\_Denis\\train_data\\MarkSet2_original")
    print(outdir)
    for n, image_name in enumerate(files):
        if image_name.find('.dcm')>=0:
            try:
                ds = dicom.dcmread(os.path.join(curdir, image_name))
                pixel_array_numpy = ds.pixel_array
                pixel_array_numpy += 2048
                pixel_array_numpy <<= 3
                pixel_array_numpy = pixel_array_numpy.astype(np.uint32)
                out_image_name = image_name.replace('.dcm', '.png')
                print(outdir +' '+out_image_name)

                pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
                out_full_name = os.path.join(outdir, out_image_name)
                im = Image.fromarray(pixel_array_numpy)  # or more verbose as Image.fromarray(ar32, 'I')
                im.save(out_full_name)

                #out_full_name = os.path.join("C:\\_Denis\\DCM2JPG", out_image_name)
                # if not cv2.imwrite(out_full_name, pixel_array_numpy):
                #     raise Exception("Could not write image")

            except Exception as e:
                print(str(e))
