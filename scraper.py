import aiohttp
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict, field
import asyncio
import random
from time import perf_counter
from typing import List
import json
import requests

@dataclass
class Product:
        name: str
        price: str
        description: str
        img: str
        link: str
        publish: str
        post: str
        address: str

@dataclass
class Scraper:
        # proxies: List[str] = field(default_factory=lambda:[
        #         '142.214.181.36:8800',
        #         '142.214.181.241:8800',
        #         '196.51.116.40:8800',
        #         '196.51.114.196:8800',
        #         '142.214.181.41:8800',
        #         '196.51.116.171:8800',
        #         '142.214.181.219:8800',
        #         '142.214.183.243:8800',
        #         '196.51.114.248:8800',
        #         '142.214.183.70:8800'
        # ])

        proxies: List[str] = None

        useragent: List[str] = field(default_factory=lambda:[
                'Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.137 Safari/537.36 Ubuntu/22.04 (5.0.2497.35-1) Vivaldi/5.0.2497.35',
                'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.48-1) Vivaldi/5.0.2497.48',
                'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.51-1) Vivaldi/5.0.2497.51,',
                'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.39',
                'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.92 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.34'
        ])
        baseurl: str = 'https://www.willhaben.at'

        async def fetch(self, s, url):
                ua = random.choice(self.useragent)
                headers = {
                        'User-Agent': ua,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        # 'Cookie': 'bbxDmpSegments=[]; bbxLastViewed={"bap":{"adList":[656862016]}}; IADVISITOR=afb2210f-26b8-4223-b378-03fef213e347; context=prod; TRACKINGID=7eb82009-ab62-4fef-b62a-1d93017e2c5e; x-bbx-csrf-token=5f2567cf-990a-4b7a-834f-d15bb3d1dd02; SRV=3|ZA+In; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22c118a7be-8680-469a-bd2d-b3b051cd9014%22%2C%22options%22%3A%7B%22end%22%3A%222024-04-13T20%3A17%3A37.455Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-612451-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A31536000%2C%22end%22%3A31536000%7D%7D; ioam2018=00010a06df4d83560640f7902:1708370818778:1678735618778:.willhaben.at:16:at_w_atwillhab:Service/Rubrikenmaerkte/Sonstiges/moewa/Kameras_TV_Multimedia/TL:noevent:1678739853806:fhwjlr; didomi_token=eyJ1c2VyX2lkIjoiMTg2ZGM3MGItMzkwNS02YmRkLThkYmEtNDg0ZmIzNjUwYmJmIiwiY3JlYXRlZCI6IjIwMjMtMDMtMTNUMTk6Mjc6MDIuMjc3WiIsInVwZGF0ZWQiOiIyMDIzLTAzLTEzVDE5OjI3OjAyLjI3N1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYW1hem9uIiwiZ29vZ2xlIiwiYzpvZXdhLVhBUW1HU2duIiwiYzphbWF6b24tbW9iaWxlLWFkcyIsImM6aG90amFyIiwiYzp1c2Vyem9vbSIsImM6YW1hem9uLWFzc29jaWF0ZXMiLCJjOnh4eGx1dHprLW05ZlFrUHRMIiwiYzpvcHRpb25hbGUtYm5BRXlaeHkiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsieHh4bHV0enItcWtyYXAzM1EiLCJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSIsImM6d2lsbGhhYmVuLVpxR242WXh6Il19LCJ2ZXJzaW9uIjoyLCJhYyI6IkFrdUFFQUZrQkpZQS5Ba3VBRUFGa0JKWUEifQ==; RANDOM_USER_GROUP_COOKIE_NAME=29; _pbjs_userid_consent_data=7882712499466548; _pulse2data=bb9fb85e-7a09-4052-8f45-0b01c9ffc8c6%2Cv%2C%2C1678740279140%2CeyJpc3N1ZWRBdCI6IjIwMjMtMDMtMTNUMTk6Mjc6MDBaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..KAIfPyO9V0C5GWTXiyV9-g.Jel9xNaPsjEC8w2z1zcv0BHIUQWqtv9KU6VtjJ08Ei4NIw8ggJN2WjwJzqhi8Uq82TertthSmd4v6cRe55Ev8mSfSZiEMxxjI4fQ4XRpVxKFs-n93EErSoU6IDYgKloQ6wXI2LqixrB3WRhc-ZyK6H0xJBWIuTc2FPUOWNFuT6fjditiHy7TUT71uXfJ0BTxyFjNeDWVoDBqwULD2YxPYQ.Zo8WuCEhIyEg6EsZx7ANqA%2C%2C%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..d3CcqTFN1s8nYMOpAmFOkBjkGV4VRnaZ8RaJh6NNG3s; euconsent-v2=CPokAsAPokAsAAHABBENC7CsAP_AAH_AAAAAIzNf_X_fb2_j-_59f_t0eY1P9_7_v-0zjhedk-8Nyd_X_L8X52M7vB36pq4KuR4ku3LBAQdlHOHcTQmw6IkVqSPsbk2Mr7NKJ7PEmlMbO2dYGH9_n1XT-ZKY79__f_7z_v-v____7r__7-3f3_vp9V-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABA3QAkw1biALsSxwJtowigRAjCsJCoBQAUUAwtEBhASuCnZXAT6wiQAIBQBGBECHAFGDAIAAAIAkIiAECPBAAACIBAACABUIhAARoAgoAJAQCAAUA0LACKAIRJCDIiIilMCAiRIKCeQIQSg_0MMIQ6igAAA.f_gAD_gAAAAA; permutive-id=352d3fa4-e48e-4ccf-8015-789bf2773800; _lr_env_src_ats=false; id5id.1st_426_nb=2; pbjs-unifiedid=%7B%22TDID%22%3A%229cfe700f-37dd-44b6-8b2c-ab8d0da8fa3f%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-03-13T19%3A27%3A03%22%7D; cto_bundle=V6Il9F9yUTAlMkYzeUJNcW43UUZBMFVqN2FuRWdWSWtjRUtLZlVDbXU2MW80eFVXWCUyQlhkNnhacWc3OThFRUlEblclMkJMSElmN0UweHo5VWd3dW5yVEZ6Y2N1QWIzbTZTVTRteFgzelNjWVUwTjJ4U1ZqJTJGV1dZM3Y4Vmp5JTJGaHpYRTE1NE5PR2hndHl6YjJFZEloaXhCNiUyRnFJZG1CMEElM0QlM0Q; cto_bidid=xFKRoV9YYkVuajNiVnFpY25RcEwlMkZ6VkRnWG91WldKR1VkMVpqTHhldkp3djBqcjlaYWlJUzl1ZEo0SFkxcjB0RyUyRkREZGNBalElMkI3QUR5WVBPREhVQzMlMkZ0SjElMkJydnYzRFBwZmd5RmYzVVF0TEJ2S28lM0Q; IS_FIRST_AD_REQUEST_V2=false; COUNTER_FOR_ADVERTISING_FIRST_PARTY_UID_V2=9; ADVERTISING_FIRST_PARTY_UID_V2=dfd12a9b-b424-492e-af85-b64e1068cb03; __gads=ID=25f53b83fe55ef4a:T=1678735706:S=ALNI_MaS7FcrQfuFPeguTs4rHCZLYTe2lw; __gpi=UID=00000bd8b59e7a73:T=1678735706:RT=1678735706:S=ALNI_MY-PMvNXW5WjW7FPx6P49huhQfN1g; CONSENT_FOR_FIRST_PARTY_COOKIES=true; FIRST_PARTY_TRACKINGID=7eb82009-ab62-4fef-b62a-1d93017e2c5e',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1'
                }

                # selected_proxy = random.choice(self.proxies)
                selected_proxy = self.proxies[0]
                proxy = f'http://{selected_proxy}'

                # async with s.get(url, headers=headers) as r:
                async with s.get(url, headers=headers, proxy=proxy, timeout=7) as r:
                        if r.status != 200:
                                r.raise_for_status()

                        return await r.text()

        async def fetch_all(self, s, urls):
                tasks = list()
                for url in urls:
                        task = asyncio.create_task(self.fetch(s,url))
                        tasks.append(task)
                res = await asyncio.gather(*tasks)
                return res

        # async def run(self, keyword):
        async def run(self):
                urls = list()
                for page in range(1,20):
                        # url = f'https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?sfId=8ef62b18-a054-404c-8f50-f28cd3ce1a00&isNavigation=true&keyword={keyword}&rows=90&page={page}'
                        url = f'https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz?sfId=2b8dd095-db9f-487f-b2a8-c595d89c1aec&isNavigation=true&page={page}&rows=90'
                        urls.append(url)

                session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=7, sock_read=10)
                async with aiohttp.ClientSession(timeout=session_timeout) as s:
                        htmls = await self.fetch_all(s, urls)
                return htmls

        def parser(self, htmls):
                product_list = list()
                for html in htmls:
                        tree = HTMLParser(html)
                        json_data = json.loads(tree.css_first('script#__NEXT_DATA__').text())
                        items = json_data['props']['pageProps']['searchResult']['advertSummaryList']['advertSummary']
                        item_name = None
                        item_price = None
                        item_desc = None
                        item_img = None
                        item_publish = None
                        item_post = None
                        item_address = None
                        item_link = None
                        for item in items:
                                attributes = item['attributes']['attribute']
                                for attribute in attributes:
                                        if attribute['name'] == 'HEADING':
                                                item_name = attribute['values'][0]
                                        if attribute['name'] == 'BODY_DYN':
                                                item_desc = attribute['values'][0]
                                        if attribute['name'] == 'PRICE_FOR_DISPLAY':
                                                item_price = attribute['values'][0]
                                        if attribute['name'] == 'ALL_IMAGE_URLS':
                                                item_img = self.baseurl + '/mmo/' + attribute['values'][0].split(';')[0]
                                        if attribute['name'] == 'PUBLISHED_String':
                                                item_publish = attribute['values'][0]
                                        if attribute['name'] == 'POSTCODE':
                                                item_post = attribute['values'][0]
                                        if attribute['name'] == 'ADDRESS':
                                                item_address = attribute['values'][0]
                                        if attribute['name'] == 'SEO_URL':
                                                item_link = self.baseurl + '/iad/' + attribute['values'][0]

                                new_item = Product(name=item_name, price=item_price, description=item_desc, img=item_img, publish=item_publish, post=item_post, address=item_address, link=item_link)
                                product_list.append(asdict(new_item))
                return product_list

        def get_proxy(self):
                # print("Collecting proxies...")
                with requests.Session() as s:
                        response = s.get('https://free-proxy-list.net/')
                tree = HTMLParser(response.text)
                list_data = tree.css('table.table.table-striped.table-bordered > tbody > tr')
                scraped_proxies = []
                blocked_cc = ['IR', 'RU']
                for i in list_data:
                        ip = i.css_first('tr > td:nth-child(1)').text()
                        port = i.css_first('tr > td:nth-child(2)').text()
                        cc = i.css_first('tr > td:nth-child(3)').text()
                        if cc in blocked_cc:
                                continue
                        else:
                                scraped_proxies.append(f'{ip}:{port}')
                # print(f"{len(scraped_proxies)} proxies collected")
                # print(scraped_proxies)
                return scraped_proxies

        async def proxy_check(self, s, scraped_proxy):
            ua = random.choice(self.useragent)
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
                }
            proxy = f'http://{scraped_proxy}'
            try:
                    async with s.get('https://www.willhaben.at', headers=headers, proxy=proxy, timeout=7) as r:
                            if r.status != 200:
                                    r.raise_for_status()
                                    return 'Null'
                            else:
                                    # print(f'{scraped_proxy} selected')
                                    return scraped_proxy
            except Exception as e:
                # print(f"not working with {e}")
                return 'Null'

        async def all_proxy_check(self, s, scraped_proxies):
                tasks = list()
                for i, scraped_proxy in enumerate(scraped_proxies):
                        task = asyncio.create_task(self.proxy_check(s,scraped_proxy))
                        tasks.append(task)
                res = await asyncio.gather(*tasks)
                return res

        async def choose_proxy(self):
                scraped_proxies = self.get_proxy()
                working_proxies = list()
                session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=7,
                                                        sock_read=10)
                async with aiohttp.ClientSession(timeout=session_timeout) as s:
                        working_proxies = await self.all_proxy_check(s, scraped_proxies)
                return working_proxies

        def main(self):
                # keyword = 'Kindermode'
                # htmls = asyncio.run(self.run(keyword=keyword))
                proxies = asyncio.run(self.choose_proxy())
                proxies = [value for value in proxies if value != 'Null']
                # print(proxies)
                # proxies = ['103.121.149.69:8080', '146.56.136.237:9090', '43.132.184.228:8181', '88.255.217.37:8080', '140.120.15.146:8088']
                self.proxies=proxies
                htmls = asyncio.run(self.run())
                return self.parser(htmls)

