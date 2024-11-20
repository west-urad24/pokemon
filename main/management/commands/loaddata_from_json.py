import json
import glob
from django.core.management.base import BaseCommand
from ...models import Pokemon, Item

class Command(BaseCommand):
    help = 'Load JSON data into database'

    def handle(self, *args, **kwargs):
        # Pokemonデータの読み込み
        all_json_files = r"/Users/nishiuradaisuke/Desktop/myprj/main/static/json/gen*.json"
        json_files = glob.glob(all_json_files)

        for json_file in json_files:
            with open(json_file, 'r', encoding="utf-8") as file:
                data = json.load(file)
                for pokemon in data:
                    Pokemon.objects.get_or_create(
                        name=pokemon["name"],
                        no=pokemon["no"],
                        abilities=pokemon["abilities"],
                        types=pokemon["types"],
                        height=pokemon["height"],
                        weight=pokemon["weight"],
                        evolutions=pokemon.get("evolutions", []),
                        level_up_moves=pokemon.get("level_up_moves", []),
                        tms=pokemon.get("tms", []),
                        trs=pokemon.get("trs", []),
                        egg_moves=pokemon.get("egg_moves", [])
                    )
        
        # Itemデータの読み込み
        item_json = r'/Users/nishiuradaisuke/Desktop/myprj/main/static/json/item.json'
        with open(item_json, 'r', encoding="utf-8") as i_file:
            item_data = json.load(i_file)
            for data in item_data:
                Item.objects.get_or_create(
                    ja_item=data['ja'],
                    en_item=data['en'],
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from JSON into the database'))
