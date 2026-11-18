from decimal import Decimal, ROUND_DOWN
from collections import defaultdict

CENT = Decimal("0.01")

def allocate_shared(cost, consumers):
    cost = Decimal(str(cost)).quantize(CENT)
    weights = {str(k): Decimal(str(v)) for k, v in consumers.items()}
    if cost < 0 or not weights or any(v < 0 for v in weights.values()):
        raise ValueError("Custo ou consumo inválido.")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("A soma do consumo deve ser maior que zero.")
    exact = {k: cost * v / total for k, v in weights.items()}
    result = {k: v.quantize(CENT, rounding=ROUND_DOWN) for k, v in exact.items()}
    cents = int((cost - sum(result.values())) / CENT)
    order = sorted(weights, key=lambda k: (-(exact[k] - result[k]), k))
    for k in order[:cents]:
        result[k] += CENT
    return result

def calculate(resources, consumption):
    usage = defaultdict(dict)
    for row in consumption:
        rid, pid = row["resource_id"], row["product_id"]
        if pid in usage[rid]:
            raise ValueError("Consumo duplicado.")
        usage[rid][pid] = Decimal(str(row["consumption"]))
    rows = []
    totals = defaultdict(lambda: Decimal("0.00"))
    for r in resources:
        rid = r["resource_id"]
        cost = Decimal(str(r["cost"])).quantize(CENT)
        if cost < 0:
            raise ValueError("Custo negativo.")
        if r["allocation_type"] == "direct":
            portions = {r["direct_product_id"]: cost}
            if not r["direct_product_id"]:
                raise ValueError("Custo direto sem produto.")
        elif r["allocation_type"] == "shared":
            portions = allocate_shared(cost, usage.get(rid, {}))
        else:
            raise ValueError("Tipo deve ser direct ou shared.")
        for product, amount in portions.items():
            rows.append({"resource_id": rid, "description": r["description"],
                         "product_id": product, "allocated_cost": amount})
            totals[product] += amount
    input_total = sum((Decimal(str(r["cost"])) for r in resources), Decimal("0.00"))
    allocated_total = sum(totals.values(), Decimal("0.00"))
    return rows, dict(sorted(totals.items())), input_total, allocated_total
