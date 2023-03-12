import httpx
import aiohttp
from selectolax.parser import HTMLParser
from dataclasses import dataclass
import asyncio
import random
from time import perf_counter
from typing import List

@data

@dataclass
class Scraper:
        proxies : List[str]

        async def fetch(self, s, url):
                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        # 'Cookie': 'bbxDmpSegments=[]; SRV=5|ZA4wu; IADVISITOR=9742ab70-deb0-43c4-9b29-7ca8553a937e; context=prod; TRACKINGID=abd7e221-9f47-4d91-a067-234ea882a501; x-bbx-csrf-token=ef17beb6-f847-4d83-8430-6f2e63c478fc; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22f0db7e6e-e50a-4c77-b292-16d1ea4cad53%22%2C%22options%22%3A%7B%22end%22%3A%222024-04-12T20%3A00%3A26.553Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-612451-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A31536000%2C%22end%22%3A31536000%7D%7D; ioam2018=00022df0f26227ab6640e2e5f:1705866976371:1678650976371:.willhaben.at:7:at_w_atwillhab:Service/Rubrikenmaerkte/Sonstiges/Mode_Accessoires/TL:noevent:1678651575434:159dew; didomi_token=eyJ1c2VyX2lkIjoiMTg2ZDc2NTItOWY0ZS02NjYxLTg0YTktNTcxZjFhOTgzMjFiIiwiY3JlYXRlZCI6IjIwMjMtMDMtMTJUMTk6NTY6MjMuNDQ1WiIsInVwZGF0ZWQiOiIyMDIzLTAzLTEyVDE5OjU2OjIzLjQ0NVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYW1hem9uIiwiZ29vZ2xlIiwiYzpvZXdhLVhBUW1HU2duIiwiYzphbWF6b24tbW9iaWxlLWFkcyIsImM6aG90amFyIiwiYzp1c2Vyem9vbSIsImM6YW1hem9uLWFzc29jaWF0ZXMiLCJjOnh4eGx1dHprLW05ZlFrUHRMIiwiYzpvcHRpb25hbGUtYm5BRXlaeHkiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsieHh4bHV0enItcWtyYXAzM1EiLCJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSIsImM6d2lsbGhhYmVuLVpxR242WXh6Il19LCJ2ZXJzaW9uIjoyLCJhYyI6IkFrdUFFQUZrQkpZQS5Ba3VBRUFGa0JKWUEifQ==; _pulse2data=590120fd-088a-41f1-9877-3794cd3e37c1%2Cv%2C%2C1678651877727%2CeyJpc3N1ZWRBdCI6IjIwMjMtMDMtMTJUMTk6NTY6MTZaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..3qH9DDYdf8XEoalGIsayMQ.DXV9o-oxncPxypbrpMN57xmbBD7axrMq7CdXF0fSZSNoRBlDkdlJjI0rRUlQD7EhXEAbS_VR0PlYDlC1gFi3BT0wLdR_nZxU1XEVnuxCyCG4ERBLLeutJCYwLX-gOgLPqQLrcEzzpB5Km0x7NqEhz6cjzr0U1VA2qlgVdosWJLaB_vFdjKkWBcauSUGHoOY9Ek6zAZn7DxOUip-zJmETkA.7ZcCDT_oj9_fWLmJiFQhLA%2C%2C%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..rBb2C2s0jzOwzy6OEdqdvbCKJ0wrQs7749UxPVnBmP4; RANDOM_USER_GROUP_COOKIE_NAME=22; _pbjs_userid_consent_data=5425172714880651; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%223c46eca8-6efd-424a-8582-4511c31870d9%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-03-12T19%3A56%3A20%22%7D; cto_bundle=brsLzV93dXVuYTd0dVBJRmgzSGdwJTJCaENTSzFtUCUyQm1HOFV5RGZyZkVRa0ZPbnh4YnlLSmtHWXVxTWFMJTJCNSUyQmhWcHpCeGhHbGRyZDVJM1l5ODhrTmh2b2x2TFBtaUdGZTg4c1o1YklKck1WZEVUUDlVJTJCclNiakJXVG4wamJ4UkV3RWNMMXNTOXdWdlVCQnN5bmowdnNDVGplSTFBJTNEJTNE; cto_bidid=WK37WF9PQ045VlV3VDE1YmJsdjdEUkUxRUdZQThBdmFCb3Rxazg3YkNYc2wlMkY5c3BKdjRpVWdpWVhCSWdRR0FTYmpTNCUyQldBZUh3aDYlMkJpSGNSNmJMSjVScWZKT3lCTDZJNkFaMXZXU1VTN01pOUpXdyUzRA; euconsent-v2=CPogtwAPogtwAAHABBENC6CsAP_AAH_AAAAAIzNf_X_fb2_j-_59f_t0eY1P9_7_v-0zjhedk-8Nyd_X_L8X52M7vB36pq4KuR4ku3LBAQdlHOHcTQmw6IkVqSPsbk2Mr7NKJ7PEmlMbO2dYGH9_n1XT-ZKY79__f_7z_v-v____7r__7-3f3_vp9V-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABA3QAkw1biALsSxwJtowigRAjCsJCoBQAUUAwtEBhASuCnZXAT6wiQAIBQBGBECHAFGDAIAAAIAkIiAECPBAAACIBAACABUIhAARoAgoAJAQCAAUA0LACKAIQJCDIgIilMCAiRIKCeQIQSg_0MMIQ6igAAA.f_gAD_gAAAAA; permutive-id=e1fb75fb-33e4-48da-b804-f0ae850e0882; id5id.1st_426_nb=4; IS_FIRST_AD_REQUEST_V2=false; COUNTER_FOR_ADVERTISING_FIRST_PARTY_UID_V2=6; __gads=ID=9642433c3eacd087:T=1678651046:S=ALNI_Mb9nNf9Ie6J-bujyAbjDBbjRMFwIg; __gpi=UID=00000bd862a85073:T=1678651046:RT=1678651046:S=ALNI_MZj3cYD2iRVy7WNzaN8D4itttRjNw; CONSENT_FOR_FIRST_PARTY_COOKIES=true; ADVERTISING_FIRST_PARTY_UID_V2=d77c5f97-8ae2-40db-9a88-a72620abf047; FIRST_PARTY_TRACKINGID=abd7e221-9f47-4d91-a067-234ea882a501; id5id.1st=%20%7B%20%22created_at%22%3A%20%222023-03-12T20%3A00%3A07.531478818Z%22%2C%20%22id5_consent%22%3A%20true%2C%20%22original_uid%22%3A%20%22ID5*OQOCQVvuyJVsBVpZZAiWkU0ygyj1O8QUrfeKSOj-L_o-HLrW7x-IZb2sPEyePSVWPh5s93X0O7L-nKFAqBWUeD4f3HzQYy2unxtqg8g8Qp8-IPZztK-xwMLTo0pgks8MPiHYO7tjhmwwYl6dQn8-UT4iEujf0QjFNwQVJGRRLTU-J3_c3ZeJ-OE_nyth3fxKPiix0T6CuRcq4bCal6piPT4pCNLw3H5rqtCANqrro-g-KopFWf6w6RYAYp4TwZUdPiwEFoX2Qk32A5G-DSZE3T4upQOIb5YQOSz8zbti_Bc-Lz0OTtlTSR6-IHvJSVNvPjBy83UvYr6XDtUXrpJ1Vz4ytDYbSSfKFjw3gUbaCxg-MwGlB5ZkA7UaMi8o54HnPjYwWkWlbVXN-qhQbRusMz43H5oSHdiLEpC8aAm9_cE-OZ7y508v0G6KPuHeAARWPjyatFU-N8jwrA3CvaWB4j49GS-KBNZGDlDV5mrr_go-P_wmS4t1gZ0RxYxIyPwePkIu4cjEZv9AdzdgINdYYz5DU350oy0Hrw2p8pp25DM-Rxo9IfZUiwmVE_y79D5J%22%2C%20%22universal_uid%22%3A%20%22ID5*l3scth2-IY0sooZx65sZWMOE_GSdoHWYLpnv5hK3VwQ-HNT3co58WUQGoNqZQ-gOPh6gvRVSDjVltBop7KBfaD4fuxAMlXOLCt27PFWD5OU-IEx05jypwTeDgsflWGWVPiEYg7Krd2JTRLjRiwkYpj4ileGdx6UQkL1NvQejwFM-J508mjfrMPjjqyXEbXAqPig55zsrJDZj0GaiZSeE0D4p7qA5pozWeVQO0qIva2s-KscDjWfQA4CVz_QzjLmLPixzaHvQoufBfOEw_cijEz4uspPBrk9nPHIxE3kWcoY-LwWkKzbxsg2Tg5iqD47UPjCzm1qzgKItcFlmFUktIj4yEt0r_iNDX6Vw1XtMy14-M0Axbm2-vCmGxUUSJ6RnPjYGimxCeDOPwznapx2_Pz43DjNmQTEpWVFvYKeIS7c-OXw2BVitWegmuFt7KIspPjwJkTVR6ZNHcN7FBNEceT49Qa30-rrwfS1yaf1ob4U-Py9LYrdm9mBr6MNcgL6jPkK3G0r-rXn1e2zwbej-Cj5Doyl0LD7og4fKjn2fujE-R9IttFfaKkOJOIT7Dboh%22%2C%20%22signature%22%3A%20%22ID5_AhD4p0SQK3Z9ncM2bDecpzIq3TK3g4dvJppOdDNnJVkxQLkwpdXsgslI9EoEsPzznhQqNL62_Vd5JCHd3a3_57fB9H2v%22%2C%20%22link_type%22%3A%201%2C%20%22cascade_needed%22%3A%20true%2C%20%22privacy%22%3A%20%7B%20%22jurisdiction%22%3A%20%22gdpr%22%2C%20%22id5_consent%22%3A%20true%7D%7D; id5id.1st_last=1678651208498',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1'
                }

                selected_proxy = random.choice(self.proxies)
                print(selected_proxy)
                proxy = f'http://{selected_proxy}'

                async with s.get(url, headers=headers, proxy=proxy) as r:
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

        async def main(self):
                urls = list()
                for page in range(1,20):
                        url = f'https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz/mode-accessoires-3275/a/zustand-neu-22?keyword=sneaker&sfId=cfccbeaa-2f0b-49ca-881f-ec28c6b42f7f&isNavigation=true&page={page}&rows=90'
                        urls.append(url)
                print(urls)

                async with aiohttp.ClientSession() as s:
                        htmls = await self.fetch_all(s, urls)
                print(htmls)


if __name__ == '__main__':
        proxies = [
                '142.214.181.36:8800',
                '142.214.181.241:8800',
                '196.51.116.40:8800',
                '196.51.114.196:8800',
                '142.214.181.41:8800',
                '196.51.116.171:8800',
                '142.214.181.219:8800',
                '142.214.183.243:8800',
                '196.51.114.248:8800',
                '142.214.183.70:8800'
        ]
        start = perf_counter()
        s = Scraper(proxies=proxies)
        asyncio.run(s.main())
        stop = perf_counter()
        print(f'time taken: {stop - start}')