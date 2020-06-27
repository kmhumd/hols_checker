# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

#for windows
#driver = webdriver.Chrome('./chromedriver.exe')
#for macintosh
driver = webdriver.Chrome('/Users/mbp16/work/hols_checker/chromedriver')


#############GUI#############
import PySimpleGUI as sg

#  セクション1 - オプションの設定と標準レイアウト
sg.theme('Default 1')

layout = [
    [sg.Text('初期設定')],
    [sg.Text('ID', size=(15, 1)), sg.InputText('19m1102')],
    [sg.Text('PASSWORD', size=(15, 1)), sg.InputText('')],
    [sg.Submit(button_text='開始')]
]

# セクション 2 - ウィンドウの生成
window = sg.Window('HOLS checker by KOKI MORITA', layout)

# セクション 3 - イベントループ
while True:
    event, values = window.read()

    if event is None:
        print('exit')
        break

    if event == '開始':
        show_message = "ID：" + values[0] + 'が入力されました。\n'
        show_message += "PASSWORD：" + values[1] + 'が入力されました。\n'
        print(show_message)

        # ポップアップ
        sg.popup(show_message)

# セクション 4 - ウィンドウの破棄と終了
window.close()





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
	title.strip()
	if(len(mt2e) > 0):
		pending[title] = driver.current_url
	else:
		settled[title] = driver.current_url


#############main#############
print('=====================================')
print('      HOLS checker Ver.1.0')
print('=====================================')

driver.get(rooturl)
WebDriverWait(driver, 5).until(EC.visibility_of_element_located)

print('120秒以内にログインしてください')
WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'main-header-image')))
print('Login Success')
x = input('指定領域でキーを押してください')

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
		print("pending:" + str(pending))
		print("settled:" + str(settled))
		break









