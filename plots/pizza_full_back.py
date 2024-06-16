from urllib.request import urlopen

import matplotlib.pyplot as plt
from PIL import Image
import sqlite3
import pandas as pd

from mplsoccer import PyPizza, add_image, FontManager

# Getting fonts for visual
font_normal = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/IBMPlexSans-Regular.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/IBMPlexSans-Italic.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/IBMPlexSans-Bold.ttf')


# Creating a connection to database, selecting all rows from VIEW created to select relevant stats from DF players with >10.0 90s. Storing results in dataframe.
conn = sqlite3.connect(r"C:\Users\Owner\dev\23_24_player_stats\data\23_24_player_stats.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM PIZZA_FULL_BACK")
rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
df = pd.DataFrame(rows, columns=column_names)
print(df)
conn.close()



# parameter and value list
# The values are taken from the excellent fbref website (supplied by StatsBomb)
params = ['xA', 'Penalty Area Entries', 'Deep Progressions', 'Progressive Actions',
          'Turnovers', 'Errors', 'PAdj Tck+Int', 'Tack/Dribbled Past %', 'Fouls',
          'Aerial Win %']

# Convert the relevant columns to percentiles
df_percentiles = df.copy()
df_percentiles[params] = df_percentiles[params].rank(pct=True) * 100

# Reverse the percentiles for 'Fouls' and 'Errors' as lower values are better
df_percentiles['Fouls'] = 100 - df_percentiles['Fouls']
df_percentiles['Errors'] = 100 - df_percentiles['Errors']

# Select a player
player_name = "Takehiro Tomiyasu"
values = df_percentiles[df_percentiles['Player'] == player_name][params].values.flatten()
values = [round(val) for val in values]

# color for the slices and text
slice_colors = ["#1A78CF"] * 2 + ["#FF9300"] * 4 + ["#d70232"] * 4
text_colors = ["#000000"] * 10

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    background_color="#222222",     # background color
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_color="#000000",    # color for last line
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
    inner_circle_size=20            # size of inner circle
)

# plot pizza
fig, ax = baker.make_pizza(
    values,                          # list of values
    figsize=(8, 8.5),                # adjust the figsize according to your need
    color_blank_space="same",        # use the same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#000000", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
        color="#F2F2F2", fontsize=11,
        fontproperties=font_normal.prop, va="center"
    ),                               # values to be used when adding parameter labels
    kwargs_values=dict(
        color="#F2F2F2", fontsize=11,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values labels
)

# add title
fig.text(
    0.5, 0.975, f"{player_name} - {df[df["Player"] == player_name]["Squad"].values[0]}", size=16,
    ha="center", fontproperties=font_bold.prop, color="#F2F2F2"
)

# add subtitle
fig.text(
    0.5, 0.945,
    f"Season 2023-24 | {df[df["Player"] == player_name]["90s"].values[0]} Games Played",
    size=13,
    ha="center", fontproperties=font_bold.prop, color="#F2F2F2"
)

# add credits
CREDIT_1 = "data: Opta via fbref"
CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"

fig.text(
    0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=9,
    fontproperties=font_italic.prop, color="#F2F2F2",
    ha="right"
)

# add text
fig.text(
    0.32, 0.91, "Attacking        Possession       Defending", size=14,
    fontproperties=font_bold.prop, color="#F2F2F2"
)

fig.text(
    0.01, 0.02,
    "Percentile Rank vs Top-Five League Full Backs",
    fontproperties=font_italic.prop,
    ha="left", color="#F2F2F2"
)

# add rectangles
fig.patches.extend([
    plt.Rectangle(
        (0.29, 0.9025), 0.025, 0.021, fill=True, color="#1a78cf",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.442, 0.9025), 0.025, 0.021, fill=True, color="#ff9300",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.612, 0.9025), 0.025, 0.021, fill=True, color="#d70232",
        transform=fig.transFigure, figure=fig
    ),
])
# # add image
# ax_image = add_image(
#     fdj_cropped, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
# )   # these values might differ when you are plotting

plt.show()