import socket
from pathlib import Path
import pickle
import wave
import time
import threading
import queue
import os

# Setando constantes
PORT = 12000
BUFF_SIZE = 65536
CHUNK = 10 * 1024
BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / 'music'
musics_list = list(MUSIC_DIR.glob('*.wav'))
q = queue.Queue(maxsize=2000)

# Criando o socket de servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', PORT))

def get_dict_musics(musics_list):
    dict_musics = {}
    for i, music in enumerate(musics_list):
        name = os.path.basename(str(music)).split('.')[0]
        dict_musics[name] = i
    return dict_musics

def set_commands(server_socket):
    while True:
        try:
            message, _ = server_socket.recvfrom(BUFF_SIZE)
            q.put(message.decode())
            print('MENSAGEM ', message.decode())
            current_time = time.time()
            if message == b'FINISH':
                break
        except ConnectionResetError:
            break

def audio_stream():
    _, client_addr = server_socket.recvfrom(BUFF_SIZE)

    # Envia a lista de músicas disponíveis para o cliente
    dict_musics = get_dict_musics(musics_list)
    server_socket.sendto(pickle.dumps(dict_musics), client_addr)

    # Recebe a seleção de música do cliente
    selected_music_msg, _ = server_socket.recvfrom(BUFF_SIZE)
    selected_music = selected_music_msg.decode()

    # Verifica se a mensagem é de reset
    if selected_music == 'RESET':
        response = 'Reiniciando para tocar outra música...'
        server_socket.sendto(response.encode(), client_addr)
    else:
        selected_music = int(selected_music)
        # Verifica se a seleção é válida
        if selected_music < 0 or selected_music >= len(musics_list):
            response = 'Erro ao selecionar música!'
            server_socket.sendto(response.encode(), client_addr)
            return

        # Abre o arquivo de música selecionado
        try:
            wf = wave.open(str(musics_list[selected_music]))
            response = 'Música escolhida com sucesso!'
            server_socket.sendto(response.encode(), client_addr)
        except Exception as e:
            response = f'Erro ao abrir a música: {str(e)}'
            server_socket.sendto(response.encode(), client_addr)
            return

        # Envia o tamanho total da música para o cliente
        server_socket.sendto(str(wf.getnframes()).encode(), client_addr)

        sample_rate = wf.getframerate()

        t2 = threading.Thread(target=set_commands, args=(server_socket,))
        t2.start()

        pause = False

        while True:
            command = q.get()
            print('Comando: ' + command)
            if command == 'FINISH':
                # Escolher a próxima música (lógica simples de avançar para a próxima)
                selected_music = (selected_music + 1) % len(musics_list)
                wf = wave.open(str(musics_list[selected_music]))

                # Enviar mensagem de transição para a próxima música
                response = 'Iniciando próxima música...'
                server_socket.sendto(response.encode(), client_addr)
                server_socket.sendto(str(wf.getnframes()).encode(), client_addr)

                sample_rate = wf.getframerate()
                pause = False
                q.put('PLAY')

            # Restante da lógica continua...

        print('FIM DE UMA MÚSICA')

# Iniciando o servidor
t1 = threading.Thread(target=audio_stream, args=())
t1.start()
