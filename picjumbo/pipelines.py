# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from typing import Any

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request

from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline, FileInfoOrError


class PicjumboPipeline:
    def __init__(self):
        self.file = open('image_info.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['image_url', 'local_path', 'name', 'category'])

    def process_item(self, item, spider):
        for link in item['links']:
            self.writer.writerow([
                link['url'],
                link['path'],
                item['name'],
                item['category'],
            ])
        return item

    def close_spider(self, spider):
        self.file.close()


class PhotosPipline (ImagesPipeline):
    def get_media_requests(self, item: Any, info: MediaPipeline.SpiderInfo) -> list[Request]:
        links = item.get('links', [])
        if links:
            for link in links:
                try:
                    # Открываем сессию по взаимодействию с сервером
                    yield scrapy.Request(link)
                except Exception as e:
                    print(e)

    def item_completed(self, results: list[FileInfoOrError], item: Any, info: MediaPipeline.SpiderInfo) -> Any:
        if results:
            item['links'] = [itm[1] for itm in results if itm[0]]
        return item # Возвращаем item после его переопределения