from colorama import Fore, Style


def calc_stats(JST, tmp, proc_working, ind):
    tmp["working_age"] = int(JST.iloc[ind + 50]["Total"])
    tmp["post_working_age"] = int(JST.iloc[ind + 57]["Total"])
    tmp["tot_taxed"] = int(
        tmp["working_age"] * proc_working + tmp["post_working_age"]
    )
    tmp["work_proc"] = tmp["working_age"] / tmp["tot_taxed"] * 100
    tmp["post_proc"] = tmp["post_working_age"] / tmp["tot_taxed"] * 100
    return tmp


def calc_stats_woj(JST, tmp, proc_working):
    tmp["working_age"] = int(
        JST.loc[JST["Wyszczegolnienie"] == "Wiek  produkcyjny  \nWorking age"][
            "Total"
        ]
    )
    tmp["post_working_age"] = int(
        JST.loc[
            JST["Wyszczegolnienie"]
            == "Wiek poprodukcyjny  \nPost-working age"  # noqa: E501
        ]["Total"]
    )
    tmp["tot_taxed"] = int(
        tmp["working_age"] * proc_working + tmp["post_working_age"]
    )
    tmp["work_proc"] = tmp["working_age"] / tmp["tot_taxed"] * 100
    tmp["post_proc"] = tmp["post_working_age"] / tmp["tot_taxed"] * 100


def get_stats_gus(gus_zip, verb=1, proc_working=0.8):
    stats = dict.fromkeys(gus_zip.keys())
    for category in gus_zip.keys():
        wojewodztwa = gus_zip[category].keys()
        stats[category] = dict.fromkeys(wojewodztwa)
        for woj in wojewodztwa:
            if category == "Wojewodztwa":
                if verb >= 1:
                    print(Fore.RED + category + Style.RESET_ALL)
                stats[category][woj] = {}
                tmp = stats[category][woj]
                JST = gus_zip[category][woj]
                calc_stats_woj(JST, tmp, proc_working)
                if verb >= 1:
                    print(Fore.CYAN + woj + Style.RESET_ALL)
                if verb >= 2:
                    print(
                        "Working age: {}, Post-working age: {}, Total PIT payers: {}\n".format(  # noqa: E501
                            tmp["working_age"],
                            tmp["post_working_age"],
                            tmp["tot_taxed"],
                        )
                        + "Working age make up: {:.2f}%, Post-working age make up: {:.2f}%\n".format(  # noqa: E501
                            tmp["work_proc"],
                            tmp["post_proc"],
                        )
                    )
            elif category == "Powiaty":
                if verb >= 1:
                    print(Fore.RED + category + Style.RESET_ALL)
                stats[category][woj] = {}
                JST_smol = stats[category][woj]
                JST_big = gus_zip[category][woj]

                JST_dropped = JST_big.drop(
                    JST_big.loc[JST_big["JST_code"] == ""].index, axis=0
                )
                JST_codes = JST_dropped
                JST_names = JST_big.iloc[JST_codes.index]["Wyszczegolnienie"]
                for name, ind in zip(JST_names, JST_codes.index):
                    if verb >= 1:
                        print(Fore.CYAN + name + Style.RESET_ALL)
                    JST_smol[r"{}".format(str(name))] = {}
                    tmp = JST_smol[r"{}".format(str(name))]
                    JST = gus_zip[category][woj]
                    calc_stats(JST, tmp, proc_working, ind)
                    if verb >= 2:
                        print(
                            "Working age: {}, Post-working age: {}, Total PIT payers: {}\n".format(  # noqa: E501
                                tmp["working_age"],
                                tmp["post_working_age"],
                                tmp["tot_taxed"],
                            )
                            + "Working age make up: {:.2f}%, Post-working age make up: {:.2f}%\n".format(  # noqa: E501
                                tmp["work_proc"],
                                tmp["post_proc"],
                            )
                        )
            else:
                if verb >= 1:
                    print(Fore.RED + category + Style.RESET_ALL)
                stats[category][woj] = {}
                JST_smol = stats[category][woj]
                JST_big = gus_zip[category][woj]

                JST_dropped = JST_big.drop(
                    JST_big.loc[JST_big["JST_code"] == "       "].index, axis=0
                )
                JST_dropped = JST_dropped.drop(
                    JST_big.loc[JST_big["JST_code"] == ""].index, axis=0
                )
                JST_codes = JST_dropped
                JST_names = JST_big.iloc[JST_codes.index]["Wyszczegolnienie"]
                for name, ind in zip(JST_names, JST_codes.index):
                    if verb >= 1:
                        print(Fore.CYAN + name + Style.RESET_ALL)
                    JST_smol[r"{}".format(str(name))] = {}
                    tmp = JST_smol[r"{}".format(str(name))]
                    JST = gus_zip[category][woj]
                    calc_stats(JST, tmp, proc_working, ind)
                    if verb >= 2:
                        print(
                            "Working age: {}, Post-working age: {}, Total PIT payers: {}\n".format(  # noqa: E501
                                tmp["working_age"],
                                tmp["post_working_age"],
                                tmp["tot_taxed"],
                            )
                            + "Working age make up: {:.2f}%, Post-working age make up: {:.2f}%\n".format(  # noqa: E501
                                tmp["work_proc"],
                                tmp["post_proc"],
                            )
                        )
    return stats
