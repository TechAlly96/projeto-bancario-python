# banco.py — V2
# Sistema bancário modular com:
# - Funções: depositar (positional-only), sacar (keyword-only), exibir_extrato (positional + keyword)
# - Usuários (cliente) e Contas (agência 0001, número sequencial, vínculo por CPF)
# - Operações atuam sobre a CONTA selecionada
# - Regras de saque: 3 por sessão/conta, e até R$ 500,00 por saque

from datetime import datetime

AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_POR_SAQUE = 500.00

# ----------------------------- UTIL ----------------------------- #
def formatar(valor: float) -> str:
    return f"R$ {valor:.2f}"

def agora_str() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# ------------------------ OPERAÇÕES BANCÁRIAS ------------------- #
def depositar(saldo, valor, extrato, /):
    """Positional-only: (saldo, valor, extrato) -> (saldo, extrato)"""
    if valor <= 0:
        print("⚠ Depósitos devem ser com valores POSITIVOS.")
        return saldo, extrato
    saldo += valor
    extrato += f"{agora_str()} | DEPÓSITO | {formatar(valor)}\n"
    print(f"✅ Depósito realizado: {formatar(valor)} | Saldo: {formatar(saldo)}")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Keyword-only: retorna (saldo, extrato, numero_saques)
    Regras: limite por saque e limite de quantidade
    """
    if numero_saques >= limite_saques:
        print(f"⚠ Limite de saques atingido ({limite_saques}).")
        return saldo, extrato, numero_saques
    if valor <= 0:
        print("⚠ O valor do saque deve ser POSITIVO.")
        return saldo, extrato, numero_saques
    if valor > limite:
        print(f"⚠ Limite por saque é de {formatar(limite)}.")
        return saldo, extrato, numero_saques
    if valor > saldo:
        print("⚠ Saldo insuficiente.")
        return saldo, extrato, numero_saques

    saldo -= valor
    numero_saques += 1
    extrato += f"{agora_str()} | SAQUE    | -{formatar(valor)}\n"
    print(
        f"✅ Saque realizado: {formatar(valor)} | Saldo: {formatar(saldo)} "
        f"| Saques: {numero_saques}/{limite_saques}"
    )
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """Positional + keyword-only: saldo (positional), extrato (keyword)"""
    print("\n====== EXTRATO ======")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato, end="")
    print("---------------------")
    print(f"SALDO ATUAL: {formatar(saldo)}")
    print("=====================\n")

# ----------------------- USUÁRIOS / CONTAS ---------------------- #
def somente_digitos(texto: str) -> str:
    return "".join(ch for ch in texto if ch.isdigit())

def filtrar_usuario(cpf: str, usuarios: list[dict]) -> dict | None:
    cpf = somente_digitos(cpf)
    for u in usuarios:
        if u["cpf"] == cpf:
            return u
    return None

def criar_usuario(usuarios: list[dict]):
    print("\n=== Novo usuário ===")
    cpf = somente_digitos(input("CPF (somente números): ").strip())
    if not cpf:
        print("⚠ CPF inválido.")
        return
    if filtrar_usuario(cpf, usuarios):
        print("⚠ Já existe usuário com esse CPF.")
        return

    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    logradouro = input("Logradouro: ").strip()
    nro = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    uf = input("UF (sigla): ").strip().upper()
    endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{uf}"

    usuarios.append(
        {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }
    )
    print("✅ Usuário criado com sucesso!")

def criar_conta(agencia: str, numero_conta: int, usuarios: list[dict], contas: list[dict]):
    print("\n=== Nova conta ===")
    cpf = somente_digitos(input("CPF do titular: ").strip())
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("⚠ Usuário não encontrado. Cadastre antes.")
        return

    conta = {
        "agencia": agencia,
        "numero": numero_conta,
        "usuario": usuario,          # vínculo
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
    }
    contas.append(conta)
    print(f"✅ Conta criada! Agência {agencia}  Conta {numero_conta:04d}  Titular: {usuario['nome']}")

def listar_contas(contas: list[dict]):
    if not contas:
        print("⚠ Não há contas cadastradas.")
        return
    print("\n=== Contas ===")
    for c in contas:
        print(
            f"Agência: {c['agencia']}  | Conta: {c['numero']:04d}  | "
            f"Titular: {c['usuario']['nome']}  | Saldo: {formatar(c['saldo'])}"
        )
    print()

def selecionar_conta(contas: list[dict]) -> dict | None:
    if not contas:
        print("⚠ Não há contas. Crie uma conta primeiro.")
        return None
    try:
        numero = int(input("Digite o número da conta (ex.: 1, 2, 3...): "))
    except ValueError:
        print("⚠ Número inválido.")
        return None
    for c in contas:
        if c["numero"] == numero:
            return c
    print("⚠ Conta não encontrada.")
    return None

# ----------------------------- MENU ----------------------------- #
def menu():
    print("""
[d] Depósito
[s] Saque
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[sc] Selecionar conta para operar
[q] Sair
""")

# ----------------------------- APP ------------------------------ #
def main():
    usuarios: list[dict] = []
    contas: list[dict] = []
    proximo_numero_conta = 1

    conta_atual: dict | None = None

    print("Bem-vindo ao Banco v2 🏦")

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "d":
            if not conta_atual:
                print("⚠ Selecione uma conta primeiro ([sc]) ou crie uma conta ([nc]).")
                continue
            try:
                valor = float(input("Valor do depósito: ").replace(",", "."))
            except ValueError:
                print("⚠ Valor inválido."); continue
            conta_atual["saldo"], conta_atual["extrato"] = depositar(
                conta_atual["saldo"], valor, conta_atual["extrato"]
            )

        elif opcao == "s":
            if not conta_atual:
                print("⚠ Selecione uma conta primeiro ([sc]) ou crie uma conta ([nc]).")
                continue
            try:
                valor = float(input("Valor do saque: ").replace(",", "."))
            except ValueError:
                print("⚠ Valor inválido."); continue

            conta_atual["saldo"], conta_atual["extrato"], conta_atual["numero_saques"] = sacar(
                saldo=conta_atual["saldo"],
                valor=valor,
                extrato=conta_atual["extrato"],
                limite=LIMITE_POR_SAQUE,
                numero_saques=conta_atual["numero_saques"],
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            if not conta_atual:
                print("⚠ Selecione uma conta primeiro ([sc]) ou crie uma conta ([nc]).")
                continue
            exibir_extrato(conta_atual["saldo"], extrato=conta_atual["extrato"])

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            criar_conta(AGENCIA, proximo_numero_conta, usuarios, contas)
            proximo_numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "sc":
            c = selecionar_conta(contas)
            if c:
                conta_atual = c
                print(
                    f"✅ Conta selecionada: Agência {c['agencia']} Conta {c['numero']:04d} — Titular: {c['usuario']['nome']}"
                )

        elif opcao == "q":
            print("Até mais! 👋")
            break

        else:
            print("⚠ Opção inválida. Tente de novo.")

if __name__ == "__main__":
    main()
