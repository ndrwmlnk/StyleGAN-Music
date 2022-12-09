import os
from os.path import isfile, join
import natsort
import cv2
import numpy
 
def nothing(x):
    pass

#Change the folder name if you not used the default settings with gen_featureGrid.py 
image_folder="stylegan3/grid_images/" 
files = [img for img in os.listdir(image_folder) if img.endswith(".png")]
files=natsort.natsorted(files)

images = numpy.empty(len(files), dtype=object)

for n in range(0, len(files)):
  images[n] = cv2.imread( join(image_folder,files[n]) )
 


windowName = 'image'
cv2.namedWindow(windowName)
cv2.createTrackbar('Feature A', windowName, 0, 5, nothing)
cv2.createTrackbar('Feature B', windowName, 0, 5, nothing)
cv2.createTrackbar('Feature C', windowName, 0, 5, nothing)


start=images[0]
i, j, k = 0, 0, 0

img=start

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:   # 27 is Escape
        break
    j = cv2.getTrackbarPos('Feature A',windowName)
    i = cv2.getTrackbarPos('Feature B',windowName)
    k = cv2.getTrackbarPos('Feature C',windowName)

    img=images[(36*i)+(6*j)+k]
    
cv2.destroyAllWindows()


 
