import socket
from pathlib import Path
import pickle
import wave
import time
import pickle
import threading
import queue
import os

# Setando constantes
PORT = 12000
BUFF_SIZE = 65536
CHUNK = 10*1024
BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / 'music'
musics_list = list(MUSIC_DIR.glob('*.wav'))
q = queue.Queue(maxsize=2000)


def get_dict_musics(musics_list):
    '''
        Retorna a lista de músicas
        em um dicionario
    '''
    dict = {}
    for i in range(0, len(musics_list)):
        name = os.path.basename(str(musics_list[i])).split('.')[0]
        dict[name] = i
    return dict


def set_configurate(server_socket):
    '''
        Essa função tem o objetivo de capturar
        as msg do usuário para pausar e continuar
        a música
    '''
    while True:
        message, _ = server_socket.recvfrom(BUFF_SIZE)
        q.put(message.decode())
        print('MENSAGEM ', message.decode())


def main():
    # Criando o socket de servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', PORT))

    # Recebendo o GET MUSICS
    _, client_addr = server_socket.recvfrom(BUFF_SIZE)
    dict_musics = get_dict_musics(musics_list)

    # Enviando o dicionario de músicas codificado
    server_socket.sendto(pickle.dumps(dict_musics), client_addr)

    # Recebendo a música selecionada
    selected_music, _ = server_socket.recvfrom(BUFF_SIZE)
    wf = wave.open(str(musics_list[int(selected_music.decode())]))
    response = 'Música Escolhida com sucesso!'
    server_socket.sendto(response.encode(), client_addr)
    message, _ = server_socket.recvfrom(BUFF_SIZE)
    server_socket.sendto(str(wf.getnframes()).encode(), client_addr)

    data = None
    sample_rate = wf.getframerate()

    t2 = threading.Thread(
        target=set_configurate,
        args=(server_socket, )
    )
    t2.start()

    pause = False
    finish = False

    while True:
        command = q.get()
        if finish:
            break
        if command == 'PAUSE':
            pause = True
        elif command == 'STOP':
            pause = True
            wf.rewind()
        elif command == 'RESUME':
            pause = False
            q.put('PLAY')
        elif command == 'PLAY' and pause is not True:
            while True:
                if q.empty() is not True:
                    break
                frame = wf.readframes(CHUNK)
                if frame == b'':
                    finish = True
                    break
                data = {
                    'frame': frame,
                    'current_frame': wf.tell()
                }
                server_socket.sendto(pickle.dumps(data), client_addr)
                time.sleep(0.8*CHUNK/sample_rate)

    message = 'FINISH'
    server_socket.sendto(message.encode(), client_addr)


t1 = threading.Thread(target=main, args=())
t1.start()
