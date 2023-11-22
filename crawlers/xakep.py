"""
Crawlers:
    AllNews: https://xakep.ru/category/news/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://xakep.ru/category/news/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Xakep'

    def collect(self) -> None:

        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('div', class_="block-article-content-wrapper")

        for news in news_container:

            # Find header
            header = news.find('h3')

            # Get info
            info = {
                'title': header.get_text(),
                'url': header.find('a').get('href'),
                'preview': news.find('p').get_text(),
            }

            # Save result
            self.payload.append(News(**info))