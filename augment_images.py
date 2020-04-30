from PIL import Image
import os
import sys
import pathlib

path=u"C:\\_Denis\\train_data\\MarkSet2_original"
outdir_ = path+"_augment"

for curdir, subdirs, files in os.walk(path):

    for n, image_name in enumerate(files):
        _, ext = os.path.splitext(image_name)

        outdir = curdir.replace(path,outdir_)
        if ext=='.jpg' or  ext=='.gif' or  ext=='.png':
            pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
            print(f'{outdir} {image_name}')
            colorImage = Image.open(curdir+'\\'+image_name)
            rotated = colorImage.rotate(3)
            rotated.save(outdir +'\\r3.'+image_name )
            rotated = colorImage.rotate(-3)
            rotated.save(outdir +'\\r-3.'+image_name )

            mode = colorImage.mode
            if len(mode) == 1:  # L, 1
                new_background = (255)
            if len(mode) == 3:  # RGB
                new_background = (255, 255, 255)
            if len(mode) == 4:  # RGBA, CMYK
                new_background = (255, 255, 255, 255)

            # img1 = colorImage.resize((512, 462), Image.ANTIALIAS)
            # newImage = Image.new(mode, (512, 512), new_background)
            # newImage.paste(img1, (0, 0, 511, 461))
            # newImage.save(outdir +'\\s.'+image_name)




