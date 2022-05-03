import socket # Importa a biblioteca "socket", ela é um recurso do sistema operacional e funciona fazendo uma comunicação, onde o SO que irá gerenciar.
import subprocess #Esta biblioteca permite a criação de processos, conexão a seus canais de entrada/saída/erro e obter seus códigos de retorno.
from ast import literal_eval

UDP_IP_ADDRESS = "127.0.0.1" # Este é o IP do Servidor, chamado de IP de LoopBack, ele se auto referencia.
UDP_PORT_NO = 6789 # Número da porta, esse valor vai dentro da mensagem que está sendo transmitida.

Message = [[[2, 3], [4, 6]], [[3, 4], [5, 7]]] # Messangem que está sendo transmitida
StringMessage = [[str(ele) for ele in sub] for sub in Message] 

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Implementação da função "socket", que basicamente faz a criação da conexão, uma requisição que será entregue ao SO.

clientSock.sendto(str(StringMessage).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO)) # Envia a mensagem por meio da função "sendto", passa a mensagem/uma string e uma tupla, passando o IP do servidor e a Porta do servidor.

received = clientSock.recv(1024) #Ele recebe a nensagem e nesse momento ele fica em estado bloqueado e será desbloqueado quando a mensagem do cliente chegue no Servidor. A partir disso, o servidor será desbloqueado.

response = literal_eval(received.decode())
response = [[int(ele) for ele in sub] for sub in response] 

print("Mensagem enviada:     {}".format(Message))#Exibe na tela a mensagem de enviada do Servidor
print("Mensagem recebida: {}".format(response))#Exibe na tela a mensagem de recebida do Servidor
