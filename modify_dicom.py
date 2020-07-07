# authors : Guillaume Lemaitre <g.lemaitre58@gmail.com>
# license : MIT

import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

files = os.listdir("C:\\_Denis\\dcm1\\")
for f in files:
    #print(f)

    #filename = get_testdata_files('CT_small.dcm')[0]

    filename = 'C:\\_Denis\\dcm1\\'+f
    dataset = pydicom.dcmread(filename)

    # Normal mode:
    #print()
    #print("Filename.........:", filename)
    #print("Storage type.....:", dataset.SOPClassUID)
    #print()

    pat_name = dataset.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    #print("Patient's name...:", display_name)
    #print("Patient id.......:", dataset.PatientID)
    #print("Modality.........:", dataset.Modality)
    #print("Study Date.......:", dataset.StudyDate)
    #myprint(dataset)
    if 'PixelData' in dataset:
        rows = int(dataset.Rows)
        cols = int(dataset.Columns)
        #print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
        #    rows=rows, cols=cols, size=len(dataset.PixelData)))
        #print(dataset.pixel_array[111])
        #for n,val in enumerate(dataset.pixel_array.flat): # example: zero anything < 300
        #    if n<10000:
        for x in range(100):
            for y in range(100):
                dataset.pixel_array.flat[(100+y)*rows+(100+x)]=-500+10*x+y*10
        dataset.PixelData = dataset.pixel_array.tostring()
        dataset.save_as("C:\\_Denis\\dcm2\\"+f)    
        #ar = np.array(dataset.pixel_array)
        #ar += 2048
        
        #print(ar.min() )
        #print(ar.max() )
        #if 'PixelSpacing' in dataset:
        #    print("Pixel spacing....:", dataset.PixelSpacing)

    # use .get() if not sure the item exists, and want a default value if missing
    #print("Slice location...:", dataset.get('SliceLocation', "(missing)"))

    # plot the image using matplotlib
        #plt.imshow(ar, cmap='gray')
        #plt.show()
