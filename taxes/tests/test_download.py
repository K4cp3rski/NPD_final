import pytest
import functools
from taxes.download import get_sheet_links_names, download_sheet_series

pytest_plugins = ["taxes.download"]

@pytest.mark.parametrize("year, res", [(2019, (['https://www.gov.pl/attachment/6594af94-cd1e-49fb-9149-99fd663aef25', 'https://www.gov.pl/attachment/5f2abc44-6a7e-4b73-8999-696920252efc', 'https://www.gov.pl/attachment/141da745-800d-44c5-ac97-e90c4cbd5e11', 'https://www.gov.pl/attachment/12150aff-d70e-412b-afdc-2bc5341dc823', 'https://www.gov.pl/attachment/141eeb3c-dedc-4491-b0bf-895587824eff'], ['20200214_Gminy_za_2019.xlsx', '20200214_Powiaty_za_2019.xlsx', '20200214_Miasta_NPP_za_2019.xlsx', '20200214_Gornoslasko_Zaglebiowska_Metropolia.xlsx', '20200214_Wojewodztwa_za_2019.xlsx'])), (2020, (['https://www.gov.pl/attachment/31d60032-a3c5-4e4f-8af8-67c8fa09afd2', 'https://www.gov.pl/attachment/82cb06d7-02e6-4d24-a8b4-9926fe0a3079', 'https://www.gov.pl/attachment/bafb6020-bca0-4ec8-9369-845e0afb94d9', 'https://www.gov.pl/attachment/e4077a76-1fbc-478e-a15d-eea0a4e3f130', 'https://www.gov.pl/attachment/0b98f8be-e9e1-48e3-8bc5-796e8c0b169e'], ['20210215_Gminy_2_za_2020.xlsx', '20210211_Powiaty_za_2020.xlsx', '20210215_Miasta_NPP_2_za_2020.xlsx', '20210211_Metropolia_2020.xlsx', '20210211_Województwa_za_2020.xlsx']))])
def test_get_sheet_links_names(year, res):
    assert get_sheet_links_names(year) == res

@pytest.mark.parametrize("year, data, count", [(2019, (['https://www.gov.pl/attachment/6594af94-cd1e-49fb-9149-99fd663aef25', 'https://www.gov.pl/attachment/5f2abc44-6a7e-4b73-8999-696920252efc', 'https://www.gov.pl/attachment/141da745-800d-44c5-ac97-e90c4cbd5e11', 'https://www.gov.pl/attachment/12150aff-d70e-412b-afdc-2bc5341dc823', 'https://www.gov.pl/attachment/141eeb3c-dedc-4491-b0bf-895587824eff'], ['20200214_Gminy_za_2019.xlsx', '20200214_Powiaty_za_2019.xlsx', '20200214_Miasta_NPP_za_2019.xlsx', '20200214_Gornoslasko_Zaglebiowska_Metropolia.xlsx', '20200214_Wojewodztwa_za_2019.xlsx']), 5), (2020, (['https://www.gov.pl/attachment/31d60032-a3c5-4e4f-8af8-67c8fa09afd2', 'https://www.gov.pl/attachment/82cb06d7-02e6-4d24-a8b4-9926fe0a3079', 'https://www.gov.pl/attachment/bafb6020-bca0-4ec8-9369-845e0afb94d9', 'https://www.gov.pl/attachment/e4077a76-1fbc-478e-a15d-eea0a4e3f130', 'https://www.gov.pl/attachment/0b98f8be-e9e1-48e3-8bc5-796e8c0b169e'], ['20210215_Gminy_2_za_2020.xlsx', '20210211_Powiaty_za_2020.xlsx', '20210215_Miasta_NPP_2_za_2020.xlsx', '20210211_Metropolia_2020.xlsx', '20210211_Województwa_za_2020.xlsx']), 5)])
def test_download_sheet_series(year, data, count):
    dir_path = download_sheet_series(data)
    sheet_count = len(list(dir_path.glob(f'{year+1}*.xlsx')))
    assert sheet_count == count