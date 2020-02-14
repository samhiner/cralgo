from selenium import webdriver
import selenium.common.exceptions #so that I can try-except selenium exceptions

NUM_PAGES = 104 #how many pages of results are at that url


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
	try:
		return driver.find_element_by_xpath('//a[contains(text(), "Ticker:")]//following-sibling::span').text
	except selenium.common.exceptions.NoSuchElementException:
		return None

#UNTESTED
def get_report_pub_time(report_link):
	driver.get(report_link)
	datetime = driver.find_element_by_css_selector('meta[property=article:published_time]').get_attribute('content')
	time = datetime.split('T')[1].split(':')
	time[0] -= 5
	return ':'.join(time)

execution_list = []
for page in range(0, NUM_PAGES):
	driver.get('https://www.moodys.com/researchandratings/viewall/ratings-news/rating-action/00300E001/00300E001%7C005000/-/0/' + str(page) + '/p_published_date_time/-1/10-02-2019/10-02-2020/-/-1/-/-/-/en/global/pdf/-/rra')
	reports = driver.find_elements_by_xpath('//a[contains(text(), "upgrades")]') #find links on the page that include the word "upgrades". 
	company_links = [report.find_element_by_xpath('//parent::td//following-sibling::td//descendant::a') for report in reports] #only gets first listed company, which should be the one with the ticker. This decision can be questioned later.
	for x in range(len(company_links)):
		execution_list.append([company_links[x].get_attribute('href'), reports[x].get_attribute('href'), reports[x].text])

csv = open('data/upgradelist.csv', 'a')
csv.write('Ticker,Publish Time,Details')
for item in execution_list:
	ticker = get_ticker(item[0])
	if ticker != None:
		csv.write('\n' + ticker + ',' + get_report_pub_time(item[1]) + ',' + item[2])

csv.close()

driver.quit()