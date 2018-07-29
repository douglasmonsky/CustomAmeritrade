from portfolio import TransactionProcessor

class SessionTracker:

    def __init__(self, Ameritrade, transaction_list=None):
        if not transaction_list:
            self.transaction_list = []
        pass

    def monitor(self):
        pass

    def notify(self):
        '''Notify userlist that a transaction has been made.'''
        pass

    def tick(self):
        '''Perform actions on a preset time basis.'''
        pass

    def close_sessions(self):
        '''End monitoring, default to end at 4pm (End of trading day).'''
        pass
