# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import pprint


if os.name == 'nt':
	driver = webdriver.Chrome('./chromedriver.exe')
elif os.name == 'posix':
	driver = webdriver.Chrome('/Users/mbp16/work/hols_checker/chromedriver')


rooturl = 'https://member.hirosaki-surgery2.org/'
pending = {}
settled = {}

# modules
def click_all(base_url):
	driver.get(base_url)
	WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'morelink')))

	links = driver.find_elements_by_class_name("morelink")
	urls = []

	for link in links:
		urls.append(link.get_attribute("href"))

	print(str(len(links)) + ' links are detected')

	for url in urls:
		driver.get(url)
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-footer')))

		##判別プログラムの場所
		check_mt2e()

def check_mt2e():
	driver.implicitly_wait(2)
	mt2e = driver.find_elements_by_class_name("mt2e")
	title = driver.title
	title = title.replace('\u3000', ' ')
	if(len(mt2e) > 0):
		pending[title] = driver.current_url
	else:
		settled[title] = driver.current_url

def clr():
	if os.name == 'nt':
		os.system('cls')
	elif os.name == 'posix':
		os.system('clear')

#############main#############
clr()

print('=====================================')
print('      HOLS checker Ver.1.0')
print('=====================================')

driver.get(rooturl)
WebDriverWait(driver, 5).until(EC.visibility_of_element_located)

print('120秒以内にログインしてください')
WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'main-header-image')))
print('Login Success')

os.system('cls')
x = input('チェック対象のページに移動してください。何かキーを押すとチェックを開始します。')

#main_routine
cur_url = driver.current_url

for i in range (1000):
	
	print("Page " + str(i+1) + " is running")
	url = cur_url + '/page/' + str(i+1)
	driver.get(url)

	click_all(url)
	
	nx_url = cur_url + '/page/' + str(i+2)
	driver.get(nx_url)
	
	
	try:	
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'morelink')))	
		
	except:
		print("end")
		print("--------未受講--------")
		for pending_key in pending.keys():
			print(pending_key)
		# pprint.pprint(pending)

		print("--------受講済み--------")
		for settled_key in settled.keys():
			print(settled_key)
		# pprint.pprint(settled)
		break










