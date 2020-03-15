import json
import pydicom
#{
#"file:.\\set1\\abdomen\\1\\1.2.392.200036.9116.2.6.1.48.1214242851.1571977503.267444.jpg-1":
#
#{"filename":"file:.\\set1\\abdomen\\1\\1.2.392.200036.9116.2.6.1.48.1214242851.1571977503.267444.jpg","size":-1,
#"regions":[{"shape_attributes":{"name":"circle","cx":272,"cy":306,"r":15.506},"region_attributes":{}}],"file_attributes":{}
#},


with open('via_export_json_try1.json', 'r') as f:
    loaded_json = json.load(f)

i=0
for jkey in loaded_json:
	#print(x)
	regions=loaded_json[jkey]['regions']
	filename=loaded_json[jkey]['filename']
	in_file = filename.replace('file:.\\set1\\abdomen\\1\\','..\\dcm1\\').replace('.jpg','.dcm')
	out_file= filename.replace('file:.\\set1\\abdomen\\1\\','..\\dcm2\\').replace('.jpg','.dcm')
	dataset = pydicom.dcmread(in_file)
	#print(loaded_json[x]['regions'])
	if 'PixelData' in dataset:
		rows = int(dataset.Rows)
		cols = int(dataset.Columns)
		for region in regions:
			cx=region['shape_attributes']['cx']
			cy=region['shape_attributes']['cy']
			radii = int( round( region['shape_attributes']['r'] ) )
			for xx in range(-radii,	+radii+1):
				for yy in range(-radii,	+radii+1):
					if (xx*xx)+(yy*yy)<=radii*radii:
						dataset.pixel_array.flat[(yy + cy) * rows + (xx + cx)] = 600
		dataset.PixelData = dataset.pixel_array.tostring()
		dataset.save_as(out_file)
	i+=1
	if i>55:
		break