import scrapy
from picjumbo.items import PicjumboItem
from scrapy.loader import ItemLoader


class PicjumbospyderSpider(scrapy.Spider):
    name = "picjumbospyder"
    allowed_domains = ["picjumbo.com", 'i0.wp.com']
    start_urls = ["https://picjumbo.com"]

    def parse(self, response):
        categories = response.xpath("//li[contains(@class, 'menu-item')]/a")
        for category in categories:
            category_name = category.xpath(
                "//li[@id='menu-item-32912']//li/a/text()").get()  # Извлечение имени категории
            category_url = category.xpath("//li[@id='menu-item-32912']//li/a/@href").get()  # Извлечение URL категории
            yield response.follow(category_url, callback=self.parse_category, cb_kwargs={'category': category_name})

    def parse_category(self, response, category):
        photos = response.xpath("//div[@class='masonry_item photo_item']//a/@href").getall()
        for photo in photos:
            yield response.follow(photo, callback=self.parse_photo, cb_kwargs={'category': category})

        next_page = response.xpath("//div[@class='pagination']/a[@class='next page-numbers']/@href").get()
        if next_page:

            try:
                yield response.follow(next_page, callback=self.parse_category, cb_kwargs={'category': category})
            except Exception as e:
                with open("errors.txt", "a") as error_file:
                    error_file.write(f"Category: {category}\n")
                    error_file.write(f"Next Page: {next_page}\n")
                    error_file.write(f"Error: {str(e)}\n")
                    error_file.write("=" * 40 + "\n")

    def parse_photo(self, response, category):
        loader = ItemLoader(item=PicjumboItem(), response=response)
        loader.add_xpath('name', "//h1/a/text()")
        loader.add_xpath('links', "//div[@class='single']//img/@src | //div[@class='single']//img/@srcset")
        loader.add_value('url', response.url)
        loader.add_value('category', category)
        yield loader.load_item()
