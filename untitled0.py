import cv2
import numpy as np
import pandas as pd

folder = 'C:/Users/Rodrigo/Documents/TCC/StereoVision/'
folder2 = 'C:/Users/Rodrigo/Documents/TCC/StereoVision/img'
intrinsecos = [pd.read_csv(folder + 'cam0_intrinsecos.csv').to_numpy(),
               pd.read_csv(folder + 'cam1_intrinsecos.csv').to_numpy()]
dist = [pd.read_csv(folder + 'cam0_distorcoes.csv').to_numpy(),
        pd.read_csv(folder + 'cam1_distorcoes.csv').to_numpy()]

ncapturas = 20
cameras = ['0', '1']
for i in range(ncapturas):
    for camera in cameras:
        fname = folder2 + '/stereo/st_cam' + camera + '_'+ str(i) +'.png'
        print(fname)
        img = cv2.imread(fname)
        
        DIM = (img.shape[1], img.shape[0])
        K = intrinsecos[int(camera)]
        D = dist[int(camera)]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        
        out = folder2 + '/undistort/st_cam' + camera + '_'+ str(i) +'.png'
        
        cv2.imwrite(out, undistorted_img)