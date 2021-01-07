import aiohttp
import asyncio
import argparse
import sys

from bs4 import BeautifulSoup
from re import findall

#To avoid the event close in windows 
if sys.version_info[0] == 3 and sys.version_info[1] >=8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


url = 'https://www.instagram.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66 '
}
parser = argparse.ArgumentParser()
parser.add_argument(dest='username', type=str, help='Enter user name to see details!')
args = parser.parse_args()


async def get_stats():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url + str(args.username)) as resp:
            r = await resp.text()
            soup = BeautifulSoup(r, 'html.parser')
            meta1 = soup.find('meta', property="og:description").attrs['content']
            data1 = meta1.split(' - ')[0]
            Followers = data1.split(',')[0]
            Following = data1.split(',')[1]
            Post = findall('Following,.(.*)', str(data1))[0]

            print('[+] ' + f'{Followers}\n' + '[+]' + f'{Following}\n' + '[+] ' + f'{Post}\n')

asyncio.run(get_stats())
