# webpdf

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Initial setup](#initial-setup)
* [Crontab](#crontab)
* [Relative links](#relative-links)

## General info
Python web to pdf converter
	
## Technologies
Project is created with:
* Python3.10
* Selenium 4.7.2
* Webdriver manager 3.8.5
* Google Chrome
* BeautifulSoup 4.11.1
	
## Initial setup

Python components, virtualenv
```
$ mkdir webpdf/
$ cd webpdf/
$ python3 -m venv env 
$ pip install selenium
$ pip install webdriver-manager
$ pip install beautifulsoup4
```
Install Chrome Using the Terminal Application Method
```
$ sudo apt update
$ sudo apt upgrade
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome-stable_current_amd64.deb
```
Check Chrome installed
```
$ google-chrome
```

## Crontab

Add user www to the group crontab
Edit your crontab
```
$ sudo usermod -a -G crontab www
$ crontab -e
* * * * * path_to_python3 pyfile.py
```
m h dom mon dow command

## Relative links

* https://github.com/kumaF/pyhtml2pdf