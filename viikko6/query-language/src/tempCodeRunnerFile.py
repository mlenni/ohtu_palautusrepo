from nhl_statistics import Statistics
from player_reader import PlayerReader
from query_builder import QueryBuilder
from matchers import *

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)
    
    matcher = (
    QueryBuilder()
    .one_of(
        QueryBuilder()
        .plays_in("PHI")
        .has_at_least(10, "assists")
        .has_fewer_than(10, "goals")
        .build(),
        QueryBuilder()
        .plays_in("EDM")
        .has_at_least(50, "points")
        .build()
    ))
   

    for player in stats.matches(matcher):
        print(player)


if __name__ == "__main__":
    main()
