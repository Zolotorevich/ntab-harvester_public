"""
Crawlers:
    Latest: https://futurism.com/latest
    Byte: https://futurism.com/the-byte
"""

import json

from crawlers.abstract import Crawler, News


class Futurism(Crawler):
    """Parent class"""
    
    url: str
    table: str = 'news'

    def __str__(self) -> str:
        return 'Futurism parent class'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Parse JSON
        script = soup.find('script', id='__NEXT_DATA__').string
        data = json.loads(script)

        # Find news list in JSON
        json_container = data['props']['pageProps']['initialApolloState']['ROOT_QUERY']
        for key in json_container:
            if key[:6] == 'posts(':
                news_container = json_container[key]['nodes']

        # Find news
        for news in news_container:
            
            # Get info
            info = {
                'url': f'https://futurism.com/the-byte/{news["slug"]}',
                'title': news['title({"format":"RENDERED"})'],
                'date': self.HTML_time_to_local(f'{news["date"]}Z'),
                'preview': news['subtitle'],
            }

            # Save result
            self.payload.append(News(**info))

class Latest(Futurism):
    url: str = 'https://futurism.com/latest'

    def __str__(self) -> str:
        return 'Futurism Latest'

class Byte(Futurism):
    url: str = 'https://futurism.com/the-byte'

    def __str__(self) -> str:
        return 'Futurism Byte'