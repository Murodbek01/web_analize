# Класс Spider
import requests
from bs4 import BeautifulSoup
from urllib import parse
from spider.domain import *
from requests import RequestException
from .models import AddUrlsInTable, AddMainUrls
from  spider.pageRunk import pageRank

class Spider:
    base_url = ''
    externalLInks = set()
    brokenLinks = set()
    main_arr = []

    def __init__(self, base_url):
        Spider.base_url = base_url
        self.boot()

    @staticmethod
    def boot():
        Spider.main_arr = []
        Spider.externalLInks = set()
        Spider.brokenLinks = set()

    @staticmethod
    def get_links(b_url):
        links = []
        try:
            source_cod = requests.get(b_url)
            text = source_cod.text
            soup = BeautifulSoup(text, 'html.parser')
            for link in soup.findAll('a', href=True):
                href = link.get('href')
                url = parse.urljoin(Spider.base_url, href)
                if url not in links:
                    if internal_links(url):
                        if get_domain_name(Spider.base_url) != get_domain_name(url):
                            Spider.externalLInks.add(url)
                        else:
                            if url != b_url:
                                links.append(url)
        except RequestException as e:
            print(str(e))
            Spider.brokenLinks.add(b_url)
            return []
        return links
    '''
    @staticmethod
    def add_links_to_main_arr(urls):
        for url in urls:
            if url in Spider.main_arr:
                continue
            Spider.main_arr.append(url)
            link = AddMainUrls(url=url)
            link.save()
    '''
    @staticmethod
    def add_urls(urls):
        urls_dict = {item['url']: item['id'] for item in Spider.main_arr}

        max_id = max(urls_dict.values())
        for url in urls:
            if url not in urls_dict:
                Spider.main_arr.append({'id': max_id + 1, 'url': url})
                max_id += 1
                link = AddMainUrls(url=url)
                link.save()

    @staticmethod
    def add_links_to_table(in_url, urls):
        for url in urls:
            links = AddUrlsInTable(inn=in_url,out=url)
            links.save()

    @staticmethod
    def set_id(urls):
        temp = []
        for url in urls:
            for i in range(len(Spider.main_arr)):
                if url == Spider.main_arr[i]['url']:
                    temp.append({'id': Spider.main_arr[i]['id'], 'url': url})
        return temp

    @staticmethod
    def work():
        Spider.main_arr.append({'id': 0, 'url': Spider.base_url})
        sv_url = Spider.main_arr[0]['url']
        link = AddMainUrls(url=sv_url)
        link.save()
        link_matrix = [[]]
        i = 0
        data = []
        while i < len(Spider.main_arr):
            url = Spider.main_arr[i]['url']
            base_id = Spider.main_arr[i]['id']
            result = Spider.get_links(url)
            if len(result) == 0:
                i += 1
                continue
            Spider.add_urls(result)
            Spider.add_links_to_table(url, result)
            result2 = Spider.set_id(result)

            for k in result2:
                data.append({'base_id': base_id, 'link_id': k['id']})
            i += 1
        if len(Spider.main_arr) > 1:
            for i in data:
                (frm, to) = i['base_id'], i['link_id']
                extend = max(frm - len(link_matrix), to - len(link_matrix)) + 1
                for i in range(extend):
                    link_matrix.append([])
                link_matrix[frm].append(to)

            pr = pageRank(link_matrix, alpha=0.85, convergence=0.00001, checkSteps=10)

            return pr
        else:
            return "URL не доступен"

