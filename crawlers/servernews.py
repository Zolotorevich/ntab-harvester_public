"""
Crawlers:
    AllNews: https://www.servernews.ru/news
"""

from datetime import datetime

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.servernews.ru/news'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Servernews'

    def collect(self) -> None:

        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.select('table.maintable-internal div.content')

        for news in news_container:

            # Find header
            header = news.find('h1')

            # Find url
            url = header.parent.get('href')

            # Find and convert date '19.08.2023 [16:19], Автор'
            date = news.find('span', class_='date').get_text()
            date = date[:date.find(']')]
            date = datetime.strptime(date + ':00', '%d.%m.%Y [%H:%M:%S')

            # Get info
            info = {
                'title': header.get_text(),
                'url': 'https://servernews.ru' + url,
                'preview': news.find('p').get_text(),
                'date': date,
            }

            # Save result
            self.payload.append(News(**info))