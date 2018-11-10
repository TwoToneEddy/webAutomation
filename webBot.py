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
#from pyvirtualdisplay import Display
import datetime
from selenium.webdriver.support.ui import Select
import time

class webBot(object):
	def __init__(self):
		print str(datetime.datetime.now())
		self.read_local_variables()
		#display = Display(visible=0, size=(1024, 768))
		#display.start()
		self.browser = webdriver.Firefox(executable_path=self.local_variables['geckoPathStr'])
		self.login()

		self.transfer(self.local_variables['MonthlyStorage'],self.local_variables['CurrentAccount'],'0.10')

	def read_local_variables(self):
		print "Reading text file"
		self.local_variables = {}
		with open('/home/localVariables.txt') as file:
			for line in file:
				(key,val) = line.split(',')
				self.local_variables[key] = val.strip('\n')


	def login(self):
		# Open correct webpage
		print "Starting login process"
		print "Opening " + self.local_variables['webSiteStr1']
		#self.browser.set_window_size(2000,2000)
		self.browser.get(self.local_variables['webSiteStr1'])
		#self.browser.execute_script("document.body.style.zoom='150%'")

		# First login screen
		# Get all elements needed on first login page
		print "Finding elements on first page"
		surname = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"surname")))
		sc1 = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"sortCodeSet1")))
		sc2 = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"sortCodeSet2")))
		sc3 = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"sortCodeSet3")))
		acc_no = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"accountNumber")))
		next_button = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.ID,"Next")))
		print "Found all elements on first page"

		# Input required credentials into fields and click next
		print "Sending keys"
		surname.send_keys(self.local_variables['surnameStr'])
		sc1.send_keys(self.local_variables['sortcode1Str'])
		sc2.send_keys(self.local_variables['sortcode2Str'])
		sc3.send_keys(self.local_variables['sortcode3Str'])
		acc_no.send_keys(self.local_variables['accountNoStr'])
		next_button.click()

		# Second login screen
		# Get all elements needed on second login page
		print "Finding elements on second page"
		passcode = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.XPATH,"//input[@name = 'passcode']")))
		memorable_word_l1 = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"firstMemorableCharacter")))
		memorable_word_l2 = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.NAME,"secondMemorableCharacter")))
		login_btn = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.ID,"Login")))
		print "Found all elements on second page"

		# Send passcode
		passcode.send_keys(self.local_variables['passcode'])
		print "Passcode Sent"

		# Get page source to determine which memorable characters are needed
		src = self.browser.page_source

		# Iterate through the potential characers, checking if the text is on the page and
		# send that character to the correct element
		found_first = False
		index = 0
		while index < 8:
			if ("Select letter " + str(index) in src):
				if found_first == False:
					print "First memorable character sent"
					memorable_word_l1.send_keys(self.local_variables['memorable'][index-1])
					found_first = True
				else:
					print "Second memorable character sent"
					memorable_word_l2.send_keys(self.local_variables['memorable'][index-1])
			index += 1

		# Complete the login process by clicking login button
		login_btn.click()
		print "Login button clicked"
		# Wait for loading
		WebDriverWait(self.browser,60).until(EC.invisibility_of_element((By.CLASS_NAME,"loading")))
		print "Logged on"



	def transfer(self,fromAccount,toAccount,amount):
		print "Starting transfer"
		print "Transferring" + str(amount) + " from " + fromAccount + " to " + toAccount

		# Wait for button and click
		#move_money_btn = WebDriverWait(self.browser, 60).until(
			#EC.presence_of_element_located((By.XPATH, "/html/body/nav[2]/div/div/div/ul/li[3]/a")))
		move_money_btn = WebDriverWait(self.browser, 60).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, ".bottom-fixed-menu > li:nth-child(3) > a:nth-child(1)")))
		move_money_btn.click()
		print "Move money button clicked"

		# Wait for loading
		print "Waiting for loading screen..."
		WebDriverWait(self.browser, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "loading")))
		print "Loading...."
		WebDriverWait(self.browser, 60).until(EC.invisibility_of_element((By.CLASS_NAME, "loading")))
		print "Loading Complete!"

		print "Finding all elements on transfer page"
		from_account = Select(WebDriverWait(self.browser, 60).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='fromAccountId']"))))
		to_account = Select(
			WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='toAccountId']"))))
		amount_field = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.ID, "transferAmount")))
		continue_btn = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.ID, "Continue")))
		print "Found ll elements on transfer page"

		print "Selecting accounts"
		from_account.select_by_value(
			str(self.local_variables['sortCode']) + str(fromAccount))
		to_account.select_by_value(str(self.local_variables['sortCode']) + str(toAccount))

		print "Sendind amount"
		amount_field.send_keys(amount)
		continue_btn.click()
		print "Continue clicked"

		# Wait for loading
		print "Loading...."
		WebDriverWait(self.browser, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "loading")))
		WebDriverWait(self.browser, 60).until(EC.invisibility_of_element((By.CLASS_NAME, "loading")))
		print "Loading Complete!"

		print "Waiting for confirm button"
		confirm = WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.ID, "Confirm")))
		confirm.click()
		print "Confirm button clicked"
		# Wait for loading

		print "Loading...."
		WebDriverWait(self.browser, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "loading")))
		WebDriverWait(self.browser, 60).until(EC.invisibility_of_element((By.CLASS_NAME, "loading")))
		print "Loading Complete!"
		print "Waiting for back to accounts button"
		back_to_acc_btn = WebDriverWait(self.browser, 60).until(EC.element_to_be_clickable((By.ID, 'Back to accounts')))
		back_to_acc_btn.click()
		print "Back to accounts clicked"

		# Wait for loading
		print "Loading...."
		WebDriverWait(self.browser, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "loading")))
		WebDriverWait(self.browser, 60).until(EC.invisibility_of_element((By.CLASS_NAME, "loading")))
		print "Loading Complete!"
		print "Transfer complete!"


def main():
	webBot()


if __name__ == "__main__":
	main()
