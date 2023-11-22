"""
Crawlers:
    AllNews: https://www.techradar.com/news
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.techradar.com/news'
    table: str = 'news'

    def __str__(self) -> str:
        return 'TechRadar'

    def collect(self) -> None:
        # List of pages urls
        urls = [
            'https://www.techradar.com/news',
            'https://www.techradar.com/news/page/2',
            'https://www.techradar.com/news/page/3',
            'https://www.techradar.com/news/page/4',
            'https://www.techradar.com/news/page/5'
        ]

        # Collect news from pages
        news_container = set()
        for url in urls:
            # Get HTML
            soup = self.request_and_parse_HTML(url)

            # Find news and add to set
            news_container.update(soup.find_all('div', class_='listingResult'))

        # Find data
        for news in news_container:

            # Check if it's AD
            if news.find('div', class_='sponsored-post'):
                continue

            try:
                category = news.find('a', class_='category-link').get_text()
                if category == 'Sponsored':
                    continue
            except AttributeError:
                pass

            # Find date
            date = news.time['datetime']
            
            # Get info
            info = {
                'title': news.find('h3').get_text(),
                'url': news.find('a', class_='article-link').get('href'),
                'preview': news.find('p', class_='synopsis').get_text(),
                'date': self.HTML_time_to_local(date)
            }

            # Save result
            self.payload.append(News(**info))