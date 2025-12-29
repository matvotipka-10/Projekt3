import csv
import requests
from bs4 import BeautifulSoup

def get_parties_results (url: str) -> dict[str]:
    """
    Returns a dictionary where the key is the name of a political party
    and the value is the number of votes.
    """
    response_get = requests.get(url)
    soup = BeautifulSoup(response_get.text, features="html.parser")
    find_div = soup.find_all("div", {"class": "t2_470"})
    name_count = {}
    for div in find_div:
        find_table = div.find_all("table", {"class": "table"})
        for table in find_table:
            find_tr = table.find_all("tr")
            for tr in find_tr[2:]:
                find_td = tr.find_all("td")
                name_count.update({find_td[1].text: find_td[2].text})
    return name_count         

def get_new_url_addresses (url: str) -> list[str]:
    """
    Returns a list of new URL addresses to get to results of certain municipalities.
    """
    response_get = requests.get(url)
    soup = BeautifulSoup(response_get.text, features="html.parser")
    find_table = soup.find_all("table", {"class": "table"})
    new_url_addresses = []
    for table in find_table:
        find_tr = table.find_all("tr")
        for tr in find_tr[2:]:
            find_td = tr.find("td")
            find_a = find_td.find("a")
            href = find_a.get("href")
            new_url = "https://www.volby.cz/pls/ps2017nss/" + href
            new_url_addresses.append(new_url)
    return new_url_addresses        

def get_municipality_codes_names (url: str) -> dict[str]:
    """
    Returns a dictionary of a municipalities codes and names. Codes are keys and names are values.
    """
    response_get = requests.get(url)
    soup = BeautifulSoup(response_get.text, features="html.parser")
    find_table = soup.find_all("table", {"class": "table"})
    codes_names = {}
    for table in find_table: 
        find_tr = table.find_all("tr")[2:] 
        for tr in find_tr: 
            find_td = tr.find_all("td") 
            codes_names.update({find_td[0].text: find_td[1].text})
    return codes_names

def get_municipality_overview (url: str) -> list:
    """
    Returns a list with the numbers of registered voters, 
    envelopes issued, and valid votes for each municipality.
    """
    response_get = requests.get(url)
    soup = BeautifulSoup(response_get.text, features="html.parser")
    find_table = soup.find("table", {"class": "table"})
    find_tr = find_table.find_all("tr")
    td = find_tr[2].find_all("td")
    overviews = [td[3].text, td[6].text, td[7].text]
    return overviews



# 5. práce se soubory - musím připravit CSV soubor s výsledky voleb.
# Zárověň základní funcke musí přijmou tdva argumetny.

csv_file = open(
    "results.csv",
    mode="w",
    encoding="UTF-8"
)
