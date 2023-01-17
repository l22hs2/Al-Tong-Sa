from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import re

writer = csv.writer(open("LG_plan_support.csv", "w", encoding="utf-8-sig", newline=""))
title = ["network", "plan", "name", "charge", "code"]
writer.writerow(title)

# selenium to open Chrome
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

# 페이지 열기
driver.get("https://shop.uplus.co.kr/pc/mobile/pricePlan/priceByModel")

def crawling(network):
    # 요금제 선택 창 열기
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//button[@id="btn_selectPricePlan"]'))).click()

    if network == "5G":
        plans_list = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="tpPP00"]/div')))
    else:
        plans_list = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="tpPP01"]/div')))

    # 요금제 전체 리스트 > title 별로 분류, title 개수 만큼
    for plan_list in plans_list:
        title = plan_list.find_element(By.XPATH, 'p').text
        plans = plan_list.find_elements(By.XPATH, 'div//div[@class="cell"]/span/label')
        for plan in plans:
            name = plan.text
            code = plan.get_attribute('for')[-10:]

            # 선택형 요금제 분류
            if (network == "LTE") and (title == "LTE 선택형 요금제"):
                if (name.startswith("LTE 선택형 망내")) or name.startswith("LTE 선택형 음성"):
                    writer.writerow([network, "LTE 선택형 망내", name, "", code])
                else:
                    writer.writerow([network, "LTE 선택형", name, "", code])
            else:
                writer.writerow([network, title, name, "", code])


crawling("5G")

driver.find_element(By.XPATH, '//div[@class="btn_close"]').click()      # 요금제 창 닫기
driver.find_element(By.XPATH, '//label[@for="fn_rd_type01"]').click()   # 기기종류 LTE 선택
crawling("LTE")

driver.quit()