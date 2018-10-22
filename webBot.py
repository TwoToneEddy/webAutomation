from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class webBot(object):
    def __init__(self):
        self.readLocalVariables()
	self.browser = webdriver.Firefox(executable_path=self.localVariables['geckoPathStr'])
	self.login()
    def readLocalVariables(self):
        self.localVariables = {}
        with open('/home/localVariables.txt') as file:
            for line in file:
                (key,val) = line.split(',')
                self.localVariables[key] = val.strip('\n')
	
    def login(self):
	self.browser.get(self.localVariables['webSiteStr'])
	self.surname=self.browser.find_element_by_name('surname')
	self.sc1=self.browser.find_element_by_name('sortCodeSet1')
	self.sc2=self.browser.find_element_by_name('sortCodeSet2')
	self.sc3=self.browser.find_element_by_name('sortCodeSet3')
	self.accNo=self.browser.find_element_by_name('accountNumber')
	self.nextButton=self.browser.find_element_by_id('Next')

	self.surname.send_keys(self.localVariables['surnameStr'])
	self.sc1.send_keys(self.localVariables['sortcode1Str'])
	self.sc2.send_keys(self.localVariables['sortcode2Str'])
	self.sc3.send_keys(self.localVariables['sortcode3Str'])
	self.accNo.send_keys(self.localVariables['accountNoStr'])
def main():
    webBot()

if __name__ == "__main__":
    main()



 
