import time
from ameritrade import Ameritrade
from datetime import datetime
from finviz import Finviz
from notify import Message
from orders import Orders
from portfolio import TransactionProcessor


class SessionTracker:

    def __init__(self, account, client_id, username, password, recepients,
                 seen_transactions=None, endtime='16:00', finviz_session=None):
        self.account = account
        self.client_id = client_id
        self.username = username
        self.password = password
        self.recepients = recepients
        self.seen_transactions = seen_transactions
        if not self.seen_transactions:
            self.seen_transactions = []
        self.starttime = datetime.now().time()
        self.endtime = datetime.strptime(endtime, '%H:%M').time()
        self.finviz_session = finviz_session
        self.session_running = False
        self.tick_rate = 60
        self.ameritrade = Ameritrade(self.account, self.client_id, print_auth=False)
        self.starting_data = self.get_position_data()
        self.orders = Orders(self.get_position_data('orders'))
        self.notify(self.starting_data, f'{self.account.nickname} start of day report', 'start_day')

    def close_session(self):
        '''End monitoring, default to end at 4pm (End of trading day).'''
        position_json = self.get_position_data()
        self.notify(position_json, f'{self.account.nickname} end of day report', 'end_day')
        self.session_running = False

    def get_new_orders(self, orders_info):
        return self.orders.get_new_orders(orders_info)

    def get_new_transactions(self):
        '''TRANSACTIONS DO NOT UPDATE LIVE, FOR LIVE UPDATES USE get_new_orders'''
        today = datetime.now().strftime("%Y-%m-%d")
        # today = '2018-07-27'#for testing remove
        transactions_json = self.ameritrade.get_transactions(today, today)
        processor = TransactionProcessor(transactions_json)

        new_transactions = []
        for transaction in processor.transaction_list:
            if transaction.transaction_id not in self.seen_transactions:
                new_transactions.append(transaction)
                self.seen_transactions.append(transaction.transaction_id)
        return new_transactions

    def get_position_data(self, data_type='positions'):
        positions_json = self.ameritrade.get_account_positions(data_type)
        return positions_json  

    def monitor(self):
        self.session_running = True
        while self.session_running == True:
            self.tick()
            time.sleep(self.tick_rate)

    def notify(self, data, subject, notification_type, data2=None, include_news=True):
        '''Notify userlist that a transaction has been made.'''
        message = Message(subject, finviz_session=self.finviz_session, end_line='<br />')
        if notification_type == 'orders':
            message.construct_orders_text(data, data2)
        elif notification_type == 'transactions':
            message.construct_trade_text(data)
        elif notification_type == 'end_day':
             message.construct_positions_text(data, self.endtime.strftime("%H:%M"))
        elif notification_type == 'start_day':
             message.construct_positions_text(data, self.starttime.strftime("%H:%M"), 
                                            end_of_day=False, include_news=include_news)
        message.send_message(self.username, self.password, self.recepients, html=True)

    def tick(self, tick_type='orders'):
        '''Perform actions on a preset time basis.'''
        if tick_type == 'orders':
            json = self.get_position_data('positions,orders')
            data = self.get_new_orders(json)
            data2 = json
        elif tick_type == 'transactions':
            data = self.get_new_transactions()
            data2 = None
        if data:
            self.notify(data, f'trades detected on {self.account.nickname}', tick_type, data2)
        now = datetime.now().time()
        if now > self.endtime:
            self.close_session()


if __name__ == "__main__":
    import privateinfo
    finviz_session = Finviz(True, privateinfo.finviz_username, privateinfo.finviz_password)
    tracking_session = SessionTracker(privateinfo.MainAccount, privateinfo.client_id,
                                      privateinfo.gmail_username, privateinfo.gmail_password,
                                      [privateinfo.send_to_email, privateinfo.send_to_email2],
                                      finviz_session=finviz_session)

    tracking_session2 = SessionTracker(privateinfo.SecondAccount, privateinfo.client_id,
                                       privateinfo.gmail_username, privateinfo.gmail_password,
                                       [privateinfo.send_to_email, privateinfo.send_to_email2],
                                       finviz_session=finviz_session)

    tracking_session.session_running = True 
    tracking_session2.session_running = True 
    while tracking_session.session_running and tracking_session2.session_running:
        try:
            tracking_session.tick()
            time.sleep(5)
            tracking_session2.tick()
            time.sleep(tracking_session.tick_rate)
        except Exception as e:
            print(e)
            time.sleep(30)
            continue  