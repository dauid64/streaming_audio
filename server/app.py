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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(1)

def get_dict_musics(musics_list):
    dict_musics = {}
    for i, music_path in enumerate(musics_list):
        name = os.path.basename(music_path).split('.')[0]
        dict_musics[name] = i
    return dict_musics

def set_commands(client_socket):
    while True:
        try:
            command = client_socket.recv(BUFF_SIZE).decode()
            q.put(command)
            print('COMANDO:', command)
            if command == 'FINISH':
                break
        except ConnectionResetError:
            break

def audio_stream(client_socket):
    dict_musics = get_dict_musics(musics_list)
    
    # Enviando o dicionario de músicas codificado
    client_socket.sendall(pickle.dumps(dict_musics))

    # Recebendo a música selecionada
    selected_music_name = client_socket.recv(BUFF_SIZE).decode()
    try:
        wf = wave.open(str(MUSIC_DIR / selected_music_name), 'rb')
        print('Selecionado:', selected_music_name)
    except ValueError:
        return print('Erro ao selecionar música!')

    response = 'Música escolhida com sucesso!'
    client_socket.sendall(response.encode())

    # Enviando o tamanho da música
    client_socket.recv(BUFF_SIZE)
    client_socket.sendall(str(wf.getnframes()).encode())

    data = None
    sample_rate = wf.getframerate()

    t2 = threading.Thread(target=set_commands, args=(client_socket,))
    t2.start()

    pause = False

    while True:
        command = q.get()
        print('COMANDO RECEBIDO:', command)
        if command == 'FINISH':
            break
        if command == 'PAUSE':
            pause = True
        elif command == 'STOP':
            pause = True
            wf.rewind()
            data = {
                'frame': 'FINISH',
                'current_frame': 'FINISH'
            }
            client_socket.sendall(pickle.dumps(data))
            break
        elif command == 'RESUME':
            pause = False
            q.put('PLAY')
        elif command == 'PLAY' and pause is False:
            while True:
                if q.empty() is not True:
                    break
                frame = wf.readframes(CHUNK)
                if frame == b'':
                    data = {
                        'frame': 'FINISH',
                        'current_frame': 'FINISH'
                    }
                    client_socket.sendall(pickle.dumps(data))
                    break
                data = {
                    'frame': frame,
                    'current_frame': wf.tell()
                }
                client_socket.sendall(pickle.dumps(data))
                time.sleep(0.8 * CHUNK / sample_rate)
    print('FIM DE UMA MÚSICA')

while True:
    print('Aguardando conexão...')
    client_socket, client_addr = server_socket.accept()
    print('Conexão recebida de', client_addr)
    t1 = threading.Thread(target=audio_stream, args=(client_socket,))
    t1.start()