# if __name__ == '__main__':
#         proxies = [
#                 '142.214.181.36:8800',
#                 '142.214.181.241:8800',
#                 '196.51.116.40:8800',
#                 '196.51.114.196:8800',
#                 '142.214.181.41:8800',
#                 '196.51.116.171:8800',
#                 '142.214.181.219:8800',
#                 '142.214.183.243:8800',
#                 '196.51.114.248:8800',
#                 '142.214.183.70:8800'
#         ]
#
#         useragent = [
#                 'Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.137 Safari/537.36 Ubuntu/22.04 (5.0.2497.35-1) Vivaldi/5.0.2497.35',
#                 'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.48-1) Vivaldi/5.0.2497.48',
#                 'Mozilla/5.0 (Wayland; Linux x86_64; System76 Galago Pro (galp2)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.175 Safari/537.36 Ubuntu/22.04 (5.0.2497.51-1) Vivaldi/5.0.2497.51,',
#                 'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.39',
#                 'Mozilla/5.0 (Wayland; Linux x86_64; System76) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.92 Safari/537.36 Ubuntu/22.04 (5.2.2623.34-1) Vivaldi/5.2.2623.34'
#         ]
#
#         keyword = 'Kindermode'
#         start = perf_counter()
        # s = Scraper(proxies=proxies, useragent=useragent)
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # htmls = asyncio.run(s.main(keyword=keyword))
        # result = s.parser(htmls)
        # for i in result:
        #         print(i)
        # print(len(result))
        # s = Scraper()
        # result = s.main()
        # print(result)
        # stop = perf_counter()
        # print(f'time taken: {stop - start}')