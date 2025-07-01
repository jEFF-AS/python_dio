menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

valor: float = 0
saldo: float = 0
limite: float = 500
extrato: list[str] = []
numero_saques: int = 1
LIMITE_SAQUES = 3

while True:
    
    opcao = int(input(menu))
    
    if opcao == 1:
        valor = float(input("R$ "))
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito de R$ {valor} efetuado.")
            print(f"Depósito de R$ {valor} efetuado com sucesso!")
    
    elif opcao == 2:
        valor = float(input("R$ "))
        if numero_saques <= LIMITE_SAQUES:
            if valor <= saldo:
                saldo -= valor
                extrato.append(f"Saque de R$ {valor} efetuado.")
                numero_saques += 1
                print(f"Saque de R$ {valor} efetuado com sucesso!")
            else:
                print("Saldo insuficiente!")
        else:
            print("Voçê atingiu o limite de saque!")
        
    elif opcao == 3:
        print("\n===== EXTRATO =====")
        if extrato:
            for item in extrato:
                print(item)
        else: 
            print("Nenhuma movimentação realizada.")
        print(f"\nSaldo atual: R$ {saldo:.2f}")
            
    elif opcao == 4:
        print("Operação finalizada!")
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")