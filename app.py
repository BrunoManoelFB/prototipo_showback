import csv
from pathlib import Path
import streamlit as st
from allocation_engine import calculate

def load(name):
    with open(Path(__file__).parent / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

st.title("Protótipo de Showback")
st.write("Distribuição demonstrativa de custos de infraestrutura por produto.")
try:
    rows, totals, total_in, total_out = calculate(load("resources.csv"), load("consumption.csv"))
    a, b, c = st.columns(3)
    a.metric("Custo informado", f"R$ {total_in:,.2f}")
    b.metric("Custo alocado", f"R$ {total_out:,.2f}")
    c.metric("Conciliação", "OK" if total_in == total_out else "Divergente")
    st.subheader("Custo por produto")
    st.dataframe([{"Produto": k, "Custo (R$)": float(v)} for k, v in totals.items()],
                 use_container_width=True, hide_index=True)
    st.subheader("Detalhamento")
    st.dataframe([{"Recurso": x["resource_id"], "Descrição": x["description"],
                   "Produto": x["product_id"], "Valor (R$)": float(x["allocated_cost"])}
                  for x in rows], use_container_width=True, hide_index=True)
except Exception as e:
    st.error(str(e))
