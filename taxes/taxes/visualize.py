import pandas as pd
import seaborn as sns


def vis_woj(med_income):
    vis = pd.DataFrame()
    for year in med_income.keys():
        # vis_tmp = pd.DataFrame
        woj_df = med_income[year]["woj_df"]
        vis_tmp = pd.DataFrame(woj_df["Nazwa JST"])
        vis_tmp["year"] = year
        vis_tmp["Inc_yr"] = woj_df["Avg_income_yearly"]
        vis_tmp["Inc_mo"] = woj_df["Avg_income_monthly"]
        vis = pd.concat([vis, vis_tmp], axis=0)
    # print(vis)

    rp_yr = sns.catplot(
        data=vis, y="Nazwa JST", x="Inc_yr", hue="year", kind="bar", orient="h"
    )
    rp_yr.fig.subplots_adjust(top=0.9)  # adjust the Figure in rp
    rp_yr.fig.suptitle("Average Yearly Income")

    rp_mo = sns.catplot(
        data=vis, y="Nazwa JST", x="Inc_mo", hue="year", kind="bar", orient="h"
    )
    rp_mo.fig.subplots_adjust(top=0.9)  # adjust the Figure in rp
    rp_mo.fig.suptitle("Average Monthly Income")
    return vis


def vis_pow(med_income):
    vis = pd.DataFrame()
    for year in med_income.keys():
        vis_tmp = pd.DataFrame()
        for woj in med_income[year]["pow_df"].keys():
            pow_tmp = med_income[year]["pow_df"][woj]
            vis_tmp = pd.concat([vis_tmp, pow_tmp], axis=0)
        vis_tmp = vis_tmp.rename(
            columns={
                "Avg_income_yearly": "Inc_yr",
                "Avg_income_monthly": "Inc_mo",
            }
        )
        vis_tmp["year"] = year
        vis = pd.concat([vis, vis_tmp], axis=0)
    # print(vis)

    rot = 90
    height = 7
    aspect = 2

    rp_yr = sns.catplot(
        data=vis,
        x="Nazwa JST",
        y="Inc_yr",
        hue="year",
        kind="bar",
        orient="v",
        col="województwo",
        col_wrap=2,
        sharex=False,
        sharey=False,
        height=height,
        aspect=aspect,
    )
    for ax in rp_yr.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(rot)
    rp_yr.fig.subplots_adjust(
        top=0.9, hspace=0.6, wspace=0.6
    )  # adjust the Figure in rp
    rp_yr.fig.suptitle("Average Yearly Income")

    rp_mo = sns.catplot(
        data=vis,
        x="Nazwa JST",
        y="Inc_mo",
        hue="year",
        kind="bar",
        orient="v",
        col="województwo",
        col_wrap=2,
        sharex=False,
        sharey=False,
        height=height,
        aspect=aspect,
    )
    for ax in rp_mo.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(rot)
    rp_mo.fig.subplots_adjust(
        top=0.9, hspace=0.6, wspace=0.6
    )  # adjust the Figure in rp
    rp_mo.fig.suptitle("Average Monthly Income")
    return vis


