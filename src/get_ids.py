import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":

    id_file = open("data/ids.txt", "a")
    for i in range(1, 70000):
        URL = f"https://www.bfro.net/GDB/show_report.asp?id={i}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        if len(soup) == 5:
            id_file.write(str(i)+"\n")
    id_file.close()
