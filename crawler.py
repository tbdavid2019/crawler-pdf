import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse
import time
import urllib3

# 禁用不安全請求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.tcdares.gov.tw/ws.php?id=11"
allowed_domain_suffix = "tcdares.gov.tw"  # 指定的網域後綴
download_folder = "pdf_downloads"
pdf_list_file = "pdf_list.txt"  # PDF清單文件
os.makedirs(download_folder, exist_ok=True)
visited_urls = set()  # 記錄已訪問的頁面
pdf_links = set()  # 用於存儲所有需要下載的PDF連結
downloaded_urls = set()  # 記錄已下載的PDF URL

def download_pdf(pdf_url):
    if pdf_url in downloaded_urls:
        print(f"Skipping duplicate PDF: {pdf_url}")
        return

    original_file_name = unquote(pdf_url.split("/")[-1])
    file_name = os.path.join(download_folder, original_file_name)
    
    count = 1
    while os.path.exists(file_name):
        name, ext = os.path.splitext(original_file_name)
        file_name = os.path.join(download_folder, f"{name}_{count}{ext}")
        count += 1

    response = requests.get(pdf_url, verify=False)
    with open(file_name, "wb") as file:
        file.write(response.content)
    print(f"Downloaded: {file_name}")
    downloaded_urls.add(pdf_url)  # 將URL加入已下載集合中

def crawl_and_collect(url, depth=1):
    if depth > 5 or url in visited_urls:
        return

    visited_urls.add(url)
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", href=True)
    for link in links:
        href = link['href']
        full_url = urljoin(url, href)
        
        # 確認連結是否屬於指定的網域後綴
        parsed_url = urlparse(full_url)
        if not parsed_url.netloc.endswith(allowed_domain_suffix):
            continue  # 跳過不屬於指定網域後綴的連結
        
        if full_url.endswith(".pdf") and full_url not in pdf_links:
            pdf_links.add(full_url)  # 收集PDF連結而非立即下載
        elif "https" in full_url or "http" in full_url:
            time.sleep(1)
            crawl_and_collect(full_url, depth + 1)

# 開始爬取並收集PDF連結
crawl_and_collect(base_url)

# 將PDF清單寫入文件
with open(pdf_list_file, "w") as file:
    for pdf_url in pdf_links:
        file.write(pdf_url + "\n")
print(f"PDF list saved to {pdf_list_file}")

# 在終端顯示PDF清單
print("PDF Files to Download:")
for pdf_url in pdf_links:
    print(pdf_url)

# 執行下載
for pdf_url in pdf_links:
    download_pdf(pdf_url)
