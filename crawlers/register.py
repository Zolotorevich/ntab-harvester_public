"""
Crawlers:
    OnPrem: https://www.theregister.com/on_prem/
    Software: https://www.theregister.com/software/
    Security: https://www.theregister.com/security/
    Offbeat: https://www.theregister.com/offbeat/
    OffPrem: https://www.theregister.com/off_prem/
"""

from crawlers.abstract import Crawler, News


class Register(Crawler):
    """Parent class"""
    
    url: str
    table: str = 'news'

    def __str__(self) -> str:
        return 'Register parent class'

    def collect(self) -> None:
        # Get HTML
        soup = self.request_and_parse_HTML(self.url)

        # Find news
        news_container = soup.find_all('article')

        for news in news_container:

            # Check if it's AD
            try:
                category_name = news.find('span', class_='section_name').get_text()
                ad_category = category_name.get_text() == 'Advertorial'
            except AttributeError:
                ad_category = False
            
            ad_wrapper = 'horiz_scroll' in news.parent.attrs['class']
            
            if ad_category or ad_wrapper:
                continue

            # Get URL
            url = news.find('a').get('href')

            # Get info
            info = {
                'url': 'https://www.theregister.com' + url,
                'title': news.find('h4').get_text(),
                'preview': news.find('div', class_='standfirst').get_text(),
            }

            # Find date
            try:
                date = news.find('span', class_='time_stamp').attrs['data-epoch']
                info['date'] = self.epoch_seconds_to_time(date, False)
            except AttributeError:
                pass

            # Save result
            self.payload.append(News(**info))

class OnPrem(Register):
    url: str = 'https://www.theregister.com/on_prem/'

    def __str__(self) -> str:
        return 'Register On-prem'

class Software(Register):
    url: str = 'https://www.theregister.com/software/'

    def __str__(self) -> str:
        return 'Register Software'

class Security(Register):
    url: str = 'https://www.theregister.com/security/'

    def __str__(self) -> str:
        return 'Register Security'

class Offbeat(Register):
    url: str = 'https://www.theregister.com/offbeat/'

    def __str__(self) -> str:
        return 'Register offbeat'

class OffPrem(Register):
    url: str = 'https://www.theregister.com/off_prem/'

    def __str__(self) -> str:
        return 'Register off-prem'