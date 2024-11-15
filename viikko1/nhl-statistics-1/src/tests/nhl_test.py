import unittest
from statistics_service import StatisticsService
from statistics_service import SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_player_found(self):
        result = self.stats.search("Semenko")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Semenko")

    def test_search_player_not_found(self):
        result = self.stats.search("lenni")
        self.assertIsNone(result)
    
    def test_team_with_players(self):
        result = self.stats.team("EDM")
        self.assertEqual(len(result), 3)
        self.assertTrue(all(player.team == "EDM" for player in result))

    def test_team_no_players(self):
        result = self.stats.team("LEN")
        self.assertEqual(result, [])
    
    def test_top_players(self):
        result = self.stats.top(2)
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].points >= result[1].points)

    def test_top_zero_players(self):
        result = self.stats.top(0)
        self.assertEqual(result, [])
        
        
    def test_top_sort_by_points(self):
        result = self.stats.top(3, SortBy.POINTS)
        self.assertEqual(result[0].name, "Gretzky")
        self.assertEqual(result[1].name, "Lemieux")
        self.assertEqual(result[2].name, "Yzerman")

    def test_top_sort_by_goals(self):
        result = self.stats.top(3, SortBy.GOALS)
        self.assertEqual(result[0].name, "Lemieux")
        self.assertEqual(result[1].name, "Yzerman")
        self.assertEqual(result[2].name, "Kurri")

    def test_top_sort_by_assists(self):
        result = self.stats.top(3, SortBy.ASSISTS)
        self.assertEqual(result[0].name, "Gretzky")
        self.assertEqual(result[1].name, "Yzerman")
        self.assertEqual(result[2].name, "Lemieux")
