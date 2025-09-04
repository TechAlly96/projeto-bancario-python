# banco.py
# v1 — Sistema bancário simples: depósito, saque e extrato.
# Regras:
# - Depósito apenas com valores positivos.
# - Saque: no máximo 3 por dia/sessão e limite de R$ 500,00 por saque.
# - Extrato lista todas as movimentações e mostra o saldo final.

from datetime import datetime

LIMITE_SAQUES = 3
LIMITE_POR_SAQUE = 500.00

saldo = 0.0
numero_saques = 0
transacoes = []  # cada item: (tipo, valor, timestamp) — tipo: "DEPÓSITO" ou "SAQUE"

def formatar(valor: float) -> str:
    """Formata valores como R$ xxx.xx (ponto como separador decimal)."""
    return f"R$ {valor:.2f}"

def registrar(tipo: str, valor: float):
    """Armazena a movimentação com data/hora."""
    transacoes.append((tipo, valor, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

def depositar():
    global saldo
    try:
        valor = float(input("Valor do depósito: ").replace(",", "."))
    except ValueError:
        print("⚠ Valor inválido.")
        return

    if valor <= 0:
        print("⚠ Depósitos devem ser com valores POSITIVOS.")
        return

    saldo += valor
    registrar("DEPÓSITO", valor)
    print(f"✅ Depósito realizado: {formatar(valor)} | Saldo: {formatar(saldo)}")

def sacar():
    global saldo, numero_saques
    if numero_saques >= LIMITE_SAQUES:
        print(f"⚠ Limite diário de saques atingido ({LIMITE_SAQUES}).")
        return

    try:
        valor = float(input("Valor do saque: ").replace(",", "."))
    except ValueError:
        print("⚠ Valor inválido.")
        return

    if valor <= 0:
        print("⚠ O valor do saque deve ser POSITIVO.")
        return
    if valor > LIMITE_POR_SAQUE:
        print(f"⚠ Limite por saque é de {formatar(LIMITE_POR_SAQUE)}.")
        return
    if valor > saldo:
        print("⚠ Saldo insuficiente para realizar o saque.")
        return

    saldo -= valor
    numero_saques += 1
    registrar("SAQUE", -valor)
    print(f"✅ Saque realizado: {formatar(valor)} | Saldo: {formatar(saldo)} "
          f"| Saques hoje: {numero_saques}/{LIMITE_SAQUES}")

def extrato():
    print("\n====== EXTRATO ======")
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for tipo, valor, ts in transacoes:
            sinal = "" if valor >= 0 else "-"
            print(f"{ts} | {tipo:<8} | {sinal}{formatar(abs(valor))}")
    print("---------------------")
    print(f"SALDO ATUAL: {formatar(saldo)}")
    print("=====================\n")

def menu():
    print("""
[d] Depósito
[s] Saque
[e] Extrato
[q] Sair
""")

if __name__ == "__main__":
    print("Bem-vindo ao Banco v1 🏦")
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "d":
            depositar()
        elif opcao == "s":
            sacar()
        elif opcao == "e":
            extrato()
        elif opcao == "q":
            print("Até mais! 👋")
            break
        else:
            print("⚠ Opção inválida. Tente de novo.")
