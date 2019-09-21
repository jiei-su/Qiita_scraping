## スクレイピング
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import deque
from log import logger
import dbaccess
import chromedriver_binary
import re
import time

# Headlessモード
opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
drv = webdriver.Chrome('./vendor/chromedriver', options=opts)

def collect():
    db = dbaccess.ScrapingData()
    today_times = ['seconds ago', 'minutes ago', 'hour ago', 'hours ago']
    today_articles = []
    page_count = 1

    while True:
        drv.get('https://qiita.com/tags/python?page=%d' % page_count)
        time.sleep(2)

        # 記事取得
        time_htmls = drv.find_elements_by_class_name('tsf-ArticleBody_time')
        value_htmls = drv.find_elements_by_class_name('tsf-ArticleBody_title')
        articles = deque([
            (re.sub(r'[0-9]+ ', '', time.get_attribute("textContent")),
             val.get_attribute("textContent"),
             val.get_attribute("href"))
            for time, val in zip(time_htmls, value_htmls)
            ])

        # 当日の記事判定
        loop_break = False
        for article in articles:
            if article[0] in today_times:
                today_articles.extend([(article[1],article[2])])
            else:
                logger.info("Not found! today's article")
                loop_break = True
                break
        if loop_break:
            break
        page_count += 1
    drv.close()

    db.insert_excel(today_articles)
    logger.info("Finish!")

if __name__ == "__main__":
    collect()
