import PySimpleGUI as sg
import socket
import queue
import pickle
import pyaudio
import time
import threading

# Setando constantes
HOST = 'localhost'
PORT = 12000
BUFF_SIZE = 65536
CHUNK = 10*1024
p = pyaudio.PyAudio()
q_frame = queue.Queue()
q_current_frame = queue.Queue()


def get_audio_data(client_socket):
    '''
        Recebe os frames e aloca na fila
    '''
    while True:
        response, _ = client_socket.recvfrom(BUFF_SIZE)
        data = pickle.loads(response)
        q_frame.put(data['frame'])
        q_current_frame.put(data['current_frame'])


def play_audio(stream, window):
    '''
        Pega os frames da fila e escreve na stream
    '''
    while True:
        frame = q_frame.get()
        window['progress_bar'].update(q_current_frame.get())
        stream.write(frame)


# Criando o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# pegando a lista de músicas do server
message = 'GET MUSICS'
client_socket.sendto(message.encode(), (HOST, PORT))
response, server_addr = client_socket.recvfrom(BUFF_SIZE)
dict_musics = pickle.loads(response)

# Interface
sg.theme('DarkAmber')

layout = [
    [sg.Image("client/assets/logo.png", size=[100, 58], pad=(200, 10))],
    [sg.Text('Bem vindo ao nosso streaming de áudio!', justification='center', size=(100, 1))],
    [sg.Text('Escolha a música que você quer ouvir: '), sg.Combo(values=list(dict_musics.keys()), key='select_music', size=(20,1))],
    [sg.Button('Play', size=(15, 1), pad=(200, 10), key='PLAY')],
    [sg.Text("", key="status", justification='center', size=(100, 1))]
]

window = sg.Window('Streaming de Aúdio', layout, size=(500, 300))

while True:
    eventos, valores = window.read()
    if eventos == sg.WINDOW_CLOSED:
        print('fechando janela.')
        break
    if eventos == 'PLAY':
        music = dict_musics.get(valores['select_music'], None)
        if music is None:
            window['status'].update("Escolha uma música valida!", text_color="red")
        else:
            client_socket.sendto(str(music).encode(), (HOST, PORT))
            response, _ = client_socket.recvfrom(BUFF_SIZE)
            window['status'].update(f"{response.decode()}", text_color="green")
            message = 'GET SIZE_MUSIC'
            client_socket.sendto(str(message).encode(), (HOST, PORT))
            response, _ = client_socket.recvfrom(BUFF_SIZE)
            music_total_frames = int(response.decode())
            window.extend_layout(window, [[sg.ProgressBar(music_total_frames, orientation='h', s=(110, 20), key='progress_bar')]])
            window.extend_layout(window, [
                    [
                        sg.Button('Pause', size=(10, 1), key='PAUSE', pad=(60, 10)),
                        sg.Button('Resume', size=(10, 1), key='RESUME', disabled=True),
                        sg.Button('Stop', size=(10, 1), key='STOP', disabled=True)
                    ]
                ]
            )

            window['PLAY'].update(disabled=True)
            message = 'PLAY'
            client_socket.sendto(message.encode(), (HOST, PORT))
            stream = p.open(
                format=8,
                channels=2,
                rate=44100,
                output=True,
                frames_per_buffer=CHUNK
            )
            t1 = threading.Thread(
                target=get_audio_data,
                kwargs={
                    'client_socket': client_socket,
                }
            )
            t1.start()
            time.sleep(5)
            t2 = threading.Thread(
                target=play_audio,
                kwargs={
                    'stream': stream,
                    'window': window
                }
            )
            t2.start()

    if eventos == 'PAUSE':
        window['PAUSE'].update(disabled=True)
        window['STOP'].update(disabled=False)
        window['RESUME'].update(disabled=False)
        client_socket.sendto(b'PAUSE', server_addr)
        print('PARANDO MÚSICA')
    if eventos == 'RESUME':
        window['PAUSE'].update(disabled=False)
        window['STOP'].update(disabled=False)
        window['RESUME'].update(disabled=True)
        client_socket.sendto(b'RESUME', server_addr)
        print('CONTINUANDO MÚSICA')
    if eventos == 'STOP':
        window['PAUSE'].update(disabled=True)
        window['STOP'].update(disabled=True)
        window['RESUME'].update(disabled=False)
        window['progress_bar'].update(0)
        client_socket.sendto(b'STOP', server_addr)
        print('PARANDO MÚSICA')
