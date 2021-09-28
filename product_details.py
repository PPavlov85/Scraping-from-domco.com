from bs4 import BeautifulSoup
import requests

from product_search import get_urls

base_url = "https://www.domko.com"

links = get_urls()

for link in links:
    product_url = base_url + link

    result = requests.get(product_url)
    doc = BeautifulSoup(result.text, "html.parser")

    image_url = doc.find("div", id="product-details-image").find("img").get("src")
    image = base_url + str(image_url)

    category = doc.find("div", id="breadcrumbs").find_all("a")[-2].text

    product_info = doc.find("div", id="product-information")

    title = product_info.h2.text
    price = product_info.h3.span.text
    product_number = product_info.find("p", class_="pr-code").span.text
    collection = product_info.find("p", class_="collection").a.text

    all_a = product_info.find_all("p", class_="collection")
    brand = ""

    for a in all_a:
        if "Марка" in a.text:
            brand = a.text.split(":")[-1].strip(" ")

    if brand == "":
        category = doc.find("div", id="breadcrumbs").find_all("a")[-1].text

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

    print(image)
    # print(category)
    print(title)
    print(price)
    print(product_number)
    print(collection)
    print(brand)
    print(sizes)
    print(sustav)
    print(colors)
    print(vid)
    print(tip)
    print(prednaznachenie)
    print(opisanie)

# взима само основната снимка
# не взима намалени цени
# може да обърка категорията!!!
