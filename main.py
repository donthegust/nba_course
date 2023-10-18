from nba_api.stats.endpoints import alltimeleadersgrids, playercareerstats, leagueleaders
from nba_api.stats.library.parameters import Season

import matplotlib.pyplot as plt
import numpy as np

# Grafico de calor - maiores pontuadores ----------------------------------------------------
# captura os dados dos top 20 de jogadores lideres da liga
top_players = leagueleaders.LeagueLeaders(season = Season.previous_season).league_leaders.get_data_frame().head(20)

# definindo as variaveis utilizadas
players = []
heatData = []
seasons = []

# preenchendo de forma dinamica essas variaveis
players = np.array(top_players['PLAYER'].head(5))
for x in range(len(players)):    
    letCareer = playercareerstats.PlayerCareerStats(player_id=top_players['PLAYER_ID'][x]).season_totals_regular_season.get_data_frame().sort_values(by='SEASON_ID', ascending=False)
    heatData.insert(x, np.array(letCareer['PTS'].head(len(players))))
seasons = np.array(letCareer['SEASON_ID'].head(len(players)))

# cria o subplot e o define com um mapa de cores
fig, ax = plt.subplots()
im = ax.imshow(heatData, cmap='viridis', aspect='auto')

# define os rótulos de cada eixo
ax.set_yticks(np.arange(len(players)), labels=players)
ax.set_xticks(np.arange(len(seasons)), labels=seasons)

# rotaciona os titulos verticais em 45 graus
plt.setp(ax.get_yticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# cria as legendas de forma dinamica no grafico
for i in range(len(seasons)):
    for j in range(len(players)):
        text = ax.text(j, i, heatData[i][j],
                       ha="center", va="center", color="r")

# defina o mapa de cores do graficos
cbar = ax.figure.colorbar(im, ax=ax)

# define o titulo do grafico
ax.set_title("5 maiores pontuadores da liga")
# plt.show()


# Grafico de dispersão - Turnover por Assistencias ----------------------------------------------------
# gera aleatóriamente as cores do nosso pontos na dispersão
colors = np.random.rand(15)

# cria o subplot
fig, ax = plt.subplots()

# definindo as variaveis utilizadas
ast = np.array(top_players['AST'].head(len(colors)))
tov = np.array(top_players['TOV'].head(len(colors)))

# calcula o tamanho dos pontos na dispersão
sizes = (ast + tov)

# define os rótulos de cada eix
ax.set_xlabel('Assistencias')
ax.set_ylabel('Turnovers')

# define o grafico como um de dispersão
ax.scatter(ast, tov, s=sizes, c=colors, alpha=0.5)

# cria as legendas de forma dinamica no grafico
for i in range(len(tov)):
    ax.annotate(top_players['PLAYER'][i], (ast[i], tov[i]), textcoords="offset points", xytext=(0, 10), ha='center')

# define o titulo do grafico
ax.set_title('Turnover por Assistencias')
# plt.show()


# Grafico de barras - maiores pontuadores ----------------------------------------------------
# captura os dados dos maiores pontuadores da liga
allTime = alltimeleadersgrids.AllTimeLeadersGrids().pts_leaders.get_data_frame()

# cria o subplot
fig, ax = plt.subplots()

# definindo as variaveis utilizadas
players = np.array(allTime['PLAYER_NAME'].head(7))
points = np.array(allTime['PTS'].head(7))
games = []

for x in allTime['PLAYER_ID'].head(7):
    letCareer = playercareerstats.PlayerCareerStats(player_id=x).career_totals_regular_season.get_data_frame()
    games.insert(x, float(format(letCareer['PTS'][0]/letCareer['GP'][0], ".1f")))

# define o grafico como de barras
bars = ax.bar(players, points)

# define os rótulos de cada eixo
ax.set_ylabel('Pontos')
ax.set_xlabel('Jogadores')

# rotaciona os titulos verticais em 45 graus
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# cria as legendas de forma dinamica no grafico
for bar, valor in zip(bars, points):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(valor), ha='center')

ax2 = ax.twinx()
ax2.set_ylabel('Média de Pontos')
ax2.plot(players, games, marker='o', color='red', label='Média de Pontos')
for categoria, valor in zip(players, games):
    ax2.text(categoria, valor, str(valor), ha='center', va='bottom', color='red')
legend = ax2.legend(loc='lower left', shadow=True, fontsize='x-large')

# define o titulo do grafico
ax.set_title('Maiores pontuadores da história')
# plt.show()



# Grafico de linha - pontuções na temporada ----------------------------------------------------
# captura os dados de temporada regular de algum jogadors
regularSeasonData = playercareerstats.PlayerCareerStats(player_id='165').season_totals_regular_season.get_data_frame()

# definindo as variaveis utilizadas
seasonIDs = regularSeasonData['SEASON_ID']
seasonOREB = regularSeasonData['OREB']
seasonDREB = regularSeasonData['DREB']
seasonREB = regularSeasonData['REB']

# cria o subplot
fig, ax = plt.subplots()

# define o grafico como de linhas (cada ax.plot é uma nova linha)
ax.plot(seasonIDs, seasonOREB, marker='o', label='Rebotes Ofensivos')
for categoria, valor in zip(seasonIDs, seasonOREB):
    ax.text(categoria, valor, str(valor), ha='center', va='bottom')
ax.plot(seasonIDs, seasonDREB, marker='o', label='Rebotes Defensivos')
for categoria, valor in zip(seasonIDs, seasonDREB):
    ax.text(categoria, valor, str(valor), ha='center', va='bottom')
ax.plot(seasonIDs, seasonREB, marker='o' ,label='Rebotes Totais')
for categoria, valor in zip(seasonIDs, seasonREB):
    ax.text(categoria, valor, str(valor), ha='center', va='bottom')

# cria a legenda do grafico
legend = ax.legend(loc='upper left', shadow=True, fontsize='x-large')

# define os rótulos de cada eixo
ax.set_xlabel('Temporada')
ax.set_ylabel('Pontos')

# define o titulo do grafico
ax.set_title('Média de rebotes na carreira - Hakeem Olajuwon')
# plt.show()


# Grafico de pizza - franquias x cp3 ----------------------------------------------------
# captura os dados dos da carreira de determinado jogador
regularSeasonData = playercareerstats.PlayerCareerStats(player_id='101108').season_totals_regular_season.get_data_frame()

# definindo as variaveis utilizadas
regularSeasonMap = regularSeasonData['TEAM_ABBREVIATION'].value_counts().to_dict()
total = sum(regularSeasonMap.values())

# cria o subplot
fig, ax = plt.subplots()

# define o grafico como de pizza
wedges, texts, autotexts = ax.pie(regularSeasonMap.values(), labels = regularSeasonMap.keys(), startangle=90, autopct='', pctdistance=0.85)

# cria as legenda do grafico
ax.legend(wedges, regularSeasonMap.values(),
          title="Temporadas",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

# define o titulo do grafico
ax.set_title('Total de temporadas por franquias - CP3')
plt.show()