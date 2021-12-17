# Standard imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

folder = 'C:\\Users\\Rodrigo\\Documents\\TCC\\StereoVision\\'
intrinsecos = [pd.read_csv(folder + 'cam0_intrinsecos.csv').to_numpy(),
               pd.read_csv(folder + 'cam1_intrinsecos.csv').to_numpy()]
dist = [pd.read_csv(folder + 'cam0_distorcoes.csv').to_numpy(),
        pd.read_csv(folder + 'cam1_distorcoes.csv').to_numpy()]


P1 = np.array([[607.959,0,604.688,0],
      [0,607.959,407.037,0],
      [0,0,1,0]]) 
P2 = np.array([[607.959, 0,604.688,-105117],
              [0,607.959,407.037,0],
              [0, 0, 1, 0]])


mtx = intrinsecos[0]
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 200;

# Filter by Area.
params.filterByArea = True
params.minArea = 100

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.5

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.4

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
ptx = []
pty = []
x0 = []

if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)

    
frame0 = cv2.imread('st_cam0_0.png')
frame = cv2.imread('st_cam1_0.png')

peb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
peb = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect blobs.
keypoints = detector.detect(peb0)
keypoints2 = detector.detect(peb)



pts0 = cv2.KeyPoint_convert(keypoints)[:3,:].reshape((3,1,2))
pts1 = cv2.KeyPoint_convert(keypoints2)[:3,:].reshape((3,1,2))

# Remover distorção dos pontos
pts0u = cv2.undistortPoints(pts0, np.float32(intrinsecos[0]), np.float32(dist[0]))
pts1u = cv2.undistortPoints(pts1, np.float32(intrinsecos[1]), np.float32(dist[1]))
# Triangulacao
triang = cv2.triangulatePoints(P1, P2, pts0u, pts1u)

vec0 = triang[0,:]
dist = []
for vec in triang:
    dist.append(np.linalg.norm(vec-vec0))
    vec0 =  vec
#Plot
ax.scatter(triang[0,:], triang[1,:], triang[2,:])

# Draw detected blobs as red circles.
im1_with_keypoints = cv2.drawKeypoints(frame0, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
im2_with_keypoints = cv2.drawKeypoints(frame, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# =============================================================================
# cv2.imshow("Camera 0", im1_with_keypoints)
# cv2.imshow("Camera 1", im2_with_keypoints)
# cv2.waitKey(0)
# =============================================================================

plt.plot(ptx,pty)
plt.grid()
plt.show()