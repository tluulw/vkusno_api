import asyncio

import httpx
from bs4 import BeautifulSoup

cookies = {
    '_ym_uid': '1712062070396684790',
    'UTMcookie': 'McD_App',
    'cookies-agreement': 'true',
    'x-client-verison': '73c68',
    'PHPSESSID': 'a196fgqt77ocab4g1m12qrqkd8',
    'client_define': 'mcd-user-66e9a165b33450.66892865',
    'selected-menu-category': 'burgery-i-rolly',
    'selected-subcategory': 'vse-burgery-i-rolly',
    'confirmed-city': 'true',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,ja;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_ym_uid=1712062070396684790; UTMcookie=McD_App; cookies-agreement=true; x-client-verison=73c68; PHPSESSID=a196fgqt77ocab4g1m12qrqkd8; client_define=mcd-user-66e9a165b33450.66892865; selected-menu-category=burgery-i-rolly; selected-subcategory=vse-burgery-i-rolly; confirmed-city=true',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://vkusnoitochka.ru/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
}

url = 'https://vkusnoitochka.ru/menu'
items = []


async def get_items_from_pages(page):
    async with httpx.AsyncClient() as session:
        req = await session.get(url + '/' + page, cookies=cookies, headers=headers)

    if req.status_code == 200:

        soup = BeautifulSoup(req.text, 'html.parser')

        for el in soup.find_all('a', 'product-card'):

            item = {'title': el.find(itemprop='name').text,
                          'image': el.find(class_='common-image__img')['src'],
                          'size': el.find(itemprop='description').text,
                          'price': int(el.find('b').text.split(' ')[1])}

            if item not in items:
                items.append({'title': el.find(itemprop='name').text,
                              'image': el.find(class_='common-image__img')['src'],
                              'size': el.find(itemprop='description').text,
                              'price': int(el.find('b').text.split(' ')[1])})


async def get_menu():
    async with httpx.AsyncClient() as session:
        main_response = await session.get(url, cookies=cookies, headers=headers)

    if main_response.status_code == 200:

        main_soup = BeautifulSoup(main_response.text, "html.parser")

        pages = [el['href'].split('/')[-1] for el in main_soup.find_all('a', 'menu-category-item') if
                 el['href'].split('/')[-1] not in ['novinki', 'populyarnoe', 'cuper-boks', 'kidz-kombo',
                                                   'sety-menee-600-kkal',
                                                   'tolko-v-dostavke',
                                                   'vygodno-dlya-megakompanii']]

        tasks = []

        for page in pages:
            tasks.append(get_items_from_pages(page))

        await asyncio.gather(*tasks)

        async with httpx.AsyncClient() as session:
            await session.post('http://localhost:8000/items/add/many', json=items)


if __name__ == '__main__':
    asyncio.run(get_menu())
