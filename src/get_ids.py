import requests
from bs4 import BeautifulSoup

"""
Parses through a range of potential report ids, and writes valid ids to a text file.
A valid report is on which has a soup length of 5 whereas invalid reports (URLs that
do not contain a report) have a soup length of 4.
"""

if __name__ == "__main__":

    id_file = open("data/ids.txt", "a")
    for i in range(1, 70000):
        URL = f"https://www.bfro.net/GDB/show_report.asp?id={i}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        if len(soup) == 5:
            id_file.write(str(i)+"\n")
    id_file.close()
