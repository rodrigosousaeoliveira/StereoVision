import cv2
import time
# Variaveis de entrada
folder = "fotos/"

# Inicia as cameras
camera0 = cv2.VideoCapture(0)
camera1 = cv2.VideoCapture(1)
# Declara variaveis auxiliares
start = time.perf_counter()
conta_fotos = 0
aviso = True

# Loop de video principal
while(True):
    
    timer = time.perf_counter() - start
    
    ret0,frame0 = camera0.read()
    ret, frame = camera1.read()
    
    cv2.imshow("Camera 0", frame0)
    cv2.imshow("Camera 1", frame)       
        
    if timer > 4 and aviso:
        print('Capturando par de fotos numero ' + str(conta_fotos+1))   
        aviso = False
    # Captura de imagens com periodo de 5 seg
    if timer > 5:

        cv2.imwrite(folder + 'cam0_'+str(conta_fotos)+'.png', frame0)
        cv2.imwrite(folder + 'cam1_'+str(conta_fotos)+'.png', frame)
        start = time.perf_counter()
        if conta_fotos >=9 :
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