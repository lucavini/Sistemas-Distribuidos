import socket
import subprocess

host_docker = socket.gethostbyname(socket.gethostname())

print('meu ip: ', host_docker)

HOST = host_docker
PORT = 7003 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
    s.connect((HOST, PORT)) 
    s.send(b'Aqui eh o servidor parceiro') 
    data = s.recv(1024)
    print('Recebido do Servidor: ', data)
