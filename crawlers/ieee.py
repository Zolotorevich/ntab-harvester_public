"""
Crawlers:
    Spectrum: https://spectrum.ieee.org/
"""

import json

from crawlers.abstract import Crawler, News


class Spectrum(Crawler):
    url: str = 'https://spectrum.ieee.org/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'IEEE Spectrum'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.findAll('article')

        for news in news_container:

            # Get JSON and find date
            script = news.find('script').string
            json_data = json.loads(script)
            date = json_data['customDimensions']['8']

            # Find title
            title_container = news.find('h2')

            # Get info
            info = {
                'title': title_container.get_text(),
                'url': title_container.a.get('href'),
                'date': self.date_notime_to_datetime(date, format='%m/%d/%Y'),
            }

            # Find preview
            try:
                info['preview'] = news.find('h3').get_text()
            except AttributeError:
                pass

            # Save result
            self.payload.append(News(**info))