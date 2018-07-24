import requests
import time
import pickle
import bs4


class Account:

    def __init__(self, account_id, refresh_token, auth_token=None):
        self.account_id = account_id
        self.refresh_token = refresh_token
        self.auth_token = auth_token


class Ameritrade:

    def __init__(self, account, client_id=''):
        '''Takes in Account Object as argument.'''
        self.account = account
        self.client_id = client_id
        self.refresh_token = account.refresh_token
        self.account_id = account.account_id
        if account.auth_token:
            self.auth_token = account.auth_token
        else:
            with open(f'auth_token_{self.account_id}.pickle', 'rb') as f:
                data = pickle.load(f)
                self.auth_token, self.expire_time = data
     
    def check_expiration(self):
        if time.time() > self.expire_time:
            self.refresh_auth()
    
    def get_live_quote(self, symbol):
        self.check_expiration()  
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'Bearer {self.auth_token}'}
        live_quote = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes?apikey={client_id}", headers=headers)
        return live_quote.json()

    def get_transactions(self, start_date, end_date, data_type='ALL'):
        self.check_expiration()
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'Bearer {self.auth_token}'}
        transactions = requests.get(f"https://api.tdameritrade.com/v1/accounts/{self.account_id}/transactions?type={data_type}&startDate={start_date}&endDate={end_date}", headers=headers)
        return transactions.json()

    def refresh_auth(self):
        print('refreshing token')
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = { 'grant_type': 'refresh_token', 'refresh_token': self.refresh_token, 'client_id': }
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        self.auth_token = authReply.json()['access_token']
        self.expire_time = time.time() + 1740 #29 mins, so token refreshes 1 min before expiration.
        data = [self.auth_token, self.expire_time]
        with open(f'auth_token_{self.account_id}.pickle', 'wb') as f:
            pickle.dump(data, f)

    # def get_price_history(self, symbol, period_type, frequency_type, period=None, frequency=None, end_date=None, start_date=None, extended_hours=None):
    #     '''CURRENTLY NOT WORKING CORRECTLY, DOES NOT CONSIDER DATA'''
    #     self.check_expiration()
    #     data = {'periodType': period_type, 'frequencyType': frequency_type, 'period': period, 'frequency': frequency,
    #             'endDate': end_date, 'startDate:': start_date, 'needExtendedHoursData': extended_hours}
    #     headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'Bearer {self.auth_token}'}
    #     price_history = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory?apikey={client_id}", headers=headers, data=data)
    #     return price_history.json()


if __name__ == '__main__':
    from privateinfo import MainAccount
    ameritrade = Ameritrade(MainAccount)
    transactions = ameritrade.get_transactions('2018-01-01', '2018-07-23')
    all_fees = 0
    for transaction in transactions:
        fees = transaction['fees']
        total_fee = sum(fees.values())
        all_fees += total_fee
    print(all_fees)