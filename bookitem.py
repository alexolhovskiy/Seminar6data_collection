import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose

def process_title(value):
    return value.strip()


def process_photo(value):
    # return list(filter(lambda item:item.startswith('https:'),value.split()))[0]
    # print(value)
    return value.split()[0].strip()

def process_published(value):
    return value[:10]


class SimpleItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(process_title))
    author = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(process_title))
    url = scrapy.Field(output_processor=TakeFirst())
    photos=scrapy.Field(input_processor=MapCompose(process_photo))
    published=scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(process_published))
    # title = scrapy.Field()
    # author = scrapy.Field()
    # url = scrapy.Field()
    # photos=scrapy.Field()
    # published=scrapy.Field()
