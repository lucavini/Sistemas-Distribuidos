import socket
import subprocess
from ast import literal_eval
#bibliotecas que foram utilizadas

def multMatriz(mat1, mat2): # função que recebe duas matrizes de tamanho qualquer e devolve a matriz resultante da multiplicação
        def getLinha(matriz, n):
            return [i for i in matriz[n]]  # ou simplesmente return matriz[n]

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

HOST = '172.17.0.7' # Este é o IP do Servidor no docker, precisa ser alterado antes de executar, por isso há prints no servidor principal para se saber qual ip colocar aqui.
# HOST = '127.0.1.1' # Este é o IP do Servidor executando local para testes antes de subir ao container.
maxqtd = 20 # quantidade de requisições que o parceiro suporta
PORT = 7027 #define a porta, nesse caso a porta 7027 será dedicada a conexão TCP do servidor parceiro ao principal.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
    s.connect((HOST, PORT)) # se conecta ao servidor principal
    s.send(str(maxqtd).encode()) # envia sua capacidade ao servidor principal
    while True: 
        data = s.recv(1024) # aguarda matriz do servidor principal
        Array = literal_eval(data.decode()) # converte a mensagem de string para uma lista de matrizes, a principio cada matriz ainda é uma string
        matriz1 = [] # Para os experimentos definimos que somente 2 matrizes serão multiplicadas
        matriz2 = []

        # Pega a primeira string e transforma na primeira matriz
        for i in Array[0]:
            matriz1.append(literal_eval(i))
        print('matriz1: ', matriz1)

        # Pega a segunda string e transforma na segunda matriz
        for i in Array[1]:
            matriz2.append(literal_eval(i))
        print('matriz2: ', matriz2)

        response = multMatriz(matriz1, matriz2)# Multiplica 2 matrizes, como já dito, por questões de praticidade definimos que somente 2 matrizes serão multiplicadas
        print('Matriz multiplicada: ',response)

        StringResponse = [[str(ele) for ele in sub] for sub in response]  # Transforma a matriz resultante numa string
        print(len(str(StringResponse))) # mostra o tamanho da string (usada para testes, pode ser removida)
        s.send(str(StringResponse).encode()) # Envia a matriz resultante para o servidor principal