import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('pic.JPG',0)
img2 = cv2.imread('dc_3rd.JPG',0)

laplacian = cv2.Laplacian(img,cv2.CV_64F)
laplacian2 = cv2.Laplacian(img2,cv2.CV_64F)

#sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
#sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original E5'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian E5'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(img2,cmap = 'gray')
plt.title('Original DC'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(laplacian2,cmap = 'gray')
plt.title('Laplacian DC'), plt.xticks([]), plt.yticks([])
#plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
#plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
#plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
#plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

#for i in range(len(sobelx)):
#    print(laplacian[i][0], laplacian[i][1])

plt.show()