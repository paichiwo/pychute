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
            options.add_argument("--headless=new")
            options.add_argument(f'user-agent={USER_AGENT}')
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(url)
            page = self.driver.page_source
            if page:
                self.__soup = BeautifulSoup(page, 'html.parser')
            else:
                raise Exception('URL could not be fetched')

        else:
            raise Exception('Need url to proceed')

    def __get_iframe_soup(self):
        iframe = self.__soup.find('iframe', {'id': 'video-player-iframe'})
        if iframe and iframe.get('src'):
            iframe_url = iframe['src']
            self.driver.get(iframe_url)
            iframe_page = self.driver.page_source
            return BeautifulSoup(iframe_page, 'html.parser')
        else:
            raise Exception('Iframe with video not found')

    def __extract_media_url(self):
        iframe_soup = self.__get_iframe_soup()
        scripts = iframe_soup.find_all('script')

        for script in scripts:
            if script.string and 'media_url' in script.string:
                match = re.search(r"media_url\s*=\s*'([^']+)'", script.string)
                if match:
                    return match.group(1)
        raise Exception('Media URL not found in iframe')

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
        media_url = self.__extract_media_url()
        request = urllib.request.Request(media_url, method='HEAD')
        response = urllib.request.urlopen(request)
        return int(response.headers.get('Content-Length', 0))

    def thumbnail(self) -> str:
        thumb_meta = self.__soup.find('meta', {'property': 'og:image'})
        if not thumb_meta or not thumb_meta.get('content'):
            raise Exception('Thumbnail not found')
        return thumb_meta['content']

    def description(self) -> str:
        result = self.__soup.find('div', {'class': 'teaser'})
        if result:
            description_text = result.get_text(separator="\n").strip()
            return description_text
        else:
            raise Exception('Description could not be fetched')

    def download(self, on_progress_callback=None, filename=None):
        media_url = self.__extract_media_url()
        output_filename = f'{filename if filename else self.title()}.mp4'

        if os.path.exists(output_filename):
            print('File already downloaded')
            return

        print('Downloading...')
        urllib.request.urlretrieve(media_url, output_filename, reporthook=on_progress_callback)
        print('Download complete')

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
