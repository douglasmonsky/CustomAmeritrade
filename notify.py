import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from order import Order



class Message:

    def __init__(self, subject='', text='', files=None, finviz_session=None, end_line='\n'):
        self.subject = subject
        self.text = text
        self.files = files
        self.finviz_session = finviz_session
        self.end_line = end_line

    def tokenize_text(self):
        sentences = self.text.split(self.end_line)
        return sentences

    def construct_trade_text(self, transactions):
        text_lines = []
        for transaction in transactions:
            net = transaction.net
            if net > 0:
                trade_type = 'bought'
            else:
                trade_type = 'sold'
            price_per_share = round(transaction.net / transaction.amount, 2)
            text = f'{transaction.transaction_type} has been executed. {abs(int(transaction.amount))} share(s) of ' \
                   f'{transaction.symbol} has been {trade_type} at aprox. {price_per_share} per share.'
            text_lines.append(text)
        self.text = self.end_line.join(text_lines)

    def construct_positions_text(self, position_data, time_of_day, end_of_day=True, include_news=False):
        text_lines = []
        start_total = position_data['securitiesAccount']["initialBalances"]["liquidationValue"]
        current_total = position_data['securitiesAccount']["currentBalances"]["liquidationValue"]
        if end_of_day:
            text_lines.append(f'You started the day with an account value of ${start_total}'
                              f' and now have ${current_total}, that is a net change of'
                              f' {round(current_total - start_total, 2)}.{self.end_line}')
        else:
            text_lines.append(f'You are starting the day with an account value of ${current_total}.{self.end_line}')
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
            market_value = position['marketValue']
            current_pps = round(market_value/quant, 2)
            symbol = position['instrument']['symbol']
            text = f'{position_type.upper()} {quant} shares of {symbol} for an average price of {avg_price}.' \
                   f' The current price per share is {current_pps}. This is a net change of {day_change}.'
            text_lines.append(text)
            if self.finviz_session and include_news == True:
                news_container = self.finviz_session.get_news(symbol)
                if news_container:
                    text_lines.append(f'Recent {symbol} news articles:')
                    for news in news_container:
                        news_text = f'{news[0]}, {news[1].strip()}: <a href="{news[3]}">{news[2]}</a>'
                        text_lines.append(news_text)
            text_lines.append('')
        self.text = self.end_line.join(text_lines)

    def construct_orders_text(self, orders_data, position_data=None):
        text_lines = []
        for order in orders_data:
            order_obj = Order(order)
            text_lines.append(f'A(n) {order_obj.instruction} {order_obj.order_type} order'
                              f' (duration: {order_obj.duration}) for {order_obj.quant} shares of'
                              f' {order_obj.symbol} at {order_obj.avg_price} a share has been placed.'
                              f' The current status as of now is {order_obj.status} with {order_obj.filled}'
                              f' shares completed.')
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
                market_value = position['marketValue']
                current_pps = round(market_value/quant, 2)
                symbol = position['instrument']['symbol']
                text = f'{position_type.upper()} {quant} shares of {symbol} for an average price of {avg_price}.' \
                       f' The current price per share is {current_pps}. This is a net change of {day_change}.'
                text_lines.append(text)
        self.text = self.end_line.join(text_lines)

    # rewrite send_text and send_message to remove repeated code...
    # probably rewrite this whole class into two, one to handle creating the text
    # the other for handling formatting and sending the message
    def send_text(self, username, password, recepients, server="smtp.gmail.com", port=587, isTls=True, html=False):
        sentences = self.tokenize_text()

        message_length = 0
        message = ''

        for sentence in sentences:
            length = len(sentence)
            if message_length + length > 160:
                msg = MIMEMultipart()
                if html:
                    msg.attach(MIMEText(message, 'html'))
                else:
                    msg.attach(MIMEText(message))

                smtp = smtplib.SMTP(server, port)
                if isTls: 
                    smtp.starttls()
                smtp.login(username, password)
                smtp.sendmail(username, recepients, msg.as_string())
                message_length = 0
                message = sentence
            else:
                message += f'sentence{self.end_line}'
                message_length += 0

    def send_message(self, username, password, recepients, server="smtp.gmail.com", port=587, isTls=True, html=False):
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = COMMASPACE.join(recepients)
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
        smtp.sendmail(username, recepients, msg.as_string())
        smtp.quit()