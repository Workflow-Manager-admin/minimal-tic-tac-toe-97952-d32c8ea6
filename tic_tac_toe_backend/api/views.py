from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TicTacToeGame


@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@api_view(['POST'])
def start_game(request):
    """
    Starts a new Tic Tac Toe Game.
    Returns the initial game state and game id.
    """
    game = TicTacToeGame()
    game.reset()
    game.save()
    return Response(game.get_state(), status=status.HTTP_201_CREATED)


# PUBLIC_INTERFACE
@api_view(['POST'])
def make_move(request, game_id):
    """
    Makes a move in the given Tic Tac Toe game.
    Expects JSON: {"row": int, "col": int}
    Returns: updated game state (or error).
    """
    try:
        game = TicTacToeGame.objects.get(id=game_id)
    except TicTacToeGame.DoesNotExist:
        return Response(
            {"error": "Game not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    data = request.data
    row = data.get('row')
    col = data.get('col')
    if row is None or col is None:
        return Response(
            {"error": "row and col required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    result = game.make_move(row, col)
    if 'error' in result:
        return Response(
            {"error": result['error'], **game.get_state()},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(result)


# PUBLIC_INTERFACE
@api_view(['GET'])
def get_state(request, game_id):
    """
    Gets the current state of a Tic Tac Toe game.
    Returns: dict with board, current_player, winner, is_draw.
    """
    try:
        game = TicTacToeGame.objects.get(id=game_id)
    except TicTacToeGame.DoesNotExist:
        return Response(
            {"error": "Game not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(game.get_state())


# PUBLIC_INTERFACE
@api_view(['POST'])
def restart_game(request, game_id):
    """
    Restarts a Tic Tac Toe game (same id, new board).
    Returns: reset game state.
    """
    try:
        game = TicTacToeGame.objects.get(id=game_id)
    except TicTacToeGame.DoesNotExist:
        return Response(
            {"error": "Game not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    game.reset()
    game.save()
    return Response(game.get_state())
