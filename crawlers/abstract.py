"""Parent classes for all Crawlers"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import feedparser
import requests
from bs4 import BeautifulSoup


@dataclass
class News():
    """Crawler payload objects"""
    
    title: str
    url: str
    preview: Optional[str] = ''
    date: Optional[datetime] = datetime.now()

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Strip title and preview text"""
        
        if __name == 'title' or __name == 'preview':
            __value = __value.strip()

        self.__dict__[__name] = __value

    def __str__(self) -> str:
        return f'{self.title} | {self.url} | {self.preview} | {self.date}'


class Crawler(ABC):
    """Abstract crawler

    Attributes:
        url: website page address
        table: database table name postfix e.g. 'news' for 'harvester_news'
        payload: collected data in News() objects

    Methods:
        __str__: crawler name
        collect: get data from website or other source
        request_and_parse_HTML: get HTML by requests + BeautifulSoup
        request_RSS: get RSS feed
        HTML_time_to_local: convert '2023-08-18T15:42:21Z' to local time
        epoch_seconds_to_time: convert Unix time to datetime, optional to local
        date_notime_to_datetime: convert 'month/day/year' to datetime with current time
    """

    url: str
    table: str
    payload: list[News] = []

    @abstractmethod
    def __str__(self) -> str:
        """Return crawler name"""

    @abstractmethod
    def collect(self) -> None:
        """Collect data and store in payload"""

    @staticmethod
    def request_and_parse_HTML(url: str,
                     encoding: str='utf-8',
                     timeout_in_sec: int=20,
                     headers: Optional[dict[str, str]]=None) -> BeautifulSoup:
        """Get website from requests and parse HTML using BeautifulSoup

        Args:
            url: website page address
            encoding: page encoding, def: utf-8
            timeout_in_sec: total timeout for reqest, def: 20
            headers: request headers {User-Agent, Content-Type}

        Returns:
            BeautifulSoup object

        Raises:
            ConnectionError: if website returns any code other than 200
        """

        # Set default headers if None provided
        headers = headers or {
                                'User-Agent': 'Mozilla/5.0',
                                'Content-Type': 'text/html;',
                            }

        # Send request
        response = requests.get(url, headers=headers, timeout=timeout_in_sec)

        # Check return code
        if response.status_code != 200:
            raise ConnectionError(f'Fail to load {url}')

        # Apply encoding
        response.encoding = encoding

        return BeautifulSoup(response.text, 'html.parser')

    @staticmethod
    def request_RSS(url: str) -> feedparser.util.FeedParserDict:
        """Get RSS and return dict or None if RSS not found

        Args:
            url: RSS feed URL

        Returns:
            feedparser {dict}

        Raises:
            AttributeError: RSS unavailable
        """
        feed = feedparser.parse(url)
        getattr(feed, 'status')
        return feed

    @staticmethod
    def HTML_time_to_local(date: str, convert_from_utc:bool = True) -> datetime:
        """Convert time, usually found in HTML, to local timezone

        Args:
            date: string like '2023-08-18T15:42:21Z' or '2023-08-21T11:00:16.449Z'

        Returns:
            Datetime object with local timezone

        Raises:
            ValueError: string doesn't match pattern
        """

        try:
            # Convert '2023-08-18T15:42:21Z'
            local_date = datetime.strptime(date, '%Y-%m-%dT%X%z')

        except ValueError:
            # Try with microseconds, like '2023-08-21T11:00:16.449Z'
            local_date = datetime.strptime(date, '%Y-%m-%dT%X.%f%z')

        # Change timezone to local
        if convert_from_utc:
            return local_date.astimezone(tz=None)

        return local_date

    @staticmethod
    def epoch_seconds_to_time(date: str, convert_from_utc: bool = True) -> datetime:
        """Convert Unix time to datetime

        Args:
            date: string like '1326244364' in seconds
            convert_from_utc: convert from UTC lo local timezone

        Returns:
            Datetime object with local timezone
        """
        
        new_date = datetime.fromtimestamp(int(date))

        if convert_from_utc:
            return new_date.replace(tzinfo=timezone.utc).astimezone(tz=None)

        return new_date

    @staticmethod
    def date_notime_to_datetime(date: str, format: str = '%d/%m/%Y') -> datetime:
        """Convert date without time to datetime with current time

        Args:
            date: string 'month/day/year' like '08/23/2023'
            format: datetime format like %d/%m/%Y

        Returns:
            Datetime with current time
        """

        now = datetime.now()
        new_date = f'{date} {str(now.time())} +03:00'

        return datetime.strptime(new_date, f'{format} %X.%f %z')