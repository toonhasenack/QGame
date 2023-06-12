from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlayerForm
from .models import Player
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def main_page(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            player = Player.objects.create(name=name)
            return redirect(f'game/' + str(player.id))
    else:
        form = PlayerForm()
    return render(request, 'index.html', {'form': form})


def game_page(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    # Logic for starting the game against another player
    return render(request, 'game.html', {'player': player})
