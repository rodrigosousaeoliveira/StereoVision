# Standard imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
im

camera0 = cv2.VideoCapture(0)
camera1 = cv2.VideoCapture(1)
#camera0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#camera0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
intrinsecos = [pd.read_csv('cam0_intrinsecos.csv').to_numpy(),
               pd.read_csv('cam1_intrinsecos.csv').to_numpy()]
dist = [pd.read_csv('cam0_distorcoes.csv').to_numpy(),
        pd.read_csv('cam1_distorcoes.csv').to_numpy()]

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
params.minInertiaRatio = 0.2

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
ptx = []
pty = []

if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)


while(True):
    
    ret0,frame0 = camera0.read()
    ret, frame = camera1.read()
    
    peb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    peb = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect blobs.
    keypoints = detector.detect(peb0)
    keypoints2 = detector.detect(peb)
    
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im1_with_keypoints = cv2.drawKeypoints(frame0, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    im2_with_keypoints = cv2.drawKeypoints(frame, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    pt = cv2.KeyPoint_convert(keypoints)
    
    # Remover distorção dos pontos
    x = cv2.undistortPoints(pt, )
    if len(pt) == 3:
        ptx.append(np.average(pt[:,0]))
        pty.append(np.average(pt[:,1]))
        
    cv2.imshow("Camera 0", im1_with_keypoints)
    cv2.imshow("Camera 1", im2_with_keypoints)
    #cv2.imshow("Camera 0", frame0)
    #cv2.imshow("Camera 1", frame)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera0.release()
camera1.release()
cv2.destroyAllWindows()

plt.plot(ptx,pty)
plt.grid()
plt.show()