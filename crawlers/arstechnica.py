"""
Crawlers:
    AllNews: https://arstechnica.com/?view=archive
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://arstechnica.com/?view=archive'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Ars Technica'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.findAll('h2', id=None)

        for news in news_container:

            # Find date
            date = news.parent.find('p', class_='byline')
            
            # Get info
            info = {
                'title': news.a.get_text(),
                'url': news.a.get('href'),
                'preview': news.parent.find('p', class_='excerpt').get_text(),
                'date': self.HTML_time_to_local(date.time['datetime']),
            }

            # Save result
            self.payload.append(News(**info))