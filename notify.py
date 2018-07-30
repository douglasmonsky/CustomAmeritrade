import smtplib
from ameritrade import Ameritrade
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from portfolio import TransactionProcessor


class Email:

    def __init__(self, subject='', text='', files=None):
        self.subject = subject
        self.text = text
        self.files = files

    def construct_trade_text(self, transactions):
        text_lines = []
        for transaction in transactions:
            net = transaction.net
            if net > 0:
                trade_type = 'bought'
            else:
                trade_type = 'sold'
            price_per_share = round(transaction.net / transaction.amount, 2)
            text = f'{transaction.transaction_type} has been executed. {abs(int(transaction.amount))} share(s) of {transaction.symbol} has been {trade_type} at aprox. {price_per_share} per share.'
            text_lines.append(text)
        self.text = '\n'.join(text_lines)

    def construct_positions_text(self, position_data, time_of_day):
        text_lines = []
        positions = position_data['securitiesAccount']['positions']
        for position in positions:
            short_quant = int(position['shortQuantity'])
            long_quant = int(position['longQuantity'])
            if short_quant:
                position_type = 'short'
                quant = short_quant
            else:
                position_type = 'long'
                quant = long_quant
            avg_price = round(float(position['averagePrice']), 2)
            day_change = round(float(position['currentDayProfitLoss']), 2)
            symbol = position['instrument']['symbol']
            text = f'As of {time_of_day} today, you are currently {position_type} {quant} shares of {symbol} for an average price of {avg_price}. This is a net change of {day_change}.'
            text_lines.append(text)
        self.text = '\n'.join(text_lines)

    def send_email(self, username, password, recepient, server="smtp.gmail.com", port=587, isTls=True):
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = COMMASPACE.join(recepient)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.text))

        if self.files:
            for f in self.files:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(f,"rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(f)))
                msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if isTls: 
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(username, recepient, msg.as_string())
        smtp.quit()




def notify_trade(id_list):
    from privateinfo import MainAccount, SecondAccount, client_id, gmail_username, gmail_password, send_to_email, send_to_phone
    ameritrade = Ameritrade(MainAccount, client_id)
    transactions_json = ameritrade.get_transactions('2018-07-27', '2018-07-27', 'TRADE')
    processer = TransactionProcessor(transactions_json)
    transactions = processer.transaction_list

    new_transactions = []
    for transaction in transactions:
        if transaction.transaction_id not in id_list:
            new_transactions.append(transaction.transaction_id)

    send_mail(gmail_username, gmail_password, [send_to_email, ], subject='Testing', text=f'{new_transactions}')   


if __name__ == "__main__":
    notify_trade([])