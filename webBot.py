# Must have the file localVariables.txt in /home with the following content:
# surnameStr,hudson
# sortcode1Str,99
# sortcode2Str,99
# sortcode3Str,99
# accountNoStr,99999999
# webSiteStr,https://bank.barclays.co.uk/olb/auth/#MobiLoginLink_displayWithNoCookieWithAccount.action
# geckoPathStr,/home/lee/Downloads/geckodriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
from selenium.common import exceptions

from selenium.webdriver.support.ui import Select
import time

class webBot(object):
	def __init__(self):
		self.read_local_variables()
		self.browser = webdriver.Firefox(executable_path=self.local_variables['geckoPathStr'])
		self.login()

	def read_local_variables(self):
		self.local_variables = {}
		with open('/home/localVariables.txt') as file:
			for line in file:
				(key,val) = line.split(',')
				self.local_variables[key] = val.strip('\n')


	def login(self):
		# Open correct webpage
		self.browser.get(self.local_variables['webSiteStr1'])

		# First login screen
		# Get all elements needed on first login page
		surname=self.browser.find_element_by_name('surname')
		sc1 = self.browser.find_element_by_name('sortCodeSet1')
		sc2 = self.browser.find_element_by_name('sortCodeSet2')
		sc3 = self.browser.find_element_by_name('sortCodeSet3')
		acc_no = self.browser.find_element_by_name('accountNumber')
		next_button = self.browser.find_element_by_id('Next')

		# Input required credentials into fields and click next
		surname.send_keys(self.local_variables['surnameStr'])
		sc1.send_keys(self.local_variables['sortcode1Str'])
		sc2.send_keys(self.local_variables['sortcode2Str'])
		sc3.send_keys(self.local_variables['sortcode3Str'])
		acc_no.send_keys(self.local_variables['accountNoStr'])
		next_button.click()

		# Second login screen
		# Get all elements needed on second login page
		passcode = self.browser.find_element_by_xpath("//input[@name = 'passcode']")
		memorable_word_l1 = self.browser.find_element_by_name("firstMemorableCharacter")
		memorable_word_l2 = self.browser.find_element_by_name("secondMemorableCharacter")
		login_btn = self.browser.find_element_by_id('Login')

		# Send passcode
		passcode.send_keys(self.local_variables['passcode'])

		# Get page source to determine which memorable characters are needed
		src = self.browser.page_source

		# Iterate through the potential characers, checking if the text is on the page and
		# send that character to the correct element
		found_first = False
		index = 0
		while index < 8:
			if ("Select letter " + str(index) in src):
				if found_first == False:
					memorable_word_l1.send_keys(self.local_variables['memorable'][index-1])
					found_first = True
				else:
					memorable_word_l2.send_keys(self.local_variables['memorable'][index-1])
			index += 1

		# Complete the login process by clicking login button
		login_btn.click()

		# Wait for loading
		WebDriverWait(self.browser,10).until(EC.invisibility_of_element((By.CLASS_NAME,"loading")))

		# Wait for button and click
		move_money_btn = WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/nav[2]/div/div/div/ul/li[3]/a")))
		move_money_btn.click()

		# Wait for loading
		WebDriverWait(self.browser,10).until(EC.invisibility_of_element((By.CLASS_NAME,"loading")))
		from_account = Select(self.browser.find_element_by_xpath("//*[@id='fromAccountId']"))
		to_account = Select(self.browser.find_element_by_xpath("//*[@id='toAccountId']"))
		amount = self.browser.find_element_by_id('transferAmount')
		continue_btn = self.browser.find_element_by_id('Continue')
		from_account.select_by_value(str(self.local_variables['sortCode'])+str(self.local_variables['MonthlyStorage']))
		to_account.select_by_value(str(self.local_variables['sortCode'])+str(self.local_variables['CurrentAccount']))
		amount.send_keys('1.10')
		continue_btn.click()

		# Wait for loading
		#WebDriverWait(self.browser,10).until(EC.invisibility_of_element((By.CLASS_NAME,"loading")))
		#time.sleep(2)
		ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
		confirm_btn = WebDriverWait(self.browser,2).until(f)
		continue_btn.send_keys(Keys.RETURN)

def main():
	webBot()


if __name__ == "__main__":
	main()