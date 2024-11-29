# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy

from itemloaders.processors import TakeFirst, MapCompose, Compose

def process_links(value):
    return value

class PicjumboItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    links = scrapy.Field(input_processor=MapCompose(process_links))

