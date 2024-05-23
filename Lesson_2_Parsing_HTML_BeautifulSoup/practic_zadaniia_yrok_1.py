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

category_info = {}

for category in categorys.find_all("li")[1:]:
    name = category.find("a")
    # print(url + name.get("href"))
    print(re.findall(regex_pattern,str(name))[0])

print()