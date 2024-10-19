import asyncio

from src.items.schemas import ItemAdd

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


async def item_serialize(position: dict, position_id: int):

    return ItemAdd(title=position['title'],
                   image=f'/src/static/items_images/{position_id}.jpg',
                   size=position['size'],
                   price=position['price'],
                   description=None)


async def items_serialize(new_positions: list[dict], last_position_id: int):
    tasks = []

    for position in new_positions:
        last_position_id += 1
        tasks.append(item_serialize(position, last_position_id))

    new_items = await asyncio.gather(*tasks)

    return new_items
