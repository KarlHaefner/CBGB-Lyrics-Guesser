import scrapy
from scrapy.http import Request


class LyricSpider(scrapy.Spider):
    name = 'lyrics'
    allowed_domains = ['lyrics.com']
    start_urls = ['https://www.lyrics.com/artist/Joy+Division/71273']

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'DEPTH_LIMIT': 10
    }

    def parse(self, response):

        urls = response.xpath('//td[@class="tal qx"]//a/@href').getall()

        for u in urls:
            full_url = response.urljoin(u)
            full_url = Request(full_url)
            yield full_url

        lyrics = response.xpath('//pre[@id="lyric-body-text"]//text()').getall()
        lyrics = ' '.join(lyrics)

        artist = response.xpath('//h3[@class="lyric-artist"]/a/text()').get()

        print(lyrics)
        print(artist)
        print('\n\n\n')
