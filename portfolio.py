import sqlite3
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
        self.group_transactions()

    def group_transactions(self):
        transactions = {}
        for transaction in self.ameritrade_json:
            transaction_type = transaction['type']
            if transaction_type == 'TRADE':
                transaction['transactionId'] = transaction['orderId']
            transaction_id = transaction['transactionId']
            if transaction_id not in transactions:
                transactions[transaction_id] = []
            transactions[transaction_id].append(transaction)

        for transaction_id, transaction_pieces in transactions.items():
            self.transaction_list.append(Transaction(transaction_id, transaction_pieces))

    def format_time(self, transaction, time_type, conversion_type=None):
        if not conversion_type:
            conversion_type = time_type
        if conversion_type != time_type and conversion_type == "transactionDate":
            transaction[time_type] = f'{transaction[conversion_type]} 00:00:00'
        else:
            transaction[time_type] = transaction[conversion_type].replace("T", " ").split("+")[0]   #"2018-07-26T15:25:29+0000" -->  "2018-07-26 15:25:29"


    def send_to_sql(self, db_name, transaction_list=None):
        if not transaction_list:
            transaction_list = self.transaction_list

        transactions = []
        for transaction in transaction_list:
            try:
                self.format_time(transaction, "transactionDate")
            except:
                self.format_time(transaction, "transactionDate", "settlementDate")


            data = (transactions['transactionId'], transactions['transactionDate'], transactions['netAmount'])
            transactions.append('')

        database = Database(db_name)

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


# class Trade(Transaction):

#     def __init__(self, transaction_pieces):
#         super().__init__(transaction_pieces)


if __name__ == '__main__':
    database = Database('MainAccount')
    columns = [('transaction_id', 'INTEGER'), ('date', 'TEXT'), ]
    database.create_table()
    ameritrade = Ameritrade(MainAccount)
    transactions_json = ameritrade.get_transactions('2018-01-01', '2018-07-23')
    processer = TransactionProcessor(transactions_json)
    processer.group_transactions()
    for transaction in processer.transaction_list:
        print(transaction.calculate_net())
    d
    # net_total = 0
    # for transaction_type in processer.transactions:
    #     for trade in processer.transactions[transaction_type].values():
    #         transaction = Transaction(trade)
    #         net_total += transaction.calculate_fees()
    # print(round(net_total, 2))