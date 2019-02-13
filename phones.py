import cv2
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np 

matplotlib.use('Qt5Cairo')


def get_rois(mask, min_size=10, min_mass=5, box_scale=4):
    """Extract foreground blobs."""
    rois = []
    centroids = []
    masses = []
    boxes = []
    comps = cv2.connectedComponentsWithStats(mask.astype('uint8'))[2]
    # drop biggest component (the background)
    filtered = np.where(comps[:, 4] != comps[:, 4].max())
    comps = comps[filtered]
    # extract regions of interest
    for i in range(comps.shape[0]):
        x_from = comps[i, 0]
        x_to = comps[i, 2] + x_from
        y_from = comps[i, 1]
        y_to = comps[i, 3] + y_from
        if (comps[i, 2] < min_size) or (comps[i, 3] < min_size):
        	continue
        rois.append(mask[y_from:y_to, x_from:x_to])
        centroids.append((np.mean([x_from, x_to]), np.mean([y_from, y_to])))
        masses.append(mask[y_from:y_to, x_from:x_to].sum())
        boxes.append(((x_from - box_scale, x_to + box_scale), (y_from - box_scale, y_to + box_scale)))
    return rois, centroids, masses, boxes


image = cv2.cvtColor(cv2.imread('phones.jpg'), cv2.COLOR_BGR2RGB)
nth_percentile = .8
# 'brightness' of image
b_im = image.sum(2)

# find some threshold
sorted = np.sort(b_im.reshape(1,-1).squeeze())
normed_cumsum = np.cumsum(sorted) / sorted.sum()
idx = np.where(normed_cumsum > nth_percentile)[0][0]# nth percentile with respect to brightness
t = sorted[idx]

# thresholded image
t_im = b_im.copy()
t_im[t_im <= t] = 0
t_im[t_im > 0] = 1
t_im = t_im.astype('uint8')

# get connected regions
rois, centroids, masses, boxes = get_rois(t_im, min_mass=100)

print("Found {} phones".format(len(boxes)))

# print 
plt.imshow(image)
for box in boxes:
	x = box[0]
	y = box[1]
	plt.plot([x[0], x[1], x[1], x[0], x[0]],
			 [y[0], y[0], y[1], y[1], y[0]],
			 'r')

plt.show()