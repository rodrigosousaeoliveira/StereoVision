import cv2
import time
# Variaveis de entrada
stereo = True
camera = 1
folder = "img"
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

# Loop de video principal
while(True):

    timer = time.perf_counter() - start
    
    frames =  [cameras[0].read()[1], cameras[1].read()[1]]
    frame = frames[camera]
        
    if timer > 4 and aviso:
        print('Capturando par de fotos numero ' + str(conta_fotos+1))   
        aviso = False
            
    # Captura de imagens com periodo de 5 seg
    if timer > 5:
        if stereo:
            cv2.imwrite(folder + '/st_cam0_' + str(conta_fotos) + '.png', frames[0])
            cv2.imwrite(folder + '/st_cam1_' + str(conta_fotos) + '.png', frames[1])
        else:
            caminho = folder + '/cam' + str(camera) + '_' + str(conta_fotos) + '.png'
            cv2.imwrite(caminho, frame)
            
        if conta_fotos >=(ncapturas-1) :
            break
        start = time.perf_counter() # Reinicia timer apos captura
        aviso = True           
        conta_fotos += 1
    
    frame2 = frame.copy()
    cv2.putText(frame2, str(5-timer)[:3], (50,50), cv2.FONT_HERSHEY_DUPLEX, 1,
                         (255,255,255))
    cv2.imshow("Camera " + str(camera), cv2.resize(frame2, (640, 360)) )
    if stereo:
        outraCamera = 1 - camera
        cv2.imshow("Camera " + str(outraCamera), cv2.resize(frames[outraCamera], (640, 360)) )
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

camera0.release()
camera1.release()
cv2.destroyAllWindows()