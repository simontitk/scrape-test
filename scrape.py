from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import datetime


def get_links(url):
    r = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(r.text, "html.parser")
    links = ["https://thehub.io" + card.find("a").attrs["href"] for card in soup.find_all("div", class_="card card-startup")]
    return links


def parse_url(url):
    r = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.find("h2", class_="startup-header__name").text
    content = soup.find("div", class_="details__text__content").find("div").text
    website = soup.find("tbody", attrs={"data-v-f8328cce":True}).find_all("tr")[1].find_all("td")[1].find("a").attrs["href"]
    employees = soup.find("tbody", attrs={"data-v-f8328cce":True}).find_all("tr")[3].find_all("td")[1].find("b").text
    return name, content, website, employees


if __name__ == "__main__":

    data = []
    i = 1
    total_companies = 0
    t0 = time.time()
    while i < 3:
        print(f"starting iteration number {i}")
        url = f"https://thehub.io/startups?industries=science&stage=goToMarket&stage=growth&location=Capital%20Region%20of%20Denmark,%20D%C3%A1nia&countryCodes=DK&page={i}"
        links = get_links(url)
        
        if not links:
            print(f"breaking at iteration {i}")
            break
        print(f"got page {i}")

        for j, link in enumerate(links):
            data.append(parse_url(link))
            print(f"added company {j+1}")
            total_companies += 1
        i += 1

    t1 = time.time()
    print(f"Processed everything. Total time required: {t1-t0}")



    df = pd.DataFrame(data=data, columns=("Company", "Description", "URL", "Employees"))
    df.to_csv("science_engineering.csv")
    df.to_excel("science_engineering.xlsx", engine="xlsxwriter")

