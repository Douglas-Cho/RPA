import os
import sys
import numpy as np
import pandas as pd
import win32com.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from pandas import ExcelWriter

#Global parameters setting
TARGET_URL1 = "https://platform.spgi.spglobal.com"
TARGET_URL2 = "https://platform.mi.spglobal.com/web/client?auth=inherit#search/manageSavedSearches"

#driver = webdriver.Chrome('/Users/xyz/Documents/chromedriver')
driver = webdriver.Chrome('C:/Downloads/chromedriver.exe')
driver.maximize_window()
driver.get(TARGET_URL1)
sleep(10)
try:
    myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".snl-widgets-input-text-wrapper:nth-child(2) > .form-control")))
    print("Page is ready!")
    driver.find_element_by_css_selector(".snl-widgets-input-text-wrapper:nth-child(2) > .form-control").click();
    driver.find_element_by_css_selector(".snl-widgets-input-text-wrapper:nth-child(2) > .form-control").send_keys("xxx@xyz.org");
    driver.find_element_by_name("password").click();
    driver.find_element_by_name("password").send_keys("xxxxxx");
    driver.find_element_by_name("password").send_keys(Keys.ENTER);
    sleep(5)
except TimeoutException:
    sys.exit("Loading took too much time!")

df_country = pd.read_excel('C:/Users/xyz/Documents/Selenium_IDE/Country_Code.xlsx', index_col=None, header=0)

for i in range(len(df_country)):
    driver.get(TARGET_URL2)
    sleep(8)
    try:
        myElem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, df_country.Code[i])))
        # print(df_country.Code[i])
    except TimeoutException:
        print("Loading took too much time!")
    driver.find_element_by_partial_link_text(df_country.Code[i]).click();
    sleep(10)
    try:
        myElem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "solrResultGrid1_i1_grid_table_page_size_selector")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        resProduct = soup.find_all('span', {"class": "ui-iggrid-pagerrecordslabel ui-iggrid-results"})
        string = ''.join(resProduct[0])
        count = int(string.split(' ')[4])
        print("Country: ", df_country.Name[i], "| News count: ", count)
        driver.find_element_by_id("solrResultGrid1_i1_grid_table_page_size_selector").click();
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Sendkeys("{PGDN}")
        sleep(1)
        shell.Sendkeys("{ENTER}")
        sleep(7)
        driver.find_element_by_css_selector(".dropdown > .snl-three-dots-icon").click();
        sleep(2)
        driver.find_element_by_partial_link_text("Export to Excel").click();
        if count > 500:
            driver.find_element_by_css_selector(".ui-iggrid-nextpagelabel").click()
            sleep(5)
            driver.find_element_by_css_selector(".dropdown > .snl-three-dots-icon").click();
            sleep(2)
            driver.find_element_by_partial_link_text("Export to Excel").click();
        pass
    except TimeoutException:
        print("Loading took too much time!")

driver.find_element_by_partial_link_text("xxx@xyz.org").click()
driver.find_element_by_partial_link_text("Sign out").click()
sleep(5)
driver.quit()

df_temp = pd.read_excel('C:/Users/xyz/Documents/SPGlobalofficeworkbook.xls', index_col=None, header=None)
df_temp['3'] = df_temp.iat[4, 1]
df_temp = df_temp[10:]
df_out = df_temp.copy(deep=True)

for i in range(1, 50):
    filename = 'C:/Users/xyz/Documents/SPGlobalofficeworkbook (' + str(i) + ').xls'
    if os.path.exists(filename):
        df_temp = pd.read_excel(filename, index_col=None, header=None)
        df_temp['3'] = df_temp.iat[4, 1]
        df_temp = df_temp[10:]
        df_out_temp = df_out.append(df_temp)
        df_out = df_out_temp.copy(deep=True)
    pass

writer = ExcelWriter('C:/Users/xyz/Documents/Sentiment_input.xlsx')
df_out.to_excel(writer, index=False, header=False)
writer.save()
