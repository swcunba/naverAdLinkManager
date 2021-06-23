from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os, sys, time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def sendMail(result):
    now = datetime.now()
    cur = ("%s-%s-%s %s시" %(now.year, now.month, now.day, now.hour))
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.login("메일주소", "앱 비밀번호")

    if len(result) == 0:
        msg = MIMEText("모든 키워드가 3페이지 이내에 존재합니다.")
    else:
        contents = result[0]
        for i in range(1, len(result)):
            contents += '\n' + result[i]
        msg = MIMEText(contents)

    msg["Subject"] = str(cur) + "제목"
    s.sendmail("송신자 이메일", "수신자 이메일", msg.as_string())
    s.quit()


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

    host = "찾고자 하는 파워링크"
    resList = []
    for i in range(0, len(keywordList)):
        search = driver.find_element_by_id("nx_query")
        btn = driver.find_element_by_class_name("btn_srch")
        search.send_keys(keywordList[i])
        btn.click()
        driver.implicitly_wait(1) #화면 넘어갈 때 안넣어주면 에러 발생.

        pagelen = driver.find_element_by_class_name("paginate")
        if len(pagelen.text) < 13:
            driver.find_element_by_id("nx_query").clear()
            continue
        
        flag = 0
        for j in range(1, 3):
            urlList = driver.find_elements_by_class_name("url")
            for link in urlList:
                if link.text == host:
                    flag = 1
                    break
                    
            driver.find_element_by_class_name("next").click()
            driver.implicitly_wait(1)

        if flag == 0:
            resList.append("키워드: " + keywordList[i] + "의 파워링크가 3페이지 이내에 존재하지 않습니다.")

        driver.find_element_by_id("nx_query").clear()

    sendMail(resList)
        
process(getData())
