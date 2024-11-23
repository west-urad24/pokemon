# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .util import sort_data,base_check,item_check
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
                #ifの入れ子を避けるために関数を使った
                context_base = base_check(pokemon,context_base)
        
        if len(context_base) == 0:
            return render(request, 'main/base.html', {'data_len': 'no_data'})  # 辞書として渡す

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

        if len(context_detail) == 0:
            return render(request, 'main/detail.html', {'data_len': 'no_data'})

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
            #ifの入れ子を避けるために関数を使った
            items = Item.objects.filter(ja_item__icontains=query)
            context_item = item_check(items,context_item,query)

        if len(context_item) == 0:
            return render(request, 'main/item.html', {'data_len': 'no_data'})

    if "sort_item" in request.GET and "ascdesc_item" in request.GET:
        context_item = sort_data(context_item,"item",request)

    return render(request, 'main/item.html', {'context_item': context_item,'data_len':len(context_item)}) 