def vis_NPP(med_income, woj_split=True):
    vis = pd.DataFrame()
    for year in med_income.keys():
        vis_tmp = pd.DataFrame()
        for woj in med_income[year]["miasta_NPP_df"].keys():
            pow_tmp = med_income[year]["miasta_NPP_df"][woj]
            vis_tmp = pd.concat([vis_tmp, pow_tmp], axis=0)
        vis_tmp = vis_tmp.rename(
            columns={
                "Avg_income_yearly": "Inc_yr",
                "Avg_income_monthly": "Inc_mo",
            }
        )
        vis_tmp["year"] = year
        vis = pd.concat([vis, vis_tmp], axis=0)

    if woj_split:
        rot = 90
        height = 7
        aspect = 2
        rp_yr = sns.catplot(
            data=vis,
            x="Nazwa JST",
            y="Inc_yr",
            hue="year",
            kind="bar",
            orient="v",
            col="województwo",
            col_wrap=2,
            sharex=False,
            sharey=False,
            height=height,
            aspect=aspect,
        )
        for ax in rp_yr.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(rot)
        rp_yr.fig.subplots_adjust(
            top=0.9, hspace=0.6, wspace=0.6
        )  # adjust the Figure in rp
        rp_yr.fig.suptitle("Average Yearly Income")

        rp_mo = sns.catplot(
            data=vis,
            x="Nazwa JST",
            y="Inc_mo",
            hue="year",
            kind="bar",
            orient="v",
            col="województwo",
            col_wrap=2,
            sharex=False,
            sharey=False,
            height=height,
            aspect=aspect,
        )
        for ax in rp_mo.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(rot)
        rp_mo.fig.subplots_adjust(
            top=0.9, hspace=0.6, wspace=0.6
        )  # adjust the Figure in rp
        rp_mo.fig.suptitle("Average Monthly Income")
    else:
        rot = 90
        height = 7
        aspect = 3
        rp_yr = sns.catplot(
            data=vis,
            x="Nazwa JST",
            y="Inc_yr",
            hue="year",
            kind="bar",
            orient="v",
            height=height,
            aspect=aspect,
        )
        for ax in rp_yr.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(rot)
        rp_yr.fig.subplots_adjust(
            top=0.9, hspace=0.6, wspace=0.6
        )  # adjust the Figure in rp
        rp_yr.fig.suptitle("Average Yearly Income")

        rp_mo = sns.catplot(
            data=vis,
            x="Nazwa JST",
            y="Inc_mo",
            hue="year",
            kind="bar",
            orient="v",
            height=height,
            aspect=aspect,
        )
        for ax in rp_mo.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(rot)
        rp_mo.fig.subplots_adjust(
            top=0.9, hspace=0.6, wspace=0.6
        )  # adjust the Figure in rp
        rp_mo.fig.suptitle("Average Monthly Income")

    return vis


def vis_gminy(med_income):
    vis = {}
    year_plot = list(med_income.keys())[0]
    for year in med_income.keys():
        for woj in med_income[year]["gminy_dict"].keys():
            vis_tmp = pd.DataFrame()
            try:
                if not isinstance(vis[woj], pd.DataFrame):
                    vis[woj] = pd.DataFrame()
            except KeyError:
                vis[woj] = pd.DataFrame()
            for gmina in med_income[year]["gminy_dict"][woj].keys():
                gm_tmp = med_income[year]["gminy_dict"][woj][gmina]
                vis_tmp = pd.concat([vis_tmp, gm_tmp], axis=0)
            vis_tmp = vis_tmp.rename(
                columns={
                    "Avg_income_yearly": "Inc_yr",
                    "Avg_income_monthly": "Inc_mo",
                }
            )
            try:
                vis_tmp["Inc_yr"] = pd.to_numeric(
                    vis_tmp["Inc_yr"], errors="coerce"
                )
                vis_tmp["Inc_mo"] = pd.to_numeric(
                    vis_tmp["Inc_mo"], errors="coerce"
                )
                vis_tmp["year"] = year
                vis[woj] = pd.concat([vis[woj], vis_tmp], axis=0)
            except KeyError:
                continue

    for woj in med_income[year_plot]["gminy_dict"].keys():
        rot = 90
        height = 7
        aspect = 2
        rp_yr = sns.catplot(
            data=vis[woj],
            x="Nazwa JST",
            y="Inc_yr",
            hue="year",
            kind="bar",
            orient="v",
            col="powiat",
            col_wrap=2,
            sharex=False,
            sharey=False,
            height=height,
            aspect=aspect,
        )
        for ax in rp_yr.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(rot)
        rp_yr.fig.subplots_adjust(
            top=0.9, hspace=0.6, wspace=0.6
        )  # adjust the Figure in rp
        rp_yr.fig.suptitle(f"{woj} - Average Yearly Income")

        rp_mo = sns.catplot(
            data=vis[woj],
            x="Nazwa JST",
            y="Inc_mo",
            hue="year",
            kind="bar",
            orient="v",
            col="powiat",
            col_wrap=2,
            sharex=False,
            sharey=False,
            height=height,
            aspect=aspect,
        )
        for ax in rp_mo.axes.flat:
            for label in ax.get_xticklabels():
                label.set_rotation(rot)
        rp_mo.fig.subplots_adjust(
            top=0.9, hspace=0.6, wspace=0.6
        )  # adjust the Figure in rp
        rp_mo.fig.suptitle("Average Monthly Income")

    return vis
