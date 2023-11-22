"""
Crawlers:
    Cryptocurrency: https://www.rbc.ru/crypto/tags/?tag=Криптовалюта
    Technology: https://www.rbc.ru/technology_and_media/
"""

from crawlers.abstract import Crawler, News


class RBC(Crawler):
    """Parent class"""
    
    url: str
    table: str = 'news'

    def __str__(self) -> str:
        return 'RBC parent class'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('div', class_='item__wrap')

        for news in news_container:

            try:
                # Get URL
                url = news.find('a', class_='item__link').get('href')
            except AttributeError:
                # It's currencies rates, ignore
                continue

            title = news.find('span', class_='item__title').get_text()

            # Get info
            info = {
                'url': url,
                'title': title,
            }

            # Save result
            self.payload.append(News(**info))

class Cryptocurrency(RBC):
    url: str = 'https://www.rbc.ru/crypto/tags/?tag=Криптовалюта'

    def __str__(self) -> str:
        return 'RBC Cryptocurrency'

class Technology(RBC):
    url: str = 'https://www.rbc.ru/technology_and_media/'

    def __str__(self) -> str:
        return 'RBC Technology'