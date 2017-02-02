
from lxml import html
from requests import get
import requests

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


PAGE = requests.get('https://archive.org/download/44_0_20071010031116_crawl100-c')
TREE = html.fromstring(PAGE.content)

LOG_NAME = TREE.xpath('//*[@id="wrap"]/div[2]/pre/a[2]/text()')
LOG_URL = TREE.xpath('//*[@id="wrap"]/div[2]/pre/a[2]/@href')


print("log name : ", LOG_NAME)
print("log url : ", LOG_URL)
download(LOG_URL, "file.gz")