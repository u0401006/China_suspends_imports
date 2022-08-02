import os
from bs4 import BeautifulSoup as BP
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pandas as pd

today = datetime.now().strftime("%Y%m%d")
url = 'https://ciferquery.singlewindow.cn/'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, ".topText2").click()
driver.execute_script('document.getElementById("country").setAttribute("value", "TWN")')
driver.execute_script("chaxun()")

allPage = int(driver.find_elements(By.CSS_SELECTOR, ".page-item")[-2].text)+1
with open(f'chinaBan-{today}.txt', 'a') as f:
    thead = str(BP(driver.page_source, 'lxml').find('table', {'id': 'ciferMessStatVoList'}).find("thead")).replace('\t','').replace('\n','')
    f.write(f'<table>{thead}')
    
    for i in range(1, allPage):
        table = str(BP(driver.page_source, 'lxml').find("tbody"))
        f.write(table)
        driver.find_element(By.CSS_SELECTOR, ".page-next > a").click()
        time.sleep(2)

    f.write(f'</table>')

with open(f'china_suspends_import-{today}.txt', 'r') as f:
    table = f.read()
df = pd.read_html(table)[0]
df.to_csv(f'china_suspends_import-{today}.csv', sep='\t', encoding='utf-8')
os.remove(f'china_suspends_import-{today}.txt')
