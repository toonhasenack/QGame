import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


class Leaderboard():
    def __init__(self, bgcolor=(21/255, 66/255, 115/255), lettercolor=(1, 1, 1)):
        fig = plt.figure(figsize=(18, 12), facecolor=bgcolor)
        ax = plt.axes()
        ax.set_facecolor(bgcolor)

        ax.set_xlabel('Wins', size=20, color=lettercolor)

        ax.spines['bottom'].set_color(lettercolor)
        ax.spines['left'].set_color(lettercolor)
        ax.spines['right'].set_color(lettercolor)
        ax.spines['top'].set_color(lettercolor)
        ax.tick_params(axis='x', colors=lettercolor, labelsize=20)
        ax.tick_params(axis='y', colors=lettercolor, labelsize=20)

        ax.set_ylabel('Name', size=20, color=lettercolor)
        ax.set_title('Leaderboard', size=40, color=lettercolor)

        # Adjusting the layout
        # plt.tight_layout()
        self.fig = fig
        self.ax = ax
        self.bgcolor = bgcolor
        self.lettercolor = lettercolor

    def update(self):
        con = sqlite3.connect('db.sqlite3')
        results = pd.read_sql('SELECT * FROM main_player', con)
        names1 = results["name1"]
        names2 = results["name2"]
        winnum = results["winner"]

        all_names = np.concatenate([names1.values, names2.values])
        for i, name in enumerate(all_names):
            all_names[i] = name.lower()
        unique_names = np.unique(all_names)

        winners = pd.DataFrame(
            {"Times": [0]*len(unique_names)}, index=unique_names)
        for i, w in enumerate(winnum.values):
            if w == 1:
                winners.loc[names1.loc[i].lower(), "Times"] += 1
            elif w == 2:
                winners.loc[names2.loc[i].lower(), "Times"] += 1
            elif w == 3:
                winners.loc[names1.loc[i].lower(), "Times"] += 1/2
                winners.loc[names2.loc[i].lower(), "Times"] += 1/2

        winners = winners.sort_values(by="Times", ascending=True).tail(10)

        # Adding labels to the bars
        for i, v in enumerate(winners["Times"]):
            self.ax.text(v + 0.5, i, str(v), color=self.lettercolor,
                         fontweight='bold', size=20)

        self.ax.barh(winners.index, winners["Times"], color=self.lettercolor)
        self.ax.set_xlim(0, 2*winners["Times"].max())

        self.fig.savefig("main/static/Leaderboard.png")
        print("AAAAA")
        plt.close()
        con.close()
