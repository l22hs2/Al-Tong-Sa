from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import csv
import re

writer = csv.writer(open("csv\SKT_plan_support.csv", "w", encoding="utf-8-sig", newline=""))
writer.writerow(["network", "plan", "name", "charge", "code"])

select = csv.writer(open("csv\SKT_select.csv", "w", encoding="utf-8-sig", newline=""))
select.writerow(["plan", "call", "amount", "charge", "code"])

others = {
    "band 데이터 6.5G",
    "표준요금제",
    "LTE 복지210+",
    "LTE 복지150+",
    "손누리 4.5G",
    "손누리 3.0G",
    "손누리 1.5G",
    "소리누리 3.0G",
    "소리누리 2.0G",
    "소리누리 1.0G",
    "뉴실버요금제"
}

# selenium for open Chrome
options = webdriver.ChromeOptions()
options.add_argument("--incognito") # 시크릿 모드
options.add_experimental_option("detach", True) # 브라우저 자동 종료 방지
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# 페이지 열기
driver.get("https://shop.tworld.co.kr/notice?modelNwType=5G&saleMonth=24&saleYn=Y")

def crawling(network):
    isSelect = False

    # 요금제 선택 창 열기
    open = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//button[@id="select-fee"]')))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", open)
    open.click()

    # 크롤링 탭 전환
    driver.switch_to.window(driver.window_handles[-1])

    # 요금제 탭 리스트
    plan_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@id="subscriptionCategory"]/li')))

    for num, plans in enumerate(plan_list):
        if num != 0:
            plans.click() # 요금제 탭 클릭
        driver.implicitly_wait(10)

        # 요금제 제목
        plan_name = plans.find_element(By.XPATH, 'a').text
        plan_name = plan_name.lstrip("#")

        if plan_name == "기타 요금제":
            isSelect = True
        
        # 요금제 리스트
        details_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@id="subscriptionList"]/li')))

        for details in details_list:
            detail_name = details.find_element(By.XPATH, 'div/div/div/div/span').text
            detail_charge = details.find_element(By.XPATH, 'div/span/div/span[@class="num"]').text
            detail_code = details.get_attribute('data-subscription-id')

            if isSelect:
                if "뉴 T끼리 맞춤형" in detail_name:
                    call_p = re.compile("\d{3}분")
                    data_p = re.compile("[0-9.]{1,3}(GB|MB)")
                    call = call_p.search(detail_name).group()
                    data = data_p.search(detail_name).group()

                    select.writerow(["뉴 T끼리 맞춤형", call, data, detail_charge, detail_code])
                    continue
                elif not detail_name in others:
                    continue

            writer.writerow([network, plan_name, detail_name, detail_charge, detail_code])

    driver.close()

crawling("5G")

## LTE 크롤링
driver.switch_to.window(driver.window_handles[0]) # 메인 창으로 복귀
driver.find_element(By.XPATH, '//li[@data-model="PHONE"]').click()
crawling("LTE")

# 메인 창 닫기
driver.switch_to.window(driver.window_handles[0])
driver.quit()


