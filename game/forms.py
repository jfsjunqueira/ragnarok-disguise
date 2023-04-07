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
    
    
class GameChoiceForm(forms.Form):
    GAME_CHOICES = [
        ('ragnarok_monsters', 'Ragnarok Online Monsters', 'https://playragnarokonlinebr.com/img/logo.png'),
        ('pokemon', 'Pokemon', 'https://logospng.org/download/pokemon/pokemon-4096.png'),
    ]

    game = forms.ChoiceField(choices=[(game[0], game[1]) for game in GAME_CHOICES], widget=forms.RadioSelect, initial='ragnarok_monsters')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.games = [
        ('ragnarok_monsters', 'Ragnarok Online', 'https://c-cl.cdn.smule.com/rs-s27/arr/10/5a/4740a56f-e57d-4922-8217-07e0c575377c.jpg'),
        ('pokemon', 'Pokemon', 'https://logospng.org/download/pokemon/pokemon-256.png'),
    ]
        self.fields['game'].choices = [(game[0], game[1]) for game in self.GAME_CHOICES]
        print(self.fields['game'].choices)
        for game in self.fields['game'].choices:
            print(game)

        self.choice_images = {}
        for game in self.fields['game'].choices:
            self.choice_images[game[0]] = self.get_image_url(game[0])
    @staticmethod
    def get_image_url(game_id):
        for game in GameChoiceForm.GAME_CHOICES:
            if game[0] == game_id:
                return game[2]
        return None