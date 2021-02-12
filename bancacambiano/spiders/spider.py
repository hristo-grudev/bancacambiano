import scrapy

from scrapy.loader import ItemLoader
from ..items import BancacambianoItem
from itemloaders.processors import TakeFirst


class BancacambianoSpider(scrapy.Spider):
	name = 'bancacambiano'
	start_urls = ['https://www.bancacambiano.it/comunicazione/area-stampa/comunicati-stampa/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="contenuto compatto fullwidth pannello sfondo calendari"]')
		for post in post_links:
			link = post.xpath('.//div[@class="presente"]/p/a/@href').get()
			date = post.xpath('.//span[@class="calendario"]//text()').getall()
			date = [p.strip() for p in date]
			date = ' '.join(date).strip()

			yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="contenuto fullwidth"]//p//text()[normalize-space() and not(ancestor::h2 | ancestor::script | ancestor::style)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BancacambianoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
