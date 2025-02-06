import time

import requests
from bs4 import BeautifulSoup

brand = 'lada'
model = 'granta'
min_price = 400_000
min_year = 2015

base_url = f'https://spb.drom.ru/{brand}/{model}'


params = {
    'minprice': min_price,
    'minyear': min_year
}


page_number = 1
while True:
    url = f'{base_url}/page{page_number}'
    response = requests.get(url, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        ads = soup.find_all(attrs={'data-ftid': 'bulls-list_bull'})

        if not ads:
            break

        for ad in ads:
            title = ad.find(attrs={'data-ftid': 'bull_title'}).text.strip().split(',')
            name = title[0]
            year = int(title[1])
            price = ad.find(attrs={'data-ftid': 'bull_price'}).text.strip()
            engine = ad.find_next(attrs={'data-ftid': 'bull_description-item'})
            fuel = engine.find_next(attrs={'data-ftid': 'bull_description-item'})
            gearbox = fuel.find_next(attrs={'data-ftid': 'bull_description-item'})

            link = ad.find(attrs={'data-ftid': 'bull_title'})['href']

            print(f'Название: {name}')
            print(f'Год выпуска: {year}')
            print(f"Тип топлива: {fuel.text.strip().replace(',', '')}")
            print(f"Двигатель: {engine.text.strip().replace(',', '')}")
            print(f"КПП: {gearbox.text.strip().replace(',', '')}")
            print(f'Цена: {price}')
            print(f'Ссылка: {link}')
            print('-' * 40)
    else:
        print(f'Ошибка при запросе: {response.status_code}')

    page_number += 1
    time.sleep(1)

