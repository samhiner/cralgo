from selenium import webdriver
import selenium.common.exceptions #so that I can try-except selenium exceptions

import time

NUM_PAGES = 2 #how many pages of results are at that url


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
	print(company_link)
	driver.get(company_link)
	time.sleep(5)
	print(driver.find_element_by_xpath('//a[contains(text(), "Ticker:")]'))
	try:
		return driver.find_element_by_xpath('//a[contains(text(), "Ticker:")]//following-sibling::span').text
	except selenium.common.exceptions.NoSuchElementException:
		return None

def get_report_pub_time(report_link):
	driver.get(report_link)
	datetime = driver.find_element_by_css_selector('meta[property=article:published_time]').get_attribute('content')
	time = datetime.split('T')[1].split(':')
	time[0] -= 5
	return ':'.join(time)

def get_debt_equity_ratio(ticker):
	driver.get('https://finance.yahoo.com/quote/' + ticker + '/key-statistics/')
	return driver.find_element_by_xpath('//span[contains(text(), "Total Debt/Equity")]//parent::td//following-sibling::td').text

execution_list = []
for page in range(0, NUM_PAGES):
	driver.get('https://www.moodys.com/researchandratings/viewall/ratings-news/rating-action/00300E001/00300E001%7C005000/-/0/' + str(page) + '/p_published_date_time/-1/10-02-2019/10-02-2020/-/-1/-/-/-/en/global/pdf/-/rra')
	time.sleep(1) #so the page loads by the time you check
	reports = driver.find_elements_by_xpath('//a[contains(text(), "upgrades")]') #find links on the page which have text that includes the word "upgrades". 
	print(reports)
	#this doesn't work and neither does all of the other methods I have tried
	company_links = [driver.find_element_by_xpath('//a[contains(text(), "upgrades")][' + str(x + 1) + ']') for x in range(len(reports))] #only gets first listed company, which should be the one with the ticker. This decision can be questioned later.
	print(company_links)
	for x in range(len(company_links)):
		execution_list.append([company_links[x].get_attribute('innerHTML'), reports[x].get_attribute('href'), reports[x].text])

print(execution_list)
driver.quit()
raise IndexError()

csv = open('data/upgradelist.csv', 'a')
csv.write('Ticker,Publish Time,Debt/Equity,Details')
for item in execution_list:
	ticker = get_ticker(item[0])
	print(ticker)
	if ticker != None:
		csv.write('\n' + ticker + ',' + get_report_pub_time(item[1]) + ',' + get_debt_equity_ratio(ticker) + ',' + item[2])

csv.close()

driver.quit()