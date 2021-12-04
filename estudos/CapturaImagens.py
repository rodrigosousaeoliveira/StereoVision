import cv2
import time
# Variaveis de entrada
folder = "calib"
ncapturas = 20

# Inicia as cameras
camera0 = cv2.VideoCapture(0)
camera1 = cv2.VideoCapture(1)
cameras = [camera0, camera1]
camera0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Declara variaveis auxiliares
start = time.perf_counter()
conta_fotos = 0
aviso = True

camera = 0
# Loop de video principal
while(True):
    
    timer = time.perf_counter() - start
    
    ret, frame = cameras[camera].read()
    
    frame2 = cv2.putText(frame, str(5-timer)[:3], (50,50), cv2.FONT_HERSHEY_DUPLEX, 1,
                         (255,255,255))
    cv2.imshow("Camera "+ str(camera), cv2.resize(frame2, (640, 360)) )       
        
    if timer > 4 and aviso:
        print('Capturando par de fotos numero ' + str(conta_fotos+1))   
        aviso = False
    # Captura de imagens com periodo de 5 seg
    if timer > 5:
        
        caminho = folder + '/cam' + str(camera) + '_' + str(conta_fotos) + '.png'
        cv2.imwrite(caminho, frame)
        start = time.perf_counter()
        if conta_fotos >=(ncapturas-1) :
            break
        conta_fotos += 1
        aviso = True
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera0.release()
camera1.release()
cv2.destroyAllWindows()
print(time.perf_counter())