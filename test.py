#네이버 들어가기 -> 검색어 입력 -> 파워링크 더보기 클릭 -> 요소 찾기 -> 검색어 재입력
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os, sys, time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def getData():
    df = pd.read_excel("키워드 목록 20210621 1646.xlsx")
    keywordList = df["키워드"]
    return keywordList

def process(keywordList):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path = "C:/Users/user/Desktop/파워링크 관리/chromedriver.exe", options=options)
    driver.maximize_window()
    # first tab
    driver.get("https://ad.search.naver.com/search.naver?where=ad&query=&x=24&y=20")

    host = "http://www.yongpt.com"

    for i in range(0, len(keywordList)):
        search = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/form/fieldset/div[1]/span/input[2]")
        btn = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/form/fieldset/input")
        search.send_keys(keywordList[i])
        btn.click()
        time.sleep(1) #화면 넘어갈 때 안넣어주면 에러 발생함.

        pagelen = driver.find_element_by_class_name("paginate")
        if len(pagelen.text) < 13:
            driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/form/fieldset/div[1]/span/input[2]").clear()
            continue
        
        flag = 0
        for j in range(1, 3):
            urlList = driver.find_elements_by_class_name("url")
            for link in urlList:
                if link.text == host:
                    flag = 1
                    break
            #페이지 넘기기. 3페이지 미만 나오는 경우 예외처리.
            driver.find_element_by_class_name("next").click()
            time.sleep(1)

        if flag == 0:
            print("3페이지 이내에 없음.")

        driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/form/fieldset/div[1]/span/input[2]").clear()
        
process(getData())


