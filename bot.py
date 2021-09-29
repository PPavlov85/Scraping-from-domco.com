from bs4 import BeautifulSoup

import requests
import csv
import random


def randint(min=0, max=10000):
    return random.randint(min, max)


try:
    base_url = "https://www.domko.com"

    products = []
    links = []

    print("Какво търсиш?")
    product_search = input()
    print("Зарежда ...")

    url = f"https://www.domko.com/search/page=1/{product_search}/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # category = doc.find("div", id="breadcrumbs").find_all("li")[-1].text

    div = doc.find(id="product-listing")

    for a in div.find_all('a', href=True):
        links.append(a.get('href'))

    if doc.find("div", id="pagination").a:
        pages_count = int(doc.find("div", id="pagination").find_all("a")[-2].text)

        for page in range(2, pages_count + 1):
            url = f"https://www.domko.com/search/page={page}/{product_search}/"
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")

            div = doc.find(id="product-listing")

            for a in div.find_all('a', href=True):
                links.append(a.get('href'))

    for link in links:

        size = ""
        created = ""
        color = ""
        kind = ""
        type_p = ""
        purpose = ""
        brand = ""

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

        for a in all_a:
            if "Марка" in a.text:
                brand = a.text.split(":")[-1].strip(" ")

        # if brand == "":
        #     category = doc.find("div", id="breadcrumbs").find_all("a")[-1].text

        product_form = product_info.find("form")

        def get_options(category, options):
            for i in options[1:]:
                category += (i.text).join(" ,").strip()
            return category


        if product_form.find("select", id="razmer"):
            size_options = list(product_form.find("select", id="razmer").children)
            size = get_options(size, size_options)

        if product_form.find("select", id="sastav"):
            created_options = list(product_form.find("select", id="sastav").children)
            created = get_options(created, created_options)

        if product_form.find("select", id="tsvyat"):
            color_options = list(product_form.find("select", id="tsvyat").children)
            color = get_options(color, color_options)

        if product_form.find("select", id="vid"):
            kind_options = list(product_form.find("select", id="vid").children)
            kind = get_options(kind, kind_options)

        if product_form.find("select", id="tip"):
            type_p_options = list(product_form.find("select", id="tip").children)
            type_p = get_options(type_p, type_p_options)

        if product_form.find("select", id="prednaznachenie"):
            purpose_options = list(product_form.find("select", id="prednaznachenie").children)
            purpose = get_options(purpose, purpose_options)

        description = doc.find("div", id="product-text").text.strip()

        product = [title, product_number, collection, brand, price, size,
                   created, color, kind, type_p, purpose, image, description]

        products.append(product)

    with open(f"{product_search}{randint()}.csv", "w", newline="") as f:

        the_writer = csv.writer(f)

        fieldnames = ["Име", "Номер", "Колекция", "Марка", "Цена", "Размери",
                      "Състав", "Цвят", "Вид", "Тип", "Предназначение", "Снимка", "Описание"]

        the_writer.writerow(fieldnames)

        for product in products:
            the_writer.writerow(product)

    print("Готово!")


except Exception:
    print("Грешка ... опитай пак!")

# взима само основната снимка
# не взима намалени цени
# може да обърка категорията!!!
# различните продукти имат различно описание!
