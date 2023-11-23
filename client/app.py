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

stream = None  # Inicializa o stream fora do loop principal

def reset_audio_state(window, stream, client_socket):
    window['PLAY'].update(disabled=False)
    window['PAUSE'].update(visible=False, disabled=True)
    window['STOP'].update(visible=False, disabled=True)
    window['RESUME'].update(visible=False, disabled=True)
    window['progress_bar'].update(0, visible=False)
    
    if stream and stream.is_active():
        stream.stop_stream()
        stream.close()

    while not q_frame.empty():
        q_frame.get()

    while not q_current_frame.empty():
        q_current_frame.get()

    message = 'RESET'
    client_socket.sendto(message.encode(), (HOST, PORT))
    time.sleep(1)  # Aguarda um breve momento para garantir que o servidor esteja pronto

    print('Reiniciando para tocar outra música...')

# Criando o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# pegando a lista de músicas do server
message = 'GET MUSICS'
client_socket.sendto(message.encode(), (HOST, PORT))
response, server_addr = client_socket.recvfrom(BUFF_SIZE)
dict_musics = pickle.loads(response)

# Interface
sg.theme('DarkAmber')

layout = [
    [sg.Text('Bem vindo ao nosso streaming de áudio!', justification='center', size=(100, 1))],
    [sg.Text('Escolha a música que você quer ouvir: '), sg.Combo(values=list(dict_musics.keys()), key='select_music', size=(20,1))],
    [sg.Button('Play', size=(15, 1), pad=(200, 10), key='PLAY')],
    [sg.Text("", key="status", justification='center', size=(100, 1))],
    [sg.ProgressBar(0, orientation='h', s=(110, 20), key='progress_bar', visible=False)],
    [
        sg.Button('Pause', size=(10, 1), key='PAUSE', pad=(80, 10), visible=False),
        sg.Button('Resume', size=(10, 1), key='RESUME', disabled=True, visible=False),
        sg.Button('Stop', size=(10, 1), key='STOP', disabled=True, visible=False)
    ]
]

window = sg.Window('Streaming de Áudio', layout, size=(500, 300))

def get_audio_data(client_socket):
    while True:
        try:
            response, server_addr = client_socket.recvfrom(BUFF_SIZE)
            data = pickle.loads(response)
            q_frame.put(data['frame'])
            if data['frame'] == 'FINISH':
                client_socket.sendto(b'FINISH', server_addr)
                break
            q_current_frame.put(data['current_frame'])
        except OSError:
            break

def play_audio(stream, window):
    while True:
        try:
            frame = q_frame.get(timeout=5)
            if frame == 'FINISH':
                window.write_event_value('FINISH', None)
                break
            window['progress_bar'].update(q_current_frame.get())
            stream.write(frame)
        except queue.Empty:
            break

while True:
    eventos, valores = window.read()
    
    if eventos == sg.WINDOW_CLOSED:
        client_socket.sendto(b'FINISH', server_addr)
        client_socket.close()
        print('fechando janela.')
        break
    if eventos == 'FINISH':
        reset_audio_state(window, stream, client_socket)
        window['progress_bar'].update(visible=False)
        window['PLAY'].update(disabled=False)
        window['PAUSE'].update(visible=False)
        window['STOP'].update(visible=False)
        window['RESUME'].update(visible=False)
        window['status'].update('Escolha outra música!', text_color="yellow")
    if eventos == 'PLAY':
        reset_audio_state(window, stream, client_socket)
        music = dict_musics.get(valores['select_music'], None)
        if music is None:
            window['status'].update("Escolha uma música válida!", text_color="red")
        else:
            client_socket.sendto(str(music).encode(), (HOST, PORT))
            response, _ = client_socket.recvfrom(BUFF_SIZE)
            window['status'].update(f"{response.decode()}", text_color="green")
            message = 'GET SIZE_MUSIC'
            client_socket.sendto(str(message).encode(), (HOST, PORT))
            response, _ = client_socket.recvfrom(BUFF_SIZE)
            music_total_frames = int(response.decode())
            window['PLAY'].update(disabled=True)
            window['progress_bar'].update(current_count=0, max=music_total_frames, visible=True)
            window['PAUSE'].update(visible=True)
            window['STOP'].update(visible=True)
            window['RESUME'].update(visible=True)
            message = 'PLAY'
            client_socket.sendto(message.encode(), (HOST, PORT))
            
            stream = p.open(
                format=pyaudio.paInt16,
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
            time.sleep(1)  # Aguarda um momento para garantir que a música começou a tocar
    # Restante do código...
