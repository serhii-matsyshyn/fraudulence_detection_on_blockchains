import random
import time

import requests
from fake_useragent import UserAgent
from tqdm import tqdm


class BlockScanAddressByTagRetrival:
    def __init__(self, save_to="search_results_all.txt"):
        self.save_to = save_to
        self.ua = UserAgent()
        # self.scraper = cloudscraper.create_scraper()
        # self.scraper = cfscrape.create_scraper()
        self.scraper = requests

        self.proxy = None

    def search_address_by_tag(self, tag='Fake_Phishing323049'):

        cookies = {
            # WARNING: use your own cookies
        }

        headers = {
            # WARNING: use your own headers
            'authority': 'etherscan.io',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'user-agent': self.ua.random,
        }

        params = {
            'f': '0',
            'q': tag,
        }

        response = self.scraper.get('https://etherscan.io/search', params=params,
                                    proxies={"http": self.proxy, "https": self.proxy},
                                    cookies=cookies,
                                    headers=headers, allow_redirects=False
                                    )
        if response.status_code == 302:
            # print(tag, response.status_code, response.headers['Location'])
            if 'busy' in response.headers['Location']:
                # print("Busy!")
                time.sleep(random.uniform(5, 15))
                return self.search_address_by_tag(tag)

            return response.headers['Location'][9:]
        # print(response.text)
        raise Exception("No tag corresponding to address!")

    def search_address_by_tag2(self, tag='Fake_Phishing323049'):
        """DO NOT USE, skips some searches"""
        headers = {
            'authority': 'etherscan.io',
            'accept': '*/*',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'user-agent': self.ua.random,
        }

        params = {
            'filterby': '0',
            'term': tag.lower(),
        }
        response = self.scraper.get('https://etherscan.io/searchhandler',
                                    params=params, headers=headers,
                                    allow_redirects=False)
        response_json = response.json()
        if len(response_json) > 0:
            print(response_json)
            return response_json[0]['address']
        raise Exception("No tag corresponding to address!")

    def process_fake_phishing(self, range_to_process):
        for i in (tqdm(range_to_process)):
            tag = f'Fake_Phishing{i}'
            try:
                result = self.search_address_by_tag(tag)

                with open(self.save_to, "a") as file:
                    print(f"{tag}|{result}", file=file)
            except Exception as err:
                print(tag, err)


if __name__ == '__main__':
    # Latest etherscan Fake_Phishing323049 on 25_02_2024
    # Processing etherscan only, any other blockscan explorer can be used as well (modifications required)

    BlockScanAddressByTag_retriever = BlockScanAddressByTagRetrival()
    BlockScanAddressByTag_retriever.process_fake_phishing(range(23702, 0, -1))
