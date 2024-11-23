import os
import sys
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests

# ---------------------------------
# パラメーター
# ---------------------------------

args = sys.argv
searchUrl = args[0]

# ---------------------------------
# 初期処理
# ---------------------------------

# プロジェクトのルートパスを定義
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# データ保存フォルダのパスを直接指定
dataDir = os.path.join(PROJECT_ROOT, 'data')

if not os.path.exists(dataDir):
    os.makedirs(dataDir)

# ---------------------------------
# 関数定義
# ---------------------------------

def initDriver(pageLoadTimeout=30, waitTime=5):
    """Selenium WebDriverを初期化"""
    try:
        service = EdgeService(EdgeChromiumDriverManager().install())
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        driver = webdriver.Edge(service=service, options=options)
        driver.set_page_load_timeout(pageLoadTimeout)
        return driver, waitTime
    except Exception as e:
        print(f"ドライバーの初期化に失敗しました: {e}")
        return None, None

def waitForPageLoad(driver, timeout=30):
    """ページロードを待機"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        print("ページのロードが完了しました。")
    except Exception as e:
        print(f"ページロード待機中にエラーが発生しました: {e}")

def collectImageLinks(driver, waitTime, url, maxLinks=1000):
    """いらすとやから画像リンクを収集"""
    driver.get(url)
    waitForPageLoad(driver)
    imageLinks = set()

    while len(imageLinks) < maxLinks:
        try:
            time.sleep(waitTime)  # ページの読み込みを待機
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # 画像要素をすべて取得
            images = soup.select("div.boxim a img")
            for img in images:
                imgUrl = img.get('src')
                if imgUrl:
                    imageLinks.add(imgUrl)

            print(f"収集した画像リンク数: {len(imageLinks)}")

            if len(imageLinks) >= maxLinks:
                break

            # 「次のページ」ボタンを探してクリック
            nextButtons = driver.find_elements(By.CSS_SELECTOR, "a.blog-pager-older-link")
            if nextButtons:
                nextButton = nextButtons[0]
                driver.execute_script("arguments[0].click();", nextButton)
                waitForPageLoad(driver)
            else:
                print("これ以上ページがありません。")
                break

        except Exception as e:
            print(f"画像リンク収集中にエラーが発生しました: {e}")
            break

    return list(imageLinks)[:maxLinks]

def downloadImage(url, folderPath):
    """指定されたフォルダに画像をダウンロード"""
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # URLから画像ファイル名を取得
            imageName = url.split('/')[-1].split('?')[0]  # クエリパラメータを除去
            imagePath = os.path.join(folderPath, imageName)
            with open(imagePath, 'wb') as f:
                f.write(response.content)
            print(f"画像をダウンロードしました: {imageName}")
        else:
            print(f"画像のダウンロードに失敗しました: {url}")
    except Exception as e:
        print(f"画像のダウンロード中にエラーが発生しました: {e}")

def removeIllegalCharacters(value):
    """Excelで使用できない文字を削除"""
    if isinstance(value, str):
        return re.sub(r"[\x00-\x1F\x7F]", "", value)
    return value

def main():
    driver, waitTime = initDriver()
    if not driver:
        return

    try:
        print("画像リンクを収集中...")
        imageLinks = collectImageLinks(driver, waitTime, searchUrl, maxLinks=1000)
        print(f"収集した画像リンク数: {len(imageLinks)}")

        # 画像をダウンロード
        if imageLinks:
            for imgUrl in imageLinks:
                downloadImage(imgUrl, dataDir)
        else:
            print("収集した画像リンクがありません。")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
