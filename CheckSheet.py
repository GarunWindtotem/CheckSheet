import pandas as pd  # Daten
from matplotlib import pyplot as plt  # plots
import numpy as np
# für Timeseries Daten
from datetime import datetime
from datetime import date  # todays date

# import os
now = datetime.now()

today = date.today().strftime("%d.%m.%Y")

# MESSUNG DEFINIEREN

##### DATAFRAME #####
soll = 60
OT = 35
UT = 10
toleranz = OT + UT
### laufende Mittelwerte / Standardabweichung anzeigen ja/nein?
rolling_bool = True

### Datum Achse ja/nein
date_axis = False

#### TextBox an/aus
text_box = False

### DIAGRAMM ####
### WIE SOLL DAS DIAGRAMM UND FILE BESCHRIFTET SEIN?
chart_name = "Testdaten Validierung v1_1"
plot_title = 'Qualitätsregelkarte - Testdaten Luftfeuchtigkeit\n'
plot_subtitle = f'{today} PW - Testdaten'
ylabel = "Luftfeuchtigkeit [%]"

if date_axis == True:
    xlabel = "Datum"
else:
    xlabel = "Messung Nr."

# größe der Texte im Chart
size = 45
sizefactor_title = 0.8
sizefactor_subtitle = 0.65
sizefactor_textbox = 0.5
sizefactor_xyticks = 0.5
sizefactor_xylabel = 0.7
sizefactor_marker = 0.2
sizefactor_marker2 = sizefactor_marker * 0.5
sizefactor_legend = 0.7
y_subtitle = 0.98


# Linien Stärke
lws = 3
lwb = 7

# Farben
rot = '#f80d0d'
cyan = '#25e5e5'
blau = '#0721ff'
lila = '#bb8fce'
gruen = '#18c213'
schwarz = '#000000'
orange = '#faac2b'

### eher unveränderliche label (standards)
plot_label_OTUT = "OTG, UTG"
plot_label_SOLL = "SOLL"
plot_label_Mittelwert = "Mittelwert"

pfad = "D:\\Github\\CheckSheet\\"  # Zuhause Pfad
# pfad = "C:\\Users\\p.waitz\\Python\\CheckSheet\\"   # Geschäftsrechner Pfad
pfad_input = "Input\\df_input.csv"
pfad_output = "Output\\"

pfad_onedrive = "D:\\OneDrive\\CheckSheet\\"

# xticks
rotation = 0

# Bezugsschriftgröße

# output größe der bilder
h = 16 * 1.49
v = 9 * 0.97
dpi = 200

# CSV einlesen
df = pd.read_csv(pfad + pfad_input, sep=";", decimal=',')

### 10 % der Datenwerte
if len(df["value"]) < 40:
    rolling_anzahl = 3
    rolling_anzahl2 = 2
else:
    rolling_anzahl = int(len(df["value"]) * 0.1)
    rolling_anzahl2 = int(len(df["value"]) * 0.05)

# df["SOLL"] = soll
df["OTG"] = soll + OT
df["UTG"] = soll - UT
df["SOLL"] = soll

sigma = df["value"].std()
mean = df["value"].mean()

df["value_mean"] = mean
df["value_std+"] = mean + sigma
df["value_std-"] = mean - sigma

df["mean_rolling"] = df.value.rolling(window=rolling_anzahl, min_periods=1).mean()
df["mean_rolling2"] = df.value.rolling(window=rolling_anzahl2, min_periods=1).mean()
df["std_rolling+"] = df["mean_rolling"] + df.value.rolling(window=rolling_anzahl, min_periods=1, center=True).std()
df["std_rolling-"] = df["mean_rolling"] - df.value.rolling(window=rolling_anzahl, min_periods=1, center=True).std()



if text_box == True:
    df["streuung_prozent"] = 100 * ((df["std_rolling+"] - df["mean_rolling"]) / toleranz)
    streuung_min = round(df["streuung_prozent"].min(), 1)
    streuung_max = round(df["streuung_prozent"].max(), 1)
    streuung_mittel = ((df["value_std+"] - df["value_mean"]).mean()) / toleranz

k = (df["OTG"].max() - df["UTG"].max())  # Spannweite zwischen OTG und UTG

if df["value"].max() > df["OTG"].max():
    y = float(max(df["value"]) - k * 0.2)  # Referenzpunkt soll sein: OTG - 10% der Spannweite
else:
    y = float(max(df["OTG"]) - k * 0.2)  # Referenzpunkt soll sein: OTG - 10% der Spannweite

x = float((1 / 2) * df["x_axis"].count() + 1)

OTG = df["OTG"].max()

df.to_csv(pfad + pfad_output + "df.csv")

x_axis = df["x_axis"].tolist()
len(x_axis)

# def y_axis_thousands(x, pos):
#    # 'The two args are the value and tick position'
#     return '{:0,d}'.format(int(x)).replace(",",".")
# formatter = FuncFormatter(y_axis_thousands)

# fig = plt.figure(figsize=(h,v))
# ax = fig.add_subplot()
# ax.yaxis.set_major_formatter(formatter)
plt.figure(figsize=(h, v))

