import smtplib
from ameritrade import Ameritrade
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from portfolio import TransactionProcessor


def send_mail(username, password, send_to, subject='', text='', files=None, server="smtp.gmail.com", port=587, isTls=True):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    if files:
        for f in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f,"rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(f)))
            msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if isTls: smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(username, send_to, msg.as_string())
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