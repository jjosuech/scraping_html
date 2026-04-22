# import scrapy


# class IdealistaSpider(scrapy.Spider):
#     # Your spider definition
#     name = "idealista"
#     custom_settings = {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'DOWNLOAD_DELAY': 2,  # or a number that makes sense for the site you are scraping
#         # Other settings like proxies, cookies, etc.
#     }

#     def start_requests(self):
#         urls = [
#             'https://www.idealista.com/areas/alquiler-habitacion/?shape=%28%28kwmuFnzbVeGmE%3FiC%7D%7E%40ivAunAwmChwBa%60ExlCdoCxQxoCc%60CzoC%29%29',
#             # other URLs
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse, headers={
#                 'Referer': 'https://www.idealista.com'
#             })
    

#     def parse(self, response):
#         # Assuming you want to iterate through all articles
#         articles = response.xpath("//*[@id='main-content']/section/article")
#         for article in articles:
#             title = article.xpath(".//div[contains(@class,'item-info-container')]/a/@title").get()
#             price = article.xpath(".//div[contains(@class,'price-row')]/span[@class='item-price']/text()").get()
#             description = article.xpath(".//div[contains(@class,'item-description')]/p/text()").get()

#             yield {
#                 'title': title,
#                 'price': price,
#                 'description': description,
#             }


import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class IdealistaSpider(scrapy.Spider):
    name = 'idealista'

    def __init__(self):
        chrome_options = Options()
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like IndeedGecko) Chrome/91.0.4472.124 Safari/537.36"
        chrome_options.add_argument(f'user-agent={USER_AGENT}')
        #chrome_options.add_argument('--headless')
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=chrome_options)

        #self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(IdealistaSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self):
        self.driver.close() 

    def start_requests(self):
        urls = [
            'https://www.idealista.com/areas/alquiler-habitacion/?shape=%28%28kwmuFnzbVeGmE%3FiC%7D%7E%40ivAunAwmChwBa%60ExlCdoCxQxoCc%60CzoC%29%29',
            # other URLs
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        body = self.driver.page_source
        response = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=response.request)
        
        # Now you can use response.xpath as you would in a regular Scrapy parse method.
        articles = response.xpath("//*[@id='main-content']/section/article")
        for article in articles:
            title = article.xpath(".//div[contains(@class,'item-info-container')]/a/@title").get()
            price = article.xpath(".//div[contains(@class,'price-row')]/span[@class='item-price']/text()").get()
            description = article.xpath(".//div[contains(@class,'item-description')]/p/text()").get()

            yield {
                'title': title,
                'price': price,
                'description': description,
            }
