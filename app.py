import argparse
from datetime import datetime

import connection
from crawlers.abstract import Crawler
from crawlers.factory import CrawlersFactory


def main(crawlers_list: list[Crawler], dry_run: bool) -> None:

    total_news: int = 0

    # Launch crawlers and save data
    for crawler in crawlers_list:
        try:
            # Collect data
            crawler.collect()
            
            # Check for dry run
            if dry_run:
                for item in crawler.payload:
                    print(f'\n[DRY RUN] {item}')
                continue

            # Write to database
            data = [item.__dict__ for item in crawler.payload]
            rows = connection.write(crawler.table, data)
            print(f'{crawler} +{rows}')

            total_news += rows
            
        except (ConnectionError, AttributeError, TimeoutError) as error:
            print(f'[!] {crawler}: {error}')

    print(f'\nTotal: +{total_news} @ {datetime.now().strftime("%H:%M")}')

if __name__ == "__main__":

    # Check CLI flags
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--crawler", dest="crawler", required=True,
                        help="Category or crawler name")

    parser.add_argument("-d", "--dry", dest="dry", action='store_true',
                        help="Don't write to database")
    
    args = parser.parse_args()

    # Get objects from crawlers factory
    factory = CrawlersFactory()
    crawlers_list = factory.register(args.crawler)

    main(crawlers_list, args.dry)