"""
Crawlers:
    AllNews: https://techcrunch.com/
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://techcrunch.com/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Techcrunch'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.findAll('div', class_='post-block')

        for news in news_container:
            
            title_container = news.find('h2')
            date_container = title_container.find_next_sibling('div')
            
            # Get info
            info = {
                'title': title_container.get_text(),
                'url': title_container.a.get('href'),
                'preview': news.find('div', class_='post-block__content').get_text(),
                'date': self.HTML_time_to_local(date_container.time['datetime']),
            }

            # Save result
            self.payload.append(News(**info))