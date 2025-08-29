# Menu do sistema
menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Usuário
[5] Cadastrar Conta Corrente
[6] Listar Contas
[7] Sair
=> """

# Variáveis globais
saldo: float = 0
limite: float = 500
extrato: list[str] = []
numero_saques: int = 0
LIMITE_SAQUES: int = 3
usuarios: list[dict] = []  # Lista para armazenar usuários
contas: list[dict] = []  # Lista para armazenar contas
numero_conta_sequencial: int = 1  # Contador para números de conta

# Função para depósito (argumentos posicionais)
def depositar(valor: float, /, *, saldo: float, extrato: list) -> tuple[float, list]:
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito de R$ {valor:.2f} efetuado.")
        print(f"Depósito de R$ {valor:.2f} efetuado com sucesso!")
    else:
        print("Valor inválido! O depósito deve ser maior que zero.")
    return saldo, extrato

# Função para saque (argumentos apenas por nome)
def sacar(*, valor: float, saldo: float, extrato: list, limite: float, numero_saques: int, limite_saques: int) -> tuple[float, list, int]:
    if numero_saques >= limite_saques:
        print("Você atingiu o limite de saques!")
    elif valor > saldo:
        print("Saldo insuficiente!")
    elif valor > limite:
        print(f"Valor excede o limite de R$ {limite:.2f} por saque!")
    elif valor <= 0:
        print("Valor inválido! O saque deve ser maior que zero.")
    else:
        saldo -= valor
        extrato.append(f"Saque de R$ {valor:.2f} efetuado.")
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} efetuado com sucesso!")
    return saldo, extrato, numero_saques

# Função para extrato (argumentos posicionais e nomeados)
def extrato(saldo: float, /, *, extrato: list) -> None:
    print("\n===== EXTRATO =====")
    if not extrato:
        print("Nenhuma movimentação realizada.")
    else:
        for item in extrato:
            print(item)
    print(f"\nSaldo atual: R$ {saldo:.2f}")

# Função para cadastrar usuário
def cadastrar_usuario(nome: str, data_nascimento: str, cpf: str, endereco: str, usuarios: list) -> list:
    # Remover caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verificar se o CPF já existe
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Erro: CPF já cadastrado!")
            return usuarios
    
    # Criar novo usuário
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    usuarios.append(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")
    return usuarios

# Função para cadastrar conta corrente
def cadastrar_conta(agencia: str, numero_conta: int, cpf: str, usuarios: list, contas: list) -> tuple[list, int]:
    # Verificar se o CPF existe
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            break
    
    if not usuario_encontrado:
        print("Erro: Usuário com este CPF não encontrado!")
        return contas, numero_conta
    
    # Criar nova conta
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario_encontrado
    }
    contas.append(conta)
    print(f"Conta {numero_conta} (agência {agencia}) criada com sucesso para {usuario_encontrado['nome']}!")
    numero_conta += 1  # Incrementar número sequencial
    return contas, numero_conta

# Função para listar contas
def listar_contas(contas: list) -> None:
    print("\n===== CONTAS CADASTRADAS =====")
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']}")

# Loop principal
while True:
    try:
        opcao = int(input(menu))
        
        if opcao == 1:  # Depositar
            valor = float(input("R$ "))
            saldo, extrato = depositar(valor, saldo=saldo, extrato=extrato)
        
        elif opcao == 2:  # Sacar
            valor = float(input("R$ "))
            saldo, extrato, numero_saques = sacar(
                valor=valor,
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        
        elif opcao == 3:  # Extrato
            extrato(saldo, extrato=extrato)
        
        elif opcao == 4:  # Cadastrar Usuário
            nome = input("Nome: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            cpf = input("CPF (somente números ou com pontos/hífen): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/estado): ")
            usuarios = cadastrar_usuario(nome, data_nascimento, cpf, endereco, usuarios)
        
        elif opcao == 5:  # Cadastrar Conta Corrente
            cpf = input("CPF do usuário (somente números ou com pontos/hífen): ")
            cpf = ''.join(filter(str.isdigit, cpf))  # Limpar CPF
            contas, numero_conta_sequencial = cadastrar_conta(
                agencia="0001",
                numero_conta=numero_conta_sequencial,
                cpf=cpf,
                usuarios=usuarios,
                contas=contas
            )
        
        elif opcao == 6:  # Listar Contas
            listar_contas(contas)
        
        elif opcao == 7:  # Sair
            print("Operação finalizada!")
            break
        
        else:
            print("Operação inválida, por favor selecione novamente.")
    
    except ValueError:
        print("Erro: Digite um valor numérico válido!")
