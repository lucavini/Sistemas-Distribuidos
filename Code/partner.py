import socket
import subprocess
from ast import literal_eval

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

host_docker = socket.gethostbyname('ipc_server_dns_name')

print('meu ip: ', host_docker)

HOST = host_docker
maxqtd = 20
PORT = 7002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
    s.connect((HOST, PORT))
    s.send(str(maxqtd).encode())
    while True: 
        data = s.recv(1024)
        Array = literal_eval(data.decode())
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

        response = multMatriz(matriz1, matriz2)
        print('Matriz multiplicada: ',response)

        StringResponse = [[str(ele) for ele in sub] for sub in response]
        print(len(str(StringResponse)))
        s.send(str(StringResponse).encode())