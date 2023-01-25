from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import csv
import re

writer = csv.writer(open("csv\LG_plan.csv", "w", encoding="utf-8-sig", newline=""))
title = ["network", "title", "name", "charge", "code"]
writer.writerow(title)

options = webdriver.ChromeOptions()
options.add_argument("--incognito") # 시크릿 모드
options.add_experimental_option("detach", True) # 브라우저 자동 종료 방지
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 페이지 열기
driver.get("https://www.lguplus.com/plan/mplan/5g-all")

CDMA = False

def crawling(network):
    if network == "5G":
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="c-tabmenu-tab c-tab-link middlearea wide_width"]/ul/li[5]/a'))).click() # 요금제 전체보기
    else:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="c-tabmenu-tab c-tab-link middlearea wide_width"]/ul/li[8]/a'))).click() # 요금제 전체보기


    sections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="accordion c-accordion accord-short-title"]/div'))) # 요금제 제목들

    if network == "LTE":
        sections = sections[:-1]

    for num, section in enumerate(sections):
        section_name = section.find_element(By.XPATH, 'div/strong')

        if num != 0:
            driver.execute_script("arguments[0].click();", section) # 요금제 제목 펼치기

        title = section_name.get_attribute("innerText") # 요금제 제목

        plans = section.find_elements(By.XPATH, 'div[2]/div/div/ul/div/table/tbody/tr') # 요금제 목록
        for plan in plans:
            contents = plan.find_elements(By.XPATH, 'td') # 요금제 내용 들

            name = contents[0].find_element(By.XPATH, 'button')
            name_clean = name.get_attribute("innerText").strip() # 요금제 이름

            code = eval(name.get_attribute("data-ec-product")) # string to dict
            code = code['ecom_prd_id'] # 요금제 코드

            charge = contents[5].find_element(By.XPATH, 'span/span').get_attribute("innerText") # 요금
            charge = re.sub("월|원|,| ", "", charge) # 문구 제거

            writer.writerow([network, title, name_clean, charge, code])

crawling("5G")

# LTE
driver.find_element(By.XPATH, '//div[@class="c-tab-slidemenu"]/ul/li[2]/a').click() # LTE 페이지로 이동
crawling("LTE")

driver.quit()