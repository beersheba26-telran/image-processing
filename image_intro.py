import numpy as np
import matplotlib.pyplot as plt
# Create image with simple diagonal line
height = 50
width = 50
img = np.full((height, width,3), 255,dtype=np.uint8)
for i in range(min(height, width)):
    img[i, i] = [255, 0, 0]  # White diagonal line
plt.axis('off')  # Hide axes
plt.imshow(img)
plt.show()