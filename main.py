from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

###
import PySimpleGUI as sg
sg.theme('Dark Blue 3')

layout = [
    [sg.Text('Python GUI')],
    [sg.Text('名前', size=(15, 1)), sg.InputText('○○〇×××')],
    [sg.Text('住所', size=(15, 1)), sg.InputText('△△△△村')],
    [sg.Text('電話番号', size=(15, 1)), sg.InputText('xxx-xxx-xxx')],
    [sg.Submit(button_text='実行ボタン')]
]

window = sg.Window('住所を入力', layout)

while True:  # Event Loop
   event, values = window.read()
   print(event, values)
   if event in (None, "Exit"):
       break
   if event == "Show":
       # "-OUTPUT-" 要素を "-IN-" 要素の値に更新
       window["-OUTPUT-"].update(values["-IN-"])



options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/MR_PC/AppData/Local/Google/Chrome/User Data") 
driver = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=options)

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
		window.close()
		break









