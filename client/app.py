import socket
import pyaudio

HOST = 'localhost'
PORT = 12000
CHUNK = 4096

audio = pyaudio.PyAudio()
FORMAT = 8
CHANNELS = 2
RATE = 44100

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    mensagem_envio = input('''
    Qual dessas musicas você quer escutar?
    [1] - One of Your Girls
    [2] - Get me Started
    [3] - Apocalypse
    Sua resposta: ''')
    cliente.sendto(mensagem_envio.encode(), (HOST, PORT))
    while True:
        data, _ = cliente.recvfrom(CHUNK)
        print('lendo')
        stream.write(data)


# Erros
# 1 - Não está produzindo bem a música
# 2 - Não entendi como rodar a musica no cliente