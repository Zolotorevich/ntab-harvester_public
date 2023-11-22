"""
Crawlers:
    Tech: https://www.theverge.com/tech
    Entertainment: https://www.theverge.com/entertainment
    Science: https://www.theverge.com/science
"""

import re

from crawlers.abstract import Crawler, News


class Verge(Crawler):
    """Parent class"""
    
    url: str
    table: str = 'news'

    def __str__(self) -> str:
        return 'Verge parent class'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('div', class_='duet--content-cards--content-card')

        for news in news_container:

            #  Get info based on post type
            if news.find('h2'):
                url = news.find('a', class_='block').get('href')

                info = {
                    'title': news.find('h2').get_text(),
                }

            else:
                url = news.find('a').get('href')
                
                info = {
                    'title': news.find('div', class_='inline').get_text(),
                    'preview': news.find('p', class_=re.compile('^duet--article')).get_text(),
                }

            # Check if it's AD
            if info['title'] == 'Advertiser Content':
                continue

            # Add website address to URL
            info['url'] = 'https://theverge.com' + url

            # Save result
            self.payload.append(News(**info))

class Tech(Verge):
    url: str = 'https://www.theverge.com/tech'

    def __str__(self) -> str:
        return 'Verge Tech'

class Entertainment(Verge):
    url: str = 'https://www.theverge.com/entertainment'

    def __str__(self) -> str:
        return 'Verge Entertainment'

class Science(Verge):
    url: str = 'https://www.theverge.com/science'

    def __str__(self) -> str:
        return 'Verge Science'