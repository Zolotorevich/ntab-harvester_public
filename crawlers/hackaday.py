"""
Crawlers:
    AllNews: https://hackaday.com/blog/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://hackaday.com/blog/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Hackaday'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('article')

        for news in news_container:

            # Find header
            header = news.find('h1')

            # Find date
            date = news.find('span', class_='entry-date').get_text()
            
            # Get info
            info = {
                'title': header.get_text(),
                'url': header.find('a').get('href'),
                'preview': news.find('p').get_text(),
                'date': self.date_notime_to_datetime(date, '%B %d, %Y'),
            }

            # Save result
            self.payload.append(News(**info))