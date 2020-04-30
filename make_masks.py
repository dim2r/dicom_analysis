import json
import numpy as np
import math

import pydicom
import os.path
from PIL import Image, ImageDraw
import sys

#{
#"file:.\\set1\\abdomen\\1\\1.2.392.200036.9116.2.6.1.48.1214242851.1571977503.267444.jpg-1":
#
#{"filename":"file:.\\set1\\abdomen\\1\\1.2.392.200036.9116.2.6.1.48.1214242851.1571977503.267444.jpg","size":-1,
#"regions":[{"shape_attributes":{"name":"circle","cx":272,"cy":306,"r":15.506},"region_attributes":{}}],"file_attributes":{}
#},


# with open('via_export_json_final_set1.json', 'r') as f:
# with open('via_export_json_set2_up_to_12000.json', 'r') as f:
with open('via_export_json_set2_12-24-.json', 'r') as f:
    loaded_json = json.load(f)

i=0
saved=0
for jkey in loaded_json:
	#print(x)
	regions=loaded_json[jkey]['regions']
	filename=loaded_json[jkey]['filename']

	# in_file = filename.replace('file:.','C:\\_Denis\\MarkSet1')
	# out_file = filename.replace('file:.','C:\\_Denis\\train_data\\MarkSet1_original').replace('.jpg','.gif')
	in_file = filename.replace('file:.','C:\\_Denis\\MarkSet2')
	out_file = filename.replace('file:.','C:\\_Denis\\train_data\\MarkSet2_original').replace('.jpg','.gif')

	img2 = Image.new('RGB', (512,512), "black")  # create a new black image
	pixels2 = img2.load()  # create the pixel map
	need_save = False
	for region in regions:
		name = region['shape_attributes']['name']
		if name == 'polyline' or name=='polygon':
			xxx=region['shape_attributes']['all_points_x']
			yyy=region['shape_attributes']['all_points_y']
			xxyy=list(zip(xxx,yyy))
			drw = ImageDraw.Draw(img2)
			drw.polygon(xxyy, fill="white", outline="black")
			# img2.show()
			print('polyline')
			need_save=True

		if name == 'Xcircle':
			cx = region['shape_attributes']['cx']
			cy = region['shape_attributes']['cy']
			radii = int(round(region['shape_attributes']['r']))

			need_save = True
			for xx in range(-radii, +radii + 1):
				for yy in range(-radii, +radii + 1):
					if (xx * xx) + (yy * yy) <= radii * radii:
						pixels2[xx+cx, yy+cy] = (255, 255, 255)  # set the colour accordingly

		if name == 'Xellipse':
			def drawEllipse(cx, cy, wx, wy, theta):
				# print('drawEllipse '+str(cx)+','+str(cy)+','+str(rx)+','+str(ry)+','+str(theta) )
				# theta = np.radians(30)
				c, s = np.cos(theta), np.sin(theta)
				R = np.array(((c, -s), (s, c)))
				dim =math.ceil( 2 * max(wx, wy) )
				for x in range(-dim, dim):
					for y in range(-dim, dim):
						x1 = x / dim
						y1 = y / dim
						if (x1 * x1 + y1 * y1 <= 1):
							xx = x1 * wx
							yy = y1 * wy

							out = R.dot([xx, yy])
							# draw.point((cx + out[0], cy + out[1]), 'blue')
							pixels2[ int(cx + out[0]), int(cy + out[1])] = (255, 255, 255)

			cx = region['shape_attributes']['cx']
			cy = region['shape_attributes']['cy']
			rx = region['shape_attributes']['rx']
			ry = region['shape_attributes']['ry']
			theta = region['shape_attributes']['theta']
			need_save = True
			drawEllipse(cx,cy, rx,ry,theta)



	if need_save:
		try:
			img2.save(out_file)
		except Exception as e:
			print(str(e))
		saved+=1
		print(out_file)
		print(saved)
	else:
		# print ("skip "+out_file)
		pass