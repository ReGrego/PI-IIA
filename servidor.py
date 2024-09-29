import socket

# Servidor
HOST = 'localhost'  
PORT = 24000        

# LOGIN
login_valido = 'RENATA'
senha_valida = '123456'

# Saldo inicial 
saldo = 0

def verificar_login_senha(requisicao):
    
    partes = requisicao.split()
    if len(partes) == 3 and partes[0] == 'LOGIN':
        login = partes[1]
        senha = partes[2]
        if login == login_valido and senha == senha_valida:
            return True
    return False

def processar_requisicao(requisicao):
    global saldo

    
    if requisicao.startswith('SAQUE'):
        valor = float(requisicao.split()[1])
        if valor > saldo:
            return "Saldo insuficiente."
        else:
            saldo -= valor
            return f"Saque de R${valor:.2f} realizado com sucesso. Saldo atual: R${saldo:.2f}"
    
    elif requisicao.startswith('DEPOSITO'):
        valor = float(requisicao.split()[1])
        saldo += valor
        return f"Depósito de R${valor:.2f} realizado com sucesso. Saldo atual: R${saldo:.2f}"

    elif requisicao == 'SALDO':
        return f"Saldo atual: R${saldo:.2f}"

    else:
        return "Operação inválida."

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockobj:
    
    sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sockobj.bind((HOST, PORT))
    sockobj.listen()
    print(f"Servidor ativo e aguardando conexões na porta {PORT}...")

    while True:
        conn, addr = sockobj.accept()
        with conn:
            print(f"Conectado a {addr}")

            login_sucesso = False  

            while not login_sucesso:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break  

                    requisicao_login = data.decode()

                    if verificar_login_senha(requisicao_login):
                        conn.sendall("Login bem-sucedido.".encode())
                        login_sucesso = True  
                    else:
                        conn.sendall("Login ou senha incorretos.".encode())

                except Exception as e:
                    print(f"Erro ao processar login: {e}")
                    conn.sendall("Erro no servidor.".encode())

            while login_sucesso:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break  

                    requisicao = data.decode()
                    print(f"Recebido: {requisicao}")

                    resposta = processar_requisicao(requisicao)
                    conn.sendall(resposta.encode())
                except Exception as e:
                    print(f"Erro ao processar operação: {e}")
                    break
