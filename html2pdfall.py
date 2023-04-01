import requests, json
from bs4 import BeautifulSoup
from pyhtml2pdf import converter
import config

request = requests.get(config.SITE_URL + config.XML_SITEMAP_URN, headers=config.HEADERS)
content = request.text

soup = BeautifulSoup(content, 'xml')
tags = soup.find_all("loc")

all_uri_in_xml_sitemap = []
for tag in tags:
	all_uri_in_xml_sitemap.append(tag.text)

posts_params = {}
posts_params_index = 0
images = [".jpg", ".jpeg", ".png", ".webp"]
for uri in all_uri_in_xml_sitemap:
	if any(image in uri for image in images):
		# do not include links to images 
		pass
	else:
		uri_parts = uri.split('/')
		if uri_parts[3]:
			slug = uri_parts[3]
			print(posts_params_index)
			print(slug)

			converter.convert(uri, './pdf/', f'{slug}.pdf')

			request = requests.get(config.SITE_URL + config.API_URN + slug, headers=config.HEADERS)
			posts_json = json.loads(request.text)
			title = posts_json[0]['title']['rendered']
			print(title) 
			posts_params[posts_params_index] = {'slug': slug, 'title': title, 'url': uri}
			posts_params_index += 1