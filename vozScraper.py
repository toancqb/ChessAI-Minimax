
import requests
from bs4 import BeautifulSoup

ignore_link = "https://2.pik.vn/2019b5ca2c26-179a-459b-84d4-e36c0c139efb.png"
ignore_link2 = "http://www.google.com/+1/button/images/icon.png"

def find_all_img_tag(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all('img', border="0")
    return res

def strncmp(str1,str2,n):
    for i in range(n):
        if i == len(str1) or i == len(str2):
            return True
        if str1[i] != str2[i]:
            return False
    return True

def print_res(res):
    global ignore_link
    for i in res:
        if not strncmp(i["src"], "images", 6) and not strncmp(i["src"], "/images", 7)\
            and not strncmp(i["src"], "custom", 6)\
            and not strncmp(i["src"], ignore_link, len(ignore_link))\
            and not strncmp(i["src"], ignore_link2, len(ignore_link2)):
            if i["src"] == "http://pik.vn/2014e767c8b5-cf61-4b65-9f7f-5213956a3c48.jpeg":
                print(i["src"])
                return True
    return False

def run(url):
    
    res = find_all_img_tag(url)
    print_res(res)

URL = "https://o.voz.vn/showthread.php?t=3793720&page="
for i in range(100, 8000):
    nURL = URL + str(i)
    #nURL = URL.join([str(i)])
    #print(nURL)
    
    if run(nURL):
        print("page",i)
        break