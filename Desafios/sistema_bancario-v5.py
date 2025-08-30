from datetime import datetime, date

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

# Decorador para log
def log_to_file(func):
    def wrapper(*args, **kwargs):
        # Capturar data e hora
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Capturar argumentos
        args_str = ", ".join(str(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        args_full = f"{args_str}" if not kwargs_str else f"{args_str}, {kwargs_str}" if args_str else kwargs_str
        # Executar a função e capturar o retorno
        result = func(*args, **kwargs)
        # Preparar a entrada de log
        log_entry = f"{timestamp} - Função: {func.__name__} - Argumentos: {args_full} - Retorno: {result}\n"
        # Salvar no arquivo
        with open("log.txt", "a") as file:
            file.write(log_entry)
        return result
    return wrapper

# Classe Cliente
class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = ''.join(filter(str.isdigit, cpf))  # Apenas números
        self.endereco = endereco

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"

# Classe Conta
class Conta:
    LIMITE_TRANSACOES_DIARIAS = 10

    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.limite = 500
        self.extrato = []
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
        self.transacoes_diarias = 0
        self.ultima_data = date.today()

    @log_to_file
    def depositar(self, valor):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        if self.transacoes_diarias >= self.LIMITE_TRANSACOES_DIARIAS:
            return "Erro: Limite de 10 transações diárias atingido!"
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"{data_hora} - Depósito de R$ {valor:.2f} efetuado.")
            self.transacoes_diarias += 1
            print(f"Depósito de R$ {valor:.2f} efetuado com sucesso!")
            return None  # Retorno explícito para consistência
        else:
            return "Valor inválido! O depósito deve ser maior que zero."

    @log_to_file
    def sacar(self, valor):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        if self.transacoes_diarias >= self.LIMITE_TRANSACOES_DIARIAS:
            return "Erro: Limite de 10 transações diárias atingido!"
        if self.numero_saques >= self.LIMITE_SAQUES:
            return "Você atingiu o limite de saques!"
        elif valor > self.saldo:
            return "Saldo insuficiente!"
        elif valor > self.limite:
            return f"Valor excede o limite de R$ {self.limite:.2f} por saque!"
        elif value <= 0:  # Corrigido de 'value' para 'valor'
            return "Valor inválido! O saque deve ser maior que zero."
        else:
            self.saldo -= valor
            self.extrato.append(f"{data_hora} - Saque de R$ {valor:.2f} efetuado.")
            self.numero_saques += 1
            self.transacoes_diarias += 1
            print(f"Saque de R$ {valor:.2f} efetuado com sucesso!")
            return None  # Retorno explícito para consistência

    @log_to_file
    def gerar_extrato(self):
        data_atual = date.today()
        if data_atual > self.ultima_data:
            self.transacoes_diarias = 0
            self.ultima_data = data_atual
        print("\n===== EXTRATO =====")
        if not self.extrato:
            print("Nenhuma movimentação realizada.")
        else:
            for item in self.extrato:
                print(item)
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        return None  # Retorno explícito para consistência

# Variáveis globais
usuarios = []  # Lista de objetos Cliente
contas = []    # Lista de objetos Conta
numero_conta_sequencial = 1

# Loop principal
while True:
    try:
        opcao = int(input(menu))
        
        if opcao == 1:  # Depositar
            numero_conta = int(input("Número da conta: "))
            valor = float(input("R$ "))
            conta_encontrada = next((conta for conta in contas if conta.numero_conta == numero_conta), None)
            if conta_encontrada:
                resultado = conta_encontrada.depositar(valor)
                if resultado:
                    print(resultado)
            else:
                print("Conta não encontrada!")

        elif opcao == 2:  # Sacar
            numero_conta = int(input("Número da conta: "))
            valor = float(input("R$ "))
            conta_encontrada = next((conta for conta in contas if conta.numero_conta == numero_conta), None)
            if conta_encontrada:
                resultado = conta_encontrada.sacar(valor)
                if resultado:
                    print(resultado)
            else:
                print("Conta não encontrada!")

        elif opcao == 3:  # Extrato
            numero_conta = int(input("Número da conta: "))
            conta_encontrada = next((conta for conta in contas if conta.numero_conta == numero_conta), None)
            if conta_encontrada:
                conta_encontrada.gerar_extrato()
            else:
                print("Conta não encontrada!")

        elif opcao == 4:  # Cadastrar Usuário
            nome = input("Nome: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            cpf = input("CPF (somente números ou com pontos/hífen): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/estado): ")
            # Verificar se CPF já existe
            if not any(usuario.cpf == ''.join(filter(str.isdigit, cpf)) for usuario in usuarios):
                novo_usuario = Cliente(nome, data_nascimento, cpf, endereco)
                usuarios.append(novo_usuario)
                print(f"Usuário {nome} cadastrado com sucesso!")
            else:
                print("Erro: CPF já cadastrado!")

        elif opcao == 5:  # Cadastrar Conta Corrente
            cpf = input("CPF do usuário (somente números ou com pontos/hífen): ")
            cpf = ''.join(filter(str.isdigit, cpf))
            usuario_encontrado = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)
            if usuario_encontrado:
                nova_conta = Conta("0001", numero_conta_sequencial, usuario_encontrado)
                contas.append(nova_conta)
                print(f"Conta {numero_conta_sequencial} (agência 0001) criada com sucesso para {usuario_encontrado.nome}!")
                numero_conta_sequencial += 1
            else:
                print("Erro: Usuário com este CPF não encontrado!")

        elif opcao == 6:  # Listar Contas
            print("\n===== CONTAS CADASTRADAS =====")
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                for conta in contas:
                    print(f"Agência: {conta.agencia}, Conta: {conta.numero_conta}, Usuário: {conta.cliente.nome}")

        elif opcao == 7:  # Sair
            print("Operação finalizada!")
            break
        
        else:
            print("Operação inválida, por favor selecione novamente.")
    
    except ValueError:
        print("Erro: Digite um valor numérico válido!")