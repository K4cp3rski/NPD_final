import pathlib
import re

import dload
import requests
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from fake_useragent import UserAgent

"""
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
"""


def get_sheet_links_names(year=2020):
    # specify the URL of the archive here
    archive_url = f"https://www.gov.pl/web/finanse/udzialy-za-{year}-r"
    data_url = "https://www.gov.pl"

    # create response object
    r = requests.get(archive_url)

    # create beautiful-soup object
    soup = BeautifulSoup(r.content, "html5lib")

    # find all links on web-page
    links = soup.findAll("a")

    # filter the names for our .xlsx files
    names = []
    for link in links:
        try:
            names.append(link["aria-label"])
        except KeyError:
            continue

    sheet_links = [data_url + link[r"href"] for link in links]

    sheet_links = [
        link
        for link in sheet_links
        if re.search("attachment", link) is not None  # noqa: E501
    ]

    names = re.findall(r"[0-9].+\.xlsx", " ".join(names))

    return sheet_links, names


def download_sheet_series(sheets, verb=False):
    if verb:
        print(sheets, len(sheets[0]))
    sheets_dir = None
    mirror_url_dir = "http://studenci.fuw.edu.pl/~kc427902/NPD_xlsx_mirror/"

    pathlib.Path.mkdir(pathlib.Path.cwd().joinpath("data"), exist_ok=True)
    filename = pathlib.Path.cwd().joinpath("data")

    for link, file_name in zip(sheets[0], sheets[1]):

        """iterate through all links in sheets
        and download them one by one"""

        print("Downloading file: %s" % file_name)

        # create response object
        headers = {"User-Agent": UserAgent().chrome}
        r = requests.get(link, headers=headers)
        if re.search("!DOCTYPE html", str(r.content)) is not None:
            print(
                Fore.RED
                + Back.WHITE
                + "Downloaded webpage. Switching to mirror source..."
                + Style.RESET_ALL
            )
            link = mirror_url_dir + file_name
            r = requests.get(link, headers=headers)
            if verb:
                print(r.content)
            # download started
            with open(
                pathlib.Path.cwd().joinpath("data", file_name), "wb"
            ) as output:  # noqa: E501
                output.write(r.content)

        else:
            # download started
            with open(
                pathlib.Path.cwd().joinpath("data", file_name), "wb"
            ) as output:  # noqa: E501
                output.write(r.content)

        p = pathlib.Path(filename)
        p = p.resolve()
        downloaded_file = p.joinpath(file_name)
        downloads_dir = downloaded_file.parent

        sheets_dir = downloads_dir

        print(Fore.CYAN + "%s downloaded!\n" % file_name)
        print(Style.RESET_ALL)

    print(Fore.GREEN + "All sheets downloaded!")
    print(Style.RESET_ALL)
    return sheets_dir


def get_gus_stats(verb=False):
    archive_url = str(
        "https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/ludnosc-stan-i-struktura-ludnosci-oraz"  # noqa: E501
        + "-ruch-naturalny-w-przekroju-terytorialnym-stan-w-dniu-31-12-2020,6,29.html"  # noqa: E501
    )

    pathlib.Path.mkdir(pathlib.Path.cwd().joinpath("data"), exist_ok=True)
    filename = pathlib.Path.cwd().joinpath("data")

    # create response object
    r = requests.get(archive_url)

    # create beautiful-soup object
    soup = BeautifulSoup(r.content, "html5lib")

    # find all links on web-page
    links = soup.findAll("a")
    sheet_links = ["https://stat.gov.pl" + link[r"href"] for link in links]

    sheet_links = [
        link for link in sheet_links if re.search("2020.zip", link) is not None
    ][0]
    if verb:
        print(sheet_links)

    dloaded = dload.save_unzip(sheet_links, str(filename), delete_after=True)
    elements = list(pathlib.Path(dloaded).glob("*"))
    elements = [el for el in elements if el.is_dir()][0]
    elements = elements.rename(filename.joinpath("gus"))
    if verb:
        print(elements)
    return elements


if __name__ == "__main__":
    #     Zbieramy ze strony wsztstkie linki do arkuszy i ich nazwy
    sheets = get_sheet_links_names()
    download_sheet_series(sheets)
    get_gus_stats()
