# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from typing import Any

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request

from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline


class PicjumboPipeline:
    def process_item(self, item, spider):
        print(item)
        return item


class PhotosPipline (ImagesPipeline):
    def get_media_requests(self, item: Any, info: MediaPipeline.SpiderInfo) -> list[Request]:
        if item['links']:
            for link in item['links']:
                try:
                    # Открываем сессию по взаимодействию с сервером
                    print(link)
                    print()
                    yield scrapy.Request(link)
                except Exception as e:
                    print(e)
