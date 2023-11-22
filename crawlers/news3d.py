"""
Crawlers:
    AllNews: https://3dnews.ru/news
"""

from datetime import datetime

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://3dnews.ru/news'
    table: str = 'news'

    def __str__(self) -> str:
        return '3D News'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find('div', id="section-content")

        all = set(news_container.find_all('div', class_='article-entry'))
        hidden = set(news_container.find_all('div', class_='newsAllFeedHideItem'))
        news_container = all - hidden

        for news in news_container:

            # Find url
            url = news.find('a', class_='entry-header').get('href')

            # Check if it's releative
            if url[:1] == '/':
                url = 'https://3dnews.ru' + url

            # Find and convert date '20.08.2023 08:12'
            date = news.find('span', class_='entry-date').get_text()
            date = datetime.strptime(date.strip() + ':00', '%d.%m.%Y %H:%M:%S')
            
            # Get info
            info = {
                'title': news.find('h1').get_text(),
                'url': url,
                'date': date,
            }

            # Check if news have preview
            if news.find('p'):
                info['preview'] = news.find('p').get_text()

            # Save result
            self.payload.append(News(**info))