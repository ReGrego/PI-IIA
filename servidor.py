from socket import *

#Configura a Conexão
HOST = 'localhost'
PORTA = 24000

 #Estabelece a conexão
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((HOST, PORTA))
sockobj.listen(1)

# Dados de login
login_data = {
    '1152021100080': '123456'
}

while True:
    #Aceita conexão do cliente 
    conexao, endereco = sockobj.accept()
    print('Conectado', endereco)
    
    while True:
        #Recebe informação e decodifica para string
         data = conexao.recv(1024)
         print("Cliente: ", data.decode())
        
        #Envia uma resposta codificada
         resposta = "Executado";
         conexao.send(resposta.encode())

         print('Desconectado', endereco)
         conexao.close()

         user, password = data.decode().split(',')
         if login_data.get(user) == password:
          conexao.sendall(b'Login bem-sucedido')
         else:
          conexao.sendall(b'Usuario ou senha incorreta')