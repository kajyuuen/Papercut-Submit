import sys
import os
from getpass import getpass
import argparse
import yaml
from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PaperCut:

    def __init__(self):
        self.url = 'https://papercut-p01.u.tsukuba.ac.jp:9192'
        self.br = Chrome()

    def __exsit_by_xpath(self, driver, xpath):
        driver = driver
        try:
            driver.find_element_by_xpath(xpath)
        except:
            return False
        return True

    def __make_soup(self):
        req = requests.get(self.br.page_source)
        soup = BeautifulSoup(req.text, 'lxml')

    def __load_credentials(self):
        if set(os.environ) >= { 'ZENGAKU_PASSWORD', 'ZENGAKU_USERNAME' }:
            self.username = os.environ['ZENGAKU_USERNAME']
            self.password = os.environ['ZENGAKU_PASSWORD']
        else:
            print('Enter your credentials')
            self.username = input('Username: ')
            self.password = getpass()

    def __login(self):
        self.__load_credentials()
        driver = self.br
        driver.get(self.url)
        driver.find_element_by_xpath('//*[@id="inputUsername"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="inputPassword"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="login"]/form/input[6]').click()
        if (self.__exsit_by_xpath('//div[@class="errorMessage"]', driver)):
            print('Invalid UserName or Password')
            driver.quit()
            sys.exit(1)
        return driver

    def print_action(self, print_objects):
        driver = self.__login()
        for print_object in print_objects:
            driver.get(self.url+'/app?service=action/1/UserWebPrint/0/$ActionLink')
            driver.find_element_by_xpath('//*[@id="main"]/div[2]/form/div[2]/input[1]').click()
            file_input = driver.find_element_by_xpath('/html/body/input')
            try:
                file_input.send_keys(print_object)
            except:
                print('No such file')
                driver.quit()
                sys.exit(1)
            driver.find_element_by_xpath('//*[@id="upload"]').click()
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="infoMessage"]')))
        driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', nargs='+', help='印刷したいファイル')
    args = parser.parse_args()
    file_names = map(os.path.abspath, args.file_names)
    paper_cut = PaperCut()
    paper_cut.print_action(file_names)
