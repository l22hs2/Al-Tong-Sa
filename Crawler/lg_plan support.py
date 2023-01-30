from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
import csv
import re

writer = csv.writer(open("csv\LG_plan_support.csv", "w", encoding="utf-8-sig", newline=""))
title = ["network", "plan", "name", "charge", "code"]
writer.writerow(title)

# selenium to open Chrome
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# driver = webdriver.Chrome(chrome_options=options)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 페이지 열기
driver.get("https://www.lguplus.com/mobile/financing-model")

# 오류 방지
while True:
    try: # 에러 발생 시 새로고침
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, '//button[@id="_uid_232"]')
        driver.refresh()
    except: break # 에러 미 발생 시 새로고침 탈출

# 더 많은 요금제 보기
def crawling(network):
    driver.find_element(By.XPATH, '//button[@class="c-btn-rect-2"]').click()

    sections = driver.find_elements(By.XPATH, '//div[@class="c-body-content"]/div') # 요금제 목록
    for section in sections:
        title = section.find_element(By.XPATH, 'h2').text
        names = section.find_elements(By.XPATH, 'div/ul/li')

        for name in names:
            code = name.find_element(By.XPATH, 'span/input').get_attribute('value')
            name = name.text
            writer.writerow([network, title, name, "", code])


crawling("5G")

driver.find_element(By.XPATH, '//*[@id="__BVID__297___BV_modal_header_"]/button').click() # 요금제 창 닫기
driver.implicitly_wait(10)
driver.find_element(By.XPATH, '//div[@class="round-box half-box"]/dl[1]/dd[1]/span[2]/input').click() # LTE탭 선택
driver.implicitly_wait(10)
crawling("LTE")

# agent = driver.execute_script('return navigator.userAgent')
# print(agent)

# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="btn-area"]/a'))).click()


# def crawling(network):
#     # 요금제 선택 창 열기
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//dd[@class="rate-plan"]'))).click()

#     if network == "5G":
#         plans_list = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="tpPP00"]/div')))
#     else:
#         plans_list = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="tpPP01"]/div')))

#     # 요금제 전체 리스트 > title 별로 분류, title 개수 만큼
#     for plan_list in plans_list:
#         title = plan_list.find_element(By.XPATH, 'p').text
#         plans = plan_list.find_elements(By.XPATH, 'div//div[@class="cell"]/span/label')
#         for plan in plans:
#             name = plan.text
#             code = plan.get_attribute('for')[-10:]

#             # 선택형 요금제 분류
#             if (network == "LTE") and (title == "LTE 선택형 요금제"):
#                 if (name.startswith("LTE 선택형 망내")) or name.startswith("LTE 선택형 음성"):
#                     writer.writerow([network, "LTE 선택형 망내", name, "", code])
#                 else:
#                     writer.writerow([network, "LTE 선택형", name, "", code])
#             else:
#                 writer.writerow([network, title, name, "", code])


# crawling("5G")

# driver.find_element(By.XPATH, '//div[@class="btn_close"]').click()      # 요금제 창 닫기
# driver.find_element(By.XPATH, '//label[@for="fn_rd_type01"]').click()   # 기기종류 LTE 선택
# crawling("LTE")

# driver.quit()

# time.sleep(10)