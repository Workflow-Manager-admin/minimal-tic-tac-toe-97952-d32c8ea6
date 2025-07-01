from django.urls import path
from .views import health, start_game, make_move, get_state, restart_game

urlpatterns = [
    path('health/', health, name='Health'),
    path('tic-tac-toe/start/', start_game, name='start_game'),
    path('tic-tac-toe/<int:game_id>/move/', make_move, name='make_move'),
    path('tic-tac-toe/<int:game_id>/state/', get_state, name='get_state'),
    path('tic-tac-toe/<int:game_id>/restart/', restart_game, name='restart_game'),
]
