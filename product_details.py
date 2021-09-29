from bs4 import BeautifulSoup
import requests

import csv

from product_search import get_urls

import random

base_url = "https://www.domko.com"

links = get_urls()

products = []

for link in links:
    product_url = base_url + link

    result = requests.get(product_url)
    doc = BeautifulSoup(result.text, "html.parser")

    product_info = doc.find("div", id="product-information")

    title = product_info.h2.text

    product_number = product_info.find("p", class_="pr-code").span.text

    collection = product_info.find("p", class_="collection").a.text

    price = product_info.h3.span.text

    # category = doc.find("div", id="breadcrumbs").find_all("a")[-2].text

    image_url = doc.find("div", id="product-details-image").find("img").get("src")
    image = base_url + str(image_url)

    all_a = product_info.find_all("p", class_="collection")
    brand = ""

    for a in all_a:
        if "Марка" in a.text:
            brand = a.text.split(":")[-1].strip(" ")

    # if brand == "":
    #     category = doc.find("div", id="breadcrumbs").find_all("a")[-1].text

    sizes = ""
    sustav = ""
    colors = ""
    vid = ""
    tip = ""
    prednaznachenie = ""

    product_form = product_info.find("form")

    def get_options(category, options):
        for i in options[1:]:
            category += (i.text).join(" ,").strip()
        return category


    if product_form.find("select", id="razmer"):
        size_options = list(product_form.find("select", id="razmer").children)
        sizes = get_options(sizes, size_options)

    if product_form.find("select", id="sastav"):
        sustav_options = list(product_form.find("select", id="sastav").children)
        sustav = get_options(sustav, sustav_options)

    if product_form.find("select", id="tsvyat"):
        color_options = list(product_form.find("select", id="tsvyat").children)
        colors = get_options(colors, color_options)

    if product_form.find("select", id="vid"):
        vid_options = list(product_form.find("select", id="vid").children)
        vid = get_options(vid, vid_options)

    if product_form.find("select", id="tip"):
        tip_options = list(product_form.find("select", id="tip").children)
        tip = get_options(tip, tip_options)

    if product_form.find("select", id="prednaznachenie"):
        prednaznachenie_options = list(product_form.find("select", id="prednaznachenie").children)
        prednaznachenie = get_options(prednaznachenie, prednaznachenie_options)

    opisanie = doc.find("div", id="product-text").text.strip()

    product = [title, product_number, collection, brand, price, sizes,
               sustav, colors, vid, tip, prednaznachenie, image, opisanie]

    products.append(product)


def randint(min=0, max=10000):
    return random.randint(min, max)


with open(f"{randint()}.csv", "w", newline="") as f:

    the_writer = csv.writer(f)

    fieldnames = ["Име", "Номер", "Колекция", "Марка", "Цена", "Размери",
                  "Състав", "Цвят", "Вид", "Тип", "Предназначение", "Снимка", "Описание"]
    the_writer.writerow(fieldnames)

    for product in products:
        the_writer.writerow(product)

print("Finished!")

# взима само основната снимка
# не взима намалени цени
# може да обърка категорията!!!
# различните продукти имат различно описание!
