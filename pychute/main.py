import os
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from pychute.config import USER_AGENT
from pychute.helpers import format_duration_string, format_date_string


class PyChute:
    def __init__(self, url):
        """Lightweight Bitchute wrapper """

        # Initial setup for the wrapper
        if url:
            if not 'old' in url:
                url = url.replace('https://www.bitchute.com/', 'https://old.bitchute.com/')

            options = webdriver.ChromeOptions()
            options.add_argument("--headless=old")
            options.add_argument(f'user-agent={USER_AGENT}')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            page = driver.page_source
            if page:
                self.__soup = BeautifulSoup(page, 'html.parser')
            else:
                raise Exception('URL could not be fetched')

        else:
            raise Exception('Need url to proceed')

    def title(self) -> str:
        result = self.__soup.find('h1', {'id': 'video-title'}).text
        if result:
            return result
        else:
            raise Exception('Video title could not be fetched')

    def publish_date(self) -> str:
        result = self.__soup.find('div', class_='video-publish-date').text
        if result:
            return format_date_string(result)
        else:
            raise Exception('Publish date could not be fetched')

    def channel(self) -> str:
        result = [div.find('a').text for div in self.__soup.findAll('div', attrs={'class': 'details'})]
        if result:
            return result[0]
        else:
            raise Exception('Channel name could not be fetched')

    def views(self) -> str:
        result = self.__soup.find('span', {'id': 'video-view-count'}).text
        if result:
            return result
        else:
            raise Exception('Views could not be fetched')

    def likes(self) -> str:
        result = self.__soup.find('span', {'id': 'video-like-count'}).text
        if result:
            return result
        else:
            raise Exception('Likes could not be fetched')

    def subscriptions(self) -> str:
        result = self.__soup.find('span', {'id': 'subscriber_count'}).text
        if result:
            return result
        else:
            raise Exception('Subscriptions could not be fetched')

    def duration(self) -> str:
        result = self.__soup.find('meta', {'name': 'duration'}).get('content')
        if result:
            return format_duration_string(result)
        else:
            raise Exception('Video duration could not be fetched')

    def filesize(self) -> int:
        result = self.__soup.find('div', {'id': 'player'})

        if len(result) != 0:
            target = result.find('source').get('src')
            request = urllib.request.Request(target, method='HEAD')
            response = urllib.request.urlopen(request)
            return int(response.headers.get('Content-Length', 0))
        else:
            raise Exception('Source for the video does not exist')

    def thumbnail(self) -> str:
        result = self.__soup.find('div', {'id': 'player'})
        if len(result) != 0:
            return result.find('img').get('src')
        else:
            raise Exception('Thumbnail could not be fetched')

    def description(self) -> str:
        result = self.__soup.find('div', {'class': 'teaser'})
        if result:
            description_text = result.get_text(separator="\n").strip()
            return description_text
        else:
            raise Exception('Description could not be fetched')

    def download(self, on_progress_callback=None, filename=None):
        result = self.__soup.find('div', {'id': 'player'})

        if len(result) != 0:
            target = result.find('source').get('src')
            output_filename = f'{filename if filename else self.title()}.mp4'  # add extension

            if not os.path.exists(output_filename):
                print('Downloading...')
                urllib.request.urlretrieve(target, output_filename, reporthook=on_progress_callback)
            else:
                print('File already downloaded')

        else:
            raise Exception('Source for the video does not exist')
