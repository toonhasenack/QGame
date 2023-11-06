from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlayerForm
from .models import Player
import numpy as np
import pickle
import base64
from QLib import *
from LLib import *

# Create your views here.


def main_page(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            name1 = form.cleaned_data['name1']
            name2 = form.cleaned_data['name2']
            player = Player.objects.create(name1=name1, name2=name2)
            player.new_id = player.id
            player.save()
            return redirect('game/' + str(player.id))
    else:
        form = PlayerForm()
    return render(request, 'index.html', {'form': form})


def set_QG(player, QG):
    player.grid1 = base64.b64encode(pickle.dumps(QG.grids[0]))
    player.grid2 = base64.b64encode(pickle.dumps(QG.grids[1]))
    player.player = QG.player
    player.steps = QG.steps
    player.winner = QG.winner


def get_QG(player):
    QG = QGame()
    QG.steps = player.steps
    if QG.steps > 0:
        QG.grids[0] = pickle.loads(base64.b64decode(player.grid1))
        QG.grids[1] = pickle.loads(base64.b64decode(player.grid2))
        QG.player = player.player
    return QG


def game_page(request, player_id):
    measure = False

    player = get_object_or_404(Player, pk=player_id)
    names = [player.name1, player.name2]
    strings = [r"$|\uparrow\rangle$", r"$|\downarrow\rangle$"]
    QG = get_QG(player)
    if QG.steps == 0:
        player.message = f"It is the turn of <span class = 'p{player.player}'>{names[player.player]}</span> {strings[player.player]} to entangle two states."

    a = {'11': r"$|\psi_{11}\rangle$", '12': r"$|\psi_{12}\rangle$", '13': r"$|\psi_{13}\rangle$",
         '21': r"$|\psi_{21}\rangle$", '22': r"$|\psi_{22}\rangle$", '23': r"$|\psi_{23}\rangle$",
         '31': r"$|\psi_{31}\rangle$", '32': r"$|\psi_{32}\rangle$", '33': r"$|\psi_{33}\rangle$"}

    b = {'11': r"$|\varphi_{11}\rangle$", '12': r"$|\varphi_{12}\rangle$", '13': r"$|\varphi_{13}\rangle$",
         '21': r"$|\varphi_{21}\rangle$", '22': r"$|\varphi_{22}\rangle$", '23': r"$|\varphi_{23}\rangle$",
         '31': r"$|\varphi_{31}\rangle$", '32': r"$|\varphi_{32}\rangle$", '33': r"$|\varphi_{33}\rangle$"}

    c = {'11': 'button0', '12': 'button0', '13': 'button0',
         '21': 'button0', '22': 'button0', '23': 'button0',
         '31': 'button0', '32': 'button0', '33': 'button0'}

    d = {'11': 'button0', '12': 'button0', '13': 'button0',
         '21': 'button0', '22': 'button0', '23': 'button0',
         '31': 'button0', '32': 'button0', '33': 'button0'}

    game_class = "game_not_won"

    QG.check()
    if request.method == 'POST' and not QG.winner:
        keys = request.POST.keys()
        idf = [key for key in keys][1]

        if player.left and player.right and idf == "measure":
            measure = True

        elif idf[3] == "1":
            player.left = True
            player.left_choice = base64.b64encode(
                pickle.dumps([int(idf[4])-1, int(idf[5])-1]))
            player.save()

        elif idf[3] == "2":
            player.right = True
            player.right_choice = base64.b64encode(
                pickle.dumps([int(idf[4])-1, int(idf[5])-1]))
            player.save()

        if player.left and player.right:
            if measure:
                left_choice = pickle.loads(
                    base64.b64decode(player.left_choice))
                right_choice = pickle.loads(
                    base64.b64decode(player.right_choice))
                coords = np.vstack([left_choice, right_choice])
                proceed = QG.step(coords)
                if proceed:
                    QG.check()
                    set_QG(player, QG)
                    if QG.winner:
                        if QG.winner == 1 or QG.winner == 2:
                            player.message = f"The winner is <span class = 'p{QG.winner-1}'>{names[QG.winner-1]}</span> {strings[QG.winner - 1]}!"
                        else:
                            player.message = f"It is a tie!"

                        game_class = "game_won"
                        new_player = Player.objects.create(
                            name1=player.name1, name2=player.name2)
                        player.new_id = new_player.pk

                    else:
                        player.message = f"It is the turn of <span class = 'p{player.player}'>{names[player.player]}</span> {strings[player.player]} to entangle two states."

                else:
                    player.message = f"Please choose two valid options, <span class = 'p{player.player}'>{names[player.player]}</span>."

                player.left = False
                player.right = False
                measure = False
            else:
                player.message = f"Happy? Please press the MEASURE button, <span class = 'p{player.player}'>{names[player.player]}</span>."

        else:
            if player.left:
                side = "right"
                player.message = f"Please make your second choice on the {side} playing field, <span class = 'p{player.player}'>{names[player.player]}</span>."
            elif player.right:
                side = "left"
                player.message = f"Please make your second choice on the {side} playing field, <span class = 'p{player.player}'>{names[player.player]}</span>."

        player.save()

    for i in range(3):
        for j in range(3):
            l_state = QG.grids[0][i, j]
            r_state = QG.grids[1][i, j]
            if l_state == 1:
                a[str(i + 1) + str(j + 1)] = r"$|\uparrow\rangle$"
                c[str(i + 1) + str(j + 1)] = "button1"
            elif l_state == -1:
                a[str(i + 1) + str(j + 1)] = r"$|\downarrow\rangle$"
                c[str(i + 1) + str(j + 1)] = "button2"
            if r_state == 1:
                b[str(i + 1) + str(j + 1)] = r"$|\uparrow\rangle$"
                d[str(i + 1) + str(j + 1)] = "button1"
            elif r_state == -1:
                b[str(i + 1) + str(j + 1)] = r"$|\downarrow\rangle$"
                d[str(i + 1) + str(j + 1)] = "button2"

    if player.left:
        left_choice = pickle.loads(base64.b64decode(player.left_choice))
        c[str(left_choice[0]+1) +
          str(left_choice[1]+1)] = "button3"

    if player.right:
        right_choice = pickle.loads(base64.b64decode(player.right_choice))
        d[str(right_choice[0]+1) +
          str(right_choice[1]+1)] = "button4"

    elif QG.winner:
        game_class = "game_won"

    return render(request, 'game.html', {'message': player.message, 'a': a, 'b': b, 'c': c, 'd': d, "game_class": game_class, "play_again_id": player.new_id})


def leaderboard_page(request):
    try:
        L = Leaderboard()
        L.update()
        return render(request, 'leaderboard.html')
    except:
        return render(request, 'leaderboard.html')
