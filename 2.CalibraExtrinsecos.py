import cv2
import numpy as np
import pandas as pd

# Variaveis de entrada
intrinsecos = [pd.read_csv('cam0_intrinsecos.csv').to_numpy(),
               pd.read_csv('cam1_intrinsecos.csv').to_numpy()]
dist = [pd.read_csv('cam0_distorcoes.csv').to_numpy(),
        pd.read_csv('cam1_distorcoes.csv').to_numpy()]
tabuleiro = (9,7) # Formato do tabuleiro: (maior,menor)
ncapturas = 15
folder = "img/stereo"
cameras = [0,1]
stereo_flags = cv2.CALIB_FIX_INTRINSIC


# Declara vetor de pontos no tabuleiro (1 casa = unidade)
pts_tabuleiro = np.zeros((1,tabuleiro[0]*tabuleiro[1], 3), np.float32)
pts_tabuleiro[0,:, :2] = np.mgrid[0:tabuleiro[0], 0:tabuleiro[1]].T.reshape(-1,2)
pts_tabuleiro = 22*pts_tabuleiro
# Listas para adicao de pontos identificados nas imagens e pontos de tabuleiro
pts_imagens = [[],[]]
pts_tabuleiros = []

# Loop for itera os indices das imagens
for i in range(ncapturas):
    
    for camera in cameras:
        fname = folder + '/st_cam' + str(camera) + '_'+ str(i) +'.png'
        img = cv2.imread(fname)
        peb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        ret, cantos = cv2.findChessboardCorners(peb, tabuleiro, None)
        
        # Se cantos detectados
        if ret == True:
            
            #pts_tabuleiros.append(pts_tabuleiro)
            pts_imagens[camera].append(cantos)
        
            cv2.drawChessboardCorners(img, tabuleiro, cantos, ret)
            #cv2.imshow('chessboard', img)
            cv2.waitKey(0)
        else:
            print('Padrao nao detectado: ', fname)
    pts_tabuleiros.append(pts_tabuleiro)

# Calibracao estéreo para parametros extrinsecos
ret, k0,d0,k1,d1,R,T,E,F = cv2.stereoCalibrate(
    pts_tabuleiros,
    pts_imagens[0],pts_imagens[1],
    intrinsecos[0], dist[0],
    intrinsecos[1], dist[1],
    peb.shape[::-1],
    stereo_flags)
R = R.get()
T = T.get()
E = E.get()
F = F.get()
# Retificacao

R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(
    intrinsecos[0], dist[0],
    intrinsecos[1], dist[1], peb.shape[::-1], R.T, -T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1)

# Imagens a retificar
leftFrame = cv2.imread(folder + '/st_cam0_0.png')
rightFrame = cv2.imread(folder + '/st_cam1_0.png')

leftMapX, leftMapY = cv2.initUndistortRectifyMap(intrinsecos[0], dist[0], R1, P1, peb.shape[::-1], cv2.CV_32FC1)
left_rectified = cv2.remap(leftFrame, leftMapX, leftMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
rightMapX, rightMapY = cv2.initUndistortRectifyMap(intrinsecos[1], dist[1], R2, P2, peb.shape[::-1], cv2.CV_32FC1)
right_rectified = cv2.remap(rightFrame, rightMapX, rightMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
vis = np.concatenate((right_rectified, left_rectified), axis=1)
cv2.imwrite('Retificados.png', vis)
# Plota resultados
print('Programa Finalizado!')
print('-retval = ', ret)


