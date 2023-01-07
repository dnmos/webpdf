import os
import json
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def convert(
	source: str,
	target_dir: str,
	target_file: str,
	timeout: int = 3,
	install_driver: bool = True,
	print_options: dict = {},
):
	"""
	Convert a given html file or website into PDF

	:param str source: source html file or website link
	:param str target_dir: target directory to save the PDF
	:param str target_file: target filename to save the PDF
	:param int timeout: timeout in seconds. Default value is set to 2 seconds
	:param dict print_options: options for the printing of the PDF. This can be any of the params in here:https://vanilla.aslushnikov.com/?Page.printToPDF
	"""

	result = __get_pdf_from_html(
		source, timeout, install_driver, print_options)

	if not os.path.exists(target_dir):
		os.makedirs(target_dir)

	with open(target_dir + target_file, "wb") as file:
		file.write(result)


def __send_devtools(driver, cmd, params={}):
	resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
	url = driver.command_executor._url + resource
	body = json.dumps({"cmd": cmd, "params": params})
	response = driver.command_executor._request("POST", url, body)

	if not response:
		raise Exception(response.get("value"))

	return response.get("value")


def __get_pdf_from_html(
	path: str, timeout: int, install_driver: bool, print_options: dict
):
	webdriver_options = Options()
	webdriver_prefs = {}
	driver = None

	webdriver_options.add_argument("--headless")
	webdriver_options.add_argument("--disable-gpu")
	webdriver_options.add_argument("--no-sandbox")
	webdriver_options.add_argument("--disable-dev-shm-usage")
	webdriver_options.experimental_options["prefs"] = webdriver_prefs

	webdriver_prefs["profile.default_content_settings"] = {"images": 2}

	if install_driver:
		driver = webdriver.Chrome(
			ChromeDriverManager().install(), options=webdriver_options
		)
	else:
		driver = webdriver.Chrome(options=webdriver_options)

	driver.get(path)

	with open('./pyhtml2pdf/converter.css', 'r') as css_file:
		css_data = css_file.read().replace('\n', '')

	css_str = f"\
		var CustomStyleSheet=document.createElement('style');\
		CustomStyleSheet.innerHTML='{css_data}';\
		document.head.appendChild(CustomStyleSheet);\
		"

	driver.execute_script(css_str)

	try:
		scheight = 1.0
		while scheight < 9.9:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
			scheight += .01
		WebDriverWait(driver, timeout).until(
			staleness_of(driver.find_element(by=By.TAG_NAME, value="html"))
		)
	except TimeoutException:
		calculated_print_options = {
			"landscape": False,
			"displayHeaderFooter": False,
			"printBackground": True,
			# "preferCSSPageSize": True,
		}
		calculated_print_options.update(print_options)
		result = __send_devtools(
			driver, "Page.printToPDF", calculated_print_options)
		driver.quit()
		return base64.b64decode(result["data"])
