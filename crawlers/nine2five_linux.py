"""
Crawlers:
    AllNews: https://9to5linux.com/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://9to5linux.com/'
    table: str = 'news'

    def __str__(self) -> str:
        return '9to5 Linux'

    def collect(self) -> None:

        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.findAll('article')

        for news in news_container:

            # Find header
            header = news.find('h2')

            # Get info
            info = {
                'title': header.get_text(),
                'url': header.find('a').get('href'),
                'preview': news.find('p').get_text(),
            }

            # Find date
            try:
                date = news.find('time', class_='entry-date published')
                info['date'] = self.HTML_time_to_local(date['datetime'])
            except TypeError:
                pass

            # Save result
            self.payload.append(News(**info))