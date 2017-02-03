
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


PAGE = requests.get('http://repoforge.org/use/')
TREE = html.fromstring(PAGE.content)

LOG_NAME = TREE.xpath(".//*[@id='content']/ul[1]/li[1]/a/text()")
LOG_URL = TREE.xpath(".//*[@id='content']/ul[1]/li[1]/a/@href").pop()


print("log name : ", LOG_NAME)
print("log url : ", LOG_URL)
download(LOG_URL, "file.gz")
