class TennisGame:
    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.scores = {player1_name: 0, player2_name: 0}

    def won_point(self, player_name):
        if player_name in self.scores:
            self.scores[player_name] += 1

    def get_score(self):
        score1, score2 = self.scores[self.player1_name], self.scores[self.player2_name]

        if score1 == score2:
            return self._get_equal_score(score1)

        if score1 >= 4 or score2 >= 4:
            return self._get_advantage_or_win(score1, score2)

        return f"{self.SCORE_NAMES[score1]}-{self.SCORE_NAMES[score2]}"

    def _get_equal_score(self, score):
        if score < 3:
            return f"{self.SCORE_NAMES[score]}-All"
        return "Deuce"

    def _get_advantage_or_win(self, score1, score2):
        score_diff = score1 - score2

        if score_diff == 1:
            return f"Advantage {self.player1_name}"
        if score_diff == -1:
            return f"Advantage {self.player2_name}"
        if score_diff >= 2:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"
