from django.db import models
from django.utils import timezone


class TicTacToeGame(models.Model):
    """
    A model representing a game of Tic Tac Toe.
    Stores board state, player turn, winner, and draw status.
    """
    board = models.JSONField(
        default=list,
        help_text="A 3x3 list of lists storing X, O, or ''."
    )
    current_player = models.CharField(
        max_length=1, choices=[('X', 'X'), ('O', 'O')], default='X'
    )
    winner = models.CharField(
        max_length=1, choices=[('X', 'X'), ('O', 'O'), ('', 'None')],
        blank=True, default=''
    )
    is_draw = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # PUBLIC_INTERFACE
    def reset(self):
        """Resets the game to the initial state."""
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.current_player = 'X'
        self.winner = ''
        self.is_draw = False

    # PUBLIC_INTERFACE
    def make_move(self, row: int, col: int) -> dict:
        """
        Makes a move at the specified board location if valid.
        Returns a dict with updated state info & error if any.
        """
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return {'error': 'Move out of bounds.'}
        if self.winner or self.is_draw:
            return {'error': 'Game has already ended.'}
        if self.board[row][col]:
            return {'error': 'Cell already occupied.'}
        self.board[row][col] = self.current_player
        self._update_game_status()
        if not self.winner and not self.is_draw:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.save()
        return self.get_state()

    def _update_game_status(self):
        """Internal: checks for winner/draw and updates fields."""
        lines = self.board + [list(col) for col in zip(*self.board)]
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])
        for line in lines:
            if line == ['X', 'X', 'X']:
                self.winner = 'X'
                return
            if line == ['O', 'O', 'O']:
                self.winner = 'O'
                return
        if all(cell for row in self.board for cell in row):
            self.is_draw = True

    # PUBLIC_INTERFACE
    def get_state(self) -> dict:
        """Returns a dictionary with current game state for frontend."""
        return {
            'id': self.id,
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner if self.winner else None,
            'is_draw': self.is_draw,
        }

    def __str__(self):
        return (
            f"TicTacToeGame {self.id} "
            f"({self.current_player}'s turn, winner={self.winner}, "
            f"draw={self.is_draw})"
        )
