import pathlib

import pandas as pd
import pytest
import taxes.download as dload
from taxes.preprocessing import (  # noqa: E501
    dload_to_df_list,
    get_gov_dir,
    gov_dir_to_names_dict,
    names_dict_to_df_dict,
)

gov_dir = {
    2019: (
        [
            "https://www.gov.pl/attachment/6594af94-cd1e-49fb-9149-99fd663aef25",  # noqa: E501
            "https://www.gov.pl/attachment/5f2abc44-6a7e-4b73-8999-696920252efc",  # noqa: E501
            "https://www.gov.pl/attachment/141da745-800d-44c5-ac97-e90c4cbd5e11",  # noqa: E501
            "https://www.gov.pl/attachment/12150aff-d70e-412b-afdc-2bc5341dc823",  # noqa: E501
            "https://www.gov.pl/attachment/141eeb3c-dedc-4491-b0bf-895587824eff",  # noqa: E501
        ],
        [
            "20200214_Gminy_za_2019.xlsx",
            "20200214_Powiaty_za_2019.xlsx",
            "20200214_Miasta_NPP_za_2019.xlsx",
            "20200214_Gornoslasko_Zaglebiowska_Metropolia.xlsx",
            "20200214_Wojewodztwa_za_2019.xlsx",
        ],
    ),
    2020: (
        [
            "https://www.gov.pl/attachment/31d60032-a3c5-4e4f-8af8-67c8fa09afd2",  # noqa: E501
            "https://www.gov.pl/attachment/82cb06d7-02e6-4d24-a8b4-9926fe0a3079",  # noqa: E501
            "https://www.gov.pl/attachment/bafb6020-bca0-4ec8-9369-845e0afb94d9",  # noqa: E501
            "https://www.gov.pl/attachment/e4077a76-1fbc-478e-a15d-eea0a4e3f130",  # noqa: E501
            "https://www.gov.pl/attachment/0b98f8be-e9e1-48e3-8bc5-796e8c0b169e",  # noqa: E501
        ],
        [
            "20210215_Gminy_2_za_2020.xlsx",
            "20210211_Powiaty_za_2020.xlsx",
            "20210215_Miasta_NPP_2_za_2020.xlsx",
            "20210211_Metropolia_2020.xlsx",
            "20210211_Wojewodztwa_za_2020.xlsx",
        ],
    ),
}

dir_sheets = pathlib.Path.cwd().joinpath("data")

gus_dir = pathlib.Path.cwd().joinpath("data", "gus")

names = {
    2019: {
        "Gminy": "20200214_Gminy_za_2019.xlsx",
        "Powiaty": "20200214_Powiaty_za_2019.xlsx",
        "Miasta_NPP": "20200214_Miasta_NPP_za_2019.xlsx",
        "Metropolia": "20200214_Gornoslasko_Zaglebiowska_Metropolia.xlsx",
        "Wojewodztwa": "20200214_Wojewodztwa_za_2019.xlsx",
    },
    2020: {
        "Gminy": "20210215_Gminy_2_za_2020.xlsx",
        "Powiaty": "20210211_Powiaty_za_2020.xlsx",
        "Miasta_NPP": "20210215_Miasta_NPP_2_za_2020.xlsx",
        "Metropolia": "20210211_Metropolia_2020.xlsx",
        "Wojewodztwa": "20210211_Wojewodztwa_za_2020.xlsx",
    },
}


def mock_sheets(year, verb):
    return gov_dir[year]


def mock_dload(sheets, verb):
    return dir_sheets


def mock_gus(verb):
    pathlib.Path.mkdir(pathlib.Path.cwd().joinpath("data"), exist_ok=True)  # noqa: E501
    return gus_dir


@pytest.mark.parametrize("years", [[2019, 2020]])
def test_get_gov_dir(years, monkeypatch):
    monkeypatch.setattr(dload, "get_sheet_links_names", mock_sheets)
    monkeypatch.setattr(dload, "download_sheet_series", mock_dload)
    monkeypatch.setattr(dload, "get_gus_stats", mock_gus)

    assert get_gov_dir(years) == (gov_dir, dir_sheets, gus_dir)


def test_gov_dir_to_names_dict():
    assert gov_dir_to_names_dict(gov_dir) == names


def test_names_dict_to_df_dict():
    df_dict = names_dict_to_df_dict(names, dir_sheets)
    assert type(df_dict) == dict
    for key in df_dict.keys():
        assert type(df_dict[key]) == dict
        for sheet in df_dict[key].keys():
            type(df_dict[key][sheet]) == pd.core.frame.DataFrame


@pytest.mark.parametrize("years", [[2019, 2020]])
def test_dload_to_df_list(years):
    df_dict = dload_to_df_list(years)
    assert type(df_dict) == dict
    for key in df_dict.keys():
        assert type(df_dict[key]) == dict
        for sheet in df_dict[key].keys():
            type(df_dict[key][sheet]) == pd.core.frame.DataFrame
