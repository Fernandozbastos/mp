import scrapy


class SampleSpider(scrapy.Spider):
    name = "sample"

    def start_requests(self):
        """Generate initial requests."""
        yield scrapy.Request("https://example.com", callback=self.parse)

    def parse(self, response):
        """Parse the response and return the page title."""
        yield {"title": response.css("title::text").get()}
