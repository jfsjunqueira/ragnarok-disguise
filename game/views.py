from django.shortcuts import render, redirect

from .models import LeaderboardEntry
from .forms import GameChoiceForm, MonsterGuessForm, LeaderboardEntryForm, PlayerNameForm
from pathlib import Path
from datetime import timedelta
from datetime import datetime
from unidecode import unidecode
import Levenshtein

from django.shortcuts import render
from .utils import PokemonMonster, RagnarokMonster
import random

ID_LISTS_PATH = Path(__file__).parent.joinpath('id_lists/')

POSSIBLE_GAMES = {
    "ragnarok_monsters" : ID_LISTS_PATH.joinpath('ragnarok/ragnarok_monsters.csv').read_text().split('\n'),
    "pokemon_monsters": ID_LISTS_PATH.joinpath('pokemon/pokemon_monsters.csv').read_text().split('\n'),
}



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
            if Levenshtein.distance(unidecode(request.session['correct_monster_name'].lower()), unidecode(guess.lower())) <= 1:
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
            return redirect('game:game_over')
        
    game_choice = request.session.get('game_choice', 'ragnarok')  # Get the selected game from the session
    
    if game_choice == 'ragnarok':
        id_list_key = 'ragnarok_monsters'
        fetch_class = RagnarokMonster
    elif game_choice == 'pokemon':
        id_list_key = 'pokemon_monsters'
        fetch_class = PokemonMonster
    else:
        id_list_key = 'ragnarok_monsters'
        fetch_class = RagnarokMonster

    # Select a random monster ID from the POSSIBLE_MONSTERS list
    id_monster = random.choice(POSSIBLE_GAMES[id_list_key])
    monster = fetch_class(id_monster).to_dict()

    request.session['correct_monster_name'] = monster['name']
    request.session.modified = True
    print("Monster ID:", id_monster)
    print("Monster name:", monster['name'])
    context = {
        'monster_sprite': monster['sprite'],
        'monster_id': id_monster, 
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
        game_choice_form = GameChoiceForm(request.POST)
        if form.is_valid() and game_choice_form.is_valid():
            request.session['player_name'] = form.cleaned_data['player_name']
            request.session['game_choice'] = game_choice_form.cleaned_data['game']
            request.session['lifes'] = 3  # Reset lifes
            request.session['score'] = 0  # Reset score
            return redirect('game:game')
    else:
        form = PlayerNameForm()
        game_choice_form = GameChoiceForm()

    context = {
        'form': form,
        'game_choice_form': game_choice_form,
        'choice_images': game_choice_form.choice_images,
        'overall_leaderboard': overall_leaderboard,
        'monthly_leaderboard': monthly_leaderboard,
        'weekly_leaderboard': weekly_leaderboard,
    }

    return render(request, 'game/start.html', context)


def game_over(request):
    if request.session.get('player_name') and request.session.get('score') is not None:
        overall_leaderboard = LeaderboardEntry.objects.all()[:10]
        monthly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=30))[:10]
        weekly_leaderboard = LeaderboardEntry.objects.filter(timestamp__gte=datetime.now() - timedelta(days=7))[:10]

        context = {
            'score': request.session['score'],  # Add the player's score to the context
            'overall_leaderboard': overall_leaderboard,
            'monthly_leaderboard': monthly_leaderboard,
            'weekly_leaderboard': weekly_leaderboard,
        }

        # Clear the score and player_name from the session to avoid duplicate entries
        del request.session['score']
        del request.session['player_name']
        request.session.modified = True

        return render(request, 'game/game_over.html', context)

    return redirect('game:start')


def leaderboard(request):
    entries = LeaderboardEntry.objects.all()
    context = {'entries': entries}
    return render(request, 'game/leaderboard.html', context)
