import aiohttp
import aiofiles
import asyncio
import datetime

from aiocsv import AsyncWriter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


async def collect_data():
    '''Collecting data from the web-site. Creating csv-file.'''
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()

    headers = {
        'Accept': (
            'text/html,application/xhtml+xml,'
            'application/xml;q=0.9,*/*;q=0.8'
            ),
        'User-Agent': ua.random
    }

    url = 'https://lidl.ie/super-savers'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        cards = soup.find_all('div', class_='nuc-a-flex-item--width-6')

        DATA = []
        for card in cards:
            card_title = card.find(
                'h3',
                class_='ret-o-card__headline').text.strip()

            try:
                card_discount = card.find(
                    'div',
                    class_='lidl-m-pricebox__discount-wrapper').text.strip()
                card_discount = card_discount[
                    card_discount.find('-'):card_discount.find('%')+1
                ]
            except AttributeError:
                continue

            card_old_price = card.find(
                'div',
                class_='lidl-m-pricebox__highlight'
            ).text.replace('€', '').strip()
            if "Was" not in card_old_price:
                card_old_price = "Was " + card_old_price

            card_sale_price = card.find(
                'span',
                class_='lidl-m-pricebox__price'
            ).text.replace(' ', '').strip()

            card_sale_date = card.find(
                'span',
                class_='lidl-m-ribbon-item__text'
            ).text.replace(' ', '').strip()

            DATA.append(
                [
                    card_title,
                    card_old_price,
                    card_discount,
                    card_sale_price,
                    card_sale_date
                ]
            )

    async with aiofiles.open(f'LIDL_{cur_time}.csv', 'w') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Product',
                'Old price',
                'Discount %',
                'Sale price',
                'Sale date'
            ]
        )
        await writer.writerows(
            DATA
        )

    return f'LIDL_{cur_time}.csv'


async def main():
    await collect_data()


if __name__ == '__main__':
    asyncio.run(main())
