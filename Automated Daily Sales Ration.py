import os
import time
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
# from selenium.webdriver import EdgeOptions

driver = webdriver.Chrome()
time1 = time.time()
# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# driver = webdriver.Chrome(options = op)

# op = webdriver.EdgeOptions()
# op.add_argument('headless')
# driver = webdriver.Edge(options = op)


driver.get('http://mahaepos.gov.in/AbstractTransReport.jsp')

driver.maximize_window()
# sleep(1)

Eregion = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, "E Region Wadala")))

# we are doing this because our element was unable to click
scroll_to_region = driver.find_element(By.LINK_TEXT , 'Kolhapur')
actions = ActionChains(driver)
actions.move_to_element(scroll_to_region).perform()

Eregion.click()

Govandi = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT , '44 E GOVANDI')))

Bhandup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT , 'BHANDUP')))

actions.move_to_element(Bhandup).perform()

Govandi.click()

scroll_to_shop = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.LINK_TEXT , '251832900172')))

sleep(0.5)
# actions = ActionChains(driver)  #ALREADY IMPORTED ABOVE
actions.move_to_element(scroll_to_shop).perform()

SHOPnumber = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.LINK_TEXT , '251832900166')))

SHOPnumber.click()

Perpage  = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , '/html/body/div/div[3]/div/div[3]/div[3]/div[2]/div[2]/div/div/div[3]/label/select')))

Perpage = Select(Perpage)

Perpage.select_by_visible_text('All')

driver.find_element(By.XPATH , "/html/body/div/div[3]/div/div[3]/div[3]/div[2]/div[2]/div/div/div[1]/a[3]").click()



# table = driver.find_elements(By.XPATH , '/html/body/div/div[3]/div/div[3]/div[3]/div[2]/div[2]/div/div/table/tbody/tr')

# len(table)

rationpage = driver.page_source

# pd.set_option('display.max_columns' , None)

# df = pd.DataFrame((table[0].text).split()).T

# for i in range(len(table)):
#     if i == 0 :
#         continue 
#     else :
#         df.loc[i , :] = (table[i].text).split()

df = pd.read_html(rationpage )[1]

# df.head(0)

column_names = 'Sl No,SRC No,Scheme,Avail Type,Receipt No,Date,Wheat (Kgs),Rice (Kgs),Sugar (Kgs),Foodgrain Kit (PKTS),K Oil (Kgs),Maize (Kgs),Jowar (Kgs),Bajra (Kgs),Ragi (Kgs),Wheat-PMGKAY (Kgs),Rice-PMGKAY (Kgs),FRice (Kgs),Fest Sugar (PKTS),Fest POil (PKTS),Fest Rava (PKTS),Fest Bag (PKTS),Fest Chana Dal ,Amount (Rs.),Portability,Auth Trans Time'.split(',')

df.columns = column_names
df.set_index('Date' , inplace=True)
df.drop(index = 'Total' , inplace= True )
df.index = df.index.map(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%S'))

dailysales = df.resample('D')['Wheat (Kgs)' ,'Rice (Kgs)' , 'Wheat-PMGKAY (Kgs)' , 'Rice-PMGKAY (Kgs)' ].sum()
dailysales = dailysales.merge(df.resample('D')['Wheat (Kgs)'].count().rename('Sale Count') , on='Date')
dailysales.index = dailysales.index.map(str).map(lambda x : x[0:11])
dailysales.loc[-1] = dailysales.sum()
dailysales.rename(index = {-1 :'Total'} , inplace = True)



# dailysales.astype('int').to_excel('dailysales.xlsx')


# dailysales.astype('int')



remaningcards = pd.read_excel(r"C:\Users\ysaur\Desktop\FSDS\007 Pandas\Pandas revision\datasets\remaningcards.xlsx" )


# yetTOcome = remaningcards[remaningcards['SRC No'].isin(df['SRC No'].astype('float'))==False].sort_values(by = 'REF').fillna(0).astype('int64').reset_index(drop = True)




# pd.set_option('display.max_rows' , None)



# yetTOcome



df = df[(df['Foodgrain Kit (PKTS)'] == 1)== False ]
#We did this here to exclude all the food kits that were sold seperately , remove it when the foodkit column disappears

yetTOcome = remaningcards[remaningcards['SRC No'].isin(df['SRC No'].astype('float'))==False].sort_values(by = 'REF').fillna(0).astype('int64').reset_index(drop = True)



monthstring = datetime.now()
year = monthstring.strftime('%Y')
monthstring = monthstring.strftime('_%m_%Y.xlsx')
savepath = r'C:\Users\ysaur\OneDrive\Ration\Daily sales\ds_excel/'
directory = os.path.exists(savepath+year)
if not directory:
    os.mkdir(savepath+year)

filepath = savepath+year+'/Dailysales'+ monthstring



with pd.ExcelWriter(filepath) as writer:
    dailysales.astype('int').to_excel(writer, sheet_name='dailysales')
    yetTOcome.to_excel(writer, sheet_name='remaining_cards' , index = False)


time2 = time.time()
print(f'{time2-time1:.1f}')