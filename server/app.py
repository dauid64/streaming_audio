import socket

HOST = ''
PORT = 12000

# Servidor family=IPV4 e type=UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# vamos escutar nesse adress
servidor.bind((HOST, PORT))

while True:
    # Recebe os dados recebidos e o endereco do cliente
    mensagem_bytes, endereco_ip_client = servidor.recvfrom(1024)

    # converte para string e coloca em uppercase
    mensagem_resposta = mensagem_bytes.decode().upper()

    # Manda a resposta para o cliente
    servidor.sendto(mensagem_resposta.encode(), endereco_ip_client)

    print(mensagem_resposta)
