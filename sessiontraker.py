import time
from datetime import datetime
from portfolio import TransactionProcessor

class SessionTracker:

    def __init__(self, account, client_id, seen_transactions=None):
        self.account = account
        self.client_id = client_id
        if not transaction_list:
            self.seen_transactions = []
        self.tick_rate = 60

    def monitor(self):
        while self.session_running == True:
            time.sleep(self.tick_rate)
            self.tick()

    def get_new_transactions(self):
        ameritrade = Ameritrade(self.account, self.client_id)
        today = datetime.now().strftime("%Y-%m-%d")
        today = '2018-07-27'#for testing remove
        transactions_json = ameritrade.get_transactions(today, today)
        processor = TransactionProcessor(transactions_json)

        new_transactions = []
        for transaction in processor.transaction_list:
        if transaction.transaction_id not in self.seen_transactions:
            new_transactions.append(transaction)
            self.seen_transactions.append(transaction)
        return new_transactions

    def notify(self, transactions):
        '''Notify userlist that a transaction has been made.'''
        pass

    def tick(self):
        '''Perform actions on a preset time basis.'''
        new_transactions = self.get_new_transactions()
        self.notify(new_transactions)
        pass

    def close_sessions(self):
        '''End monitoring, default to end at 4pm (End of trading day).'''
        pass




if __name__ == "__main__":
    from privateinfo import MainAccount, SecondAccount, client_id
    tracking_session = SessionTracker(MainAccount, client_id)