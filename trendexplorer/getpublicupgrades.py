from selenium import webdriver
import selenium.common.exceptions #so that I can try-except selenium exceptions

import time

#IMPORTANT NOTES
#this version takes out the getting links (i have them stored in a file from a previous run) and just adds stocks until it breaks when you set up again (will have to delete old ones manually and the first one in the list isn't searched for)
#if you want the full version, go to the last commit, add yahoo data, and figure out how to prevent connections from getting forcibly closed every now and then.
#also if you run this again make sure to make it only pass US companies (or get the international ticker) because it will take an international ticker and find the US company with the same ticker.

START_PAGE = 0
END_PAGE = 104
#last page is 104

# LOGIN
with open('data/userpass.txt', 'r') as file:
	text = file.readlines()
	USERNAME = text[0][:-1]
	PASSWORD = text[1]

driver = webdriver.Chrome('C:/Users/Sam Hiner/Desktop/Resources/chromedriver.exe') #this is a file you download from chromedriver
driver.get('https://www.moodys.com/researchandratings/viewall/ratings-news/rating-action/00300E001/00300E001%7C005000/-/0/0/p_published_date_time/-1/10-02-2019/10-02-2020/-/-1/-/-/-/en/global/pdf/-/rra')

login_fields = driver.find_elements_by_css_selector('.StyledComponents-sc-31xgrq-2.dfWISP')

login_fields[0].send_keys(USERNAME)
login_fields[1].send_keys(PASSWORD)

driver.find_element_by_css_selector('.StyledComponents__StyledButton-sc-10r1lbp-2.grwNPl').click()

# PAGE CRAWLING

def get_ticker(company_link):
	driver.get(company_link)
	time.sleep(1)
	try:
		return driver.find_element_by_xpath('//span[contains(text(), "Ticker:")]//following-sibling::span').text
	except selenium.common.exceptions.NoSuchElementException:
		return None

def get_report_pub_time(report_link):
	driver.get(report_link)
	datetime = driver.find_element_by_css_selector('meta[property="article:published_time"]').get_attribute('content')
	time = datetime[:-1].split('T')[1].split(':')
	time[0] = str(int(time[0]) - 5)
	return ':'.join(time)

#gets debt/equity ratio and name
def get_yahoo_data(ticker):
	try:
		driver.get('https://finance.yahoo.com/quote/' + ticker + '/key-statistics/')
		name = ' ('.join(driver.find_element_by_css_selector('h1').text.split(' (')[:-1])
		return driver.find_element_by_xpath('//span[contains(text(), "Total Debt/Equity")]//parent::td//following-sibling::td').text, name
	except selenium.common.exceptions.NoSuchElementException:
		return None, None

file = open('data/execlist.txt', 'r')
exec('execution_list = ' + file.readline())
file.close()

csv = open('data/upgradelist.csv', 'a')
for x in range(len(execution_list)):
	item = execution_list[x]
	try:
		ticker = get_ticker(item[0])
		print(item[0], ticker)
		if ticker != None:
			leverage, name = get_yahoo_data(ticker)
			if leverage == None:
				continue
			#ERROR breaks for solar winds holdings upgrade on 28 Jan 2020. May be related to error of data only going back to Jan 2020 (this is last stock)
			csv.write('\n' + ticker + '|' + name + '|' + get_report_pub_time(item[1]) + '|' + leverage + '|' + item[2])
			execution_list.pop(0)
	except:
		file = open('data/execlist.txt', 'w')
		file.truncate()
		print(execution_list)
		file.write(str(execution_list))
		file.close()
		raise RuntimeError()

csv.close()

driver.quit()