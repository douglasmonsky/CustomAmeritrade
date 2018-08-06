import bs4
import requests


class EarningsWhisper:

    def __init__(self, stock):
        self.stock = stock
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }
        self.soup = self.get_page(self.stock)

    def get_page(self, stock):
        req = self.session.get(f'https://www.earningswhispers.com/epsdetails/{stock}')
        return bs4.BeautifulSoup(req.text, 'html.parser')

    def get_text(self, item):
        return self.soup.find('div', {'class': item}).text

    def get_results(self):
        data = {'reported_earnings': self.get_text('mainitem'), 'whisper_earnings': self.get_text('seconditem'),
                'estimated_earnings': self.get_text('thirditem'), 'reported_revenue': self.get_text('fourthitem'),
                'estimated_revenue': self.get_text('fifthitem')}
        return data


if __name__ == "__main__":
    earnings = EarningsWhisper('tdoc')
    data = earnings.get_results()
    print(data)
