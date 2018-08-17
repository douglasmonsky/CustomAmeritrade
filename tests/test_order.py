import pytest
from order import Order
from sample_orders import sample_orders

class TestOrder:

    def test_init_values(self):
        for order in sample_orders:
            order_obj = Order(order)
            assert order_obj.session == 'NORMAL'
            assert type(order_obj.quant) is int

    def test_avg_price(self):
        pass
