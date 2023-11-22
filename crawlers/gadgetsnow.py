"""
Crawlers:
    Technology: https://www.gadgetsnow.com/tech-news
"""

from crawlers.abstract import Crawler, News


class AllNews(Crawler):
    url: str = 'https://www.gadgetsnow.com/tech-news'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Gadgets Now'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('div', class_='col_l_12')

        for news in news_container:

            # Check for empty container
            try:
                title = news.find('figcaption').get_text()
            except AttributeError:
                continue

            # Find url
            url = news.find('a').get('href')

            # Check url for updated news, with '?frmapp=yes' on the end
            if url[-11:] == '?frmapp=yes':
                url = url[:-11]
            
            # Get info
            info = {
                'title': title,
                'url': url,
            }

            # Save result
            self.payload.append(News(**info))