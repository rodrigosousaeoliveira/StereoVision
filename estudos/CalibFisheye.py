import cv2
import numpy as np
import pandas as pd

# Variaveis de entrada
tabuleiro = (9,7) # Formato do tabuleiro: (maior,menor)
camera = "0" # Camera a calibrar: 0 ou 1
ncapturas = 20
folder = "calib"
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW

# Declara vetor de pontos no tabuleiro (1 casa = unidade)
pts_tabuleiro = np.zeros((1,tabuleiro[0]*tabuleiro[1], 3), np.float32)
pts_tabuleiro[0,:, :2] = np.mgrid[0:tabuleiro[0], 0:tabuleiro[1]].T.reshape(-1,2)
pts_tabuleiro = 22*pts_tabuleiro
# Listas para adicao de pontos identificados nas imagens e pontos de tabuleiro
pts_imagens = []
pts_tabuleiros = []

# Loop for itera os indices das imagens
for i in range(ncapturas):
    
    fname = folder + '/cam' + camera + '_'+ str(i) +'.png'
    img = cv2.imread(fname)
    peb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, cantos = cv2.findChessboardCorners(peb, tabuleiro, None)
    
    # Se cantos detectados
    if ret == True:
        
        pts_tabuleiros.append(pts_tabuleiro)
        pts_imagens.append(cantos)
    
        cv2.drawChessboardCorners(img, tabuleiro, cantos, ret)
    else:
        print('Padrao nao detectado: ', fname)
    """
    cv2.imshow(fname,img)
    cv2.waitKey(0)
    
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(pts_tabuleiros, pts_imagens
                                                  , peb.shape[::-1], None, None)
    """
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(ncapturas)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(ncapturas)]
retval, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    pts_tabuleiros,
    pts_imagens,
    peb.shape[::-1],
    K,
    D,
    rvecs,
    tvecs,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6))

img = cv2.imread(folder + '/cam1_14.png')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, (w,h), 1, (w,h))

DIM = (img.shape[1], img.shape[0])
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
"""
# undistort
undistorted_img = cv2.undistort(img, K, D, None, K)
# crop the image
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
"""
cv2.imwrite('calibresult.png', undistorted_img)

# Exporta par??metros para arquivo CSV
mtxSaida = pd.DataFrame(K)
mtxSaida.to_csv('cam'+str(camera)+'_intrinsecos.csv', index = False)
distSaida = pd.DataFrame(D)
distSaida.to_csv('cam'+str(camera)+'_distorcoes.csv', index = False)

