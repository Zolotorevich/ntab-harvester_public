"""
Crawlers:
    AllNews: https://www.novostiitkanala.ru/news/
"""

from datetime import datetime

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.novostiitkanala.ru/news/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'IT Channel News'

    def collect(self) -> None:

        # Get RSS
        try:
            feed = self.request_RSS('https://www.novostiitkanala.ru/rss/')
        except AttributeError:
            print(f'[!] {self}: RSS error')
            return None

        for news in feed.entries:

            # Check URL and process only 'novostiitkanala.ru/news/'
            if news.link[31:35] != 'news':
                continue

            # Get info
            info = {
                'title': news.title,
                'url': news.link,
                'preview': news.summary.replace('&nbsp;', ' '),
                'date': datetime.strptime(news.published, '%a, %d %b %Y %X %z'),
            }

            # Save result
            self.payload.append(News(**info))