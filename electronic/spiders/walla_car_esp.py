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
    name = 'dose'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    ]

    def __init__(self):
        # Configuración de opciones de Firefox
        firefox_options = Options()
        firefox_options.set_preference("general.useragent.override", random.choice(self.USER_AGENTS))
        
        # Ruta al perfil de Firefox
        profile_path = r'C:\Users\Usuario\AppData\Roaming\Mozilla\Firefox\Profiles\yfg9gzjx.default-release'
        firefox_options.profile = profile_path

        # Iniciar WebDriver con el perfil y opciones
        s = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=s, options=firefox_options)

        self.login_timer_started = False  # Variable de control para el temporizador

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DondeSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self):
        # Cierra el navegador al finalizar
        self.driver.quit()

    def start_requests(self):
        urls = [
            'https://es.wallapop.com/app/buscar?filters_source=search_box&keywords=coches%20madrid&category_ids=100&longitud=-3.69196&latitud=40.41956'
        ]
        for url in urls:
            headers = {
                'User-Agent': random.choice(self.USER_AGENTS),
                'Referer': 'https://www.google.com',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
            time.sleep(random.randint(1, 5))

    def parse(self, response):
        # Abre la URL en el navegador Selenium
        self.driver.get(response.url)

        # Temporizador de 1 minuto para iniciar sesión manualmente
        if not self.login_timer_started:
            self.login_timer_started = True
            self.logger.info("Temporizador de 1 minuto activado para loguearse.")
            time.sleep(20)  # Espera de 1 minuto para que puedas loguearte

        try:
            # Espera a que los elementos de la página sean visibles
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'ItemCardList__item')]"))
            )
            
            # Captura el contenido de la página para procesarlo con Scrapy
            body = self.driver.page_source
            response = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=response.request)
            
            # Extrae los datos de los artículos
            articles = response.xpath("//a[contains(@class, 'ItemCardList__item')]")
            for article in articles:
                title = article.xpath(".//span[contains(@class,'ItemCardWide__title')]/text()").get()
                price = article.xpath(".//span[contains(@class,'ItemCardWide__price')]/text()").get()
                type_1 = article.xpath(".//div[contains(@class,'ItemExtraInfo')]/label[1]/text()").get()
                type_2 = article.xpath(".//div[contains(@class,'ItemExtraInfo')]/label[2]/text()").get()
                type_3 = article.xpath(".//div[contains(@class,'ItemExtraInfo')]/label[3]/text()").get()
                type_4 = article.xpath(".//div[contains(@class,'ItemExtraInfo')]/label[4]/text()").get()
                type_5 = article.xpath(".//div[contains(@class,'ItemExtraInfo')]/label[5]/text()").get()
                type_6 = article.xpath(".//div[contains(@class,'ItemExtraInfo')]/label[6]/text()").get()
                description = article.xpath(".//span[contains(@class,'ItemCardWide__description--with-highlight-label')]/text()").get()
                link = article.xpath(".//@href").get()

                yield {
                    'title': title,
                    'price': price,
                    'type1': type_1,
                    'type2': type_2,
                    'type3': type_3,
                    'type4': type_4,
                    'type5': type_5,
                    'type6': type_6,
                    'description': description,
                    'link': link
                }
                time.sleep(random.uniform(0.5, 2))  # Retardo aleatorio entre artículos
            
        except Exception as e:
            self.logger.error(f"Error al procesar la página: {e}")
