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
    On error, returns details.
    """
    try:
        game = TicTacToeGame()
        game.reset()
        game.save()
        return Response(game.get_state(), status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"error": f"Could not start game: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# PUBLIC_INTERFACE
@api_view(['POST'])
def make_move(request, game_id):
    """
    Makes a move in the given Tic Tac Toe game.
    Expects JSON: {"row": int, "col": int}
    Returns: updated game state or error details.
    """
    try:
        game = TicTacToeGame.objects.get(id=game_id)
    except TicTacToeGame.DoesNotExist:
        return Response(
            {"error": "Game not found.", "game_id": game_id},
            status=status.HTTP_404_NOT_FOUND
        )

    # Defensive: handle wrong content type (non-JSON POST)
    data = request.data if hasattr(request, "data") else {}
    row = data.get('row')
    col = data.get('col')
    # Defensive type checks
    if row is None or col is None:
        return Response(
            {"error": "row and col required.", "received": {"row": row, "col": col}},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        row = int(row)
        col = int(col)
    except (TypeError, ValueError):
        return Response(
            {"error": "row and col must be integers.", "received": {"row": row, "col": col}},
            status=status.HTTP_400_BAD_REQUEST
        )

    result = game.make_move(row, col)
    if 'error' in result:
        # Also provide board state for frontend context
        error_state = game.get_state()
        error_state["error"] = result['error']
        return Response(
            error_state,
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(result)


# PUBLIC_INTERFACE
@api_view(['GET'])
def get_state(request, game_id):
    """
    Gets the current state of a Tic Tac Toe game.
    Returns: dict with board, current_player, winner, is_draw, or error.
    """
    try:
        game_id_int = int(game_id)
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid game_id provided (must be int).", "game_id": game_id},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        game = TicTacToeGame.objects.get(id=game_id_int)
    except TicTacToeGame.DoesNotExist:
        return Response(
            {"error": "Game not found.", "game_id": game_id},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Unexpected error: {str(e)}", "game_id": game_id},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(game.get_state())


# PUBLIC_INTERFACE
@api_view(['POST'])
def restart_game(request, game_id):
    """
    Restarts a Tic Tac Toe game (same id, new board).
    Returns: reset game state or error message.
    """
    try:
        game_id_int = int(game_id)
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid game_id provided (must be int).", "game_id": game_id},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        game = TicTacToeGame.objects.get(id=game_id_int)
    except TicTacToeGame.DoesNotExist:
        return Response(
            {"error": "Game not found.", "game_id": game_id},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Unexpected error: {str(e)}", "game_id": game_id},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    try:
        game.reset()
        game.save()
        return Response(game.get_state())
    except Exception as e:
        return Response(
            {"error": f"Could not restart game: {str(e)}", "game_id": game_id},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