plt.style.use('seaborn')
plt.grid(True)

### SOLL, OTG, UTG ###
plt.plot(df.x_axis, df.OTG, color='red', linestyle='dashed', linewidth=lws, label=plot_label_OTUT)
plt.plot(df.x_axis, df.SOLL, color='green', linestyle='dashed', linewidth=lws, label=plot_label_SOLL)
plt.plot(df.x_axis, df.UTG, color='red', linestyle='dashed', linewidth=lws, label="")

### values ###
plt.plot(df.x_axis, df['value'], marker='.', linestyle='',
         color="grey", linewidth=lws, label="Einzelmesswerte", markersize=size * sizefactor_marker)

### Darstellung der rolling Darstellung oder mit konstanten Werten
if rolling_bool == True:
    # rolling
    plt.plot(df.x_axis, df['mean_rolling'], marker='', linestyle='-', color=schwarz, linewidth=lwb,
             label=f'laufender Mittelwert ({rolling_anzahl})', markersize=size * sizefactor_marker)
    plt.plot(df.x_axis, df['mean_rolling2'], marker='', linestyle='-', color="black", alpha=0.55, linewidth=lws,
             label=f'laufender Mittelwert ({rolling_anzahl2})', markersize=size * sizefactor_marker2)

    plt.plot(df.x_axis, df['std_rolling+'], marker='', linestyle='', color=schwarz, linewidth=lws,
             label='', markersize=size * sizefactor_marker)
    plt.plot(df.x_axis, df['std_rolling-'], marker='', linestyle='', color=schwarz, linewidth=lws,
             label='', markersize=size * sizefactor_marker)
    plt.fill_between(df.x_axis, df['std_rolling+'], df['std_rolling-'], color='grey', alpha=0.5, label
    =f'laufendes sigma ({rolling_anzahl})')

    if text_box == True:
        plt.text(x - 0.5, y,
                 f'Streuung mittel = {round((100) * sigma / toleranz, 1)} % ({round(100 / ((100) * sigma / toleranz), 1)} sigma)\n min = {streuung_min} %,   max = {streuung_max} %',
                 horizontalalignment='center', size=size * sizefactor_textbox, style='italic',
                 bbox={'facecolor': "blue", 'alpha': 0.5, 'pad': 5})

else:
    plt.plot(df.x_axis, df["value_mean"], color='grey', linestyle='-.', linewidth=lws, label=plot_label_Mittelwert)
    plt.plot(df.x_axis, df["value_std+"], color='grey', linestyle='-', linewidth=lws, label="")
    plt.plot(df.x_axis, df["value_std-"], color='grey', linestyle='-', linewidth=lws, label="")
    plt.fill_between(df.x_axis, df['value_std+'], df['value_std-'], color='grey', alpha=0.5, label="±1 sigma")

    if text_box == True:
        plt.text(x - 0.5, y,
                 r'mittlere Streuung =  $\frac{sigma\ }{(1/2)\cdot(OTG\ - UTG)\ }\cdot100$ = 'f'{round((100) * sigma / toleranz, 1)} % (= {round(100 / ((100) * sigma / toleranz), 1)} sigma)',
                 horizontalalignment='center', size=size * sizefactor_textbox, style='italic',
                 bbox={'facecolor': "blue", 'alpha': 0.5, 'pad': 5})

# Legende
plt.legend(loc='upper center',
           bbox_to_anchor=(0.5, -0.2),
           fancybox=True,
           shadow=True,
           ncol=3,
           fontsize=size * sizefactor_legend)

# Schriftgrößen x und y achsenwerte
# plt.margins(x=0)
plt.xticks(fontsize=size * sizefactor_xyticks, rotation=rotation)
plt.yticks(fontsize=size * sizefactor_xyticks)

plt.ylabel(ylabel, fontsize=size * sizefactor_xylabel)
plt.xlabel(xlabel, fontsize=size * sizefactor_xylabel)

plt.title(f'{plot_title}\n', fontsize=size * sizefactor_title)
plt.suptitle(plot_subtitle, fontsize=size * sizefactor_subtitle, y=y_subtitle)

x_axis = df["x_axis"].tolist()
if max(x_axis) > 10:
    plt.xticks(np.arange(min(x_axis), max(x_axis) + 1, round(max(x_axis) / 10)))  # Teile x-achse in 10 Teile
elif max(x_axis) <= 10:
    plt.xticks(np.arange(min(x_axis), max(x_axis) + 1, 1))  # Teile x-achse nicht

# Diagramm als Bild exporieren und Auflösung definieren

if rolling_bool == True:
    plt.savefig(pfad + pfad_output + chart_name + ".png", dpi=dpi, bbox_inches='tight')
    # plt.savefig(pfad_onedrive + "diagram dynamic mean.png", dpi = dpi, bbox_inches='tight')
else:
    plt.savefig(pfad + pfad_output + chart_name + ".png", dpi=dpi, bbox_inches='tight')
    # plt.savefig(pfad_onedrive + "diagram static mean.png", dpi = dpi, bbox_inches='tight')

# plt.show()
