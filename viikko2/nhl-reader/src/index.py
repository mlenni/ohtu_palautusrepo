import requests
from player import Player
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

class PlayerReader:
    def __init__(self, url):
        self.url = url
        
        
    def get_players(self):
        response = requests.get(self.url).json()
        if isinstance(response, list):
            print("ok")
        else:
            print("we done fucked up")
            return []
        return [Player(dict) for dict in response]


class PlayerStats:
    def __init__(self, reader: PlayerReader):
        self.players = reader.get_players()
        
    
    def top_scorers_by_nationality(self, nationality):
        nat_players = [player for player in self.players if player.nationality == nationality]
        return sorted(nat_players, key=lambda player: player.goals + player.assists, reverse=True)


def show_players(players, nationality, season):
    console = Console()
    table = Table(title=f"Top scorers of {nationality} for the season {season}")
    table.add_column("name", style="cyan", justify="left")
    table.add_column("team", style="magenta", justify="center")
    table.add_column("goals", style="green", justify="right")
    table.add_column("assists", style="green", justify="right")
    table.add_column("points", style="green", justify="right")
    
    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists)
        )
    
    console.print(table)
        
    
def main():
    console = Console()
    
    season = Prompt.ask("Select season", choices=["2018-19", "2019-20", "2020-21", 
        "2021-22", "2022-23", "2023-24", "2024-25"], default="2024-25")
    nationality = Prompt.ask("Select nationality", choices=["AUT", "CZE", "AUS", "SWE",
        "GER", "DEN", "SUI", "SVK", "NOR", "RUS", "CAN", "LAT", "BLR", "SLO", "USA", "FIN", "GBR"], default="FIN")
    
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    print(url)
    
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    top_players = stats.top_scorers_by_nationality(nationality)
    
    show_players(top_players, nationality, season)


if __name__ == "__main__":
    main()
    