"""If you're looking for 9to5linux, it's in the nine2five_linux

Crawlers:
    Google: https://9to5google.com
    Mac: https://9to5mac.com
"""

from crawlers.abstract import Crawler, News


class Nine2Five(Crawler):
    """Parent class, do not disturb"""
    
    url: str
    table: str = 'news'

    def __str__(self) -> str:
        return '9to5 parent class'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.findAll('article', class_=['standard', 'aside'])

        # Find news
        for news in news_container:

            # Find news header
            header = news.find('h2')
            
            if not header:
                header = news.find('h3')

            # Find url
            url = header.find('a').get('href')

            # Check if it's AD, which points to other website
            if url[:len(self.url)] != self.url:
                continue

            # Get date from url: https://9to5google.com/2023/08/31/samsung-galaxy/
            date = url[len(self.url) + 1:len(self.url) + 11]
            
            # Get info
            info = {
                'url': url,
                'title': header.get_text(),
                'date': self.date_notime_to_datetime(date, format='%Y/%m/%d'),
                'preview': news.find('p').get_text(),
            }

            # Save result
            self.payload.append(News(**info))

class Google(Nine2Five):
    url: str = 'https://9to5google.com'

    def __str__(self) -> str:
        return '9to5 Google'

class Mac(Nine2Five):
    url: str = 'https://9to5mac.com'

    def __str__(self) -> str:
        return '9to5 Mac'