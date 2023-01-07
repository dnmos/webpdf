import requests
from bs4 import BeautifulSoup
from pyhtml2pdf import converter

url = "https://visitbudapest.ru/post-sitemap.xml"
headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
}
request = requests.get(url, headers=headers)
content = request.text

soup = BeautifulSoup(content, 'xml')
tags = soup.find_all("loc")
urls = []
urls_article = []
words = [".jpg", ".jpeg", ".png", ".webp"]
for tag in tags:
	urls.append(tag.text)
for url in urls:
	if any(word in url for word in words):
		pass
	else:
		urls_article.append(url)
		url_split = url.split('/')
		if url_split[3]:
			slug = url_split[3]
			converter.convert(url, './pdf/', f'{slug}.pdf')