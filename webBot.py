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
		surname=self.browser.find_element_by_name('surname')
		sc1 = self.browser.find_element_by_name('sortCodeSet1')
		sc2 = self.browser.find_element_by_name('sortCodeSet2')
		sc3 = self.browser.find_element_by_name('sortCodeSet3')
		acc_no = self.browser.find_element_by_name('accountNumber')
		next_button = self.browser.find_element_by_id('Next')

		# Input required credentials into fields
		surname.send_keys(self.local_variables['surnameStr'])
		sc1.send_keys(self.local_variables['sortcode1Str'])
		sc2.send_keys(self.local_variables['sortcode2Str'])
		sc3.send_keys(self.local_variables['sortcode3Str'])
		acc_no.send_keys(self.local_variables['accountNoStr'])
		next_button.click()

		# Second login screen
		passcode = self.browser.find_element_by_id('passcode')
		passcode.send_keys(self.local_variables['passcode'])


def main():
	webBot()


if __name__ == "__main__":
	main()