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

    print(categ)
    name["name"] = re.findall(regex_pattern,str(categ))[0]
    name["link"] = (url + categ.get("href"))#.replace("index.html","page-1.html")

    all_categorys.append(name)

currency = {"$":{"name":"dollar", "code":"USD"},
"€":{"name":"euro", "code":"EUR"},
"£":{"name":"british pound", "code":"GBP"},
"¥":{"name":"yuan", "code":"JPY"},
"₽":{"name":"ruble", "code":"RUB"}}

dict_full_book = {}

for category in all_categorys:
    name,link = category.values()

    page_url = link.split("/")[-1]
    page_url_clear =  link.replace(link.split("/")[-1],"")

    end_url = page_url.split(".")[-1]
    # full_page = page_url.split(".")[0].split("-")
    #
    # page = int(full_page[-1])
    #
    # full_page = f"{full_page[0]}-{page}"
    # full_end_url = f"{full_page}.{end_url}"
    #
    # full_url = f"{page_url_clear}{full_end_url}"
    # print(full_url)

    categ_response = session.get(link, headers=headers)
    categ_soup = BeautifulSoup(categ_response.text, features="html.parser")

    books = categ_soup.find_all("article", {"class": "product_pod"})

    for book in books:
        all_full_book_info = {}

        base_book = book.find("h3")
        title = base_book.find('a')["title"]
        link = f'{base_book.find("a").get("href")}'
        link = f"{url}catalogue/"+link.replace("../","")

        price_book = book.find("div",{"class":"product_price"})
        price = price_book.find('p',{'class':'price_color'}).getText()[1:]

        for i in currency.keys():
            if i in price:
                price = {"price":float(price.replace(i, "")),"currency": {"name":currency.get(i).get("name"),"code":currency.get(i).get("code")}}


        book_response = session.get(link, headers=headers)
        book_soup = BeautifulSoup(book_response.text, features="html.parser")

        info_book = book_soup.find_all("table",{"class":"table"})
        for inf_bok in info_book:
            for ibk in inf_bok.find_all("td"):
                if "In stock" in ibk.getText():
                    availability = int(re.search("\\(([0-9]+) ",ibk.getText())[1])

        find_description_in_book = book_soup.find_all("p")
        for p_find in find_description_in_book:
            if "...more" in p_find.getText():
                description_book = p_find.getText()


        all_full_book_info["category"] = name
        all_full_book_info["title"] = title
        all_full_book_info["link"] = link
        all_full_book_info["price"] = price.get("price")
        all_full_book_info["currency"] = price.get("currency").get("code")
        all_full_book_info["availability"] = availability if availability else ""
        all_full_book_info["description"] = description_book if description_book else ""
        all_full_book_info["id"] = int(re.search("([0-9]+)/index.html",link)[1])

    print(category)
    print(all_full_book_info.get("category"))
    dict_full_book[all_full_book_info.get("id")] = {"category": all_full_book_info["category"],
                                                    "title": all_full_book_info["title"],
                                                    "link": all_full_book_info["link"],
                                                    "description": all_full_book_info["description"],
                                                    "availability": all_full_book_info["availability"],
                                                    "price": all_full_book_info["price"],
                                                    "currency": all_full_book_info["currency"]}
