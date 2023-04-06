from django import forms
from .models import Monster, LeaderboardEntry

class MonsterGuessForm(forms.Form):
    guess = forms.CharField(label="Your guess", max_length=255)

class LeaderboardEntryForm(forms.ModelForm):
    class Meta:
        model = LeaderboardEntry
        fields = ['player_name']
        
class PlayerNameForm(forms.Form):
    player_name = forms.CharField(label='Your Name', max_length=100)