from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import re

writer = csv.writer(open("KT_plan.csv", "w", encoding="utf-8-sig", newline=""))
title = ["network", "plan", "name", "charge", "code"]
writer.writerow(title)

# selenium to open Chrome
driver = webdriver.Chrome()

# 페이지 열기
driver.get("https://product.kt.com/wDic/index.do?CateCode=6002")

# 크롤링 함수
def crawling(network):
    time.sleep(1)

    # 더보기 클릭
    while True:
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//a[@class="btn-more"]'))).click()
            time.sleep(0.3)
        except:
            break

    # 페이지의 요금제 상품 개수 측정
    plans_len = len(driver.find_elements(By.XPATH, '//table[@class="detail-list"]'))

    # 상품 개수 만큼 리스트 펼치기
    for plan_list_num in range(0, plans_len):
        driver.execute_script(f"document.getElementsByClassName('detail-list')[{plan_list_num}].setAttribute('style', 'display: table;')")
    
    # 요금제 전체 테이블
    plan_list = driver.find_elements(By.XPATH, '//div[@class="plan-list-area"]/table')
 
    for plans in plan_list:
        # 요금제 명
        if plans.get_attribute("class") == "plan-list":
            plan_name = plans.find_element(By.XPATH, 'tbody/tr/th/strong').text

        # 상세 요금제
        elif plans.get_attribute("class") == "detail-list":
            # 상세 요금제 목록
            for details in plans.find_elements(By.XPATH, 'tbody/tr'):
                detail_name = details.find_element(By.XPATH, 'th[@class="title"]').text # 상세 요금제 명
                detail_charge = details.find_element(By.XPATH, 'td[@class="charge"]/strong').text # 상세 요금제 가격
                code = details.find_element(By.XPATH, 'td[@class="btns"]/a[@class="btn regular is-line-navygray"]').get_attribute('id') # 상세 요금제 코드

                if network == "5G":
                    writer.writerow(["5G", plan_name, detail_name, detail_charge, code])
                elif network == "LTE":
                    writer.writerow(["LTE", plan_name, detail_name, detail_charge, code])

## 5G 요금제 크롤링
crawling("5G")

## LTE 요금제 크롤링
# 스크롤 최상단으로 이동 후 LTE탭 클릭
driver.execute_script("window.scrollTo(0, 0)")
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="2"]/a/span'))).click()
crawling("LTE")

driver.quit()