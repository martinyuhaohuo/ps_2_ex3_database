import seaborn
import matplotlib.pyplot as plt
import pandas as pd


def plot_avg_points_led(pts_team_year: pd.DataFrame) -> None:
    temp_frame = (
        pts_team_year.loc[pts_team_year.groupby(by="year")["avg_pts"].idxmax()]
        .sort_values("year")
        .tail(10)
    )
    teams = temp_frame["abbreviation"].unique()
    palette = seaborn.color_palette("inferno", len(teams))
    team_colors = dict(zip(teams, palette))
    plt.figure(figsize=(10, 6))

    for team, subframe in temp_frame.groupby(by="abbreviation"):
        plt.bar(subframe["year"], subframe["avg_pts"], color=team_colors[team])

    for _, row in temp_frame.iterrows():
        plt.text(
            row["year"], row["avg_pts"] + 2, row["abbreviation"], ha="center"
        )

    plt.xlabel("Year")
    plt.xticks(range(2014, 2024), rotation=45)
    plt.ylabel("Avg Points")
    plt.title("NBA Teams with Highest Average Points Per Year (From 2014)")
    plt.show()


def plot_avg_attend(team_attendance: pd.DataFrame) -> None:
    plt.figure(figsize=(16, 6))

    for _, row in team_attendance.iterrows():
        plt.text(
            row["abbreviation"],
            row["avg_atend"] + 2,
            str(int(row["avg_atend"] / 1000)) + "k",
            ha="center",
        )

    plt.bar(
        team_attendance["abbreviation"],
        team_attendance["avg_atend"],
        color="coral",
    )
    plt.xlabel("Team Name")
    plt.xticks(rotation=45)
    plt.ylabel("Avg Attendence")
    plt.grid(axis="y", linestyle="-", alpha=0.3)
    plt.title("Avg Attendece at Home Games by NBA Teams in Past Two Decades")
    plt.tight_layout()
    plt.show()
