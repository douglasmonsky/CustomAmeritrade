import smtplib
from ameritrade import Ameritrade
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from portfolio import TransactionProcessor


class Email:

    def __init__(self, subject='', text='', files=None, finviz_session=None):
        self.subject = subject
        self.text = text
        self.files = files
        self.finviz_session = finviz_session

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
        self.text = '<br />'.join(text_lines)

    def construct_positions_text(self, position_data, time_of_day, end_of_day=True, include_news=False):
        text_lines = []
        start_total = position_data['securitiesAccount']["initialBalances"]["liquidationValue"]
        current_total = position_data['securitiesAccount']["currentBalances"]["liquidationValue"]
        if end_of_day:
            text_lines.append(f'You started the day with an account value of ${start_total} and now have ${current_total}, that is a net change of {round(current_total - start_total, 2)}.<br />')
        else:
            text_lines.append(f'You are starting the day with an account value of ${current_total}.<br />')
        text_lines.append(f'As of {time_of_day} today,  Your current positions are as follows:')
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
            text = f'{position_type.upper()} {quant} shares of {symbol} for an average price of {avg_price}. This is a net change of {day_change}.'
            text_lines.append(text)
            if self.finviz_session and include_news == True:
                news_container = self.finviz_session.get_news(symbol)
                if news_container:
                    text_lines.append(f'Recent {symbol} news articles:')
                    for news in news_container:
                        news_text = f'{news[0]}, {news[1].strip()}: <a href="{news[3]}">{news[2]}</a>'
                        text_lines.append(news_text)
            text_lines.append('')
        self.text = '<br />'.join(text_lines)

    def construct_orders_text(self, orders_data, position_data=None):
        text_lines = []
        for order in orders_data:
            order_type = order['orderType']
            session = order['session']
            quant = int(order['quantity'])
            filled = int(order['filledQuantity'])
            price = order['price']
            duration = order['duration']
            status = order['status']
            specifics = order['orderLegCollection'][0]
            symbol = specifics['instrument']['symbol']
            instruction = specifics['instruction']
            effect = specifics['positionEffect']
            text_lines.append(f'A(n) {instruction} {order_type} order (duration: {duration}) for {quant} shares of {symbol} at {price} a share has been placed. The current status as of now is {status} with {filled} shares completed.')
        text_lines.append('<br />This results in the following active postions:')
        if position_data:
            positions_data = position_data['securitiesAccount']['positions']
            for position in positions_data:
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
                text = f'{position_type.upper()} {quant} shares of {symbol} for an average price of {avg_price}. This is a net change of {day_change}.'
                text_lines.append(text)
        self.text = '<br />'.join(text_lines)
       



    def send_email(self, username, password, recepient, server="smtp.gmail.com", port=587, isTls=True, html=True):
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = COMMASPACE.join(recepient)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = self.subject
        if html:
            msg.attach(MIMEText(self.text, 'html'))
        else:
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
