from bs4 import BeautifulSoup
import requests

from product_search import get_urls

base_url = "https://www.domko.com"

links = get_urls()

for link_list in links:
    for link in link_list:
        product_url = base_url + link

        result = requests.get(product_url)
        doc = BeautifulSoup(result.text, "html.parser")

        product_info = doc.find("div", id="product-information")

        image_url = doc.find("div", id="product-details-image").find("img").get("src")
        image = base_url + str(image_url)

        category = doc.find("div", id="breadcrumbs").find_all("a")[-2].text

        title = product_info.h2.text
        price = product_info.h3.span.text
        product_number = product_info.find("p", class_="pr-code").span.text
        collection = product_info.find("p", class_="collection").a.text
        all_a = product_info.find_all("p", class_="collection")
        brand = ""

        for a in all_a:
            if "Марка" in a.text:
                brand = a.text.split(":")[-1].strip(" ")

        product_form = product_info.find("form")

        size_options = list(product_form.find("select", id="razmer").children)
        sustav_options = list(product_form.find("select", id="sastav").children)
        color_options = list(product_form.find("select", id="tsvyat").children)
        vid_options = list(product_form.find("select", id="vid").children)
        tip_options = list(product_form.find("select", id="tip").children)
        prednaznachenie_options = list(product_form.find("select", id="prednaznachenie").children)

        sizes = ""
        sustav = ""
        colors = ""
        vid = ""
        tip = ""
        prednaznachenie = ""


        def get_options(category, options):
            for i in options[1:]:
                category += (i.text).join(" ,").strip()
            return category


        sizes = get_options(sizes, size_options)
        sustav = get_options(sustav, sustav_options)
        colors = get_options(colors, color_options)
        vid = get_options(vid, vid_options)
        tip = get_options(tip, tip_options)
        prednaznachenie = get_options(prednaznachenie, prednaznachenie_options)

        opisanie = doc.find("div", id="product-text").text.strip()

        print(image)
        print(category)
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
