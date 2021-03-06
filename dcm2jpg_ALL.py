# -*- coding: utf-8 -*-

import pydicom as dicom
import pathlib
import os
import cv2
import PIL # optional
from numba import jit
path=u"I:\\Tomography\\set1"

#
for curdir, subdirs, files in os.walk(path):
    outdir = curdir.replace("I:","C:\\_Denis\\MarkSet1v2")
    print(outdir)
    for n, image_name in enumerate(files):
        if image_name.find('.dcm')>=0:
            try:
                ds = dicom.dcmread(os.path.join(curdir, image_name))

                pixel_array_numpy = ds.pixel_array

                print(pixel_array_numpy.min())
                print(pixel_array_numpy.max())
                if curdir.find('-h')>-1:
                    pixel_array_numpy-=910
                else:
                    pixel_array_numpy+=70

                out_image_name = image_name.replace('.dcm', '.jpg')
                print(outdir +' '+out_image_name)

                pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
                out_full_name = os.path.join(outdir, out_image_name)
                #out_full_name = os.path.join("C:\\_Denis\\DCM2JPG", out_image_name)
                if not cv2.imwrite(out_full_name, pixel_array_numpy):
                    raise Exception("Could not write image")

            except Exception as e:
                print(str(e))
