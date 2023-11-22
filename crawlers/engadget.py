"""
Crawlers:
    AllNews: https://www.engadget.com
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.engadget.com'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Engadget'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.findAll('article')

        for news in news_container:

            title_container = news.find('h2')
            
            # Get info
            info = {
                'title': title_container.a.get_text(),
                'url': f'https://www.engadget.com{title_container.a.get("href")}',
                'preview': title_container.find_next_sibling('div').get_text(),
            }

            # Save result
            self.payload.append(News(**info))