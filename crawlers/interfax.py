"""
Crawlers:
    Digital: https://www.interfax.ru/digital/
"""

from crawlers.abstract import Crawler, News


class Digital(Crawler):
    url: str = 'https://www.interfax.ru/digital/'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Interfax Digital'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url, 'windows-1251')

        # Find news
        news_container = soup.select('.timeline h3')

        for news in news_container:
            
            # Find url
            url = news.parent.get('href')

            # Find date
            date = news.parent.parent.time['datetime']
            
            # Get info
            info = {
                'title': news.get_text(),
                'url': 'https://www.interfax.ru' + url,
                'date': self.HTML_time_to_local(date + ':00+03:00'),
            }

            # Save result
            self.payload.append(News(**info))