import bs4
import requests
from datetime import datetime, timedelta

class Finviz:

    def __init__(self, elite=False, username=None, password=None):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
        if elite:
            login = {'email' : self.username, 'password' : self.password}
            self.session.post('https://finviz.com/login_submit.ashx', data=login, headers=self.headers)
        self.current_page = None
        self.current_soup = None

    def check_login_status(self):
        self.page_check('https://elite.finviz.com/myaccount.ashx')
        try:
            name_displayed = self.current_soup.find('span', {'class': 'body-text'}).text
            logged_in = name_displayed == f'Account: {self.username}'
        except AttributeError:
            logged_in = False
        return logged_in

    def page_check(self, search_page):
        if self.current_page != search_page:
            req = self.session.get(search_page, headers=self.headers)
            soup = bs4.BeautifulSoup(req.text, "html.parser")
            self.current_page = search_page
            self.current_soup = soup

    def get_news(self, symbol, days_back=2):
        new_articles = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        refrence_day = today - timedelta(days=days_back)
        search_page = f'https://elite.finviz.com/quote.ashx?t={symbol}'
        self.page_check(search_page)
        table = self.current_soup.find('table', {'class':'fullview-news-outer'})
        rows = table.find_all('tr')
        for row in rows:
            time, article = row.find_all('td')
            date_time = time.text.split(" ")
            if len(date_time) > 1:
                date = datetime.strptime(date_time[0], '%b-%d-%y')
                time = date_time[1]
            else:
                time = date_time[0]
            time = time.split('\\xa0\\')[0]
            if date >= refrence_day:
                href = article.find('a')['href']
                title = article.text
                new_articles.append([datetime.strftime(date,'%b-%d-%y'), time, title, href])
        return new_articles

    def open_screener(self, link_suffix=''):
        self.page_check(f'https://finviz.com/screener.ashx?{link_suffix}')
        presets = {}
        try:
            presets_soup = self.current_soup.find('select', {'class': 'body-combo-text'})
            for item in presets_soup.find_all('option'):
                name = item.text
                if 's:' in name:
                    name = name.split('s: ')[1]
                    link_suffix = item['value']
                    presets[name] = link_suffix
        except KeyError:
            pass
        return presets

    def download(self, filename='finviz_data.csv'):
        '''
        Downloads the data on the page via finviz's export functionality.
        currently only downloads on screener page, planning to add functionality for groups.
        '''
        if 'screener' not in self.current_page:
            self.open_screener()
        try:
            links = self.current_soup.find_all('a', {'class': 'tab-link'})
            download_link = links[-2]['href']
            download_link = f'https://elite.finviz.com/{download_link}'
        except:
            download_link = 'https://elite.finviz.com/export.ashx?v=111'
        req = self.session.get(download_link, headers=self.headers, allow_redirects=True, stream=True)
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        with open(filename, 'w', newline='') as csvfile:
            for row in soup:
                csvfile.write(row)

if __name__ == "__main__":
    from privateinfo import finviz_username, finviz_password
    finviz = Finviz(True, finviz_username, finviz_password)
    # news =  finviz.get_news('aapl')
    # finviz.download()
    # presets = finviz.open_screener()
    # finviz.open_screener(presets['New Screen'])
    # finviz.download()