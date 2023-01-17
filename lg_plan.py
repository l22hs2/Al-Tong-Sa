from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import re

writer = csv.writer(open("LG_plan.csv", "w", encoding="utf-8-sig", newline=""))
title = ["network", "plan", "name", "charge", "code"]
writer.writerow(title)

# selenium to open Chrome
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome()

# 페이지 열기
driver.get("https://www.uplus.co.kr/ent/spps/chrg/RetrieveChrgList.hpi?catgCd=All&mid=11014")
time.sleep(1)

def crawling(network):
    # time.sleep(0.5)

    # 페이지 수 계산 (잔여 페이지 + 1)
    page_num = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="number"]/a')))
    lastPage = len(page_num) + 1

    # 페이지 수 만큼 반복
    for nowPage in range(1, lastPage + 1):
        # 요금제 전체 테이블
        plan_list = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="prodSvcList-item"]')))

        # 페이지의 요금제 수 만큼 반복
        for plans in plan_list:
            name = plans.find_element(By.XPATH, 'div//h3[@class="titLevel02"]').text # 요금제 명
            charge = plans.find_element(By.XPATH, 'div//div[@class="prodSvcList-price"]/p/strong').text # 요금제 가격
            charge = re.sub("월|원", "", charge) # 문구 제거
            code = plans.find_element(By.XPATH, 'div//div[@class="prodSvcList-btn"]/a').get_attribute("href")[28:38] # 요금제 코드
            writer.writerow([network, "", name, charge, code])

        # 마지막 페이지가 아니면
        if nowPage != lastPage:
            # 다음 페이지로 이동
            driver.find_element(By.XPATH, f'//*[@id="svcForm"]/div[2]/div[1]/div/div/span[3]/a[{nowPage}]').click()
            # time.sleep(0.5)

## LTE
crawling("LTE")

## 5G
# 5G 탭으로 이동
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="select_wrap1"]/a'))).click()          # 드랍박스 오픈
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="select_wrap1"]/ul/li[2]'))).click()   # "5G폰" 선택
WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchListBtn"]'))).click()           # "검색하기" 버튼 클릭

crawling("5G")

driver.quit()