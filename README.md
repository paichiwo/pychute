# PyChute

![PyPI - Downloads](https://img.shields.io/pypi/dm/pychute)


### A library that helps download videos from BitChute website



### Installation:
`pip install pychute`


### How to use:
```python
from pychute import PyChute

url = "bitchute url"

pc = PyChute(url=url)
pc.download()
```


### Additional features:


#### Progress callback
If you need to get progress like percentage or download speed, you can create a function 
and pass as a parameter in the download method.

```python
import time
from pychute import PyChute

start_time = time.time()

def show_progress(count, block_size, total_size):
    
    # progress percentage
    progress = min(1.0, float(count * block_size) / total_size)
    print("Progress:", progress)

    # download speed
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        speed = (count * block_size) / (1024 * elapsed_time)  # speed in KB/s
        print(f'Download speed: {speed:.2f} KB/s')


url = "bitchute url"

pc = PyChute(url=url)
pc.download(on_progress_callback=show_progress)
```


#### Filename
You can pass filename as a parameter in the form of a string to specify download location.
Using download method without the `filename` parameter will save the file to where your script is located.

```python
from pychute import PyChute

url = "bitchute url"

pc = PyChute(url=url)
output_path = f"D:\\Downloads/{pc.title()}"

pc.download(filename=output_path)
```


#### Other data
Apart from downloading, you can access other data about BitChute video:

```python
from pychute import PyChute

url = "bitchute url"
pc = PyChute(url=url)

# video title
print(pc.title())

# channel name
print(pc.channel())

# video publish date
print(pc.publish_date())

# video duration
print(pc.duration())

# subscriptions number
print(pc.subscriptions())

# video likes
print(pc.likes())

# video views
print(pc.views())

# file size in bytes
print(pc.filesize())

# description
print(pc.description())

# thumbnail image
print(pc.thumbnail())
```
