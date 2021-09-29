from bs4 import BeautifulSoup
import requests

print("Какво търсиш?")
product_search = input()
print("Loading ...")


def get_urls():
    url = f"https://www.domko.com/search/page=1/{product_search}/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # category = doc.find("div", id="breadcrumbs").find_all("li")[-1].text
    links = []

    if doc.find("div", id="pagination").a:
        pages_count = int(doc.find("div", id="pagination").find_all("a")[-2].text)

        for page in range(1, pages_count + 1):
            url = f"https://www.domko.com/search/page={page}/{product_search}/"
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")

            div = doc.find(id="product-listing")

            for a in div.find_all('a', href=True):
                links.append(a.get('href'))

        return links

    else:
        div = doc.find(id="product-listing")

        for a in div.find_all('a', href=True):
            links.append(a.get('href'))

    return links
