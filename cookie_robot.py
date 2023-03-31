import asyncio
import json
import random
from dataclasses import dataclass

import requests
from playwright.async_api import async_playwright


'''
Nice to have:
0. Make Playwright able to use proxies
1. Make Webdriver (browser window) reusable.
2. Apply useragent spoofing, for example generate useragent using Dolphin API and use it for robot and for profile.
3. Try to improve cookies collecting mechanism: for example get sites by categories.
4. Add randomization options for categories, number of sites etc.
'''


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
SW_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': UA,
}
SW_COOKIES = dict()
BL = {'xhamster42.desi'}  # Somehow most popular porn site in India is in 'Computers Electronics and Technology' cat


@dataclass
class Proxy:
    host: str
    port: int
    user: str = None
    password: str = None

    def __str__(self):
        """Return a formatted string representation of the proxy."""
        if self.user and self.password:
            return f"{self.user}:{self.password}@{self.host}:{self.port}"
        else:
            return f"{self.host}:{self.port}"


def get_country_from_ip(ip_address: str) -> str:
    response = requests.get(f'https://ipapi.co/{ip_address}/json/')
    if response.status_code == 200:
        data = response.json()
        return data.get('country')
    else:
        raise Exception(f'Failed to get country for {ip_address}, status code {response.status_code}')


def get_top_websites_for_country(country: str, num: int = 40) -> set[str]:
    num = min(num, 50)
    with open('country.json', 'r') as f:
        country = json.load(f)[country]

    response = requests.get(f'https://www.similarweb.com/api/gettopwebsites?country={country}',
                            headers=SW_HEADERS,
                            cookies=SW_COOKIES)

    if response.status_code == 200:
        objects = response.json().get('sites', [])
        websites = [obj.get('domain') for obj in objects if obj.get('categoryId') != 'adult']
        return set(random.sample(websites, num))
    else:
        raise Exception(f'Failed to get websites for {country}, status code {response.status_code}')


def get_top_websites_global(num: int = 50) -> set[str]:
    num = min(num, 50)
    response = requests.get(f'https://www.similarweb.com/api/gettopwebsites',
                            headers=SW_HEADERS,
                            cookies=SW_COOKIES)

    if response.status_code == 200:
        objects = response.json().get('sites', [])
        websites = [obj.get('domain') for obj in objects if obj.get('categoryId') != 'adult']
        return set(random.sample(websites, num))
    else:
        raise Exception(f'Failed to get global websites, status code {response.status_code}')


async def process_url(context, url):
    page = await context.new_page()
    try:
        await page.goto('https://' + url)
    except Exception as e:
        print(f"Error occurred while connecting to {url}: {e}\n")

    cookies = []
    while not cookies:
        cookies = await page.context.cookies()
        await asyncio.sleep(0.5)

    await page.close()
    print(f"Successfully collected {len(cookies)} cookies from {url}!")

    return cookies


async def manage_tabs(context, urls, max_tabs):
    semaphore = asyncio.Semaphore(max_tabs)
    lock = asyncio.Lock()
    all_cookies = []

    async def sem_task(url):
        async with semaphore:
            cookies = await process_url(context, url)
            async with lock:
                all_cookies.extend(cookies)

    tasks = [sem_task(url) for url in urls]
    await asyncio.gather(*tasks)

    return all_cookies


async def collect_cookies(
        urls: set[str],
        max_tabs: int = 50,
        headless: bool = False,
        proxy: Proxy = None
) -> list[dict]:

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()

        all_cookies = await manage_tabs(context, urls, max_tabs)

        await browser.close()

    return all_cookies


def save_cookies_to_file(cookies: list[dict], filename: str = 'cookies.txt') -> None:
    with open(filename, 'w') as f:
        json.dump(obj=cookies, fp=f, skipkeys=True, indent=4)


async def main(ip_address: str = None, proxy: Proxy = None):
    country = get_country_from_ip(ip_address)
    print(f'Country detected: {country}')

    global SW_COOKIES
    cookies_list = await collect_cookies({'www.similarweb.com'})
    SW_COOKIES = {c['name']: c['value'] for c in cookies_list}
    print(f'Cookies for SimilarWeb: {SW_COOKIES}')

    country_websites = get_top_websites_for_country(country, 30)
    print(f'Top websites for {country}: {country_websites}')

    global_websites = get_top_websites_global(20)
    print(f'Top global websites: {global_websites}')

    all_websites = country_websites.union(global_websites).difference(BL)
    print(f'Total unique websites to visit: {len(all_websites)}')

    cookies = await collect_cookies(all_websites, proxy=proxy)
    save_cookies_to_file(cookies)
    print("Successfully saved cookies to file!")


if __name__ == '__main__':
    # ip_input = input('Enter an IP address: ')
    # pr = Proxy(host='192.92.191.91', port=64444, user='your_user', password='your_password')
    asyncio.run(main())
