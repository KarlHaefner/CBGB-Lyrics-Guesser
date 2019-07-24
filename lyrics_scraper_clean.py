# -*- coding: utf-8 -*-
"""To run:
scrapy runspider -o output_lyrics.csv -L WARNING lyrics_scraper_clean.py
"""

import scrapy
from scrapy.http import Request
import re

class LyricsSpider(scrapy.Spider):
    name = 'lyrics'
    allowed_domains = ['lyrics.com']
    start_urls = ['https://www.lyrics.com/artist/Ramones/5223',
                  'https://www.lyrics.com/artist/Iggy+Pop/5167',
                  'https://www.lyrics.com/artist/Blondie/3703',
                  'https://www.lyrics.com/artist/Talking+Heads/5594',
                  'https://www.lyrics.com/artist/Patti+Smith/126485'
                  ]

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5.0,
        'AUTOTHROTTLE_MAX_DELAY': 60.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
    }

    def parse(self, response):

        url = response.xpath('//td[@class="tal qx"]/strong/a/@href').getall()

        for url_next in url:
            url = response.urljoin(url_next)
            yield Request(url)

        lyric = response.xpath('//pre[@id="lyric-body-text"]').getall()
        artist = response.xpath('//h3[@class="lyric-artist"]/a//text()').get()

        div_pattern = '<[^>]+>'
        new_line_pattern = '\\n'
        white_space_pattern = '\s+'

        try:
            lyric = re.sub(div_pattern, ' ', lyric[0])
            lyric = re.sub(new_line_pattern, ' ', lyric)
            lyric = re.sub(white_space_pattern, ' ', lyric).strip()
            lyric = [lyric]
            artist = [artist]

            if len(lyric) == len(artist):
                for l, a in zip(lyric, artist):
                    d = {'text': l, 'label': a}
                    print(d)
                    yield(d)

        except IndexError:
            pass

if __name__ == "__main__":

    spider = LyricsSpider()
    spider.parse()
