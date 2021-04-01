import scrapy

from scrapy.loader import ItemLoader

from ..items import CarolinabankItem
from itemloaders.processors import TakeFirst


class CarolinabankSpider(scrapy.Spider):
	name = 'carolinabank'
	start_urls = ['https://www.carolinabank.net/about/blog']

	def parse(self, response):
		post_links = response.xpath('/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('/text()').get()

		item = ItemLoader(item=CarolinabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
