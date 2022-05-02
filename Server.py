import socketserver #Esta biblioteca tenta capturar os vários aspectos da definição de um servidor baseados em socket
import threading #Importação da biblioteca threading constrói interfaces de threading.
import time #Importação da biblioteca Time, que é utilizada pra fazer o calculo dos tempos no código.

print("SERVIDOR UDP INICIADO") # Exibe na tela a mensagem "SERVIDOR UDP INICIADO"

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):#Declaração do classe "ThreadedUDPRequestHandler" que recebe como parâmetro "socketserver.BaseRequestHandler"
    
    def handle(self): #Declaração do método "handle"
        data = self.request[0].strip() #Declaração da variável "data" com a função "strip" voltada para strings, que tira os espaços em branco.
        socket = self.request[1] #Declaração da variável "socket" 
        current_thread = threading.current_thread() #Declaração da variável "current_thread" que recebe a Thread atual
        print("{}: Cliente: {}, Escreve: {}".format(current_thread.name, self.client_address, data)) #Exibe na tela a Thread e o número dela, O IP e Porta utilizados, e a mensagem enviada pelo cliente.
        socket.sendto(data.upper(), self.client_address) # O socket envia a resposta ao Cliente por meio da função "sendto"

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer): # Declaração do classe "ThreadedUDPServer" que apenas recebe os parâmetros "socketserver.ThreadingMixIn" e "socketserver.UDPServer"
    pass

if __name__ == "__main__":# Inicio da execução do código
    UDP_IP_ADDRESS = "127.0.0.1" # Este é o IP que o Servidor está sendo associado
    UDP_PORT_NO = 6789 # A porta que o Servidor vai ficar escutando.

    server = ThreadedUDPServer((UDP_IP_ADDRESS, UDP_PORT_NO), ThreadedUDPRequestHandler) # A varável "server" recebe a classe "ThreadedUDPServer", O Endereço e Porta e a primeira classe "ThreadedUDPRequestHandler"
    server_thread = threading.Thread(target=server.serve_forever) # Recebe a Thread e ocorre a chamada de "server.serve_forever"
    server_thread.daemon = True # Variável Booleana e recebe "True"

    try: # Tenta fazer a execução do código
        server_thread.start() #A Thread é iniciada
        print("Servidor iniciado no endereço {} e na porta {}".format(UDP_IP_ADDRESS, UDP_PORT_NO))# Exibe na tela a mensagem "Servidor iniciado no endereço {} e na porta {}"
        while True: #Loop infinito que deixa o servidor sempre ativo
            time.sleep(2)# Tempo da Thread dormir, caso o Loop não seja infinito
    except (KeyboardInterrupt, SystemExit):#Caso o código dê algum erro
        server.shutdown()#Desliga o Server
        server.server_close()#Fecha o Server
        exit()#O código said execução