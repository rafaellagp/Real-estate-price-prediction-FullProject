from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
import json
import time
from bs4 import BeautifulSoup as BSoup


start_time = time.time()

def create_driver():
    safari_driver_path = "/usr/bin/safaridriver"
    return webdriver.Safari(executable_path=safari_driver_path)

driver = create_driver()
driver.get("https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre?countries=BE")
cookie_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='uc-btn-accept-banner']")))
cookie_button.click()

first_listing = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/main/div/div[2]/div/div[3]/div/div[1]/div[1]/div[1]/ul/li[1]/article/div[1]/h2/a")
first_listing.click()


def split_url():
    url = driver.current_url
    split_url = re.split('/|\?', url)
    return split_url


def get_next_url():
    link = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/main/div[1]/div[2]/div/div/div[1]/div/div[1]/ul/li[2]/a')
    next_url = link.get_attribute('href')
    print(next_url)
    return next_url

def get_houses():

    houses_list = []

    file = open("houses_dict2.json","a+")
    for j in range (0, 20):
        bs_obj = BSoup(driver.page_source, 'html.parser')
        list_from_url = split_url()
        find_all_ths = bs_obj.find_all('th')
        ths = []
        for th in find_all_ths:
            ths.append(re.sub('\s\s+', '', th.get_text()))
        print(ths)
        tds = []
        find_all_tds = bs_obj.find_all('td')
        for td in find_all_tds:
            tds.append(re.sub('\s\s+', '', td.get_text()))
        print(tds)
        post_code = list_from_url[8]
        locality = list_from_url[7]
        type_of_property = ' '.join(list_from_url[5].split('-'))
        type_of_sale = ' '.join(list_from_url[6].split('-'))
        house_id = list_from_url[9]
        

        house_list = []
        print(house_list)
        for i in range(len(ths)):
            house_list.append([ths[i],tds[i]])

        house_list.insert(0,["locality",locality])
        house_list.insert(0,["post code",post_code])
        house_list.insert(0,["type of property",type_of_property])
        house_list.insert(0,["type of sale",type_of_sale])
        house_list.insert(0,["id",house_id])

        house_dict = dict(house_list)
        print(house_dict)
        houses_list.append(house_dict)
        
        json.dump(house_dict,file,indent=4)
        next_button = get_next_url()
        print(f'house number {j} register at time: {"--- %s seconds ---" % (time.time() - start_time)}')
        driver.get(next_button)
        j += 1
    print(houses_list)
    driver.close()
    return houses_list

all_houses = get_houses()
print("--- %s seconds ---" % (time.time() - start_time))
df = pd.DataFrame(all_houses) 

# out_file = open("houses_dict.json", "w")
# json.dump(houses_list, out_file, default=lambda o: '<not serializable>', indent = 4)
# out_file.close()
# print('json file write')

df.to_csv('houses_infos_test.csv') 
print('csv file write')
