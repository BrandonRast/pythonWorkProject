#---------------------------
#Library and pluggin imports
#---------------------------
import time
import csv
import os
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#------------
#Main program
#------------
if __name__ == "__main__":

    #----------
    #Login Keys
    #----------

    #Enter your username and password into the variables
    #Username:  Enter in the '__' field below!
    user_name = ' '         #Example: youremail@asu.edu
    #Password:  Enter in the '__' field below!
    user_pass = ' '                    #Example: 12345abcde

    #Prepares a csv file to write data to
    csv_file = open('listOfSubAccounts.csv', 'wb')
    writer = csv.writer(csv_file)

    #Chrome driver setup
    options = webdriver.ChromeOptions()
    #Headless = 'true' for windowless data collection, headless = 'false' for windowed collection
    options.headless = True

    #Chrome driver path setup, copy path from 'chromedriver.exe' located in the venv directory

    # Enter your chrome driver path into the variable
    # driver:  Enter in the '__' field below! Example: C:\Users\YourDirectoryNameHere\PycharmProjects\ASU\venv\chromedriver.exe
    driver = webdriver.Chrome(options=options, executable_path= r" ")
    #Gets the instance of the website for data collection
    #website hidden due to sensitive information
    driver.get(" ")

    #----------------------------------------------
    #Automated page navigation using element xpaths
    #----------------------------------------------

    # Sends email keys for login
    time.sleep(3)
    enter_email = driver.find_element_by_xpath('//*[@id="pseudonym_session_unique_id"]')
    enter_email.send_keys(user_name)

    # Sends password keys for login
    time.sleep(3)
    enter_password = driver.find_element_by_xpath('//*[@id="pseudonym_session_password"]')
    enter_password.send_keys(user_pass)

    #Activates login button
    time.sleep(3)
    log_in = driver.find_element_by_xpath('//*[@id="login_form"]/div[3]/div[2]/button')
    log_in.click()

    #Navigates to admin panel
    time.sleep(3)
    admin_button = driver.find_element_by_xpath('//*[@id="global_nav_accounts_link"]')
    admin_button.click()
    time.sleep(1)

    #Navigates to VIL page for data collection
    verizon_innovation_learning_button = driver.find_element_by_xpath('//*[@id="nav-tray-portal"]/span/span/div/div/div/div/div/ul/li[1]')
    verizon_innovation_learning_button.click()
    time.sleep(3)

    #--------------------
    #Data collection loop
    #--------------------
    j = 2
    with open('listOfSubAccounts.csv', 'w', newline = '') as csv_file:
        writer = csv.writer(csv_file)
        while True:
            i = 0
            url_list = '//*[@id="content"]/div/table/tbody/tr[%s]/td[5]'
            url_list_two = '//*[@id="content"]/div/table/tbody/tr[%s]/td[6]'

            #Attempts to iterate through the page and grab data elements
            try:
                while True:
                    i += 1
                    url = url_list %i
                    url_two = url_list_two %i
                    sub_account = driver.find_element_by_xpath(url)
                    print(sub_account.text)
                    students = driver.find_element_by_xpath(url_two)
                    print(students.text)
                    tuple_element = (sub_account.text, students.text)
                    writer.writerow(tuple_element)
            except NoSuchElementException:
                print("End of Page")

            #Attempts to navigate to next page
            next_page_url = '//*[@id=\"content\"]/div/nav/span/span[%s]/button'
            try:
                next_page_final = next_page_url % j
                next_page = driver.find_element_by_xpath(next_page_final)
                next_page.click()
                j = 3
                time.sleep(3)
            except NoSuchElementException:
                print("End of List")
                break
    csv_file.close()
