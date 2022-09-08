from bs4 import BeautifulSoup
import requests
import csv

url = "https://mgoblue.com/sports/softball/stats/2021"
soup = BeautifulSoup(requests.get(url).text, 'html.parser')

players = soup.find_all('tr')
player_names = []
for player in players:
    ths = player.find('th')
    try:
        a = ths.find('a', {'data-player-id':True})
        player_names.append(a.text)
    except:
        continue

hits = [int(x.text) for x in soup.find_all('td', {'data-label':'H'})]
bb = [int(x.text) for x in soup.find_all('td', {'data-label':'BB'})]
hbp = [int(x.text) for x in soup.find_all('td', {'data-label':'HBP'})]
tb = [int(x.text) for x in soup.find_all('td', {'data-label':'TB'})]
ab = [int(x.text) for x in soup.find_all('td', {'data-label':'AB'})]
gdp = [int(x.text) for x in soup.find_all('td', {'data-label':'GDP'})]
sf = [int(x.text) for x in soup.find_all('td', {'data-label':'SF'})]
sh = [int(x.text) for x in soup.find_all('td', {'data-label':'SH'})]
sbatt = [x.text for x in soup.find_all('td', {'data-label':'SB'})]

cs = []
for sb in sbatt:
    s = sb.split('-')
    try:
        c = int(s[1]) - int(s[0])
        cs.append(c)
    except:
        continue

stats = {}
counter = 0
for player in player_names:
    stats[player] = {'hits':hits[counter], 'bb':bb[counter], 'hbp':hbp[counter], 'tb': tb[counter], 'ab':ab[counter], 'gdp':gdp[counter], 'sf':sf[counter], 'sh':sh[counter], 'cs':cs[counter]}
    counter += 1
    if player == 'Gonzalez, Thais':
        break

player_rcs = []
for player in stats:
    rc = ((stats[player]['hits'] + stats[player]['bb'] + stats[player]['hbp']) * stats[player]['tb'])/(stats[player]['ab'] + stats[player]['bb'] + stats[player]['hbp'])

    outs = 0.982 * stats[player]['ab'] - stats[player]['hits'] + stats[player]['gdp'] +stats[player]['sf'] + stats[player]['sh'] + stats[player]['cs']

    games = outs/21

    final_rc = round(rc/games, 2)

    player_rcs.append((player, final_rc))

with open('umsoftball_2021rc.csv', "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["player", "rc"])
    csvwriter.writerows(player_rcs)
