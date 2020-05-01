from PIL import Image
import os
import sys
import pathlib

in_path= u"C:\\_Denis\\train_data\\MarkSet2_original"
out_path = in_path.replace('_original', '_augment')

for curdir, subdirs, files in os.walk(in_path):

    for n, image_name in enumerate(files):
        _, ext = os.path.splitext(image_name)

        outdir = curdir.replace(in_path, out_path)
        if ext=='.jpg' or  ext=='.gif' or  ext=='.png':
            ff1=outdir +'\\r3.'+image_name
            ff2=outdir +'\\r-3.'+image_name

            if not os.path.isfile(ff1) or not  os.path.isfile(ff2) :
                pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
                print(f'{outdir} {image_name}')
                colorImage = Image.open(curdir+'\\'+image_name)
                rotated = colorImage.rotate(3)
                rotated.save( ff1)
                rotated = colorImage.rotate(-3)
                rotated.save( ff2 )

            # mode = colorImage.mode
            # if len(mode) == 1:  # L, 1
            #     new_background = (255)
            # if len(mode) == 3:  # RGB
            #     new_background = (255, 255, 255)
            # if len(mode) == 4:  # RGBA, CMYK
            #     new_background = (255, 255, 255, 255)

            # img1 = colorImage.resize((512, 462), Image.ANTIALIAS)
            # newImage = Image.new(mode, (512, 512), new_background)
            # newImage.paste(img1, (0, 0, 511, 461))
            # newImage.save(outdir +'\\s.'+image_name)




