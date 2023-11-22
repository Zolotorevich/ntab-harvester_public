"""
Crawlers:
    AllNews: https://www.404media.co/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.404media.co/'
    table: str = 'news'

    def __str__(self) -> str:
        return '404 media'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('div', class_='post-card__content')

        for news in news_container:
            
            # Find header
            header = news.find('h4')

            # Find url
            url = header.a.get('href')

            # Find date
            date = news.find('time')['datetime']
            
            # Get info
            info = {
                'title': header.get_text(),
                'url': f'https://www.404media.co{url}',
                'preview': news.find('div', class_='post-card__excerpt').get_text(),
                'date': self.date_notime_to_datetime(date, '%Y-%m-%d'),
            }

            # Save result
            self.payload.append(News(**info))