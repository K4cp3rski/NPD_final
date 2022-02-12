import re

import pandas as pd
from colorama import Fore, Style
from taxes.download import get_gus_stats  # noqa: E501
from taxes.download import (  # noqa: E501
    download_sheet_series,
    get_sheet_links_names,
)


def get_gov_dir(years, verb=False):
    gov_dir = {}
    for year in years:
        sheets = get_sheet_links_names(year, verb)
        gov_dir[year] = sheets
        dir_sheets = download_sheet_series(sheets, verb)

    gus_dir = get_gus_stats(verb)

    if verb:
        print(
            f"PIT earnings dir path = {dir_sheets}\nGUS data dir path = {gus_dir}"  # noqa: E501
        )  # noqa: E501
    return gov_dir, dir_sheets, gus_dir


def gov_dir_to_names_dict(gov_dir, verb=False):
    names = {}
    for year in gov_dir.keys():
        names[year] = gov_dir[year][1]

    for year in names.keys():
        classes = dict.fromkeys(
            ["Gminy", "Powiaty", "Miasta_NPP", "Metropolia", "Wojewodztwa"]
        )  # noqa: E501
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
                "WPLYWY_RAW",
                "Dochody_Final",
            ]

            dtype = {
                "WK": "str",
                "PK": "str",
                "GK": "str",
                "GT": "str",
            }

            file_extension = fl.suffix.lower()[1:]

            if file_extension == "xlsx":
                df = pd.read_excel(
                    fl,
                    skiprows=7,
                    header=None,
                    names=col_names,
                    dtype=dtype,
                    usecols="A:L",
                    engine="openpyxl",  # noqa: E501
                )
            elif file_extension == "xls":
                df = pd.read_excel(
                    fl,
                    skiprows=7,
                    header=None,
                    usecols="A:L",
                    names=col_names,
                    dtype=dtype,
                    engine="xlrd",
                )  # noqa: E501
            else:
                raise Exception("File not supported")

            df.insert(loc=4, column="JST_code", value="")
            for ind in df.index:
                a = df["WK"][ind]
                b = df["PK"][ind]
                c = df["GK"][ind]
                d = df["GT"][ind]
                if key == "Gminy":
                    df.at[ind, "JST_code"] = f"{a:0>2}{b:0>2}{c:0>2}{d:0>1}"
                elif key == "Powiaty":
                    df.at[ind, "JST_code"] = f"{a:0>2}{b:0>2}"
                elif key == "Miasta_NPP":
                    df.at[ind, "JST_code"] = f"{a:0>2}{b:0>2}"

            df_dict[year][key] = df

    return df_dict


def extract_and_zip_gus(gus_dir, verb=False):
    """
    Interesują nas tylko tabele:
    * tabela3.xls -> Województwa
    * tabela6.xls -> Powiaty
    * tabela12.xls -> Gminy
    """
    tables = {
        "Wojewodztwa": "tabela03.xls",
        "Powiaty": "tabela06.xls",
        "Gminy": "tabela12.xls",
    }  # noqa: E501
    gus_dir_files = list(gus_dir.glob("*.xls"))
    for filename, key in zip(tables.values(), tables.keys()):
        for file in gus_dir_files:
            if filename == file.name:
                tables[key] = file

    for JST in tables.keys():
        df = tables[JST]
        if JST == "Wojewodztwa":
            columns = [
                "Wyszczegolnienie",
                "Total",
                "Males",
                "Females",
                "Cities_Total",
                "Cities_Males",
                "Cities_Females",
                "Rural_Total",
                "Rural_Males",
                "Rural_Females",
            ]
            dtype = {"JST_code": "str"}
        else:
            columns = [
                "Wyszczegolnienie",
                "JST_code",
                "Total",
                "Males",
                "Females",
                "Cities_Total",
                "Cities_Males",
                "Cities_Females",
                "Rural_Total",
                "Rural_Males",
                "Rural_Females",
            ]
            dtype = {"JST_code": "str"}
        tables[JST] = pd.read_excel(
            df,
            sheet_name=None,
            skiprows=7,
            names=columns,
            dtype=dtype,
            keep_default_na=False,
        )
    return tables


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

    gus_zip = extract_and_zip_gus(gus_dir)

    if verb:
        print(df_dict[2020]["Gminy"].head())

    print(Fore.CYAN + "Ended preprocessing!" + Style.RESET_ALL)

    return df_dict, gus_zip


if __name__ == "__main__":
    years = [2019, 2020]
    verb = False
    dload_to_df_list(years, verb)
