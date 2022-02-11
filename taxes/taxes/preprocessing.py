import re

import pandas as pd
from colorama import Fore, Style
from taxes.download import get_gus_stats  # noqa: E501
from taxes.download import download_sheet_series, get_sheet_links_names  # noqa: E501


def get_gov_dir(years, verb=False):
    gov_dir = {}
    for year in years:
        sheets = get_sheet_links_names(year, verb)
        gov_dir[year] = sheets
        dir_sheets = download_sheet_series(sheets, verb)

    gus_dir = get_gus_stats(verb)

    if verb:
        print(f"PIT earnings dir path = {dir_sheets}\nGUS data dir path = {gus_dir}")  # noqa: E501
    return gov_dir, dir_sheets, gus_dir


def gov_dir_to_names_dict(gov_dir, verb=False):
    names = {}
    for year in gov_dir.keys():
        names[year] = gov_dir[year][1]

    for year in names.keys():
        classes = dict.fromkeys(["Gminy", "Powiaty", "Miasta_NPP", "Metropolia", "Wojewodztwa"])  # noqa: E501
        for key in classes.keys():
            for name in names[year]:
                if re.search(key, name) is not None:
                    classes[key] = name
                else:
                    continue
        names[year] = classes
    return names


def names_dict_to_df_dict(names, dir_sheets, verb=False):
    df_dict = dict.fromkeys(names.keys())

    for year in df_dict.keys():
        df_dict[year] = dict.fromkeys(names[year].keys())
        for key in df_dict[year].keys():
            fl = dir_sheets.joinpath(names[year][key])
            if verb:
                print(fl)

            col_names = [
                "WK",
                "PK",
                "GK",
                "GT",
                "Nazwa JST",
                "województwo",
                "powiat",
                "DZIAŁ",
                "ROZDZIAŁ",
                "PARAGRAF",
                "Należności (saldo początkowe plus przypisy minus odpisy)",
                "Dochody wykonane (wpłaty minus zwroty)",
                "ogółem",
                "zaległości netto",
                "nadpłaty",
            ]

            file_extension = fl.suffix.lower()[1:]

            if file_extension == "xlsx":
                df = pd.read_excel(
                    fl,
                    skiprows=7,
                    header=None,
                    names=col_names,
                    engine="openpyxl",  # noqa: E501
                )
            elif file_extension == "xls":
                df = pd.read_excel(fl, skiprows=7, header=None, names=col_names, engine="xlrd")  # noqa: E501
            else:
                raise Exception("File not supported")

            df_dict[year][key] = df

    return df_dict


def dload_to_df_list(years, verb=False):
    print(Fore.GREEN + "Beginning download...\n" + Style.RESET_ALL)
    gov_dir, dir_sheets, gus_dir = get_gov_dir(years, verb)
    print(
        Fore.GREEN
        + "Download ended.\n\n"
        + Style.RESET_ALL
        + Fore.CYAN
        + "Beginning preprocessing...\n"
        + Style.RESET_ALL
    )

    names = gov_dir_to_names_dict(gov_dir, verb)

    df_dict = names_dict_to_df_dict(names, dir_sheets, verb)

    if verb:
        print(df_dict[2020]["Gminy"].head())

    print(Fore.CYAN + "Ended preprocessing!" + Style.RESET_ALL)

    return df_dict


if __name__ == "__main__":
    years = [2019, 2020]
    verb = False
    dload_to_df_list(years, verb)
