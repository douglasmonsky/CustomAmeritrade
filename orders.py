class Orders:

    def __init__(self, ameritrade_json):
        self.all_orders = ameritrade_json['securitiesAccount']['orderStrategies']
        # self.seen_order_ids = [order['orderId'] for order in self.orders_data]
        self.seen_order_ids = []
        self.active_orders_ids= []

    def get_new_orders(self, ameritrade_json):
        orders = ameritrade_json['securitiesAccount']['orderStrategies']
        new_orders = []
        for order in orders:
            order_id = order['orderId']
            if order_id not in self.seen_order_ids:
                new_orders.append(order)
                if order['status'] == "QUEUED":
                    self.active_order_ids.append(order_id)
                self.seen_order_ids.append(order_id)
        return new_orders

