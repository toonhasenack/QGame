from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def main_page(request):
    return render(request, "index.html")


@csrf_exempt
def game_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        print(name)
    if request.POST.get("btn11") == "btn11":
        print(11111)

    return render(request, "game.html")
