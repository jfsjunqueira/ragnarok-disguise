import requests
from bs4 import BeautifulSoup

def fetch_monster(id_monster):
    url = f"http://www3.worldrag.com/database/?act=mobsearch&cid=on&id={id_monster}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        monster_name_element = soup.find('td', text=lambda x: x and f'({id_monster})' in x)
        
        if monster_name_element:
            monster_name = monster_name_element.text.split(' (')[0]  # Remove the ID from the monster name
        else:
            monster_name = f"Monster {id_monster}"
        
        monster_img_element = soup.find('img', {'src': True, 'alt': True})
        if monster_img_element:
            monster_img_url = f"http://www3.worldrag.com/database/{monster_img_element['src']}"
        else:
            monster_img_url = None
        
        return {
            'id': id_monster,
            'name': monster_name,
            'sprite': monster_img_url,
        }
    else:
        return None
