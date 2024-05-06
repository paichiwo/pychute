import os.path
import re
import sys
import time
import pathlib
from lxml import html
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from moviepy.editor import *

class PyChute:
    def __init__(self, url):
        """ Bitchute wrapper """

        # Bitchute url given by the user
        self.url = url

        # Initial setup for the wrapper
        self.tree = None

        if self.url:

            # --------- urllib -----------
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0'}
            request = urllib.request.Request(url, headers=headers)
            html_page = urllib.request.urlopen(request).read()
            self.tree = html.document_fromstring(html_page)

            # -------- selenium ----------
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument(
                f'user-agent={'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0'}')
            driver = webdriver.Chrome(options=options)
            driver.get(url)

            page = driver.page_source
            if page:
                self.soup = BeautifulSoup(page, 'html.parser')

        else:
            raise Exception('Need url to proceed')

    def title(self):
        result = self.tree.xpath('//*[@id="video-title"]')
        if len(result) != 0:
            title = result[0].text_content()
            formatted_title = re.sub(r'[^\w ]', '', title).replace(' ', '_')
            return formatted_title
        else:
            raise Exception('Video title could not be fetched')

    def publish_date(self):
        result = self.tree.xpath('//*[@id="video-watch"]/div/div[1]/div[3]/div/div[1]')
        if len(result) != 0:
            date_fetched = result[0].text_content()
            date_stripped = date_fetched[20:-10] + date_fetched[-8:-2]
            date = datetime.strptime(date_stripped, '%H:%M %Z on %B %d, %Y').strftime('%d %m %Y %H:%M:%S')
            return date
        else:
            raise Exception('Publish date could not be fetched')

    def channel(self):
        result = self.tree.xpath('//*[@id="video-watch"]/div/div[1]/div[3]/div/div[2]/div[3]/p[1]/a')
        if len(result) != 0:
            channel = str(result[0].text_content())
            return channel
        else:
            raise Exception('Channel name could not be fetched')

    def views(self):
        result = self.soup.find('span', {'id': 'video-view-count'}).text
        if result:
            return result
        else:
            raise Exception('Views could not be fetched')

    def likes(self):
        result = self.soup.find('span', {'id': 'video-like-count'}).text
        if result:
            return result
        else:
            raise Exception('Likes could not be fetched')

    def subscriptions(self):
        result = self.soup.find('span', {'id': 'subscriber_count'}).text
        if result:
            return result
        else:
            raise Exception('Subscriptions could not be fetched')

    def length(self):
        result = self.soup.find('meta', {'name': 'duration'}).get('content')
        if result:
            return result
        else:
            raise Exception('Video length could not be fetched')

    def download(self, on_progress_callback=None):
        result = self.tree.xpath('//*[@id="player"]/source')

        if len(result) != 0:
            target = result[0].get('src')
            output_filename = f'{self.title()}.mp4'  # add extension

            if not os.path.exists(output_filename):
                print('Downloading media')
                urllib.request.urlretrieve(target, output_filename, reporthook=on_progress_callback)

                self.convert_to_mp3(output_filename, output_filename[:-3]+'mp3')

            else:
                print('File already downloaded')

        else:
            raise Exception('Source for the video does not exist')

    @staticmethod
    def convert_to_mp3(mp4_path, mp3_path):
        file_to_convert = AudioFileClip(mp4_path)
        file_to_convert.write_audiofile(mp3_path)
        file_to_convert.close()


if __name__ == '__main__':

    start_time = time.time()

    def report_hook(count, block_size, total_size):
        # progress percentage
        progress = min(1.0, float(count * block_size) / total_size)
        print(progress)

        # download speed
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            speed = (count * block_size) / (1024 * elapsed_time)  # speed in KB/s
            print(f'Download speed: {speed:.2f} KB/s')

    link = 'https://www.bitchute.com/video/n75YV5it6lHm/'
    link2 = 'https://www.bitchute.com/video/C8dHQCDlRlvY/'

    pc = PyChute(url=link)
    pc.download()
