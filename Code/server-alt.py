import socket, threading
from ast import literal_eval
import time
import os
from operator import itemgetter
import ctypes
#bibliotecas que foram utilizadas

class Thread(threading.Thread): # Esta classe cria uma thread q lida individualmente com cada requisição UDP do cliente
    def __init__(self,Message,Adress,Socket): # Recebe e armazena a mensagem, que são as matrizes, o remetente e o socket para devolver a mensagem
        threading.Thread.__init__(self)
        self.Mess=Message
        self.Ad=Adress
        self.socket=Socket
        print('Iniciada conexão com cliente',Adress)


    def multMatriz(mat1, mat2): # função que recebe duas matrizes de tamanho qualquer e devolve a matriz resultante da multiplicação
        def getLinha(matriz, n):
            return [i for i in matriz[n]]  

        def getColuna(matriz, n):
            return [i[n] for i in matriz]

        mat1lin = len(mat1)                
        mat1col = len(mat1[0])             

        mat2lin = len(mat2)               
        mat2col = len(mat1[0])           

        matRes = []
        
        for i in range(mat1lin):           
            matRes.append([])
            for j in range(mat2col):
                # multiplica cada linha de mat1 por cada coluna de mat2;
                listMult = [x*y for x, y in zip(getLinha(mat1, i), getColuna(mat2, j))]

                # e em seguida adiciona a matRes a soma das multiplicações
                matRes[i].append(sum(listMult))
        return matRes


    def run(self): # Inicializa a thread UDP que lida com uma requisição
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        SYS_gettid = 186
        
        t1 = time.time() # Usado para checar tempo durante testes locais (pode ser removido)
        Array = literal_eval(self.Mess.decode()) # converte a mensagem de string para uma lista de matrizes, a principio cada matriz ainda é uma string
        matriz1 = [] # Para os experimentos definimos que somente 2 matrizes serão multiplicadas 
        matriz2 = []

        # Pega a primeira string e transforma na primeira matriz
        for i in Array[0]:
            matriz1.append(literal_eval(i))

        # Pega a segunda string e transforma na segunda matriz
        for i in Array[1]:
            matriz2.append(literal_eval(i))

        response = Thread.multMatriz(matriz1, matriz2) # Multiplica 2 matrizes, como já dito, por questões de praticidade definimos que somente 2 matrizes serão multiplicadas 

        StringResponse = [[str(ele) for ele in sub] for sub in response] # Transforma a matriz resultante numa string
        self.socket.sendto(str(StringResponse).encode(),self.Ad) # Devolve a matriz resultante
        global requestinappointment 
        print('Dentro da Funcao antes: ', requestinappointment)
        requestinappointment -= 1 # Diz ao programa principal que uma requisição local foi encerrada
        print('Dentro da Funcao depois: ', requestinappointment)
        t2 = time.time() # Usado para checar tempo durante testes locais (pode ser removido)
        t = t2 - t1 # Usado para checar tempo durante testes locais (pode ser removido)
        cmd = "echo {0}, {1}, >> data2.csv".format(t, libc.syscall(SYS_gettid)) # Usado para checar tempo durante testes locais (pode ser removido)
        os.system(cmd) # Usado para checar tempo durante testes locais (pode ser removido)

        
