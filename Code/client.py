import socket # Importa a biblioteca "socket", ela é um recurso do sistema operacional e funciona fazendo uma comunicação, onde o SO que irá gerenciar.
import subprocess #Esta biblioteca permite a criação de processos, conexão a seus canais de entrada/saída/erro e obter seus códigos de retorno.
from ast import literal_eval


UDP_IP_ADDRESS = socket.gethostbyname('ipc_server_dns_name') # Este é o IP do Servidor, chamado de IP de LoopBack, ele se auto referencia.
UDP_PORT_NO = 7002 # Número da porta, esse valor vai dentro da mensagem que está sendo transmitida.
# Message = [[[6, 0], [3, 0]],[[6, 0], [3, 0]]] # Messangem que está sendo transmitida
Message = [[[6, 0, 1, 4, 5, 8, 9, 9, 4, 8], [3, 0, 2, 8, 6, 8, 1, 8, 5, 5], [5, 3, 2, 8, 1, 1, 3, 5, 7, 9], [4, 0, 6, 4, 9, 8, 0, 6, 7, 8], [7, 1, 6, 2, 9, 3, 0, 0, 8, 5], [2, 8, 7, 1, 9, 1, 5, 0, 6, 4], [4, 4, 0, 4, 1, 0, 8, 1, 1, 3], [9, 3, 3, 0, 9, 3, 7, 3, 9, 8], [4, 6, 9, 6, 8, 5, 1, 6, 4, 4], [2, 8, 7, 6, 5, 4, 0, 0, 1, 6]], [[7, 0, 4, 3, 9, 5, 4, 1, 2, 5], [7, 3, 9, 9, 7, 8, 4, 1, 9, 2], [7, 6, 8, 5, 9, 1, 5, 0, 6, 9], [9, 4, 6, 3, 5, 2, 3, 2, 4, 5], [1, 0, 0, 1, 0, 7, 4, 0, 6, 7], [1, 8, 4, 4, 2, 6, 4, 0, 7, 6], [6, 3, 4, 7, 4, 1, 1, 0, 7, 5], [4, 7, 0, 7, 5, 9, 4, 7, 7, 6], [9, 0, 0, 2, 1, 7, 9, 6, 5, 3], [7, 1, 1, 2, 9, 8, 8, 8, 1, 3]]] # Messangem que está sendo transmitida
StringMessage = [[str(ele) for ele in sub] for sub in Message] 


clientSock = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) # Implementação da função "socket", que basicamente faz a criação da conexão, uma requisição que será entregue ao SO.

clientSock.sendto(str(StringMessage).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO)) # Envia a mensagem por meio da função "sendto", passa a mensagem/uma string e uma tupla, passando o IP do servidor e a Porta do servidor.
print(len(str(StringMessage).encode()))

received = clientSock.recvfrom(1024) #Ele recebe a nensagem e nesse momento ele fica em estado bloqueado e será desbloqueado quando a mensagem do cliente chegue no Servidor. A partir disso, o servidor será desbloqueado.

response = literal_eval(received[0].decode())
response = [[int(ele) for ele in sub] for sub in response] 

print("Mensagem enviada:     {}".format(Message))#Exibe na tela a mensagem de enviada do Servidor
print("Mensagem recebida: {}".format(response))#Exibe na tela a mensagem de recebida do Servidor