"""
Crawlers:
    AllNews: https://venturebeat.com/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://venturebeat.com/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'VentureBeat'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find('div', id='primary').find_all('article')

        for news in news_container:

            # Find date
            date = news.find('time')

            # Find news type
            try:
                newsType = news.find('span', class_='article-type').get_text()
            except AttributeError:
                newsType = 'no type'

            # Check for AD
            if not date or newsType == 'Sponsored':
                continue

            # Get info
            info = {
                'title': news.find('h2').get_text(),
                'url': news.find('a').get('href'),
                'date': self.HTML_time_to_local(date['datetime']),
            }

            # Save result
            self.payload.append(News(**info))