import scrapy


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://movie.douban.com"
        ]

    def parse(self, response):
        filename = "test.txt"
        with open(filename, 'wb') as f:
            f.write(response.body)
