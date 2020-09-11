import requests
from bs4 import BeautifulSoup
import json

"""Loops through the valid ids from ids.txt, injects them into a URL,
   and web scrapes the sighting data for each report,
   writing them to a json file as they are scraped.
"""


def get_data_from_id(id):
    """
    Parses the URL and stores the data in a dictionary.

            Parameters:
                    id (str): Valid id to inject into a URL.

            Returns:
                    sighting_d (dict): A dictionary of data from the relevant
                    sighting.
    """
    sighting_d = dict()
    URL = f"https://www.bfro.net/GDB/show_report.asp?id={id}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    for br in soup.find_all("br"):
        br.replace_with(" ")
    for i in soup.find_all("p"):
        split_text = i.getText().split(": ")
        if len(split_text) > 2:
            split_text = [split_text[0], ': '.join(split_text[1:])]
        if len(split_text) == 2:
            sighting_d[split_text[0]] = split_text[1]
    return sighting_d


if __name__ == "__main__":

    f = open("data/ids.txt", "r")
    ids = f.read().splitlines()
    f.close()
    print("length of ids: ", len(ids))
    with open("data/data.json", "a") as f:
        for id in ids:
            bigfoot_d = dict()
            bigfoot_d[id] = get_data_from_id(id)
            with open('data/data.json') as f:
                data = json.load(f)
            data.update(bigfoot_d)
            with open('data/data.json', 'w') as f:
                json.dump(data, f, indent=4, sort_keys=False)
    f.close()
