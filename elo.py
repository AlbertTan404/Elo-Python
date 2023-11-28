"""
@author: Albert Tan
@date: 2023-11-28
"""

import numpy as np
import matplotlib.cm as cm  
import matplotlib.pyplot as plt  
from typing import List


class Elo:    
    def __init__(self, players: List[str] = {}, initial_rating: int = 1500, k_factor: int = 32):  
        """Initialize the Elo rating system with a default rating and k-factor.  
  
        :param players: Initial players
        :param initial_rating: The initial rating for a new player.
        :param k_factor: The factor used in Elo rating calculation.
        """
        self.players = {player_name: initial_rating for player_name in players}
        self.initial_rating = initial_rating  
        self.k_factor = k_factor  
        self.matches = []
    
    def add_player(self, name: str) -> None:  
        """Add a new player with the initial rating.  
  
        :param name: The name of the new player.  
        """  
        if name in self.players.keys():
            print(f'WARNING: player {name} already exists')
            return
        self.players[name] = self.initial_rating  
    
    def _expected_score(self, player1: str, player2: str) -> float:  
        """Calculate the expected score (probability of winning) of player1 against player2.  
  
        :param player1: The name of the first player.  
        :param player2: The name of the second player.  
        """  
        rating1 = self.players[player1]  
        rating2 = self.players[player2]  
        return 1 / (1 + 10 ** ((rating2 - rating1) / 400))  
    
    def _update_rating(self, player1: str, player2: str, score1: float) -> None:  
        """Update the rating of player1 based on their score in a match against player2.  
  
        :param player1: The name of the first player.  
        :param player2: The name of the second player.  
        :param score1: The score of the first player.  
        """  
        expected1 = self._expected_score(player1, player2)  
        rating1 = self.players[player1]  
        self.players[player1] = rating1 + self.k_factor * (score1 - expected1)  
    
    def from_txt(self, file_path: str):
        try:
            with open(file_path, 'r') as f:
                matches = f.readlines()
        except FileNotFoundError as e:
            print(f'In {self.__class__}.from_text: {e}')
        
        try:
            for match in matches:
                match = match.strip().split()
                self.add_match_result(player1=match[0], player2=match[1], score1=float(match[2]))
        except Exception as e:
            print(f'In {self.__class__}.from_text: {e}')
  
    def add_match_result(self, player1: str, player2: str, score1: float) -> None:  
        """Record the result of a match between two players.  
  
        :param player1: The name of the first player.  
        :param player2: The name of the second player.  
        :param score1: The score of the player1: 1-win, 0.5-draw, 0-lose.  
        """  
        if score1 not in (1, 0.5, 0):
            print(f'WARNING: invalid competition result for ({player1} {player2} {score1}): score1 must be 1 (win) or 0.5 (draw) or 0 (lose)')
            return

        if player1 not in self.players:  
            self.add_player(player1)  
        if player2 not in self.players:  
            self.add_player(player2)  
        
        self.matches.append((player1, player2, score1))
    
        self._update_rating(player1, player2, score1)  
        self._update_rating(player2, player1, 1 - score1)  
    
    def print_rating(self):
        players_ratings = list(self.players.items())  
        players_ratings.sort(key=lambda x: x[1], reverse=True)  
        print('==========================================================')
        print('Results:')
        print([f"{player}: {rating}" for player, rating in players_ratings])
        print('==========================================================')
 
    def plot_ratings(self, save_path='rank_list.png') -> None:  
        players_ratings = list(self.players.items())  
        players_ratings.sort(key=lambda x: x[1], reverse=True)  
        players, ratings = zip(*players_ratings)  
        colors = cm.rainbow(np.linspace(0, 1, len(players)))  
  
        plt.bar(players, ratings, color=colors)  
        plt.xlabel('Players')  
        plt.ylabel('Ratings')  
        plt.title('Player Ratings')  
        plt.savefig(save_path)  


elo = Elo()
elo.from_txt(file_path='matches.txt')
elo.add_player('f')
elo.add_player('c')
elo.add_match_result('a', 'b', 1)
elo.add_match_result('b', 'c', 0.5)
elo.add_match_result('c', 'd', 0)
elo.add_match_result('d', 'e', 0.5)
elo.add_match_result('e', 'f', -1)

elo.print_rating()
elo.plot_ratings(save_path='rank_list.png')
