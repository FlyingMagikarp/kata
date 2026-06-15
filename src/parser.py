import re
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup


def parse_article_data(article):
    if article.find('footer') is None:
        return None
    if article.find('footer').find('strong').getText() == '':
        return None
    player_name = article.find('div', class_='player-info').find('div').find('strong').getText()
    player_name = re.sub(r"\s+", " ", player_name).strip()
    player_id = article.find('div', class_='player-card').get('data-athlete-id')
    kata_nr, kata_name = article.find('footer').find('strong').getText().split(' ', 1)
    winner = article.find('div', class_='player-card player-loser') is None

    return {
        'player_name': player_name,
        'player_id': player_id,
        'kata_nr': kata_nr,
        'kata_name': kata_name,
        'winner': winner
    }


def parse_html_file(raw_file: Path) -> pd.DataFrame:
    html = raw_file.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, features='html.parser')
    players = soup.find_all('article', class_='player')

    rows = []
    for player in players:
        parsed = parse_article_data(player)
        if parsed is not None:
            rows.append(parsed)

    return pd.DataFrame(rows)