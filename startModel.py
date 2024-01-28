import cv2
import torch
import numpy as np
import RPi.GPIO as GPIO

# Inicializar os pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)  # Pino GPIO para receber o sinal para executar a função

# Carregar o modelo ONNX
model = torch.onnx.load('caminho/para/seu/modelo/best.onnx')

# Função para salvar a imagem quando a classe Lightning é detectada
def salvar_imagem(img, nome_arquivo):
    cv2.imwrite(nome_arquivo, img)
    print(f"Imagem salva como {nome_arquivo}")

# Função para detecção de raios e obtenção de coordenadas do centróide
def detectar_raios(img):
    # Pré-processamento da imagem
    img_resized = cv2.resize(img, (224, 224))  # Ajuste ao tamanho esperado pelo modelo
    img_resized = np.transpose(img_resized, (2, 0, 1))  # Transpor para formato CxHxW
    img_resized = np.expand_dims(img_resized, axis=0)  # Adicionar dimensão batch

    # Converter para tensor PyTorch
    input_tensor = torch.tensor(img_resized.astype(np.float32))

    # Executar inferência
    with torch.no_grad():
        output = model(input_tensor)

    # Processar a saída
    classes = output.argmax(dim=1)  # Obtém a classe predita
    if classes.item() == 0:  # Verifica se a classe predita é "Lightning"
        print("Raio detectado!")
        # Salvar a imagem quando a classe "Lightning" é detectada
        salvar_imagem(img, "raio_detectado.jpg")

# Função principal
def main():
    cap = cv2.VideoCapture('tcp://127.0.0.1:8888')  # Inicia captura de vídeo via TCP

    # Loop principal
    while True:
        ret, frame = cap.read()  # Lê um frame do fluxo de vídeo
        if not ret:
            print("Erro ao ler o frame.")
            break

        if GPIO.input(2) == GPIO.HIGH:  # Verifica se o pino GPIO recebeu o sinal
            print("Sinal recebido para detecção de raios.")
            detectar_raios(frame)  # Chama a função de detecção de raios para o frame atual

        cv2.imshow('Frame', frame)  # Mostra o frame

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Aguarda a tecla 'q' para sair do loop
            break

    cap.release()
    cv2.destroyAllWindows()

# Chamada da função principal
if __name__ == "__main__":
    main()

