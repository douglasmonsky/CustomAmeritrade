import requests
import time
import pickle
import bs4


class Account:

    def __init__(self, account_id, refresh_token, nickname=None, auth_token=None):
        self.account_id = account_id
        self.refresh_token = refresh_token
        self.nickname = nickname
        self.auth_token = auth_token


class Ameritrade:

    def __init__(self, account, client_id='', print_auth=False):
        '''Takes in Account Object as argument.'''
        self.account = account
        self.client_id = client_id
        self.print_auth = print_auth
        self.refresh_token = account.refresh_token
        self.account_id = account.account_id
        if account.auth_token:
            self.auth_token = account.auth_token
            self.expire_time = time.time() + 1500
        else:
            with open(f'auth_token_{self.account_id}.pickle', 'rb') as f:
                data = pickle.load(f)
                self.auth_token, self.expire_time = data
        self.check_expiration()
        self.default_headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'Bearer {self.auth_token}'}
        if self.print_auth:
            print(self.auth_token)
     
    def check_expiration(self):
        if time.time() > self.expire_time:
            self.refresh_auth()

    def check_error(self, json):
        if json == {"error": "The access token being passed has expired or is invalid."}:
            print(json)
            self.refresh_auth()
            time.sleep(5)
            return True
        else:
            return False

    def get_account_positions(self, info_type='positions'):
        self.check_expiration()
        data = requests.get(f"https://api.tdameritrade.com/v1/accounts/{self.account_id}?fields={info_type}", headers=self.default_headers)
        data = data.json()
        error = self.check_error(data)
        if error:
            self.get_account_positions(info_type)
        else:
            return data
    
    def get_live_quote(self, symbol):
        self.check_expiration()  
        data = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes?apikey={self.client_id}", headers=self.default_headers)
        data = data.json()
        error = self.check_error(data)
        if error:
            self.get_live_quote(symbol)
        else:
            return data

    def get_transactions(self, start_date, end_date, data_type='ALL'):
        ''''start and end date must be in YYYY-MM-DD format'''
        self.check_expiration()
        data = requests.get(f"https://api.tdameritrade.com/v1/accounts/{self.account_id}/transactions?type={data_type}&startDate={start_date}&endDate={end_date}", headers=self.default_headers)
        data = data.json()
        error = self.check_error(data)
        if error:
            self.get_transactions(start_date, end_date, data_type)
        else:
            return data

    def refresh_auth(self):
        print(f'refreshing {self.account.account_id} {self.account.nickname} token')
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = { 'grant_type': 'refresh_token', 'refresh_token': self.refresh_token, 'client_id': self.client_id}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        self.auth_token = authReply.json()['access_token']
        self.expire_time = time.time() + 1500 #25 mins, so token refreshes 5 mins before expiration.
        data = [self.auth_token, self.expire_time]
        with open(f'auth_token_{self.account_id}.pickle', 'wb') as f:
            pickle.dump(data, f)
        if self.print_auth:
            print(self.auth_token)

    # def get_price_history(self, symbol, period_type, frequency_type, period=None, frequency=None, end_date=None, start_date=None, extended_hours=None):
    #     '''CURRENTLY NOT WORKING CORRECTLY, DOES NOT CONSIDER DATA'''
    #     self.check_expiration()
    #     data = {'periodType': period_type, 'frequencyType': frequency_type, 'period': period, 'frequency': frequency,
    #             'endDate': end_date, 'startDate:': start_date, 'needExtendedHoursData': extended_hours}
    #     headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': f'Bearer {self.auth_token}'}
    #     price_history = requests.get(f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory?apikey={self.client_id}", headers=headers, data=data)
    #     return price_history.json()


if __name__ == '__main__':
    from privateinfo import MainAccount, SecondAccount, client_id
    ameritrade = Ameritrade(SecondAccount, client_id, print_auth=True)
    print(ameritrade.get_account_positions('positions,orders')['securitiesAccount']['currentBalances']['liquidationValue'])
    # print(ameritrade.get_transactions('2018-07-01', '2018-07-29'))