from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

driver = webdriver.Chrome('C:/Users/Sam Hiner/Desktop/Resources/chromedriver.exe') #this is a file you download from chromedriver
driver.get('https://www.finam.ru/profile/akcii-usa-bats/abbott-laboratories_abt/export/') #go to a random company to start


with open('data/upgradelist.csv') as file:
	lines = file.readlines()
	for x in range(12, 13):
		line = lines[x].split('|')
		time.sleep(7)
		company_input = driver.find_element_by_css_selector('input.finam-ui-quote-selector-title')
		company_input.clear()
		company_input.send_keys(line[1] + Keys.ENTER)
		date = line[2].split('-')
		time.sleep(8)
		if datetime.datetime.strptime(line[2], '%Y-%m-%d').strftime('%A') == 'Monday':
			print('On a Monday')
			driver.execute_script('document.getElementById("issuer-profile-export-from-d").value = ' + str(int(date[2]) - 3))
		else :
			driver.execute_script('document.getElementById("issuer-profile-export-from-d").value = ' + str(int(date[2]) - 1))
		driver.execute_script('document.getElementById("issuer-profile-export-from-m").value = ' + str(int(date[1]) - 1))
		driver.execute_script('document.getElementById("issuer-profile-export-from-y").value = ' + str(int(date[0])))
		driver.execute_script('document.getElementById("issuer-profile-export-to-d").value = ' + str(int(date[2]) + 1))
		driver.execute_script('document.getElementById("issuer-profile-export-to-m").value = ' + str(int(date[1]) - 1))
		driver.execute_script('document.getElementById("issuer-profile-export-to-y").value = ' + str(int(date[0])))

		driver.execute_script('document.getElementById("issuer-profile-export-period").children[6].selected = ""')
		driver.execute_script('document.getElementById("issuer-profile-export-period").children[1].selected = "selected"')
		

		driver.find_element_by_css_selector('button.finam-ui-dialog-button-cancel').click()

time.sleep(5)

driver.quit()