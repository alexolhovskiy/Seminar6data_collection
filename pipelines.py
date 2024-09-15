from pprint import pprint
import csv
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class SimplePhotosPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)
                    
    def item_completed(self,results,item,info):
        # pprint(result)
        if results:
            item['photos']=[itm[1] for itm in results if itm[0]]
        return item
        

class SimplePipeline:

    def open_spider(self, spider):
        self.file = open('output.csv', 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=['title', 'author', 'url','published','photos'])
        self.writer.writeheader()
        pass

    def process_item(self, item, spider):
        # Записываем данные в CSV файл
        self.writer.writerow(item)
        print(item)  # Выводим данные на экран
        return item

    def close_spider(self, spider):
        self.file.close()  # Закрываем файл после завершения работы паука
        print("Done")
