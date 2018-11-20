import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('tiny_img.jpg',0)
# print(img)
# img2 = cv2.imread('dc_3rd.JPG',150)

# blurred = cv2.GaussianBlur(img,(5,5),0)
laplacian = cv2.Laplacian(img,cv2.CV_64F)

newlaplacian = laplacian
for i in range(len(laplacian)):
    for j in range(len(laplacian)):
        if laplacian[i][j] <= 60: #found this number by trial and error, need to find a way to do this for all maps
            newlaplacian[i][j] = 1
        else:
            newlaplacian[i][j] = 0

# for i in range(len(laplacian)):
#     print(laplacian[i])


plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original E5'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian E5'), plt.xticks([]), plt.yticks([])

plt.show()