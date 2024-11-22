# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .util import sort_data
from .models import Pokemon,Item

context_base = []
context_detail = []
context_item = []

def index(request):
    global context_detail
    global context_base
    global context_item
    context_detail,context_item,context_base = [],[],[]
    return render(request, 'main/index.html')

def base_view(request):  # 名前、図鑑番号、タイプ、特性、進化レベル表示
    global context_base  # リスト形式に変更
    global context_detail
    global context_item

    context_detail,context_item = [],[]
    if 'base' in request.GET:
        query = request.GET.get('base', '')  # ポケモン名
        pokemons = Pokemon.objects.filter(name__icontains=query)
        context_base = []
        for pokemon in pokemons:  # ファイル1つずつチェック
            if "-" not in pokemon.name:
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
                    'query': pokemon.name,
                    'no': pokemon.no,
                    'ability': set(pokemon.abilities),
                    'types': pokemon.types,
                    'height': f"{pokemon.height}m",
                    'weight': f"{pokemon.weight}kg",
                    'message': message
                })
    
    if "sort_base" in request.GET and "ascdesc_base" in request.GET:
        context_base = sort_data(context_base,"base",request)

    return render(request, 'main/base.html', {'context_base': context_base,'data_len':len(context_base)})  # 辞書として渡す
    

def detail_view(request):#名前、図鑑番号、タイプ、覚える技、わざマシン、たまご
    global context_detail  # リスト形式に変更
    global context_base
    global context_item
    
    context_base,context_item = [],[]
    # 初期化
    if 'detail' in request.GET:
        query = request.GET.get('detail', '')  # ポケモン名
        pokemons = Pokemon.objects.filter(name__icontains=query)
        context_detail = []
        for pokemon in pokemons:#データを一つずつチェック
            if "-" not in pokemon.name:#ポケモンの名前が一致
                no = pokemon.no#図鑑番号
                lv_up =  pokemon.level_up_moves#レベルアップで覚えるわざ
                tms = pokemon.tms#tms=わざマシン
                trs = pokemon.trs#trs=わざレコード
                egg_moves = pokemon.egg_moves#egg_moves＝たまごわざ

                context_detail.append({
                    'query': pokemon.name,
                    'no': no,
                    'lv_up': lv_up,
                    'tms': tms,
                    'trs': trs,
                    'egg_moves': egg_moves,
                })
    if "sort_detail" in request.GET and "ascdesc_detail" in request.GET:
        context_detail = sort_data(context_detail,"detail",request)

    return render(request, 'main/detail.html', {'context_detail': context_detail,'data_len':len(context_detail)})

def item_view(request):
    #アイテム入力→英語に変換→アイテム説明、画像、名称表示
    global context_item  # リスト形式に変更
    global context_base
    global context_detail
    
    context_base,context_detail = [],[]
    if 'item' in request.GET:
        context_item = []
        query = request.GET.get('item', '')
        if query:
            items = Item.objects.filter(ja_item__icontains=query)
            for item in items:
                if query in item.ja_item:
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
    if "sort_item" in request.GET and "ascdesc_item" in request.GET:
        context_item = sort_data(context_item,"item",request)

    return render(request, 'main/item.html', {'context_item': context_item,'data_len':len(context_item)}) 