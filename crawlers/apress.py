"""
Crawlers:
    Technology: https://apnews.com/technology
"""

from crawlers.abstract import Crawler, News


class Technology(Crawler):
    url: str = 'https://apnews.com/technology'
    table: str = 'news'

    def __str__(self) -> str:
        return 'Associated Press'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('div', class_='PagePromo-content')

        for news in news_container:

            # Fund url
            url = news.find('a')

            # Get info
            info = {
                'title': url.get_text(),
                'url': url.get('href'),
            }

            # Get time if any
            try:
                # Find Epoch time in microseconds and keep only seconds
                date = news.find('bsp-timestamp')['data-timestamp'][:-3]
                info['date'] = self.epoch_seconds_to_time(date, False)
            except TypeError:
                pass

            # Get preview if any
            try:
                info['preview'] = news.find('div', class_='PagePromo-description').get_text()
            except AttributeError:
                pass

            # Save result
            self.payload.append(News(**info))