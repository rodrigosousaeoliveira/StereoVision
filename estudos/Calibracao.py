import cv2
import numpy as np

# Variaveis de entrada
tabuleiro = (9,7) # Formato do tabuleiro: (maior,menor)
camera = "1" # Camera a calibrar: 0 ou 1

# Declara vetor de pontos no tabuleiro (1 casa = unidade)
pts_tabuleiro = np.zeros((tabuleiro[0]*tabuleiro[1], 3), np.float32)
pts_tabuleiro[:, :2] = np.mgrid[0:tabuleiro[0], 0:tabuleiro[1]].T.reshape(-1,2)

# Listas para adicao de pontos identificados nas imagens e pontos de tabuleiro
pts_imagens = []
pts_tabuleiros = []

# Loop for itera os indices das imagens
for i in range(10):
    
    fname = 'cam' + camera + '_'+ str(i) +'.png'
    img = cv2.imread(fname)
    peb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, cantos = cv2.findChessboardCorners(peb, tabuleiro, None)
    
    # Se cantos detectados
    if ret == True:
        
        pts_tabuleiros.append(pts_tabuleiro)
        pts_imagens.append(cantos)
    
        cv2.drawChessboardCorners(img, tabuleiro, cantos, ret)
    """
    cv2.imshow(fname,img)
    cv2.waitKey(0)
    """
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(pts_tabuleiros, pts_imagens
                                                  , peb.shape[::-1], None, None)
img = cv2.imread('cam1_4.png')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult.png', dst)