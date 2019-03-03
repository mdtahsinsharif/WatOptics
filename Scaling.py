from PictureProcessing import opencv_wrapper as cvw
import matplotlib.image as mpimg
import numpy as np

img = cvw.ImgToNumpy("data/e5_4f.jpg") ## can possibly use cvw.ImgToNumpy
edged = cvw.ProcessImage(img)

cvw.DisplayImage('Final image', img)

# ## ROI 

# ymax, xmax, channels = img.shape ## x --> num columns, y --> num rows 
# p1 = (0, int(ymax)) ## bottom left 
# p2 = (int(xmax/4), int(ymax)) ## top left
# p3 = (0, int((3*ymax)/4)) ## bottom right
# p4 = (int(xmax/4), int((3*ymax)/4)) ## top right 

# v = np.array([[[p1], [p2], [p4], [p3]]])

# mask = np.zeros_like(edged)

# if len(edged.shape) > 2: 
#     channel_count = edged.shape[2]
#     ignore_mask_color = (255,)*channel_count
# else:
#     ignore_mask_color = 255

