"""
Crawlers:
    AllNews: https://www.tomshardware.com/news
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.tomshardware.com/news'
    table: str = 'news'

    def __str__(self) -> str:
        return "Tom's hardware"

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('article')

        for news in news_container:

            # Preview
            preview = news.find('p', class_='synopsis').get_text()
            
            # Get info
            info = {
                'title': news.find('h3').get_text(),
                'url': news.parent.get('href'),
                'preview': preview.replace('\n', ''),
                'date': self.HTML_time_to_local(news.time['datetime']),
            }

            # Save result
            self.payload.append(News(**info))