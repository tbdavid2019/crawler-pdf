import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse
import time
import urllib3
from tqdm import tqdm  # 新增進度條套件

# 禁用不安全請求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://www.tcdares.gov.tw/ws.php?id=11"
allowed_domain_suffix = "tcdares.gov.tw"
download_folder = "/content/data/pdf3"
pdf_list_file = "pdf_list.txt"

os.makedirs(download_folder, exist_ok=True)
visited_urls = set()
pdf_links = set()
downloaded_urls = set()

# 計數器
total_pages_visited = 0
total_pdfs_found = 0
total_pdfs_downloaded = 0

def download_pdf(pdf_url):
    global total_pdfs_downloaded
    
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

    response = requests.get(pdf_url, verify=False, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(file_name, "wb") as file, tqdm(
        desc=original_file_name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)
            
    total_pdfs_downloaded += 1
    downloaded_urls.add(pdf_url)

def crawl_and_collect(url, depth=1):
    global total_pages_visited, total_pdfs_found
    
    if depth > 5 or url in visited_urls:
        return
        
    total_pages_visited += 1
    visited_urls.add(url)
    
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", href=True)
        
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            
            parsed_url = urlparse(full_url)
            if not parsed_url.netloc.endswith(allowed_domain_suffix):
                continue
            
            if full_url.endswith(".pdf") and full_url not in pdf_links:
                pdf_links.add(full_url)
                total_pdfs_found += 1
                print(f"\rFound PDFs: {total_pdfs_found}", end="")
            elif "https" in full_url or "http" in full_url:
                time.sleep(1)
                crawl_and_collect(full_url, depth + 1)
    except Exception as e:
        print(f"\nError crawling {url}: {str(e)}")

print("Starting crawl...")
crawl_and_collect(base_url)
print(f"\n\nCrawl Summary:")
print(f"Total pages visited: {total_pages_visited}")
print(f"Total PDFs found: {total_pdfs_found}")

# 將PDF清單寫入文件
with open(pdf_list_file, "w") as file:
    for pdf_url in pdf_links:
        file.write(pdf_url + "\n")
print(f"\nPDF list saved to {pdf_list_file}")

# 下載PDF文件
print("\nStarting downloads...")
for pdf_url in tqdm(pdf_links, desc="Overall Progress"):
    download_pdf(pdf_url)

print(f"\nDownload Summary:")
print(f"Total PDFs downloaded: {total_pdfs_downloaded}")
