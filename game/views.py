from django.shortcuts import render, redirect

from .models import LeaderboardEntry
from .forms import MonsterGuessForm, LeaderboardEntryForm, PlayerNameForm
from pathlib import Path
from datetime import timedelta
from datetime import datetime
from unidecode import unidecode

from django.shortcuts import render
from django.http import JsonResponse
from .utils import fetch_monster
import random

POSSIBLE_MONSTERS = Path(__file__).parent.joinpath('ids.csv').read_text().split('\n')



def game(request):
    form = MonsterGuessForm()
    scored = False
    
    if request.method == 'POST':
        form = MonsterGuessForm(request.POST)
        if 'restart' in request.POST:
            request.session['score'] = 0
            request.session['lifes'] = 3
        else:
            guess = request.POST.get('guess', '').lower()
            if unidecode(request.session['correct_monster_name'].lower()) == unidecode(guess):
                request.session['score'] = request.session.get('score', 0) + 1
                scored = True
            else:
                request.session['lifes'] = request.session.get('lifes', 3) - 1
            request.session.modified = True
            
        if request.session['score'] % 5 == 0 and request.session['score'] != 0:
            request.session['lifes'] = request.session.get('lifes', 3) + 1
            

        if request.session['lifes'] <= 0:
            player_name = request.session.get('player_name', 'Anonymous')
            score = request.session['score']

            # Save the player's score to the leaderboard.
            leaderboard_entry = LeaderboardEntry(player_name=player_name, score=score)
            leaderboard_entry.save()

            overall_leaderboard = LeaderboardEntry.objects.all()[:10]
            monthly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=30))[:10]
            weekly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=7))[:10]

            context = {
                'score': score,
                'overall_leaderboard': overall_leaderboard,
                'monthly_leaderboard': monthly_leaderboard,
                'weekly_leaderboard': weekly_leaderboard,
            }
            return render(request, 'game/game_over.html', context)

    # Select a random monster ID from the POSSIBLE_MONSTERS list
    id_monster = random.choice(POSSIBLE_MONSTERS)
    monster = fetch_monster(id_monster)

    request.session['correct_monster_name'] = monster['name']
    request.session.modified = True
    print("Monster ID:", id_monster)
    print("Monster name:", monster['name'])
    context = {
        'monster_sprite': monster['sprite'],
        'monster_id': id_monster, 
        # 'correct_monster_name': correct_monster_name,
        'score': request.session['score'],
        'lifes': request.session['lifes'],
        'form': form,  # Pass the form object to the context
        'scored': scored
    }
    
    return render(request, 'game/game.html', context)

def start(request):
    overall_leaderboard = LeaderboardEntry.objects.all()[:10]
    monthly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=30))[:10]
    weekly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=7))[:10]

    if request.method == 'POST':
        form = PlayerNameForm(request.POST)
        if form.is_valid():
            request.session['player_name'] = form.cleaned_data['player_name']
            request.session['lifes'] = 3  # Reset lifes
            request.session['score'] = 0  # Reset score
            return redirect('game:game')
    else:
        form = PlayerNameForm()

    context = {
        'form': form,
        'overall_leaderboard': overall_leaderboard,
        'monthly_leaderboard': monthly_leaderboard,
        'weekly_leaderboard': weekly_leaderboard,
    }

    return render(request, 'game/start.html', context)


def game_over(request):
    if request.session.get('player_name') and request.session.get('score') is not None:
        entry = LeaderboardEntry(player_name=request.session['player_name'], score=request.session['score'])
        entry.save()
        
        overall_leaderboard = LeaderboardEntry.objects.all()[:10]
        monthly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=30))[:10]
        weekly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=7))[:10]

        context = {
            'overall_leaderboard': overall_leaderboard,
            'monthly_leaderboard': monthly_leaderboard,
            'weekly_leaderboard': weekly_leaderboard,
        }

        return render(request, 'game/game_over.html', context)

    return redirect('game:start')

def leaderboard(request):
    entries = LeaderboardEntry.objects.all()
    context = {'entries': entries}
    return render(request, 'game/leaderboard.html', context)
