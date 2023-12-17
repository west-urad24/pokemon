# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import glob
import json
import requests


def index(request):
  return render(request, 'main/index.html')

def base_view(request):#名前、図鑑番号、タイプ、特性、進化レベル表示
    context = {'name': "",'no': "",'ability': "","types":""}
    # 初期化
    if 'base' in request.GET:
        query = request.GET.get('base', '')#ポケモン
        all_json_files = r"/Users/nishiuradaisuke/Desktop/myprj/main/static/json/*.json"
        json_files = glob.glob(all_json_files)
        for json_file in json_files:#ファイル1つずつチェック
            with open(json_file, 'r',encoding="utf-8") as file:
                data = json.load(file)
                for pokemon in data:#データを一つずつチェック
                    if query == pokemon["name"]:#ポケモンの名前が一致
                        no = pokemon["no"]#図鑑番号
                        ability = set(pokemon["abilities"])#特性
                        types = pokemon["types"]#タイプ
                        height = str(pokemon["height"])+"m"#身長
                        weight = str(pokemon["weight"])+"kg"#体重

                        evolutions = pokemon["evolutions"]
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
                        else:#進化しないとき
                            message = "-"

                        context = {'name': query, 'no': no, 'ability': ability, "types": types, "height": height,"weight": weight, "message": message}
                        return render(request, 'main/base.html', context)
    return render(request, 'main/base.html', context)
    

def detail_view(request):#名前、図鑑番号、タイプ、覚える技、わざマシン、たまご
    context = {'name': "",'no': "",'ability': "","types":""}
    # 初期化
    if 'detail' in request.GET:
        query = request.GET.get('detail', '')#ポケモン
        all_json_files = r"/Users/nishiuradaisuke/Desktop/myprj/main/static/json/*.json"
        json_files = glob.glob(all_json_files)
        for json_file in json_files:#ファイル1つずつチェック
            with open(json_file, 'r') as file:
                data = json.load(file)
                for pokemon in data:#データを一つずつチェック
                    if "name" in pokemon and query == pokemon["name"]:#ポケモンの名前が一致
                        name = pokemon["name"]
                        no = pokemon["no"]#図鑑番号
                        lv_up =  pokemon["level_up_moves"]#レベルアップで覚えるわざ
                        tms = pokemon["tms"]#tms=わざマシン
                        trs = pokemon["trs"]#trs=わざレコード
                        egg_moves = pokemon["egg_moves"]#egg_moves＝たまごわざ

                        context = {'name': name, 'no': no, 'lv_up': lv_up, "tms": tms, "trs": trs,"egg_moves": egg_moves}
                        return render(request, 'main/detail.html', context)
    return render(request, 'main/detail.html', context)
    


def item_view(request):
    #アイテム入力→英語に変換→アイテム説明、画像、名称表示
    context = {'ja_item': '','eng_item':'',"item_id":'',"text":''}
    if 'item' in request.GET:
        query = request.GET.get('item', '')
        item_json = r'/Users/nishiuradaisuke/Desktop/myprj/main/static/json/item.json'
        with open(item_json,'r',encoding="utf-8") as i_file:
            item_data = json.load(i_file)
        
         # 初期化
        ja_item = ''
        eng_item = ''
        item_id = ''
        text = ''
        
        for data in item_data:
            if 'ja' in data and data['ja'] == query:
                ja_item = data['ja']
                eng_item = data['en'].replace(' ','-').lower()
                item_api_url = f'https://pokeapi.co/api/v2/item/{eng_item}'
                response = requests.get(item_api_url)
                
                if response.status_code == 200:
                    url2json_data = response.json()
                    item_id = url2json_data["id"]
                    text = url2json_data["flavor_text_entries"][-2]["text"].replace("　","")

        context = {'ja_item': ja_item,'eng_item':eng_item,"item_id":item_id,"text":text}
    return render(request, 'main/item.html', context)
    