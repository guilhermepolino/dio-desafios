class User:
    agencia_bancaria = 1
    numero_conta_atual = 1

    def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def criar_conta_corrente(self):
        nova_conta = ContaCorrente(self)
        self.contas.append(nova_conta)
        return nova_conta

class ContaCorrente:
    def __init__(self, usuario):
        self.numero_conta = usuario.numero_conta_atual
        self.saldo = 0
        self.usuario = usuario
        usuario.numero_conta_atual += 1

    def saque(self, *, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return self.saldo, self.extrato()
        else:
            return self.saldo, "Saldo insuficiente."

    def deposito(self, valor):
        self.saldo += valor
        return self.saldo, self.extrato()

    def extrato(self, *, saldo=False):
        if saldo:
            return self.saldo
        else:
            return f"Saldo da Conta Corrente {self.numero_conta}: R$ {self.saldo:.2f}"

usuarios_existentes = {}
contas_correntes = {}

acesso = """
[c] CONTA_CORRENTE
[n] Novo_usuário

==> """

while True:
    escolha = input(acesso)

    if escolha == 'c':
        cpf_login = input("Digite o CPF para acessar sua conta: ")
        if cpf_login in usuarios_existentes:
            usuario = usuarios_existentes[cpf_login]
            while True:
                opcao = input(f"""
                Olá, {usuario.nome}!
                Opções da Conta Corrente:
                [d] Depositar
                [s] Sacar
                [e] Extrato
                [v] Voltar

                => """)
                if opcao == 'd':
                    valor = float(input("Digite o valor a ser depositado: "))
                    saldo, extrato = usuario.criar_conta_corrente().deposito(valor)
                    print(f"Saldo após depósito: R$ {saldo:.2f}")
                    print(extrato)
                elif opcao == 's':
                    valor = float(input("Digite o valor a ser sacado: "))
                    saldo, extrato = usuario.criar_conta_corrente().saque(valor=valor)
                    print(f"Saldo após saque: R$ {saldo:.2f}")
                    print(extrato)
                elif opcao == 'e':
                    extrato = usuario.criar_conta_corrente().extrato(saldo=True)
                    print(f"Saldo da Conta Corrente: R$ {extrato:.2f}")
                elif opcao == 'v':
                    break
                else:
                    print("Opção inválida.")
        else:
            print("CPF não cadastrado. Use a opção 'n' para criar uma nova conta.")

    elif escolha == 'n':
        cpf = input("Digite o CPF: ")

        if cpf in usuarios_existentes:
            print("Este CPF já possui uma conta.")
        else:
            nome = input("Digite o nome: ")
            data_nascimento = input("Digite a data de nascimento: ")
            endereco = input("Digite o endereço: ")

            novo_usuario = User(cpf, nome, data_nascimento, endereco)
            print("Novo usuário criado:")
            print(f"Agência Bancária: {novo_usuario.agencia_bancaria}")
            print(f"CPF: {novo_usuario.cpf}")
            print(f"Nome: {novo_usuario.nome}")
            print(f"Data de Nascimento: {novo_usuario.data_nascimento}")
            print(f"Endereço: {novo_usuario.endereco}")

            usuarios_existentes[cpf] = novo_usuario

            opcao = input("""
            Deseja criar uma Conta Corrente para este usuário? (s/n): """)
            if opcao.lower() == 's':
                nova_conta = novo_usuario.criar_conta_corrente()
                print(f"Conta Corrente criada para o usuário {novo_usuario.nome}: {nova_conta.numero_conta}")

    else:
        print("Opção inválida. Digite 'c' ou 'n' para continuar.")
