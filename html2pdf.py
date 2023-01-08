from pyhtml2pdf import converter
from credentials import site_url

converter.convert(site_url, './pdf/', 'site.pdf')