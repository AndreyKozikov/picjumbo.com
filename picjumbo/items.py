# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy

from itemloaders.processors import TakeFirst, MapCompose, Compose


def process_links(values):
    # Список для хранения всех найденных ссылок
    urls = set()

    for value in values:
        # Разделяем строки по запятой, удаляем лишние пробелы и переносы строк
        parts = [part.strip() for part in value.split(',')]

        for part in parts:
            # Убираем пробелы, оставляем только часть перед пробелом
            url = part.split(' ')[0].strip()
            # Проверяем и добавляем "http:" вместо "//", если это необходимо
            if url.startswith('//'):
                url = 'http:' + url
            # Добавляем обработанный URL в список, если это ссылка
            if url.startswith('http') and (url.find("photo") == -1):
                urls.add(url)

    # Убираем дубликаты и возвращаем список
    return list(urls)

class PicjumboItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    links = scrapy.Field(input_processor=Compose(process_links))

