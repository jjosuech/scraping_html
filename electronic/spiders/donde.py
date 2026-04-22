import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import random
import time

class DondeSpider(scrapy.Spider):
    name = 'donde'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    ]

    def __init__(self):
        # Configuración de opciones para Firefox
        firefox_options = Options()
        firefox_options.set_preference("general.useragent.override", random.choice(self.USER_AGENTS))
        # firefox_options.add_argument('--headless')  # Descomenta esta línea para ejecutar en modo headless

        # Inicializa el controlador de Firefox con GeckoDriver
        s = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=s, options=firefox_options)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DondeSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self):
        self.driver.quit()

    def start_requests(self):
        urls = [
            'https://www.adondevivir.com/en-venta-en-pueblo-libre-pagina-22-q-lima.html',
        ]
        for url in urls:
            headers = {
                'User-Agent': random.choice(self.USER_AGENTS),
                'Referer': 'https://www.google.com',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
            time.sleep(random.randint(1, 5))  # Retraso aleatorio entre 1 y 5 segundos

    def parse(self, response):
        self.driver.get(response.url)

        # Espera explícita para asegurarse de que los elementos estén cargados
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'postings-container')]"))
        )
        
        body = self.driver.page_source
        response = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=response.request)
        
        articles = response.xpath("//div[contains(@class, 'postings-container')]/div")
        for article in articles:
            address = article.xpath(".//div[contains(@class,'postingAddress')]/text()").get()
            ciudad = article.xpath(".//h2[contains(@data-qa, 'POSTING_CARD_LOCATION')]/text()").get()
            price = article.xpath(".//div[contains(@data-qa, 'POSTING_CARD_PRICE')]/text()").get()
            des_un = article.xpath(".//h3[@data-qa='POSTING_CARD_FEATURES']/span[1]/text()").get()
            des_dor = article.xpath(".//h3[@data-qa='POSTING_CARD_FEATURES']/span[2]/text()").get()
            des_mt2 = article.xpath(".//h3[@data-qa='POSTING_CARD_FEATURES']/span[3]/text()").get()
            link = article.xpath(".//h3[contains(@data-qa, 'POSTING_CARD_DESCRIPTION')]/a/@href").get()
            descripcion = article.xpath(".//h3[contains(@data-qa, 'POSTING_CARD_DESCRIPTION')]/a/text()").get()

            yield {
                'city': ciudad,
                'address': address,
                'price': price,
                'des_un': des_un,
                'des_dor': des_dor,
                'des_mt2': des_mt2,
                'descripcion': descripcion,
                'link': 'https://www.adondevivir.com' + link,
            }
