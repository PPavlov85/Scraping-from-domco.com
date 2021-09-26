from bs4 import BeautifulSoup
import requests

product_search = input("Какво търсиш?")


def get_urls():
    url = f"https://www.domko.com/search/page=1/{product_search}/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    pages_count = int(doc.find("div", id="pagination").find_all("a")[-2].text)
    links = []

    for page in range(1, pages_count + 1):
        url = f"https://www.domko.com/search/page={page}/{product_search}/"
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")

        div = doc.find(id="product-listing")
        links.append([a.get('href') for a in div.find_all('a', href=True)])

    return links
