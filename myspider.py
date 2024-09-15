import scrapy
from scrapy.http import HtmlResponse
from pymongo.mongo_client import MongoClient
from bookitem import SimpleItem
from scrapy.loader import ItemLoader


class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains=["unsplash.com"]
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('category')}"]
        
    #Парсим данные по инструкции
    def parse(self, response:HtmlResponse):
        # print(response.status,response.url)
        # links=response.xpath("//a[@class='zNNw1']")
        links=response.xpath("//a[@class='zNNw1']/@href")
        for link in links:
            yield response.follow(link,callback=self.parse_book) #может сам доставать ссылку из элементов (работает не всегда)
        
                       
    def parse_book(self,response:HtmlResponse):
        # item{
        #     'title':response.xpath("//p[@class='liDlw']/text()").get()
        #     'author':response.xpath("//a[@class='vGXaw uoMSP kXLw7 R6ToQ JVs7s R6ToQ']/text()").get()
        #     'published':response.xpath("//time/@datetime").get()
        #     'url':response.url
        #     'photos':response.xpath("//img[@class='I7OuT DVW3V L1BOa']/@srcset").getall()
        # }
        loader=ItemLoader(item=SimpleItem(),response=response)
        loader.add_xpath('title',"//p[@class='liDlw']/text()")
        loader.add_xpath('author',"//a[@class='vGXaw uoMSP kXLw7 R6ToQ JVs7s R6ToQ']/text()")
        loader.add_xpath('published',"//time/@datetime")
        loader.add_value('url',response.url)
        loader.add_xpath('photos',"//img[@class='I7OuT DVW3V L1BOa']/@srcset")
        
        yield loader.load_item()
        # yield item
    
    # Закрытие соединения с MongoDB после завершения работы паука
    def closed(self, reason):
        print("Done")
        # self.client.close()
