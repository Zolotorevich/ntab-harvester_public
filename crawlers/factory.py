"""Crawlers factory"""

import importlib

from crawlers import (apress, arstechnica, coindesk, engadget, futurism,
                      gadgetsnow, guardian, hackaday, ieee, interfax,
                      itchannel, media404, news3d, nine2five, nine2five_linux,
                      opennet, rbc, register, reuters, servernews, techcrunch,
                      techradar, tomshardware, venturebeat, verge, xakep)
from crawlers.abstract import Crawler


class CrawlersFactory():
    """Factory for Crawler objects

    Methods:
        register: generate crawlers by name or category
    """

    def register(self, crawler: str) -> list[Crawler]:
        """Generate crawlers

        Args:
            crawler: crawler or category name

        Returns:
            List with Crawler objects

        Raises:
            AttributeError: category or crawler not found
        """

        if crawler == 'news':
            return [
                    apress.Technology(),
                    arstechnica.AllNews(),
                    coindesk.AllNews(),
                    engadget.AllNews(),
                    futurism.Latest(),
                    futurism.Byte(),
                    gadgetsnow.AllNews(),
                    guardian.Technology(),
                    hackaday.AllNews(),
                    ieee.Spectrum(),
                    interfax.Digital(),
                    itchannel.AllNews(),
                    media404.AllNews(),
                    news3d.AllNews(),
                    nine2five_linux.AllNews(),
                    nine2five.Google(),
                    nine2five.Mac(),
                    opennet.AllNews(),
                    rbc.Cryptocurrency(),
                    rbc.Technology(),
                    register.OnPrem(),
                    register.Software(),
                    register.Security(),
                    register.Offbeat(),
                    register.OffPrem(),
                    reuters.Technology(),
                    reuters.MediaTelecom(),
                    servernews.AllNews(),
                    techcrunch.AllNews(),
                    techradar.AllNews(),
                    tomshardware.AllNews(),
                    venturebeat.AllNews(),
                    verge.Entertainment(),
                    verge.Tech(),
                    verge.Science(),
                    xakep.AllNews(),
                    ]

        else:
            # Find crawler by name
            try:
                moduleName = crawler[:crawler.find('.')]
                className = crawler[crawler.find('.') + 1:]

                module = importlib.import_module('crawlers.' + moduleName)
                requested_crawler = getattr(module, className)

                return [requested_crawler()]
            
            except AttributeError:
                print(f'FAIL: Category or crawler {crawler} not found')
                exit(1)