import pytest
from decimal import Decimal
from allocation_engine import allocate_shared

def test_proportional_allocation():
    assert allocate_shared("100", {"A": 1, "B": 3}) == {
        "A": Decimal("25.00"), "B": Decimal("75.00")}

def test_rounding_preserves_total():
    result = allocate_shared("10", {"A": 1, "B": 1, "C": 1})
    assert sum(result.values()) == Decimal("10.00")

def test_zero_consumption_fails():
    with pytest.raises(ValueError):
        allocate_shared("10", {"A": 0, "B": 0})
