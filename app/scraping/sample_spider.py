import logging

import scrapy

from .pipelines import save_item


logging.basicConfig(level=logging.INFO)


class SampleSpider(scrapy.Spider):
    name = "sample"

    def start_requests(self):
        """Generate initial requests."""
        self.logger.info("Starting requests")
        yield scrapy.Request("https://example.com", callback=self.parse)

    async def parse(self, response):
        """Parse the response and persist the page title."""
        data = {"title": response.css("title::text").get()}
        await save_item(data)
        self.logger.info("Saved item: %s", data)
        yield data
