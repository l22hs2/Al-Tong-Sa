from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import csv
import re

# writer = csv.writer(open("csv\LG_select.csv", "w", encoding="utf-8-sig", newline=""))
# title = ["plan", "call", "amount", "charge", "code"]
# writer.writerow(title)


options = webdriver.ChromeOptions()
options.add_argument("--incognito") # 시크릿 모드
options.add_experimental_option("detach", True) # 브라우저 자동 종료 방지
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 페이지 열기
driver.get("https://www.lguplus.com/plan/mplan/lte-all/lte-general/ST00001")

plan_tab = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="accordion c-accordion accord-short-title"]/div[2]/div/div')))
# plan_tab.click()
driver.execute_script("arguments[0].click();", plan_tab) # 펼치기

# # 전체 테이블
# table = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="prdtview_inner"]/div')))
# normal = table[0] # 선택형
# msg    = table[1] # 문자
# within = table[2] # 선택형 망내

# def crawling(plan, type):
#     thead = plan.find_elements(By.XPATH, 'div[@class="tblType list txtR hidden-xs"]/table/thead/tr/th')
#     tbody = plan.find_elements(By.XPATH, 'div[@class="tblType list txtR hidden-xs"]/table/tbody/tr')

#     datas = []

#     for data in thead:
#         datas.append(data.text)

#     for calls in tbody:
#         for num, call in enumerate(calls.find_elements(By.XPATH, 'td')):
#             if num == 0:
#                 amount = call.text
#                 continue
            
#             charge = re.sub(",|원", "", call.text) # 문구 제거

#             writer.writerow([type, amount, datas[num], charge])
        
# crawling(normal, "LTE 선택형")
# crawling(within, "LTE 선택형 망내기본")

# ## 문자
# writer.writerow(["문자", "", "미선택", 0])

# thead = msg.find_elements(By.XPATH, 'div[@class="tblType list txtR hidden-xs mt5"]/table/thead/tr/th')
# tbody = msg.find_elements(By.XPATH, 'div[@class="tblType list txtR hidden-xs mt5"]/table/tbody/tr')

# datas = []

# for data in thead:
#     datas.append(data.text)

# for calls in tbody:
#     for num, call in enumerate(calls.find_elements(By.XPATH, 'td')):
#         if num == 0:
#             amount = call.text
#             continue
        
#         charge = re.sub(",|원", "", call.text) # 문구 제거

#         writer.writerow(["문자", "", datas[num], charge])

# driver.quit()