import time
from ameritrade import Ameritrade
from datetime import datetime
from portfolio import TransactionProcessor
from notify import Email

class SessionTracker:

    def __init__(self, account, client_id, username, password, recepients, seen_transactions=None, endtime='16:00'):
        self.account = account
        self.client_id = client_id
        self.username = username
        self.password = password
        self.recepients = recepients
        self.seen_transactions = seen_transactions
        if not self.seen_transactions:
            self.seen_transactions = []
        self.endtime = datetime.strptime(endtime, '%H:%M').time()
        self.session_running = False
        self.tick_rate = 60
        self.ameritrade = Ameritrade(self.account, self.client_id)
        self.starting_data = self.get_position_data()

    def get_position_data(self):
        positions_json = self.ameritrade.get_account_positions()
        return positions_json

    def monitor(self):
        self.session_running = True
        while self.session_running == True:
            self.tick()
            time.sleep(self.tick_rate)
            

    def get_new_transactions(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today = '2018-07-27'#for testing remove
        transactions_json = self.ameritrade.get_transactions(today, today)
        processor = TransactionProcessor(transactions_json)

        new_transactions = []
        for transaction in processor.transaction_list:
            if transaction.transaction_id not in self.seen_transactions:
                new_transactions.append(transaction)
                self.seen_transactions.append(transaction)
        return new_transactions

    def notify(self, transactions, username=None, password=None, recepients=None):
        '''Notify userlist that a transaction has been made.'''
        if not username:
            username = self.username
        if not password:
            password = self.password
        if not recepients:
            recepients = self.recepients
        email = Email(f'trades detected on {self.account.nickname}')
        email.construct_trade_text(transactions)
        email.send_email(username, password, recepients)

    def tick(self):
        '''Perform actions on a preset time basis.'''
        new_transactions = self.get_new_transactions()
        self.notify(new_transactions)
        now = datetime.now().time()
        if now > self.endtime:
            self.close_session()

    def close_session(self):
        '''End monitoring, default to end at 4pm (End of trading day).'''
        position_json = self.get_position_data()
        email = Email(f'{self.account.nickname} end of day report')
        email.construct_positions_text(position_json, self.endtime.strftime("%H:%M"))
        email.send_email(self.username, self.password, self.recepients)
        self.session_running = False





if __name__ == "__main__":
    from privateinfo import MainAccount, SecondAccount, client_id, gmail_username, gmail_password, send_to_email
    tracking_session = SessionTracker(MainAccount, client_id, gmail_username, gmail_password, [send_to_email])
    tracking_session.monitor()