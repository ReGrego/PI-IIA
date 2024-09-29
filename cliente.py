import socket

HOST = '127.0.0.1'  
PORT = 24000        

def realizar_login():
    login = input("Login: ")
    senha = input("Senha: ")
    return f"LOGIN {login} {senha}"

def menu():
    print("\nCaixa Eletrônico:")
    print("1. Sacar")
    print("2. Depositar")
    print("3. Visualizar saldo")
    print("4. Sair")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao:
    conexao.connect((HOST, PORT))

    while True:
        requisicao_login = realizar_login()
        conexao.sendall(requisicao_login.encode())

        resposta = conexao.recv(1024).decode()
        print(f"{resposta}")

        if resposta == "Login bem-sucedido.":
            break  
        else:
            print("Tente novamente.\n")

    while True:
        menu()
        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            valor = input("Digite o valor que deseja sacar: ")
            requisicao = f"SAQUE {valor}"

        elif opcao == '2':
            valor = input("Digite o valor que deseja depositar: ")
            requisicao = f"DEPOSITO {valor}"

        elif opcao == '3':
            requisicao = "SALDO"

        elif opcao == '4':
            print("Encerrando a sessão...")
            print('Sessão encerrada.')
            break

        else:
            print("Opção inválida.")
            continue

        conexao.sendall(requisicao.encode())
        data = conexao.recv(1024)

        print(f"{data.decode()}")
