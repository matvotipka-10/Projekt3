import csv
import requests
import argparse
from bs4 import BeautifulSoup
from urllib import parse

parser = argparse.ArgumentParser()
parser.add_argument(
    "url_adress"
    )
parser.add_argument(
    "csv_name"
    )

def get_parties_results(url: str) -> dict[str, dict[str]]:
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
    get_key = parse.urlparse(url)
    key_list = get_key.query.split("&")
    key = key_list[2].split("=")
    results = {key[1]: name_count} 
    return results

def get_new_url_addresses(url: str) -> list[str]:
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
            if find_a is None:
                continue
            href = find_a.get("href")
            new_url = "https://www.volby.cz/pls/ps2017nss/" + href
            new_url_addresses.append(new_url)
    return new_url_addresses        

def get_municipality_codes_names(url: str) -> dict[str, dict[str]]:
    """
    Returns a dictionary of dictionaries with codes and names of municipalities.
    """
    response_get = requests.get(url)
    soup = BeautifulSoup(response_get.text, features="html.parser")
    find_table = soup.find_all("table", {"class": "table"})
    codes_names = {}
    for table in find_table: 
        find_tr = table.find_all("tr")[2:] 
        for tr in find_tr: 
            find_td = tr.find_all("td") 
            codes_names.update({find_td[0].text: {"code": find_td[0].text, "location": find_td[1].text}})
    return codes_names

def get_municipality_overview(url: str) -> dict[str, dict[str]]:
    """
    Returns a dict of lists with the numbers of registered voters, 
    envelopes issued, and valid votes for each municipality.
    """
    response_get = requests.get(url)
    soup = BeautifulSoup(response_get.text, features="html.parser")
    find_table = soup.find("table", {"class": "table"})
    find_tr = find_table.find_all("tr")
    td = find_tr[2].find_all("td")
    get_key = parse.urlparse(url)
    key_list = get_key.query.split("&")
    key = key_list[2].split("=")
    overview = {key[1]: {"registered": td[3].text, "envelopes": td[6].text, "valid": td[7].text}}
    return overview
# možno napsat mnohem čištěji

def rows_for_csv(
        codes_names: dict[str, dict],
        overviews: dict[str, dict],
        results: dict[str, dict]
        ) -> dict[str, dict]:
    """
    Creats dictionary of rows for csv format with all data needed.
    """
    rows = {}
    for code, base in codes_names.items():
        if code not in overviews or code not in results:
            continue
        row = base.copy()
        row.update(overviews[code])
        row.update(results[code])
        rows[code] = row
    return rows

def save_rows_to_csv(rows: dict[str, dict], csv_name: str):
    with open (csv_name, mode="w", encoding="UTF-8") as csvfile:
        fieldnames = []
        for fieldname in rows:
            fieldnames = rows[fieldname].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(rows[row])

def main():
    args = parser.parse_args()
    users_url = args.url_adress
    csv_name = args.csv_name
    codes_names = get_municipality_codes_names(users_url)    
    new_url_adresses = get_new_url_addresses(users_url)    
    overviews = {}
    results = {}
    for one_url in new_url_adresses:
        overview = get_municipality_overview(one_url)
        overviews.update(overview)
        result = get_parties_results(one_url)
        results.update(result)
    rows = rows_for_csv(codes_names, overviews, results)
    save_rows_to_csv(rows, csv_name)
    print(rows)

if __name__ == "__main__":
    main()