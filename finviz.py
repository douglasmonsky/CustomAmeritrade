import bs4
import requests
from datetime import datetime, timedelta

class Finviz:

    def __init__(self, elite=False, username=None, password=None):
        self.session = requests.Session()
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
        if elite:
            login = {'email' : username, 'password' : password}
            self.session.post('https://finviz.com/login_submit.ashx', data=login, headers=self.headers)
        self.current_page = None
        self.current_soup = None

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

if __name__ == "__main__":
    from privateinfo import finviz_username, finviz_password
    finviz = Finviz(True, finviz_username, finviz_password)
    news =  finviz.get_news('aapl')
    for story in news:
        print(story)