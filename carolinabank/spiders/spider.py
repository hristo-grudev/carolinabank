import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import CarolinabankItem
from itemloaders.processors import TakeFirst


class CarolinabankSpider(scrapy.Spider):
	name = 'carolinabank'
	start_urls = ['https://www.carolinabank.net/about/blog']

	def parse(self, response):
		post_links = response.xpath('//a[@data-link-type-id="page"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space() and not(ancestor::a | ancestor::strong)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//*[(@id = "main")]//strong/text()').getall()
		date = [p.strip() for p in date if '{' not in p]
		date = ' '.join(date).strip()
		date = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', date) or ['']

		item = ItemLoader(item=CarolinabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date[0])

		return item.load_item()
