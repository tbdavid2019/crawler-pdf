
PDF Crawler for tcdares.gov.tw

This project is a Python-based web crawler designed to collect and download PDF files from the tcdares.gov.tw domain and its subdomains. The crawler recursively scans the specified URL, collects PDF links, and saves them locally in a specified directory.

Features

	•	Crawls and downloads only PDF files within the tcdares.gov.tw domain and its subdomains.
	•	Saves a list of collected PDF URLs in pdf_list.txt before downloading.
	•	Skips duplicate downloads if the file already exists locally.
	•	Allows control over crawling depth and domain filtering.

PDF 爬蟲 for tcdares.gov.tw

這是一個基於 Python 的網頁爬蟲專案，用於從 tcdares.gov.tw 網域及其子網域中收集並下載 PDF 文件。爬蟲會遞迴地掃描指定的 URL，收集 PDF 連結並將其本地儲存。

功能特色

	•	僅爬取並下載 tcdares.gov.tw 網域及其子網域中的 PDF 文件。
	•	在下載前將所有收集到的 PDF 連結儲存在 pdf_list.txt 中。
	•	若本地已存在相同檔案，則跳過重複下載。
	•	允許控制爬取深度及網域篩選。

Requirements / 環境需求

	•	Python 3.x
	•	需要安裝的 Python 套件：
	•	requests
	•	beautifulsoup4

Installation / 安裝

	1.	Clone the repository / 複製專案庫:

git clone https://github.com/yourusername/pdf-crawler.git
cd pdf-crawler


	2.	Install dependencies / 安裝依賴套件:
```
pip install -r requirements.txt
```
Alternatively, you can manually install the required packages:
或者您可以手動安裝所需套件：
```
pip install requests beautifulsoup4

```

Usage / 使用方法

	1.	Edit the base URL / 編輯起始 URL：在 crawler.py 文件中設定爬取的起始 URL。
```
base_url = "https://www.tcdares.gov.tw/ws.php?id=11"
```

	2.	Run the script / 執行程式:
```
python crawler.py
```
This will start the crawler, collect all PDF links within the specified domain and its subdomains, and save the links in pdf_list.txt. After collecting, it will download each PDF into the pdf_downloads folder.
程式將啟動爬蟲，收集指定網域及其子網域中的所有 PDF 連結，並將連結儲存在 pdf_list.txt 中。收集完成後，程式會將每個 PDF 下載至 pdf_downloads 資料夾中。

	3.	PDF List Output / PDF 清單輸出：所有找到的 PDF 連結都會儲存在 pdf_list.txt 文件中，方便檢查。

Code Structure / 程式結構

	•	crawler.py：主要的爬蟲腳本。
	•	pdf_downloads/：下載的 PDF 文件儲存目錄。
	•	pdf_list.txt：存放所有收集到的 PDF 連結。

Configuration / 配置

	•	Crawling Depth / 爬取深度：爬取的最大深度預設為 5。您可以在 crawl_and_collect 函數中修改此值：
```
if depth > 5 or url in visited_urls:
    return
```

	•	Allowed Domain / 許可網域：爬蟲限制在 tcdares.gov.tw 網域及其子網域。您可以根據需要在 allowed_domain_suffix 變數中修改此值。

allowed_domain_suffix = "tcdares.gov.tw"



Example Output / 範例輸出

```
PDF Files to Download:
https://www.tcdares.gov.tw/upload/tcdares/files/web_structure/13142/file1.pdf
https://www.tcdares.gov.tw/upload/tcdares/files/web_structure/13143/file2.pdf
...

Downloaded: pdf_downloads/file1.pdf
Downloaded: pdf_downloads/file2.pdf
```

Notes / 注意事項

	•	SSL Warnings / SSL 警告：此程式禁用了 SSL 警告，以允許未驗證的 HTTPS 請求。啟用此功能時請謹慎。
	•	Duplicate Checking / 重複檢查：爬蟲會透過 downloaded_urls 集合來避免重複下載相同的文件。

