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
        self.starttime = datetime.now().time()
        self.endtime = datetime.strptime(endtime, '%H:%M').time()
        self.session_running = False
        self.tick_rate = 60
        self.ameritrade = Ameritrade(self.account, self.client_id)
        self.starting_data = self.get_position_data()
        self.notify(self.starting_data, f'{self.account.nickname} start of day report', 'start_day')

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
        # today = '2018-07-27'#for testing remove
        transactions_json = self.ameritrade.get_transactions(today, today)
        processor = TransactionProcessor(transactions_json)

        new_transactions = []
        for transaction in processor.transaction_list:
            if transaction.transaction_id not in self.seen_transactions:
                new_transactions.append(transaction)
                self.seen_transactions.append(transaction.transaction_id)
        return new_transactions

    def notify(self, data, subject, notification_type):
        '''Notify userlist that a transaction has been made.'''
        email = Email(subject)
        if notification_type == 'trade':
            email.construct_trade_text(data)
        elif notification_type == 'end_day':
             email.construct_positions_text(data, self.endtime.strftime("%H:%M"))
        elif notification_type == 'start_day':
             email.construct_positions_text(data, self.starttime.strftime("%H:%M"), end_of_day=False)
        email.send_email(self.username, self.password, self.recepients)

    def tick(self):
        '''Perform actions on a preset time basis.'''
        new_transactions = self.get_new_transactions()
        if new_transactions:
            self.notify(new_transactions, f'trades detected on {self.account.nickname}', 'trade')
        now = datetime.now().time()
        if now > self.endtime:
            self.close_session()

    def close_session(self):
        '''End monitoring, default to end at 4pm (End of trading day).'''
        position_json = self.get_position_data()
        self.notify(position_json, f'{self.account.nickname} end of day report', 'end_day')
        self.session_running = False





if __name__ == "__main__":
    from privateinfo import MainAccount, SecondAccount, client_id, gmail_username, gmail_password, send_to_email
    tracking_session = SessionTracker(MainAccount, client_id, gmail_username, gmail_password, [send_to_email])
    # tracking_session.monitor()
    tracking_session2 = SessionTracker(SecondAccount, client_id, gmail_username, gmail_password, [send_to_email])
    # tracking_session2.monitor()

    while tracking_session.session_running == True and tracking_session2.session_running == True:
            tracking_session.tick()
            time.sleep(2)
            tracking_session2.tick()
            time.sleep(tracking_session.tick_rate)  