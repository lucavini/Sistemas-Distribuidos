import socket
import subprocess

host_docker = socket.gethostbyname(socket.gethostname())

print('meu ip: ', host_docker)

HOST = host_docker
PORT = 7005 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
    s.connect((HOST, PORT))
    s.send(b'recebida a mensagem')
    while True: 
        data = s.recv(1024)
        print('Recebido do Servidor: ', data)
        s.send(b'recebida a mensagem')
