"""
Crawlers:
    Technology: https://www.reuters.com/technology/
    MediaTelecom: https://www.reuters.com/business/media-telecom/
"""

import re

from crawlers.abstract import Crawler, News


class Reuters(Crawler):
    """Parent class"""
    
    url: str
    table: str = 'news'

    def __str__(self) -> str:
        return 'Reuters parent class'

    def collect(self) -> None:

        def find_time(news):
            try:
                return news.time['datetime']
            except TypeError:
                return news.date['datetime']
            
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Parse hero
        hero_container = soup.find_all('li', class_=re.compile('^story-collection__hero'))
        
        for news in hero_container:

            # Get news url container
            news_link = news.find('a', attrs={"data-testid": "Link"})

            # Get info
            info = {
                'url': 'https://www.reuters.com' + news_link.get('href'),
                'title': news_link.get_text(),
                'preview': news.find('p', attrs={"data-testid": "Body"}).get_text(),
            }

            # Save result
            self.payload.append(News(**info))

        # Hero news, for exclude from other
        hero = set(soup.find_all('div', class_=re.compile('^media-story-card__hero')))

        # Parse news with images
        img_news = set(soup.find_all('div', attrs={'data-testid': 'MediaStoryCard'}))
        news_container = img_news - hero

        for news in news_container:

            # Get news url container
            news_link = news.find('a', class_=re.compile('^media-story-card__heading'))

            # Get info
            info = {
                'url': 'https://www.reuters.com' + news_link.get('href'),
                'title': news_link.get_text(),
                'date': self.HTML_time_to_local(find_time(news))
            }

            # Save result
            self.payload.append(News(**info))

        # Parse news without images
        noimg_news = set(soup.find_all('div', attrs={'data-testid': 'TextStoryCard'}))
        news_container = noimg_news - hero

        for news in news_container:
            
            # Get news url container
            news_link = news.find('a', attrs={'data-testid': 'Heading'})

            # Get info
            info = {
                'url': 'https://www.reuters.com' + news_link.get('href'),
                'title': news_link.get_text(),
                'preview': news.find('p', attrs={'data-testid': 'Body'}).get_text(),
                'date': self.HTML_time_to_local(find_time(news))
            }

            # Save result
            self.payload.append(News(**info))
            

class Technology(Reuters):
    url: str = 'https://www.reuters.com/technology/'

    def __str__(self) -> str:
        return 'Reuters Technology'

class MediaTelecom(Reuters):
    url: str = 'https://www.reuters.com/business/media-telecom/'

    def __str__(self) -> str:
        return 'Reuters Media and Telecom'