import sqlite3
import os
from ameritrade import Ameritrade
from database import Database


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
            print(transaction)
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

    def send_to_sql(self, db_name, table_name, transaction_list=None):
        if not transaction_list:
            transaction_list = self.transaction_list

        transactions = []
        for transaction in transaction_list:
            data = (transaction.transaction_id, transaction.transaction_type, transaction.symbol, 
                    transaction.date_time, transaction.net, transaction.fees, transaction.amount)
            transactions.append(data)

        database = Database(db_name)
        database.data_entry(table_name, transactions, executemany=True)


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
            try:
                self.date_time = self.format_time()
            except:
                self.date_time = self.format_time(conversion_type="settlementDate")

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

    def format_time(self, time_type="transactionDate", conversion_type=None):
        if not conversion_type:
            conversion_type = time_type
        if conversion_type != time_type and conversion_type == "transactionDate":
            date_time = f'{self.transaction_pieces[0][conversion_type]} 00:00:00'
        else:
            #"2018-07-26T15:25:29+0000" -->  "2018-07-26 15:25:29"
            date_time = self.transaction_pieces[0][conversion_type].replace("T", " ").split("+")[0]
        return date_time


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
    from privateinfo import MainAccount, SecondAccount, client_id
    # database = Database('MainAccount.db')
    # columns = [('transaction_id', 'TEXT'), ('transaction_type', 'TEXT'), ('symbol', 'TEXT'),
                 # ('date', 'TEXT'), ('net', 'TEXT'), ('fees', 'TEXT'), ('amount', 'TEXT') ]
    # database.create_table('TestTable', columns)

    ameritrade = Ameritrade(SecondAccount, client_id)
    # processer = TransactionProcessor(transactions_json)
    # processer.send_to_sql('MainAccount.db', 'TestTable')