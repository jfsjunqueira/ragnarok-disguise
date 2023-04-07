import requests
from bs4 import BeautifulSoup

# Create separate classes for fetching monster data from different franchises


class RagnarokMonster:
    def __init__(self, id_monster:int):
        self.id_monster = id_monster
        self.url = f"http://www3.worldrag.com/database/?act=mobsearch&cid=on&id={id_monster}"
        self.soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.monster_name = self.fetch_ragnarok_monster_name()
        self.sprite_url = self.fetch_ragnarok_monster_sprite_url()

    def fetch_ragnarok_monster_name(self):
        monster_name_element = self.soup.find('td', text=lambda x: x and f'({self.id_monster})' in x) # type: ignore
        if monster_name_element:
            monster_name = monster_name_element.text.split(' (')[0]  # Remove the ID from the monster name
        else:
            monster_name = f"Monster {self.id_monster}"
        return monster_name
    
    def fetch_ragnarok_monster_sprite_url(self):
        return f"https://static.ragnaplace.com/db/npc/gif/{self.id_monster}.gif"
    
    def to_dict(self):
        return {
            'id': self.id_monster,
            'name': self.monster_name,
            'sprite': self.sprite_url,
        }


class PokemonMonster:
    def __init__(self, id_monster:int):
        self.id_monster = id_monster
        self.url = f"https://pokemondb.net/pokedex/{id_monster}"
        self.soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.monster_name = self.fetch_ragnarok_monster_name()
        self.sprite_url = self.fetch_ragnarok_monster_sprite_url()

    def fetch_ragnarok_monster_name(self):
        monster_name_element = self.soup.find('h1') # type: ignore
        if monster_name_element:
            monster_name = monster_name_element.text  # Remove the ID from the monster name
        else:
            monster_name = f"Pokemon {self.id_monster}"
        return monster_name
    
    def fetch_ragnarok_monster_sprite_url(self):
        return f"https://img.pokemondb.net/artwork/{self.monster_name.lower()}.jpg"
    
    def to_dict(self):
        return {
            'id': self.id_monster,
            'name': self.monster_name,
            'sprite': self.sprite_url,
        }
