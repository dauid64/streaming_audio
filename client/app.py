import socket

HOST = 'localhost'
PORT = 12000

# mesma configuração do socket do servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    mensagem_envio = input('Digite a mensagem: ')
    cliente.sendto(mensagem_envio.encode(), (HOST, PORT))
    mensagem_bytes, endereco_ip_servidor = cliente.recvfrom(1024)
    print(mensagem_bytes.decode())
