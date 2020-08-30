import requests
from bs4 import BeautifulSoup
import re
import urllib

url = "http://www.cs.tau.ac.il/~zwick/alg2020.html"

page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')


def downloadfile(name,url):
    r=requests.get(url)
    f=open(name,'wb');
    for chunk in r.iter_content(chunk_size=255):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

for link in soup.findAll('a'):
    url = link["href"]
    if url[-3:] == "mp4":
        file_name = url.rsplit('/', 1)[-1]
        downloadfile(file_name,url)
        print("downloaded: ", file_name)

print("done")
