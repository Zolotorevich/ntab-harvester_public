"""
Crawlers:
    AllNews: https://www.opennet.ru/opennews/index.shtml
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.opennet.ru/opennews/index.shtml'
    table: str = 'news'

    def __str__(self) -> str:
        return 'OpenNET'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url, 'KOI8-R')

        # Find news
        news_container = soup.find_all('a', class_='title2')

        for news in news_container:

            # Find date
            date = news.parent.parent.find('td', class_='tdate').get_text()

            # Find preview
            preview = news.parent.parent.next_sibling.next_sibling.find('td',
                                                                        class_='chtext2')
            
            # Get info
            info = {
                'title': news.get_text(),
                'url': f'https://www.opennet.ru{news.get("href")}',
                'preview': preview.find(text=True),
                'date': self.date_notime_to_datetime(date, '%d.%m.%Y'),
            }

            # Save result
            self.payload.append(News(**info))