from socket import *

#Configuração Conexão
HOST = '127.0.0.1'
PORTA = 24000
 # Estabelece a conexão
conexao = socket(AF_INET, SOCK_STREAM)
conexao.connect((HOST, PORTA))


# Dados de login
usuario = '1152021100080'
senha = '123456'

socket.sendall(f'{usuario},{senha}'.encode())


while True:

    #Envia dados
    msg = input("Conectado")
    
    #Usa a função send para enviar os dados codificado
    conexao.send(msg.encode())
    #Recebe dados e decodifica para string novamente
    data = conexao.recv(1024)
    print('Servidor: ', data.decode())
    conexao.close()

    entradausuario = input('usuario: ')
    entradasenha = input('senha: ')

    if entradausuario == usuario and entradasenha == senha:
      print('Seja bem-vindo!')
    else:
      print('Usuario ou senha incorretos. Por favor, tente novamente.')  



    menu = """
    [1] Depositar
    [2] Sacar
    [3] Saldo
    [4] Sair

    => """

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu)

        if opcao == "d":
         print("Depósito")
         deposito = float(input("Digite o valor do depósito: "))
         saldo += deposito
         extrato.append(f"DEPOSITO: + R${deposito:.2f}.")
         print(f"Saldo atual da conta: {saldo}")

        elif opcao == "s":
         print("Saque")

         if numero_saques < LIMITE_SAQUES:
             if saldo >= limite:
                 valor_saque = float(input("Digite o valor de saque que deseja: "))
            
                 if valor_saque > limite:
                    print("O valor desejado excede o limite, tente outro valor.")
                 else:
                    numero_saques += 1 
                    extrato.append(f"SAQUE: -R${valor_saque:.2f} {numero_saques}/{LIMITE_SAQUES}.")
                    print("Saque realizado, retire o dinheiro")
             else:
              print("Não será possível sacar o dinheiro por falta de saldo")

         else: 
            print("Você não pode fazer mais saques hoje.")

        elif opcao == "e":
          print("Extrato") 

          if extrato:
            print("\n ========== EXTRATO =========")
            print('\n'.join(extrato))
            print("\n ============================")
            print(f"Saldo atual da conta: {saldo}")
          else:
            print("Não foram realizadas movimentações.")

        elif opcao == "q":
         break

        else:
         print("Operação inválida. Favor selecionar novamente a operação desejada.")