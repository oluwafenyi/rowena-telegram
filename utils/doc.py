import logging
from urllib.parse import urlsplit

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def present_options(bookateria, genesis):
    text = ''
    if bookateria:
        for i, option in enumerate(bookateria):
            title = option[0].text.strip()
            size = option[1]
            text += f'{i+1}.\t{title}\n'
            text += f' \t{size}\n\n'

    elif genesis:
        for i, option in enumerate(genesis):
            cols = option.find_all('td')
            title = option.select_one('a[id]').text.strip()
            author = cols[1].text.strip()
            size = cols[7].text.strip()
            ext = cols[8].text.strip()

            text += f'{i+1}.\t{title}\n'
            text += f' \t{author}\n'
            text += f' \t{size}\n'
            text += f' \t{ext}\n\n'
    return text


def get_documents_bookateria(query):
    query = '+'.join(query)
    try:
        params = {'query': query}
        r = requests.get(f'https://bookateria.net/documents/search',
                         params=params)
    except RequestException:
        logging.warning('Bookateria seems to be down.')
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('tbody')
    data = [row.select_one('a:nth-child(1)') for row in rows][:5]
    sizes = []
    for datum in data:
        link = datum['href']
        r = requests.get(f'https://bookateria.net{link}')
        el = BeautifulSoup(r.text, 'html.parser')\
            .find('div', {'class': ['col-md-3', 'pt-2']})
        size = el.select_one('strong:nth-child(7)').text
        sizes.append(size)
    data = list(zip(data, sizes))
    return data


def download_choice_bookateria(link):
    url = f'https://bookateria.net{link}'
    client = requests.session()
    client.get(url)
    token = client.cookies['csrftoken']
    formdata = {'csrfmiddlewaretoken': token}
    r = client.post(f'https://bookateria.net{link}download',
                    data=formdata,
                    headers=dict(Referer=url),
                    allow_redirects=False)
    return r.headers['Location']


def get_documents_genesis(query):
    query = '+'.join(query)
    params = {
        'req': f'{query}',
        'open': '0',
        'view': 'simple',
        'res': '25',
        'phrase': '1',
        'column': 'def'
    }
    try:
        page = requests.get('http://gen.lib.rus.ec/search.php', params=params)
    except RequestException:
        logging.warning('Library Genesis seems to be down.')
        return None
    soup = BeautifulSoup(page.text, 'html.parser')
    rows = soup.select('table[align="center"] tr')
    english_docs = list(filter(
        lambda row: row.select_one('td:nth-child(7)').text.strip().lower() == 'english',
        rows
    ))[:5]
    return english_docs


def download_choice_genesis(link):
    url = f'http://gen.lib.rus.ec/{link}'
    try:
        res = requests.get(url)
    except RequestException:
        logging.warning(f'Could not find: {url}')
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    row = soup.select_one('body > table > tr:nth-child(18)')
    td = row.select_one('td:nth-child(2)')
    tr = td.select_one('table > tr > td:nth-child(1)')
    link = tr.find('a')['href']

    try:
        res = requests.get(link)
    except RequestException:
        logging.warning(f'Could not find: {url}')
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    download = soup.select_one('#info > h2 > a')['href']

    link_split = urlsplit(link)
    download = link_split.scheme + '://' + link_split.netloc + download
    return download
