import requests
from django.http import HttpResponse

def sort_data(data,name,request):
    sort_key = request.GET.get(f"sort_{name}", "no")
    sort_order = request.GET.get(f"ascdesc_{name}", "asc")
    
    reverse = True if sort_order == "desc" else False
    #floatでソート
    if sort_key == "height" or sort_key == "weight":
        data = sorted(data,key=lambda x: float(x[sort_key].replace("kg","").replace("m","")),reverse=reverse)
    #数値、ひらがな、カタカナでソート
    else:
        data = sorted(data,key=lambda x: x[sort_key],reverse=reverse)
     
    return data

def base_check(pokemon,context_base):
    evolutions = pokemon.evolutions
    if evolutions:
        evolution = evolutions[0]  # 最初の進化情報を取得
        if evolution["method"] == "LevelUp":
            num = int(evolution["method_value"])
            message = f"Lv{num}で進化"
        elif evolution["method"] == "Trade":
            message = "通信交換で進化"
        elif evolution["method"] == "UseItem":
            message = "アイテムで進化"
        elif evolution["method"] == "LevelUpFriendshipMorning":
            message = "懐いた状態で朝、昼、夜にレベルアップ"
        elif evolution["method"] == "LevelUpFriendshipNight":
            message = "懐いた状態で夜にレベルアップ"
        elif evolution["method"] == "LevelUpFriendship":
            message = "懐いた状態でレベルアップ"
        else:
            message = "-"
    else:  # 進化しないとき
        message = "-"

    # ポケモンの情報をリストに追加
    context_base.append({
        'base_name': pokemon.name,
        'no': pokemon.no,
        'ability': set(pokemon.abilities),
        'types': pokemon.types,
        'height': f"{pokemon.height}m",
        'weight': f"{pokemon.weight}kg",
        'message': message
    })
    return context_base

def item_check(items,context_item,item_name):
    for item in items:
        if item_name in item.ja_item:
            ja_item = item.ja_item
            eng_item = item.en_item.replace(' ','-').lower()
            item_api_url = f'https://pokeapi.co/api/v2/item/{eng_item}'
            response = requests.get(item_api_url)
            
            if response.status_code == 200:
                url2json_data = response.json()
                item_id = url2json_data["id"]
                text = url2json_data["flavor_text_entries"][-2]["text"].replace("　","")

                context_item.append({
                    'ja_item': ja_item,
                    'eng_item':eng_item,
                    "item_id":item_id,
                    "text":text
                })
        else:
            context_item = []

    return context_item