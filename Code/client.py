import socket # Importa a biblioteca "socket", ela é um recurso do sistema operacional e funciona fazendo uma comunicação, onde o SO que irá gerenciar.
import subprocess #Esta biblioteca permite a criação de processos, conexão a seus canais de entrada/saída/erro e obter seus códigos de retorno.
from ast import literal_eval
import random
import threading
import time
#bibliotecas que foram utilizadas

def generateMatrix(): # gera uma matriz [10,10], como o socket não envia mensagens grandes demais, esse foi um tamanho plausivel para se colocar numa mensagem
    mat=[]
    for x in range(10):
        aux=[]
        for y in range(10):
            aux.append(random.randint(1,20))
        mat.append(aux)
    return mat

class Thread(threading.Thread): # thread que envia requisição ao servidor
    def __init__(self,Message,Adress,Port,Socket): # armazena a mensagem com as matrizes, o endereço e porta do servidor, e o socket UDP
        threading.Thread.__init__(self)
        self.Mess=Message
        self.Ad=Adress
        self.Port=Port
        self.socket=Socket

    def run(self):
        self.socket.sendto(str(StringMessage).encode(), (self.Ad, self.Port)) # Envia a mensagem por meio da função "sendto", passa a mensagem/uma string e uma tupla, passando o IP do servidor e a Porta do servidor.
        received = self.socket.recvfrom(1024) #Ele recebe a nensagem e nesse momento ele fica em estado bloqueado e será desbloqueado quando a mensagem voltar do Servidor.
        response = literal_eval(received[0].decode()) # essas duas linhas transformam a matriz de string para lista de inteiros
        response = [[int(ele) for ele in sub] for sub in response] 

        print("Mensagem enviada:     {}".format(Message))#Exibe na tela a mensagem enviada ao Servidor
        print("Mensagem recebida: {}".format(response))#Exibe na tela a mensagem recebida do Servidor


UDP_IP_ADDRESS = '172.17.0.7' # Este é o IP do Servidor no docker, precisa ser alterado antes de executar, por isso há prints no servidor principal para se saber qual ip colocar aqui.
# UDP_IP_ADDRESS = '127.0.1.1' # Este é o IP do Servidor executando local para testes antes de subir ao container.
UDP_PORT_NO = 7006 # Número da porta, esse valor vai dentro da mensagem que está sendo transmitida.
threads=[] # lista de threads que serão executadas
Message=[]
for x in range(30):
    clientSock = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) # Implementação da função "socket", que basicamente faz a criação da conexão, uma requisição que será entregue ao SO, nessa caso cria uma conexão UDP.
    Message.append(generateMatrix())  # Gera matriz e coloca na lista para ser enviada
    Message.append(generateMatrix())  # Gera matriz e coloca na lista para ser enviada
    StringMessage = [[str(ele) for ele in sub] for sub in Message]  # transorma a lista de matrizes em uma string
    newthread = Thread(StringMessage, UDP_IP_ADDRESS, UDP_PORT_NO, clientSock) # cria a thread e coloca em uma lista logo abaixo
    threads.append(newthread)
    Message=[]

t1=time.time() # usado para medir tempo de processamento
for x in threads: # inicia todas as threads
    x.start()

for x in threads: # espera o termino de todas as threads
    x.join()
t2=time.time() # usado para medir tempo de processamento

print('tempo de processamento =', t2-t1) # mostra o tempo de processamento

# print(len(str(StringMessage).encode()))

