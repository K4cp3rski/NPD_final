import warnings

import numpy as np


def get_med_income_woj(df_dict, stats_out, year=2019, verb=0):
    share_proc = 1.6 / 100
    prog = 0.17
    woj_df = df_dict[year]["Wojewodztwa"]
    wojewodztwa = df_dict[year]["Wojewodztwa"]["Nazwa JST"]
    woj_df["Avg_income_yearly"] = ""
    woj_df["Avg_income_monthly"] = ""

    for x in wojewodztwa:
        try:
            stats = stats_out["Wojewodztwa"][x.capitalize()]
        except KeyError as err:
            if verb == 1:
                print("KeyError", err, " not found :c")
        rec = (
            x.capitalize(),
            stats,
            int(
                woj_df[woj_df["Nazwa JST"] == x.lower()]["Dochody_Final"]
                / share_proc
                / prog
            ),
        )
        woj_df.loc[woj_df["Nazwa JST"] == x, "Avg_income_yearly"] = float(
            (rec[2] * rec[1]["work_proc"])
            / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
        )
        woj_df.loc[woj_df["Nazwa JST"] == x, "Avg_income_monthly"] = float(
            (rec[2] * rec[1]["work_proc"])
            / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
            / 12
        )
    return woj_df


def get_med_income_powiaty(df_dict, stats_out, year=2019, verb=0):
    share_proc = 10.25 / 100
    prog = 0.17

    powiaty = {}
    pow_df = df_dict[year]["Powiaty"]
    wojewodztwa = df_dict[year]["Powiaty"]["województwo"]
    pow_df["Avg_income_yearly"] = ""
    pow_df["Avg_income_monthly"] = ""

    powiaty_df = {}
    for x in wojewodztwa:
        powiaty[x] = df_dict[year]["Powiaty"].loc[
            df_dict[year]["Powiaty"]["województwo"] == x
        ]
        pow_names = powiaty[x]

        for powiat in list(pow_names["Nazwa JST"].unique()):
            pow_name = f"powiat {powiat}"
            try:
                if x == "mazowieckie":
                    x = "mazowiecke"
                    stats = stats_out["Powiaty"][x.capitalize()][pow_name]
                    x = "mazowieckie"
                else:
                    stats = stats_out["Powiaty"][x.capitalize()][pow_name]
            except KeyError as err:
                if verb == 1:
                    print("KeyError", err, " not found :c")
            rec = (
                x.capitalize(),
                stats,
                int(
                    list(
                        pow_df[pow_df["Nazwa JST"] == powiat]["Dochody_Final"]
                    )[0]
                    / share_proc
                    / prog
                ),
            )
            pow_names.loc[
                pow_names["Nazwa JST"] == powiat, "Avg_income_yearly"
            ] = float(
                (rec[2] * rec[1]["work_proc"])
                / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
            )
            pow_names.loc[
                pow_names["Nazwa JST"] == powiat, "Avg_income_monthly"
            ] = float(
                (rec[2] * rec[1]["work_proc"])
                / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
                / 12
            )
        powiaty_df[x] = powiaty[x]

    return powiaty_df


def get_med_income_miasta_NPP(df_dict, stats_out, year=2019, verb=0):
    share_proc = 10.25 / 100
    prog = 0.17

    powiaty = {}
    pow_df = df_dict[year]["Miasta_NPP"]
    wojewodztwa = df_dict[year]["Miasta_NPP"]["województwo"]
    pow_df["Avg_income_yearly"] = ""
    pow_df["Avg_income_monthly"] = ""

    powiaty_df = {}
    for x in wojewodztwa.unique():
        powiaty[x] = df_dict[year]["Miasta_NPP"].loc[
            df_dict[year]["Miasta_NPP"]["województwo"] == x
        ]
        powiaty[x] = powiaty[x].loc[powiaty[x]["ROZDZIAŁ"] == 75622]
        pow_names = powiaty[x]
        if verb > 0:
            print(pow_names)

        for powiat in list(pow_names["Nazwa JST"].unique()):
            powiat_low = powiat.lower()
            if verb > 0:
                print(powiat)
            try:
                if x == "mazowieckie":
                    x = "mazowiecke"
                    if powiat_low == "m. st. warszawa":
                        powiat_low = f"powiat {powiat_low}"
                    else:
                        powiat_low = f"powiat m. {powiat_low}"
                    stats = stats_out["Powiaty"][x.capitalize()][powiat_low]
                    x = "mazowieckie"
                else:
                    powiat_low = f"powiat m. {powiat_low}"
                    stats = stats_out["Powiaty"][x.capitalize()][powiat_low]
            except KeyError as err:
                if verb == 1:
                    print("KeyError", err, " not found :c")
            rec = (
                x.capitalize(),
                stats,
                int(
                    list(
                        pow_df[pow_df["Nazwa JST"] == powiat]["Dochody_Final"]
                    )[0]
                    / share_proc
                    / prog
                ),
            )
            pow_names.loc[
                pow_names["Nazwa JST"] == powiat, "Avg_income_yearly"
            ] = float(
                (rec[2] * rec[1]["work_proc"])
                / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
            )
            pow_names.loc[
                pow_names["Nazwa JST"] == powiat, "Avg_income_monthly"
            ] = float(
                (rec[2] * rec[1]["work_proc"])
                / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
                / 12
            )
        powiaty_df[x] = powiaty[x]

    return powiaty_df


