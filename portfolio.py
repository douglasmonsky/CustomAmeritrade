import sqlite3
from ameritrade import Ameritrade
from database import Database
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
            transaction_type = transaction_pieces[0]['type']
            if transaction_type == 'TRADE':
                transaction_obj = Trade(transaction_id, transaction_pieces)
            elif transaction_type == 'RECEIVE_AND_DELIVER':
                transaction_obj = RecieveAndDeliever(transaction_id, transaction_pieces)
            elif transaction_type == 'JOURNAL':
                transaction_obj = Journal(transaction_id, transaction_pieces)
            else:
                transaction_obj = Transaction(transaction_id, transaction_pieces)
            self.transaction_list.append(transaction_obj)
    

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

    def __init__(self, transaction_id, transaction_pieces, transaction_type=None, auto=True):
        self.transaction_id = transaction_id
        self.transaction_pieces = transaction_pieces
        self.transaction_type = transaction_type
        self.amount = 0
        self.symbol = 'N/A'

        if auto:
            self.fees = self.calculate_fees()
            self.net = self.calculate_net()
            # self.date_time = self.format_time()

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

    def format_time(self, time_type, conversion_type=None):
        if not conversion_type:
            conversion_type = time_type
        if conversion_type != time_type and conversion_type == "transactionDate":
            transaction[time_type] = f'{transaction[conversion_type]} 00:00:00'
        else:
            transaction[time_type] = transaction[conversion_type].replace("T", " ").split("+")[0]   #"2018-07-26T15:25:29+0000" -->  "2018-07-26 15:25:29"


class Journal(Transaction):

    def __init__(self, transaction_id, transaction_pieces, transaction_type='JOURNAL', auto=True):
        super().__init__(transaction_id, transaction_pieces, transaction_type, auto)


class Trade(Transaction):

    def __init__(self, transaction_id, transaction_pieces, transaction_type='TRADE', auto=True):
        super().__init__(transaction_id, transaction_pieces, transaction_type, auto)
        if auto:
            self.amount = self.calculate_amount()
            self.symbol = transaction_pieces[0]['transactionItem']['instrument']['symbol']

    def calculate_amount(self):
        amount = 0
        for transaction in self.transaction_pieces:
            piece_amount = transaction['transactionItem']['amount']
            piece_description = transaction['description']
            if piece_description == "TRADE CORRECTION":
                continue
            elif piece_description == "SELL TRADE":
                amount -= piece_amount
            else:
                amount += piece_amount  
        return amount


class RecieveAndDeliever(Transaction):

    def __init__(self, transaction_id, transaction_pieces, transaction_type='RECEIVE_AND_DELIVER', auto=True):
        super().__init__(transaction_id, transaction_pieces, transaction_type, auto)
        self.symbol = transaction_pieces[0]['transactionItem']['instrument']['symbol']


if __name__ == '__main__':
    # database = Database('MainAccount')
    # columns = [('transaction_id', 'INTEGER'), ('date', 'TEXT'), ]
    # database.create_table()
    ameritrade = Ameritrade(MainAccount)
    transactions_json = ameritrade.get_transactions('2018-01-01', '2018-07-23')
    processer = TransactionProcessor(transactions_json)
    for transaction in processer.transaction_list:
        # if transaction.transaction_id == '275581114':
        print(transaction.transaction_type, transaction.symbol, transaction.amount, transaction.net, transaction.transaction_id)

    # net_total = 0
    # for transaction_type in processer.transactions:
    #     for trade in processer.transactions[transaction_type].values():
    #         transaction = Transaction(trade)
    #         net_total += transaction.calculate_fees()
    # print(round(net_total, 2))