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
    # print(vis)

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
