"""
1. ngambil data website secara otomatis
2. data judul produk, harga, variasi produk dkk
3. 2 tahapn utama, akses html/page source/websitenya di python dan ngelakuin scrapingnya
4a. requests, httpx, curl_cffi dan masih banyak lagi, itu ngatasin error kode ketika akses sebuah website
4b. untuk ngelakuin scrapingnya, itu aku pake beautifulsoup
4c. alat buat nyimpan hasilnya, biasa xlsx, itu pandas
5. scrapy

note
solusi ngatasin forbidden 
1. pakai rotating proxies
2. rotating headers
3. rotating premium proxies 

website :
https://books.toscrape.com/
"""

from bs4 import BeautifulSoup
import requests


def get_request(url):
    r = requests.get(url)
    if r.status_code == 200:
        html = r.content
        return (html, True)
    else:
        html = None
        return (html, False)


def get_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup


"""

1. kumpulin urls per produk satu persatu
2. ngeloop perporduk

Keyword arguments:
argument -- description
Return: return_description
"""


def get_max_page(soup: BeautifulSoup):
    max_page = soup.find("li", class_="current").get_text()
    fix_page = max_page.strip()
    final_page = fix_page.replace("Page 1 of ", "")
    return int(final_page)


if __name__ == "__main__":
    base_url = "https://books.toscrape.com/"
    html, isAccessible = get_request(base_url)
    soup = get_soup(html)
    max_page = get_max_page(soup)
    urls = []
    for page in range(1, 2):  # range(49, max_page + 1):
        modified_url = f"{base_url}catalogue/page-{page}.html"
        print(f"accessing page {modified_url}")
        html, isAccessible = get_request(modified_url)
        soup = get_soup(html)
        cards: list[BeautifulSoup] = soup.find_all(
            "li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"
        )
        for i in cards:
            url = i.find("a")["href"]
            fix_url = f"https://books.toscrape.com/catalogue/{url}"
            urls.append(fix_url)
    for url in urls:
        print(f"accessing page {url}")
        html, isAccessible = get_request(url)
        if isAccessible == True:
            soup = get_soup(html)
            title = soup.find("div", class_="col-sm-6 product_main")
            fix_title = title.find("h1").get_text()
            print(fix_title)
