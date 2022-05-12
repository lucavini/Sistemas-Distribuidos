import socket # Importa a biblioteca "socket", ela é um recurso do sistema operacional e funciona fazendo uma comunicação, onde o SO que irá gerenciar.
import subprocess #Esta biblioteca permite a criação de processos, conexão a seus canais de entrada/saída/erro e obter seus códigos de retorno.
from ast import literal_eval
import random
import threading
import time

def generateMatrix():
    mat=[]
    for x in range(10):
        aux=[]
        for y in range(10):
            aux.append(random.randint(1,20))
        mat.append(aux)
    return mat

class Thread(threading.Thread):
    def __init__(self,Message,Adress,Port,Socket):
        threading.Thread.__init__(self)
        self.Mess=Message
        self.Ad=Adress
        self.Port=Port
        self.socket=Socket

    def run(self):
        self.socket.sendto(str(StringMessage).encode(), (self.Ad, self.Port)) # Envia a mensagem por meio da função "sendto", passa a mensagem/uma string e uma tupla, passando o IP do servidor e a Porta do servidor.
        received = self.socket.recvfrom(1024) #Ele recebe a nensagem e nesse momento ele fica em estado bloqueado e será desbloqueado quando a mensagem do cliente chegue no Servidor. A partir disso, o servidor será desbloqueado.
        response = literal_eval(received[0].decode())
        response = [[int(ele) for ele in sub] for sub in response] 

        print("Mensagem enviada:     {}".format(Message))#Exibe na tela a mensagem de enviada do Servidor
        print("Mensagem recebida: {}".format(response))#Exibe na tela a mensagem de recebida do Servidor


UDP_IP_ADDRESS = '172.17.0.2' # Este é o IP do Servidor, chamado de IP de LoopBack, ele se auto referencia.
UDP_PORT_NO = 7002 # Número da porta, esse valor vai dentro da mensagem que está sendo transmitida.
clientSock = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) # Implementação da função "socket", que basicamente faz a criação da conexão, uma requisição que será entregue ao SO.
threads=[]
Message=[]
for x in range(30):
    Message.append(generateMatrix())  # Messangem que está sendo transmitida
    Message.append(generateMatrix())  # Messangem que está sendo transmitida
    StringMessage = [[str(ele) for ele in sub] for sub in Message] 
    newthread = Thread(StringMessage, UDP_IP_ADDRESS, UDP_PORT_NO, clientSock)
    threads.append(newthread)
    Message=[]

t1=time.time()
for x in threads:
    x.start()

for x in threads:
    x.join()
t2=time.time()

print('tempo de processamento =', t2-t1)

# print(len(str(StringMessage).encode()))

