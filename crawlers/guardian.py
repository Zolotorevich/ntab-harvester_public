"""
Crawlers:
    Technology: https://www.theguardian.com/technology/all
"""

from crawlers.abstract import Crawler, News


class Technology(Crawler):
    url: str = 'https://www.theguardian.com/technology/all'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Guardian'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('h3')

        for news in news_container:

            # Find date
            date = news.parent.parent.time['datetime']
            
            # Get info
            info = {
                'title': news.find('span').get_text(),
                'url': news.find('a').get('href'),
                'date': self.HTML_time_to_local(date),
            }

            # Save result
            self.payload.append(News(**info))