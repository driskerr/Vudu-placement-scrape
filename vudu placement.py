# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:05:59 2018

@author: kerrydriscoll
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 09:21:44 2018

@author: kerrydriscoll
"""
import pandas as pd
from pandas import ExcelWriter
import re
from time import time, sleep
from random import randint
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


"""
Measure Runtime to Evaluate Code Performance
"""
start_time = time()

"""
Open Web Browser
"""
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/Users/kerrydriscoll/Downloads/chromedriver', chrome_options=option)

"""
Input MOVIE IDs to reach URL
"""

#Just the Exercise Titles
#IDs=[835625, 763662, 743740, 525129, 873206, 651466]

#All A24 Titles
IDs=[906857,835625,651466,763662,908845,743740,449248,873206,767196,682856,648015,464733,922802,465463,629676,841184,777616,761091,569326,682864,532860,906851,857020,904978,613624,859637,892541,875682,548125,569937,613628,577582,449252,525129,854035,820936,752289,802860,656520,682769,772893,778798,701080,772897,554166,400352,910082,770860,772913,841181,752293,805744,772889,732396,914602,656524,829645]


"""
Open Home Page
"""
browser.get("https://www.vudu.com/")

# Wait 20 seconds for page to load
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_1LI1Z']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

"""
Create DataFrame to Populate
"""
df_final = pd.DataFrame(columns=['Display Category', 'Title', 'Row Num','Column Num'])

    
    
"""
Collect All the Display Category Names
"""
display_category_element = browser.find_elements_by_xpath("//div[@class='nr-mb-15']")
display_category_ugly = [x.text for x in display_category_element]
display_category_ugly = list(filter(None, display_category_ugly))
display_category_clean=[re.search('(\A.*)', display_category_ugly[i]).group(1) for i in range(len(display_category_ugly))]
display_category_order_inv=dict(enumerate(display_category_clean, start=1))
display_category_order= {v: k for k, v in display_category_order_inv.items()}
print(display_category_order)

"""
Collect Titles Within Each Display Category
"""
for i in range(len(display_category_element)):
    title_element=display_category_element[i].find_elements_by_css_selector("a[href*='/content/movies/details/']")
    if not title_element:
        continue
    titles = [x.text for x in title_element]
    titles_order=dict(enumerate(titles, start=1))
    #print(titles_order)
    
    df = pd.DataFrame(list(titles_order.items()), columns=['Column Num', 'Title'])    
    df['Display Category'] = re.search('(\A.*)', display_category_element[i].text).group(1)
    df['Row Num'] = df['Display Category'].apply(lambda x: display_category_order.get(x))

    df_final = df_final.append(df, ignore_index=True)
    df_final = df_final[['Row Num','Display Category','Column Num','Title']]
    df_final[['Row Num','Column Num']]=df_final[['Row Num','Column Num']].astype(int)

browser.quit()     


run_time=time() - start_time
print("--- {} seconds ---".format(run_time))