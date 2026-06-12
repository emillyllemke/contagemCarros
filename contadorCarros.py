import cv2
import numpy as np

# Carrega o vídeo que você enviou
video = cv2.VideoCapture('carro.mp4')
contador = 0
liberado = True

while True:
    ret, img = video.read()
    
    # Se o vídeo acabar, encerra o loop de forma segura
    if not ret:
        break
        
    img = cv2.resize(img, (1100, 720))
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    x, y, w, h = 120, 470, 120, 80
    
    # Tratamento da imagem
    imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((8, 8), np.uint8)
    imgDil = cv2.dilate(imgTh, kernel, iterations=2)

    # Recorte da área de interesse
    recorte = imgDil[y:y+h, x:x+w]
    brancos = cv2.countNonZero(recorte)

    # Lógica de contagem e trava
    print(f"Pixels brancos na nova área: {brancos}")

    # Mantendo o limite de pixels em 2500
    if brancos > 3000 and liberado == True:
        contador += 1
        liberado = False
    elif brancos < 2500:
        liberado = True

    # Desenho do retângulo na imagem principal
    if liberado == False:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4) # Verde ao detectar
    else:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 4) # Rosa quando livre

    # Textos na tela
    cv2.putText(img, f"Pixels: {brancos}", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Fundo e texto do Contador Principal
    cv2.rectangle(img, (575, 155), (575 + 88, 155 + 85), (255, 255, 255), -1)
    cv2.putText(img, str(contador), (590, 220), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    # Exibição do vídeo
    cv2.imshow('Contador de Carros', img)

    # Pressione a tecla 'q' no teclado para encerrar
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Limpa a memória e fecha as janelas
video.release()
cv2.destroyAllWindows()