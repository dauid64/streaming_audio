from pathlib import Path
import socket
import wave
import pyaudio

BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / 'music'

HOST = ''
PORT = 12000
CHUNK = 10*1024

musics_list = list(MUSIC_DIR.glob('*.wav'))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((HOST, PORT))

while True:
    msg_bytes, addr_ip_client = server.recvfrom(CHUNK)
    try:
        recv_msg = int(msg_bytes.decode())
        send_msg = 'Iniciando a música'
        server.sendto(send_msg.encode(), addr_ip_client)
        music_selected = musics_list[recv_msg]
        with wave.open(str(music_selected), 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            while len(data := wf.readframes(CHUNK)):
                server.sendto(data, addr_ip_client)

            send_msg = 'Música acabou'
            server.sendto(send_msg.encode(), addr_ip_client)
            stream.close()

            p.terminate()
    except ValueError:
        send_msg = 'Opção Inválida'
        server.sendto(send_msg.encode(), addr_ip_client)
