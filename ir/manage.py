#!/usr/bin/env python
import os
import sys
import schedule
import time
from threading import Thread


def auto_crawl():
    schedule.every(100).minutes.do(crawl)
    while True:
        schedule.run_pending()
        time.sleep(1)


def crawl():
    os.system('scrapy runspider auto_crawler.py')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ir.settings")

    thread = Thread(target=auto_crawl)
    thread.start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)