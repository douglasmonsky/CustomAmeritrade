from ameritrade import Ameritrade
from privateinfo import MainAccount, SecondAccount


class Portfolio:

    def __init__(self, transactions=None):
        if not transactions:
            transactions = []
        self.transactions = transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)


class TransactionProcessor:

    def __init__(self, ameritrade_json):
        self.ameritrade_json = ameritrade_json
        self.transaction_list = []

    def group_transactions(self):
        transactions = {}
        for transaction in self.ameritrade_json:
            transaction_type = transaction['type']
            if transaction_type not in transactions:
                transactions[transaction_type] = {}
            if transaction_type == 'TRADE':
                transaction_id = transaction['orderId']
            else:
                transaction_id = transaction['transactionId']
            if transaction_id not in transactions[transaction_type]:
                transactions[transaction_type][transaction_id] = []
            transactions[transaction_type][transaction_id].append(transaction)

        for transcation_type in transactions['TRADE']:
            print(transaction_type)
            for transaction_id, transaction_pieces in transaction_type.items():
                self.transaction_list.append(Transaction(transaction_id, transaction_pieces))


class Transaction:

    def __init__(self, transaction_id, transaction_pieces):
        self.transaction_id = transaction_id
        self.transaction_pieces = transaction_pieces

    def calculate_fees(self):
        fees = 0
        for transaction in self.transaction_pieces:
            fees += sum(transaction['fees'].values())
        # fees = sum([sum(transaction['fees'].values()) for transaction in self.transaction_pieces])
        return round(fees, 2)
        
    def calculate_net(self):
        net = 0
        for transaction in self.transaction_pieces:
            net += transaction['netAmount']
        return round(net, 2)

class Trade(Transaction):

    def __init__(self, transaction_pieces):
        super().__init__(transaction_pieces)

if __name__ == '__main__':
    ameritrade = Ameritrade(MainAccount.account_id)
    transactions_json = ameritrade.get_transactions('2018-01-01', '2018-07-23')
    processer = TransactionProcessor(transactions_json)
    processer.group_transactions()
    for transaction in processer.transaction_list:
        print(transaction)
    # net_total = 0
    # for transaction_type in processer.transactions:
    #     for trade in processer.transactions[transaction_type].values():
    #         transaction = Transaction(trade)
    #         net_total += transaction.calculate_fees()
    # print(round(net_total, 2))