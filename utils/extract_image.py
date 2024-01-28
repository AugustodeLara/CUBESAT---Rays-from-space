import cv2
import os

def extrair_frames(video_path, output_folder):
    # Abre o vídeo
    cap = cv2.VideoCapture(video_path)

    # Verifica se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    # Cria a pasta de saída, se não existir
    os.makedirs(output_folder, exist_ok=True)

    # Loop para extrair frames
    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Salva o frame como uma imagem
        frame_count += 1
        frame_name = f"frame_{frame_count:04d}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)

    # Libera os recursos
    cap.release()

# Exemplo de uso
video_path = "/home/aglara/Imagens/raios/station.mp4"
output_folder = "/home/aglara/Imagens/raios/station"
extrair_frames(video_path, output_folder)

