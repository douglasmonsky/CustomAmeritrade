import requests
from bs4 import BeautifulSoup

def parse_article(soup):
    h1 = soup.find('h1')
    root = h1

    # find the common parent for <h1> and all <p>s.
    root = h1
    while root.name != 'body' and len(root.find_all('p')) < 5:
        root = root.parent

    if len(root.find_all('p')) < 5:
        return None

    # find all the content elements.
    ps = root.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre'])
    ps.insert(0, h1)
    content = [tag2md(p) for p in ps]

    return {'title': h1.text, 'content': content}

def tag2md(tag):
    if tag.name == 'p':
        return tag.text
    elif tag.name == 'h1':
        return f'{tag.text}\n{"=" * len(tag.text)}'
    elif tag.name == 'h2':
        return f'{tag.text}\n{"-" * len(tag.text)}'
    elif tag.name in ['h3', 'h4', 'h5', 'h6']:
        return f'{"#" * int(tag.name[1:])} {tag.text}'
    elif tag.name == 'pre':
        return f'```\n{tag.text}\n```'


req = requests.post('https://www.bizjournals.com/sanjose/news/2018/08/03/'
                    'roku-signs-massive-lease-at-san-joses-coleman.html?ana=yahoo&yptr=yahoo')
soup = BeautifulSoup(req.text, 'html.parser')

article_data = parse_article(soup)
title = article_data['title']
print(title)

data = {'txt': title}
req = requests.post('http://sentiment.vivekn.com/api/text/', data=data)
print(req.text)



