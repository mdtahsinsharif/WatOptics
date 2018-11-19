import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('pic.JPG',0)
edges = cv2.Canny(img,100,200)
img2 = cv2.imread('dc_3rd.JPG',0)
edges2 = cv2.Canny(img2,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original E5'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Canny E5'), plt.xticks([]), plt.yticks([])

# plt.subplot(123),plt.imshow(edges2,cmap = 'gray')
# plt.title('Canny DC'), plt.xticks([]), plt.yticks([])

plt.show()