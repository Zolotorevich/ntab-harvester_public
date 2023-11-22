"""
Crawlers:
    AllNews: https://www.coindesk.com/livewire/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.coindesk.com/livewire/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'CoinDesk'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('article')

        for news in news_container:
            
            # Find header
            header = news.find('h3')

            # Find url
            url = header.a.get('href')

            # Find date
            date = news.find('time').get_text()
            
            # Get info
            info = {
                'title': header.get_text(),
                'url': f'https://www.coindesk.com/{url}',
                'preview': news.find('p').get_text(),
                'date': self.date_notime_to_datetime(date, '%B %d, %Y'),
            }

            # Save result
            self.payload.append(News(**info))