def get_med_income_gminy(df_dict, stats_out, year=2019, verb=0):
    share_proc = 39.34 / 100
    prog = 0.17

    wojewodztwa = df_dict[year]["Wojewodztwa"]["Nazwa JST"]

    gminy = {}
    gminy_dict = {}

    for x in wojewodztwa:
        if x == "śląskie":
            x = "śląske"
        gminy[x] = df_dict[year]["Gminy"].loc[
            df_dict[year]["Gminy"]["województwo"] == x
        ]
        gminy_dict[x] = {}
        for powiat in list(gminy[x]["powiat"].unique()):
            gminy_dict[x][powiat] = gminy[x].loc[gminy[x]["powiat"] == powiat]
            gminy_dict[x][powiat] = gminy_dict[x][powiat].drop_duplicates(
                subset=["Nazwa JST"]
            )
            gminy_dict[x][powiat]["Avg_income_yearly"] = ""
            gminy_dict[x][powiat]["Avg_income_monthly"] = ""

            for gmina in list(gminy_dict[x][powiat]["Nazwa JST"]):
                # gmina = gmina.lower()
                # print(x, powiat, gmina)
                try:
                    stats = stats_out["Gminy"][x.capitalize()][gmina.lower()]
                except KeyError as err:
                    if verb == 1:
                        print("KeyError", err, " not found :c")
                    continue
                rec = (
                    x,
                    stats,
                    int(
                        int(
                            list(
                                gminy_dict[x][powiat].loc[
                                    gminy_dict[x][powiat]["Nazwa JST"] == gmina
                                ]["Dochody_Final"]
                            )[0]
                        )
                        / share_proc
                        / prog
                    ),
                )
                gminy_dict[x][powiat].loc[
                    gminy_dict[x][powiat]["Nazwa JST"] == gmina,
                    "Avg_income_yearly",
                ] = float(
                    (rec[2] * rec[1]["work_proc"])
                    / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
                )
                gminy_dict[x][powiat].loc[
                    gminy_dict[x][powiat]["Nazwa JST"] == gmina,
                    "Avg_income_monthly",
                ] = float(
                    (rec[2] * rec[1]["work_proc"])
                    / (rec[1]["tot_taxed"] * rec[1]["work_proc"])
                    / 12
                )

    return gminy_dict


def get_var(gminy_dict, df_dict, stats_out, year=2019):
    gminy_var = {}
    woj_var = {}
    wojewodztwa = df_dict[year]["Wojewodztwa"]["Nazwa JST"]

    gminy = {}
    for x in wojewodztwa:
        if x == "śląskie":
            x = "śląske"
        gminy[x] = df_dict[year]["Gminy"].loc[
            df_dict[year]["Gminy"]["województwo"] == x
        ]
        gminy_var[x] = {}
        for powiat in list(gminy_dict[x].keys()):
            try:
                gminy_var[x][powiat] = {
                    "var": float(
                        gminy_dict[x][powiat]["Avg_income_yearly"].var()
                    ),
                    "mean": float(
                        gminy_dict[x][powiat]["Avg_income_yearly"].mean()
                    ),
                }
            except TypeError:
                continue
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            try:
                woj_var[x] = {
                    "var": np.var(
                        np.asarray(
                            [
                                gminy_var[x][key]["var"]
                                for key in gminy_var[x].keys()
                            ]
                        )
                    ),
                    "mean": np.mean(
                        np.asarray(
                            [
                                gminy_var[x][key]["var"]
                                for key in gminy_var[x].keys()
                            ]
                        )
                    ),
                }
            except Warning:
                continue

    return gminy_var, woj_var


def get_med_income(df_dict, stats_out, years, verb=0):
    med_income = {}
    for year in years:
        woj_df = get_med_income_woj(df_dict, stats_out, year, verb)
        pow_df = get_med_income_powiaty(df_dict, stats_out, year, verb)
        gminy_dict = get_med_income_gminy(df_dict, stats_out, year, verb)
        miasta_NPP_df = get_med_income_miasta_NPP(
            df_dict, stats_out, year, verb
        )
        var = get_var(gminy_dict, df_dict, stats_out)
        med_income[year] = {
            "woj_df": woj_df,
            "pow_df": pow_df,
            "gminy_dict": gminy_dict,
            "miasta_NPP_df": miasta_NPP_df,
            "var": var,
        }
    return med_income
