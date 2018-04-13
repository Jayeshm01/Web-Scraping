#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Mar 29 23:04:04 2018

@author: Jayesh Mehta
"""

from bs4 import BeautifulSoup
import re
import time
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException


def get_jobs_data(url):


    chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    time.sleep(5)
    print("first wait...")
    inputElement = driver.find_element_by_xpath('//*[@id="skill"]/div[1]/div[2]/input')
    time.sleep(5)
    print("second wait...")
    inputElement.send_keys('Data Scientist')
    time.sleep(5)
    print("third wait...")
    inputElement.send_keys(Keys.ENTER)
    time.sleep(7)
    print("fourth wait...")

    #elem = driver.find_element_by_class_name('grayBtn')
    count=0
    time.sleep(5)
    print("fifth wait...")
    page_needed = 3

    while(True):

            try:
                elem = driver.find_element_by_link_text('Next')
                elem.click()
                time.sleep(5)

                soup = BeautifulSoup(driver.page_source,"lxml")
                jobs = soup.find_all('div', {'itemtype':re.compile('http://schema.org/JobPosting')})

                csv_file = open('DS_jobs.csv', 'a')
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Company_Name','Job_Desc','Exp','Location','Skills','Salary'])

                for title in jobs:


                    comp = title.find('span', {'itemprop':re.compile('hiringOrganization')}).text.strip()
                    desc = title.find('li', {'itemprop':re.compile('title')}).text.strip()
                    exp = title.find('span', {'class':re.compile('exp')}).text.strip()
                    loc = title.find('span', {'itemprop':re.compile('jobLocation')}).text.strip()
                    skills = title.find('span', {'itemprop':re.compile('skills')}).text.strip()
                    sal = title.find('span', {'itemprop':re.compile('baseSalary')}).text.strip()

                    csv_writer.writerow([comp,desc,exp,loc,skills,sal])


                count = count + 1
                print("Pages clicked : "+str(count))
                wait = WebDriverWait(driver, 30)
                time.sleep(10)
                wait = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'Next')))
                if count == page_needed:
                    print("we got the no. of pages we are looking for")

                    break
            except ElementNotVisibleException:
                break
            except TimeoutException:
                break


    csv_file.close()

    driver.quit()


if __name__=='__main__':
    url='https://www.naukri.com/browse-jobs'
    get_jobs_data(url)
