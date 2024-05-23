import requests
from bs4 import BeautifulSoup, BeautifulSoup as bs
from fake_useragent import UserAgent
from pprint import pprint
import re
# ua = UserAgent()

# Сбор и разметка данных (семинары)
# Урок 2. Парсинг HTML. BeautifulSoup
# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте
# во всех категориях: название, цену, количество товара
# в наличии (In stock (19 available)) в формате integer, описание.
#
# Затем сохранить эту информацию в JSON-файле.



url = "http://books.toscrape.com/"

# https://books.toscrape.com/index.html
# https://books.toscrape.com/catalogue/page-1.html
# https://books.toscrape.com/catalogue/category/books_1/index.html
# https://books.toscrape.com/catalogue/category/books_1/page-1.html




headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'}
page = 1
params = {"catalogue": f"page-{page}"}

session = requests.session()


regex_pattern = r"(\w+ *\w* *\w* *\w*)\n"

response = session.get(url,params=params, headers=headers)
soup = BeautifulSoup(response.text, features="html.parser")

categorys = soup.find_all("div", {"class":"side_categories"})[0]#.find_all("a",{"href":"category/books_1/index.html"})

all_categorys = []

for category in categorys.find_all("li")[1:]:
    name = {}
    categ = category.find("a")
    name["name"] = re.findall(regex_pattern,str(categ))[0]
    name["link"] = (url + categ.get("href")).replace("index.html","page-1.html")

    all_categorys.append(name)


for category in all_categorys:
    name,link = category.values()

    page_url = link.split("/")[-1]
    page_url_clear =  link.replace(link.split("/")[-1],"")

    end_url = page_url.split(".")[-1]
    full_page = page_url.split(".")[0].split("-")

    page = int(full_page[-1])

    full_page = f"{full_page[0]}-{page}"
    full_end_url = f"{full_page}.{end_url}"

    full_url = f"{page_url_clear}{full_end_url}"

    print(full_url)

