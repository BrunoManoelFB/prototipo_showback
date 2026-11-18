# Protótipo simples de Showback

Projeto acadêmico demonstrativo com dados fictícios.

- `allocation_engine.py`: cálculo dos custos.
- `app.py`: painel Streamlit.
- `resources.csv`: custos diretos e compartilhados.
- `consumption.csv`: consumo por produto.
- `test_allocation_engine.py`: testes básicos.

## Executar (Python 3.10+)

```bash
pip install -r requirements.txt
python -m pytest -v
streamlit run app.py
```

## Regra de negócio
Custos diretos são atribuídos integralmente ao produto informado. Custos compartilhados são rateados proporcionalmente ao consumo. O algoritmo distribui eventuais centavos residuais para que o total alocado seja igual ao custo informado.

## Resultado esperado
- P001 (Vendas): R$ 2.100,00
- P002 (Atendimento): R$ 1.675,00
- P003 (Logística): R$ 2.225,00
- Total: R$ 6.000,00

Os dados são sintéticos. O protótipo não representa implantação nem validação em organização real.
