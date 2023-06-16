from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlayerForm
from .models import Player
import numpy as np
import pickle
import base64
from QLib import *

# Create your views here.


def main_page(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            name1 = form.cleaned_data['name1']
            name2 = form.cleaned_data['name2']
            player = Player.objects.create(name1=name1, name2=name2)
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
    player = get_object_or_404(Player, pk=player_id)
    names = [player.name1, player.name2]
    strings = [r"$|\uparrow\rangle$", r"$|\downarrow\rangle$"]
    QG = get_QG(player)
    if QG.steps == 0:
        player.message = f"It is the turn of {names[player.player]} {strings[player.player]} to entangle two states."

    a = {'11': r"$|\psi_{11}\rangle$", '12': r"$|\psi_{12}\rangle$", '13': r"$|\psi_{13}\rangle$",
         '21': r"$|\psi_{21}\rangle$", '22': r"$|\psi_{22}\rangle$", '23': r"$|\psi_{23}\rangle$",
         '31': r"$|\psi_{31}\rangle$", '32': r"$|\psi_{32}\rangle$", '33': r"$|\psi_{33}\rangle$"}

    b = {'11': r"$|\varphi_{11}\rangle$", '12': r"$|\varphi_{12}\rangle$", '13': r"$|\varphi_{13}\rangle$",
         '21': r"$|\varphi_{21}\rangle$", '22': r"$|\varphi_{22}\rangle$", '23': r"$|\varphi_{23}\rangle$",
         '31': r"$|\varphi_{31}\rangle$", '32': r"$|\varphi_{32}\rangle$", '33': r"$|\varphi_{33}\rangle$"}

    if request.method == 'POST' and not QG.winner:
        keys = request.POST.keys()
        idf = [key for key in keys][1]
        if int(idf[3]) == 1:
            player.left = True
            player.left_choice = base64.b64encode(
                pickle.dumps([int(idf[4])-1, int(idf[5])-1]))
            player.save()

        elif int(idf[3]) == 2:
            player.right = True
            player.right_choice = base64.b64encode(
                pickle.dumps([int(idf[4])-1, int(idf[5])-1]))
            player.save()

        if player.left and player.right:
            left_choice = pickle.loads(base64.b64decode(player.left_choice))
            right_choice = pickle.loads(base64.b64decode(player.right_choice))
            coords = np.vstack([left_choice, right_choice])
            proceed = QG.step(coords)
            if proceed:
                QG.check()
                set_QG(player, QG)
                if QG.winner:
                    if QG.winner == 1 or QG.winner == 2:
                        player.message = f"The winner is {names[QG.winner - 1]} {strings[QG.winner - 1]}!"
                    else:
                        player.message = f"It is a tie!"
                else:
                    player.message = f"It is turn of {names[player.player]} {strings[player.player]} to entangle two states."

            else:
                player.message = f"Please choose two valid options, {names[player.player]}."

            player.left = False
            player.right = False
            player.save()

        else:
            sides = ["right", "left"]
            player.message = f"Please make your second choice on the {sides[int(idf[3])-1]} playing field, {names[player.player]}"
            player.save()

    for i in range(3):
        for j in range(3):
            l_state = QG.grids[0][i, j]
            r_state = QG.grids[1][i, j]
            if l_state == 1:
                a[str(i + 1) + str(j + 1)] = r"$|\uparrow\rangle$"
            elif l_state == -1:
                a[str(i + 1) + str(j + 1)] = r"$|\downarrow\rangle$"
            if r_state == 1:
                b[str(i + 1) + str(j + 1)] = r"$|\uparrow\rangle$"
            elif r_state == -1:
                b[str(i + 1) + str(j + 1)] = r"$|\downarrow\rangle$"

    return render(request, 'game.html', {'message': player.message, 'a': a, 'b': b})


def winner_page(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    QG = get_QG(player)
    QG.check()

    return render(request, 'winner.html', {'winner': QG.winner})
