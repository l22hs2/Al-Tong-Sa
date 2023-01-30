from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv

filename = "csv\SKT_plan.csv"
file = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(file)

title = ["network", "plan", "name", "charge", "code"]
writer.writerow(title)

# selenium for open Chrome
driver = webdriver.Chrome()

# 페이지 열기
driver.get("http://www.tworld.co.kr/normal.do?serviceId=S_MSA_0012&viewId=V_PROD7001&idxCtgCd=F01100")
time.sleep(4)

def crawling(network):

    ## 망 선택 (필터 설정)
    # 조건 설정 창 열기
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="prdFilter_lay fRight"]/a'))).click()

    # 기기 선택 - 5G
    if network == "5G":
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="optsItem"]/ul/li[1]/span'))).click()
    # 기기 선택 - LTE
    elif network == "LTE":
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="btnBox"]/button'))).click() # 필터 초기회
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="optsItem"]/ul/li[2]/span'))).click()
    
    # 조건 적용
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//button[@id="getProdList"]'))).click()


    # 요금제 페이지 수 측정
    pages = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="pager"]/a')))
    total = int(pages[-3].text) # 마지막 페이지의 숫자 확인 == 총 페이지 수 (-3 : 필요없는 a태그 제외)

    # 1 페이지 ~ 마지막 페이지 까지 반복
    for page in range(1, total + 1): 
        # 요금제 전체 테이블
        plan_list = driver.find_elements(By.XPATH, '//div[@class="result_view"]/table/tbody/tr')
        
        # 현 페이지의 요금제 수 만큼 반복
        for plan in plan_list:
            plan_info = plan.find_element(By.XPATH, 'td/span/a')
            plan_name = plan_info.text
            plan_charge = plan.find_element(By.XPATH, 'td[@class="fee on"]').text
            plan_charge = plan_charge.rstrip("원")
            plan_code = plan_info.get_attribute('href')[-17:-7] # 코드 부분만 추출

            writer.writerow([network, "", plan_name, plan_charge, plan_code])

        # 현재 페이지가 마지막 페이지가 아니면
        if page != total:
            # 다음 페이지로 이동
            driver.execute_script(f"movePage({page + 1});") # 현재 페이지 + 1

## 5G 크롤링
crawling("5G")

## LTE 크롤링
crawling("LTE")

# 창 닫기
driver.close()