import time
from pychute.main import PyChute

if __name__ == '__main__':

    start_time = time.time()

    def format_file_size(size_bytes) -> str:
        """Convert bytes to MB / GB"""
        if size_bytes >= 1024 ** 3:
            return f'{(size_bytes / (1024 ** 3)):.2f} GB'
        else:
            return f'{(size_bytes / (1024 ** 2)):.2f} MB'

    def report_hook(count, block_size, total_size):
        # progress percentage
        progress = min(1.0, float(count * block_size) / total_size)
        print(progress)

        # download speed
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            speed = (count * block_size) / (1024 * elapsed_time)  # speed in KB/s
            print(f'Download speed: {speed:.2f} KB/s')

    link1 = 'https://www.bitchute.com/video/n75YV5it6lHm/'
    link2 = 'https://old.bitchute.com/video/fFUV9Gpim7zc/'
    link3 = 'https://www.bitchute.com/video/aC8qhbI16PWs'

    pc = PyChute(url=link3)
    # pc.download(on_progress_callback=report_hook, filename='d:\\test')
    print(pc.title())
    print(pc.channel())
    print(pc.publish_date())
    print(pc.duration())
    print(pc.subscriptions())
    print(pc.likes())
    print(pc.views())
    print(pc.filesize())
    print(pc.thumbnail())
    print(pc.description())
