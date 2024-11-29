
import scrapy
from picjumbo.items import PicjumboItem
from scrapy.loader import ItemLoader

class PicjumbospyderSpider(scrapy.Spider):
    name = "picjumbospyder"
    allowed_domains = ["picjumbo.com", 'i0.wp.com']
    start_urls = ["https://picjumbo.com"]

    def parse(self, response):
        # Находим все категории на главной странице
        categories = response.xpath("//li[contains(@class, 'menu-item')]/a")
        for category in categories:
            # Извлекаем имя и URL каждой категории
            category_name = category.xpath("//li[@id='menu-item-32912']//li/a/text()").get()
            category_url = category.xpath("//li[@id='menu-item-32912']//li/a/@href").get()
            # Переходим на страницу категории, передавая имя категории
            yield response.follow(category_url, callback=self.parse_category, cb_kwargs={'category': category_name})

    def parse_category(self, response, category):
        # Находим все ссылки на фотографии в категории
        photos = response.xpath("//div[@class='masonry_item photo_item']//a/@href").getall()
        for photo in photos:
            # Переходим на страницу каждой фотографии
            yield response.follow(photo, callback=self.parse_photo, cb_kwargs={'category': category})

        # Проверяем наличие следующей страницы
        next_page = response.xpath("//div[@class='pagination']/a[@class='next page-numbers']/@href").get()
        if next_page:
            try:
                # Переходим на следующую страницу категории
                yield response.follow(next_page, callback=self.parse_category, cb_kwargs={'category': category})
            except Exception as e:
                # Логируем ошибки при переходе на следующую страницу
                with open("errors.txt", "a") as error_file:
                    error_file.write(f"Category: {category}\n")
                    error_file.write(f"Next Page: {next_page}\n")
                    error_file.write(f"Error: {str(e)}\n")
                    error_file.write("=" * 40 + "\n")

    def parse_photo(self, response, category):
        # Используем ItemLoader для извлечения данных
        loader = ItemLoader(item=PicjumboItem(), response=response)
        # Извлекаем название фотографии
        loader.add_xpath('name', "//h1/a/text()")
        # Извлекаем ссылки на изображения
        loader.add_xpath('links', "//div[@class='single']//img/@src | //div[@class='single']//img/@srcset")
        # Добавляем URL страницы
        loader.add_value('url', response.url)
        # Добавляем категорию
        loader.add_value('category', category)

        # Возвращаем заполненный item
        yield loader.load_item()