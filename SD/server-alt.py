# from msilib.schema import Class
import socket, threading
from ast import literal_eval
import time
import os
import random

class Thread(threading.Thread):
    def __init__(self,Message,Adress,Socket):
        threading.Thread.__init__(self)
        self.Mess=Message
        self.Ad=Adress
        self.socket=Socket
        print('Iniciada conexão com cliente',Adress)


    def multMatriz(mat1, mat2):
        def getLinha(matriz, n):
            return [i for i in matriz[n]]  # ou simplesmente return matriz[n]

        def getColuna(matriz, n):
            return [i[n] for i in matriz]

        mat1lin = len(mat1)                # retorna 2
        mat1col = len(mat1[0])             # retorna 2

        mat2lin = len(mat2)                # retorna 2
        mat2col = len(mat1[0])             # retorna 3

        matRes = []
        
        for i in range(mat1lin):           
            matRes.append([])
            for j in range(mat2col):
                # multiplica cada linha de mat1 por cada coluna de mat2;
                listMult = [x*y for x, y in zip(getLinha(mat1, i), getColuna(mat2, j))]

                # e em seguida adiciona a matRes a soma das multiplicações
                matRes[i].append(sum(listMult))
        return matRes


    def run(self):
        # recebe = self.Sock.recv(1024)
        Array = literal_eval(self.Mess.decode())
        matriz1 = []
        matriz2 = []

        # Pega a primeira matriz
        for i in Array[0]:
            matriz1.append(literal_eval(i))
        print('matriz1: ', matriz1)

        # Pega a segunda matriz
        for i in Array[1]:
            matriz2.append(literal_eval(i))
        print('matriz2: ', matriz2)

        response = Thread.multMatriz(matriz1, matriz2)
        print('Matriz multiplicada: ',response)

        StringResponse = [[str(ele) for ele in sub] for sub in response]
        print(len(str(StringResponse)))
        self.socket.sendto(str(StringResponse).encode(),self.Ad)

class ThreadProc(threading.Thread):
    def __init__(self,Message,Conn,SocketUdp,Udpad):
        threading.Thread.__init__(self)
        self.Mess=Message
        self.TCP=Conn
        self.UDP=SocketUdp
        self.UDPAd=Udpad

    def run(self):
        filho=os.fork()
        if filho == 0:
            self.TCP.send(self.Mess)
            data = self.TCP.recv(1024)
            self.UDP.sendto(data,self.UDPAd)
        else:
            os.waitpid(filho,0)



if __name__ == '__main__':
    LOCALHOST = '' #define o localhost, como é passado '' ele assume o valor padrão, que é 127.0.0.1
    PORT = 7002 #define a porta, nesse caso a porta 7002 será dedicada a conexão UDP do servidor
    server = socket.socket(family=socket.AF_INET ,type=socket.SOCK_DGRAM) #define o socket, onde, family=socket.AF_INET diz que será utilizado ipv4 e type=socket.SOCK_DGRAM define o socket como um socket UDP
    server.bind((LOCALHOST, PORT)) #vincula o ip e porta que serão usados
    print("Servidor iniciado!")
    print("Aguardando nova conexao..")


    print('Criando conexão TCP')
    print("Aguardando nova conexao TCP..")
    tcpServer = socket.socket(family=socket.AF_INET ,type=socket.SOCK_STREAM)
    PORT2 = 7006
    tcpServer.bind((LOCALHOST, PORT2))
    servidores=[]
    for x in range(2):
        tcpServer.listen()
        conn, addr = tcpServer.accept()
        data = conn.recv(1024).decode("ascii") 
        print('Endereço do servidor parceiro: ', addr)
        print('Mensagem recebida: ', data)
        servidores.append((conn,addr))
    print(servidores)

    # while True:
    #     time.sleep(5)
    #     conn.send(b'Confirmada conexao')
    #     data = conn.recv(1024).decode("ascii")
    #     print(data) 

    while True:
        print('numero de threads ativas: ',threading.active_count()) #mostra o número de threads ativas no momento (usaremos para limitar o número de conexões)
        rec=server.recvfrom(1024) #espera alguém mandar uma mensagem
        newthread = ThreadProc(rec[0],servidores[random.randint(0,1)][0],server,rec[1]) #cria uma trhead e armazena nela (a mensagem recebida, o ip e porta de quem enviou, e o socket UDP para enviar a resposta
        newthread.start() #inicia a thread