class ThreadProc(threading.Thread): # Thread que vai lidar com a criação de um suprocesso para realizar a conexão TCP
    def __init__(self,Message,Conn,SocketUdp,Udpad): # Recebe e armazena a mensagem recebida com as matrizes, a conexão com um dos servidores parceiros, o socket UDP e o endereço do remetente
        threading.Thread.__init__(self)
        self.Mess=Message
        self.TCP=Conn
        self.UDP=SocketUdp
        self.UDPAd=Udpad

    def run(self): # Inicia a thread que lida com a conexão TCP via subprocesso
        t1 = time.time() # Usado para calcular a tempo de processamento do parceiro
        filho=os.fork() # Cria um subprocesso
        if filho == 0: # O subprocesso irá entrar nessa condição, ou seja, tudo nessa condição será executado num subprocesso
            self.TCP.send(self.Mess) # Envia mensagem via TCP ao parceiro
            data = self.TCP.recv(1024) # Espera a mensagem do parceiro
            print(self.UDPAd) # Print para fins de teste (pode ser removido)
            self.UDP.sendto(data,self.UDPAd) # Devolve matriz resultante ao cliente via UDP, como o subprocesso não compartilha variáveis com a thread que o criou, utilizá-lo para devolver a metriz via UDP foi a solução que foi pensada, uma vez que o cliente não conseguiria diferenciar ser foi a thread UDP ou o subprocesso que devolveu o resultado.
        else: # A thread segue pelo else
            os.waitpid(filho,0) # Espera o subprocesso encerrar para continuar
            t2 = time.time() # Usado para calcular a tempo de processamento do parceiro
            t = t2 - t1 # calcula o tempo de processamento que o parceiro levou para processar.
            cmd = "echo {0}, {1}, >> data1.csv".format(t, filho) # Usado para checar tempo durante testes locais (pode ser removido)
            os.system(cmd) # Usado para checar tempo durante testes locais (pode ser removido)
            Array = literal_eval(self.Mess.decode()) # Assim como na thread UDP o trecho abaixo serve para transformar a mensagem em duas matrizes 
            matriz1 = []
            matriz2 = []

            # Pega a primeira matriz
            for i in Array[0]:
                matriz1.append(literal_eval(i))

            # Pega a segunda matriz
            for i in Array[1]:
                matriz2.append(literal_eval(i))
            tp = len(matriz1) * len(matriz2[0]) # Com as matrizes podemos calcular o tamanho do processamento
            td = t/tp # Calculo da taxa de desempenho
            global serverslist # variáveis globais usadas para guardar as filas de servidores
            global unavailablelist
            ind = -1

            for item in range(len(serverlist)): # Procura o servidor usado na lista de disponíveis
                if serverlist[item][0] == self.TCP:
                    ind = item
            
            if ind != -1: # Se encontrou o servidor atualiza a capacidade e a taxa de desempenho do servidor parceiro
                serverlist[ind][1] += 1
                serverlist[ind][2] = td
            else: # Senão procura ele na lista de indisponíveis
                for item in range(len(unavailablelist)):
                    if unavailablelist[item][0] == self.TCP:
                        ind = item
                unavailablelist[ind][1] += 1 # Atualiza a capacidade e a taxa de desempenho do servidor parceiro
                unavailablelist[ind][2] = td
                serverlist.append(unavailablelist.pop(ind)) # Remove da lista de indisponiveis e coloca na lista de disponíveis

            sorted(serverlist, key=itemgetter(2)) # Organiza a lista de servidores disponíveis de acordo com a taxa de desempenho deles

if __name__ == '__main__':
    # Variáveis locais que podem precisar ser alteradas
    global maxrequest # Requisições que o servidor principal consegue lidar de forma local
    global requestinappointment # Quantidade de requisições em andamento
    global serverslist # Lista de servidores indisponíveis
    global unavailablelist # Lista de servidores indisponíveis
    unavailablelist = []
    requestinappointment = 0
    maxrequest = 1
    serverlist = []
    LOCALHOST = socket.gethostbyname(socket.gethostname()) # Pega o ip do host
    PORT = 7006 #define a porta, nesse caso a porta 7006 será dedicada a conexão UDP do servidor
    server = socket.socket(family=socket.AF_INET ,type=socket.SOCK_DGRAM) #define o socket, onde, family=socket.AF_INET diz que será utilizado ipv4 e type=socket.SOCK_DGRAM define o socket como um socket UDP
    server.bind((LOCALHOST, PORT)) #vincula o ip e porta que serão usados
    print("Servidor iniciado!")
    print("Aguardando nova conexao..")
    print('servidor: ', server) # Prints para teste

    tcpServer = socket.socket(family=socket.AF_INET ,type=socket.SOCK_STREAM)#define o socket, onde, family=socket.AF_INET diz que será utilizado ipv4 e type=socket.SOCK_STREAM define o socket como um socket TCP
    PORT2 = 7027 #define a porta, nesse caso a porta 7027 será dedicada a conexão TCP do servidor
    tcpServer.bind((LOCALHOST, PORT2)) #vincula o ip e porta que serão usados
    for x in range(1): # espera por n servidores de acordo com o range desse for
        tcpServer.listen() # espera uma conexão TCP
        conn, addr = tcpServer.accept() # aceita conexão
        data = conn.recv(1024).decode("ascii") # recebe o a quantidade de requisições que o servidor parceiro suporta
        serverlist.append([conn,int(data),0]) # Coloca o servidor na lista de disponíveis, com sua capacidade e taxa de desempenho inicialmente definida para 0
    print(serverlist) 

    while True:
        rec=server.recvfrom(1024) #espera alguém mandar uma mensagem
        if requestinappointment < maxrequest: # ve se ainda pode ser processado no servidor
            newthread = Thread(rec[0],rec[1],server) #cria uma trhead e armazena nela (a mensagem recebida, o ip e porta de quem enviou, e o socket UDP para devolver a mensagem
            requestinappointment += 1 # indica que mais uma requisição está em andamento
        else: # cria thread para lidar com o subprocesso que conecta ao parceiro via TCP
            serverlist[0][1] -= 1 # tira capacidade do primeiro servidor da lista
            if serverlist[0][1] == 0: # se a capacidade do servidor se esgotar manda ele para a lista de indisponíveis
                unavailablelist.append(serverlist.pop(0))
            newthread = ThreadProc(rec[0],serverlist[0][0],server,rec[1]) #cria uma trhead e armazena nela (a mensagem recebida, a conexão do parceiro que irá processar, o socket UDP para enviar a resposta, e o ip e porta de quem enviou
        print('Dentro do Main: ', requestinappointment)
        newthread.start() #inicia a thread