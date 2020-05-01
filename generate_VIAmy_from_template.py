import pathlib
import os
import array

path=u".\\"

file_list = list()
#
for curdir, subdirs, files in os.walk(path):
	for n, image_name in enumerate(files):
		if image_name.find('.jpg')>=0:
			s=os.path.join(curdir, image_name)
			s=s.replace('\\','\\\\')
			#print(',"file:'+s+'"')
			file_list.append('"file:'+s+'"')



f = open('C:\\_Denis\\dicom_analysis\\via_MY_Template.html', "r")
lines = f.readlines()
f.close()



f = open('via_my.html', 'w')


writing_list=False
for line in lines:
	if not writing_list:
		f.write(line)
	if line.find("var _via_demo_wikimedia_commons_featured_img_list = [")>-1:
		writing_list=True
		f.write('\n,'.join(file_list))
	if  writing_list and line.find("]")>-1:
		writing_list=False
		f.write(line)

f.close()