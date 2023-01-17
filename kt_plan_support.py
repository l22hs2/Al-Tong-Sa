from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import re

writer = csv.writer(open("KT_plan_support.csv", "w", encoding="utf-8-sig", newline=""))
writer.writerow(["network", "plan", "name", "charge", "code"])

select = csv.writer(open("KT_select.csv", "w", encoding="utf-8-sig", newline=""))
select.writerow(["plan", "call", "amount", "charge", "code"])

# selenium to open Chrome
driver = webdriver.Chrome()

# 페이지 열기
driver.get("https://shop.kt.com/smart/supportAmtList.do")

# 크롤링 함수
def crawling(network):
    isSelect = False

    # 요금제 선택
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="prodPaymentInfo"]/button'))).click()

    # 제목 리스트
    titles = len(WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="prodPaySort"]/div/button'))))

    # num_title = len(titles)
    for num in range(2, titles + 1): # 맨 앞 전체요금제 제외 -> 2부터 시작
        driver.find_element(By.XPATH, f'//div[@id="pplGroupNmList"]/button[{num}]').click() # 크롤링할 요금제 탭 선택

        title = driver.find_element(By.XPATH, f'//div[@id="pplGroupNmList"]/button[{num}]/span').text # 현재(선택된) 요금제 탭 제목

        if (title == "순 선택형(LTE)") or (title == "순 망내무한 선택형(LTE)"):
            isSelect = True
            title = title[:-5]

        plans_list = len(WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="chargeListWrap"]/ul/li'))))

        for i in range(1, plans_list + 1):
            plans = driver.find_element(By.XPATH, f'//div[@class="chargeListWrap"]/ul/li[{i}]')

            name_strong = plans.find_element(By.XPATH, 'div/a/div/strong').text     # 필요한 요금제 명
            name_span = plans.find_element(By.XPATH, 'div/a/div/strong/span').text  # 불필요한 요금제 설명
            name = name_strong.rstrip(name_span) # 불필요 설명 제거
            name = name.rstrip() # 공백 제거

            charge = plans.find_element(By.XPATH, 'div/div/span').text
            charge = charge.strip("월원")

            plans.click() # 요금제 클릭
            driver.find_element(By.XPATH, '//button[@id="btnLayerItem"]').click() # 선택 완료 버튼 클릭
            code = driver.find_element(By.XPATH, '//input[@id="prdcCd"]').get_attribute('value') # 코드 크롤링

            # 선택형 요금제 분리
            if isSelect:
                call_p = re.compile("\d{3}분")
                data_p = re.compile("\d{1,3}(GB|MB)")
                call = call_p.search(name).group()
                data = data_p.search(name).group()

                select.writerow([title, call, data, charge, code])
            else:
                writer.writerow([network, title, name, charge, code])

            driver.find_element(By.XPATH, '//div[@class="prodPaymentInfo"]/button').click() # 다시 요금제 선택 창 열기

        isSelect = False

        # # 마지막 페이지가 아니면
        # if num != titles:
        #     # 다음 요금제 탭 클릭
        #     driver.find_element(By.XPATH, f'//div[@id="pplGroupNmList"]/button[{num + 1}]').click()


## 5G
crawling("5G")

## LTE
time.sleep(1)
driver.find_element(By.XPATH, '//button[@id="btnLayerClose"]').click() # 요금제 창 닫기
time.sleep(0.3)
driver.find_element(By.XPATH, '//div[@class="prodCateWrap support"]/ul/li[2]').click()
crawling("LTE")

driver.quit()
