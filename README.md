# Sistema Bancário v1 (Python)

Desafio DIO: implementar **depósito**, **saque** e **extrato**.

### Regras
- Depósito apenas com valores **positivos**.
- Saque: **máx. 3 por sessão** e **até R$ 500,00 por saque**.
- Extrato: lista movimentações e **saldo atual** no formato `R$ xxx.xx`.

### Como executar (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python banco.py
