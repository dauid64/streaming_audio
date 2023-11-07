
# ESSE É O EXEMPLO QUE ESTÁ FUNCIONANDO

import socket
import time
import wave
import pyaudio
import threading
from pathlib import Path

host_name = socket.gethostname()
host_ip = ''
print(host_ip)
port = 9633


BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / 'music' / 'music1.wav'
print(MUSIC_DIR)


def audio_stream_UDP():
    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    server_socket.bind((host_ip, (port)))
    CHUNK = 10*1024
    wf = wave.open(str(MUSIC_DIR))
    p = pyaudio.PyAudio()
    print('server listening at', (host_ip, (port)), wf.getframerate())
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    data = None
    sample_rate = wf.getframerate()
    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr,msg)
   
        while True:
            data = wf.readframes(CHUNK)
            server_socket.sendto(data, client_addr)
            time.sleep(0.8*CHUNK/sample_rate)                


t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()
