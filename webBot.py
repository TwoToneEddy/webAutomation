# Must have the file localVariables.txt in /home with the following content:
# surnameStr,hudson
# sortcode1Str,99
# sortcode2Str,99
# sortcode3Str,99
# accountNoStr,99999999
# webSiteStr,https://bank.barclays.co.uk/olb/auth/#MobiLoginLink_displayWithNoCookieWithAccount.action
# geckoPathStr,/home/lee/Downloads/geckodriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
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
		# First login screen
		# Get all elements needed

		self.browser.get(self.local_variables['webSiteStr'])

		surname = WebDriverWait(self.browser, 10).until(
			EC.presence_of_element_located((By.ID, "surname0"))
		)

		card_no_rb = self.browser.find_element_by_xpath("//div[4]/div[1]/div[@class='row validation-combo' and 1]/span[@class='col-5-xl col-4-m col-6-s col-6-xs' and 1]/div[@class='radio-control' and 1]/label[@class='narrow' and 1]")
		card_no_rb.click()
		card_no_0 = self.browser.find_element_by_xpath("//input[@id='cardNumber0']")
		card_no_1 = self.browser.find_element_by_xpath("//input[@id='cardNumber1']")
		card_no_2 = self.browser.find_element_by_xpath("//input[@id='cardNumber2']")
		card_no_3 = self.browser.find_element_by_xpath("//input[@id='cardNumber3']")
		#surname = self.browser.find_element_by_id('surname0')
		next_step_bt = self.browser.find_element_by_xpath("//button")

		surname.send_keys(self.local_variables['surnameStr'])
		card_no_0.send_keys(self.local_variables['card0'])
		card_no_1.send_keys(self.local_variables['card1'])
		card_no_2.send_keys(self.local_variables['card2'])
		card_no_3.send_keys(self.local_variables['card3'])
		next_step_bt.click()

		# Second login screen
		mem_characters = WebDriverWait(self.browser, 10).until(
			EC.presence_of_element_located((By.ID, "label-memorableCharacters"))
		)

		first_char =  mem_characters.text.split()[1][0]
		second_char = mem_characters.text.split()[3][0]

		first_char_menu = self.browser.find_element_by_xpath("//div[@class='dropdown firstMemorableCharacter']/div[@id='selectedCharacter' and @class='dropdown__selected ng-binding' and 2]")
		first_char_menu.click()

		print int(first_char)
		print self.local_variables['memorable'][int(first_char)]
		print mem_characters.text.split()

		#surname=self.browser.find_element_by_name('surname')
		#sc1 = self.browser.find_element_by_name('sortCodeSet1')
		#sc2 = self.browser.find_element_by_name('sortCodeSet2')
		#sc3 = self.browser.find_element_by_name('sortCodeSet3')
		#acc_no = self.browser.find_element_by_name('accountNumber')
		#next_button = self.browser.find_element_by_id('Next')

		# Input required credentials into fields


		#sc1.send_keys(self.local_variables['sortcode1Str'])
		#sc2.send_keys(self.local_variables['sortcode2Str'])
		#sc3.send_keys(self.local_variables['sortcode3Str'])
		#acc_no.send_keys(self.local_variables['accountNoStr'])
		#next_button.click()

		# Second login screen
		# passcode = self.browser.find_element_by_id('passcode')
		#passcode = self.browser.find_element_by_xpath("//input[@name = 'passcode']")
		#passcode.send_keys(self.local_variables['passcode'])


def main():
	webBot()


if __name__ == "__main__":
	main()