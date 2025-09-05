# Sistema Bancário (Python) — V1 e V2

Projeto do Bootcamp **Suzano | DIO**. Este repositório contém:
- **V1**: `banco.py` — depósito, saque e extrato.
- **V2 (recomendada)**: `bancov2.py` — versão modular com usuários e contas.

> **Para testar a versão mais completa (V2):** `python bancov2.py`

---

## Regras comuns
- Depósito apenas com valores **positivos**.
- Saque: **máx. 3 por sessão** e **até R$ 500,00 por saque**.
- Extrato: lista movimentações e mostra o **saldo** em `R$ xxx.xx`.

---

## Como executar (Windows / PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# V1:
python banco.py

# V2 (recomendada):
python bancov2.py
