import pytest
from order import Order
from sample_orders import sample_orders2

class TestOrder:

    def test_init_values(self):
        for order in sample_orders2:
            Order(order)

    def test_avg_price(self):
        for order in sample_orders2:
            order_obj = Order(order)
            avg_price = order_obj.calc_avg_price()
            assert avg_price > 0

