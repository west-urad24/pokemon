# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .util import sort_data,base_check,item_check
from .models import Pokemon,Item
import locale

context_base = []
context_detail = []
context_item = []
context_generation = []

#ソートするときに値を保存するためにグローバル変数
base_name = ""
detail_name = ""
item_name = ""
generation_name = ""


def index(request):
    global context_detail
    global context_base
    global context_item
    global context_generation

    context_detail,context_item,context_base,context_generation = [],[],[],[]
    return render(request, 'main/index.html')

def base_view(request):  # 名前、図鑑番号、タイプ、特性、進化レベル表示
    global context_base  # リスト形式に変更
    global context_detail
    global context_item
    global context_generation
    global base_name

    context_detail,context_item,context_generation = [],[],[]
    if 'base' in request.GET:
        base_name = request.GET.get('base', '')  # ポケモン名
        pokemons = Pokemon.objects.filter(name__icontains=base_name)
        context_base = []
        for pokemon in pokemons:  # ファイル1つずつチェック
            if "-" not in pokemon.name:
                #ifの入れ子を避けるために関数を使った
                context_base = base_check(pokemon,context_base)
        
        if len(context_base) == 0:
            return render(request, 'main/base.html', {'data_len': 'no_data','word':base_name})  # 辞書として渡す

    if "sort_base" in request.GET and "ascdesc_base" in request.GET:
        context_base = sort_data(context_base,"base",request)
    
    return render(request, 'main/base.html', {'context_base': context_base,'data_len':len(context_base),'word':base_name})  # 辞書として渡す
    
def detail_view(request):#名前、図鑑番号、タイプ、覚える技、わざマシン、たまご
    global context_detail  # リスト形式に変更
    global context_base
    global context_item
    global context_generation
    global detail_name

    context_base,context_item,context_generation = [],[],[]
    # 初期化
    if 'detail' in request.GET:
        detail_name = request.GET.get('detail', '')  # ポケモン名
        pokemons = Pokemon.objects.filter(name__icontains=detail_name)
        context_detail = []
        for pokemon in pokemons:#データを一つずつチェック
            if "-" not in pokemon.name:#ポケモンの名前が一致
                no = pokemon.no#図鑑番号
                lv_up =  pokemon.level_up_moves#レベルアップで覚えるわざ
                tms = pokemon.tms#tms=わざマシン
                trs = pokemon.trs#trs=わざレコード
                egg_moves = pokemon.egg_moves#egg_moves＝たまごわざ

                context_detail.append({
                    'detail_name': pokemon.name,
                    'no': no,
                    'lv_up': lv_up,
                    'tms': tms,
                    'trs': trs,
                    'egg_moves': egg_moves,
                })

        if len(context_detail) == 0:
            return render(request, 'main/detail.html', {'data_len': 'no_data','word':detail_name})

    if "sort_detail" in request.GET and "ascdesc_detail" in request.GET:
        context_detail = sort_data(context_detail,"detail",request)

    return render(request, 'main/detail.html', {'context_detail': context_detail,'data_len':len(context_detail),'word':detail_name})

def generation_view(request):
    global context_detail
    global context_base
    global context_item
    global context_generation
    global generation_name

    context_detail,context_item,context_base =[],[],[]
    
    #1~151=1,152~251=2,252~386=3,387~493=4,494~649=5,650~721=6,722~809=7
    if "generation_1_7" in request.GET and "type" in request.GET and "type2" in request.GET:
        context_generation = []
        generation = int(request.GET.get("generation_1_7",1))
        generation_name = request.GET.get("type","ノーマル") + " " + request.GET.get("type2","指定なし")
        pokemon_type = [request.GET.get("type","ノーマル")]
        pokemon_type2 = [request.GET.get("type2","指定なし")]
        
        if "指定なし" not in pokemon_type2:
            pokemon_type.extend(pokemon_type2)
            #ユーザが選択したタイプを五十音順に並べる。同じタイプはsetで1つにする
        
        generation_dic = {1:[1,151],2:[152,251],3:[252,386],4:[387,493],5:[494,649],6:[650,721],7:[722,809],8:[1,809]}
        min_no,max_no = generation_dic[generation]
        no_match_pokemons = Pokemon.objects.filter(no__range=(min_no,max_no))

        for pokemon in no_match_pokemons:
            if ("-" not in pokemon.name) and (pokemon_type[0] in pokemon.types) and (pokemon_type[-1] in pokemon.types):
                context_generation.append({
                    'generation_name': pokemon.name,
                    'no': pokemon.no,
                    'ability': set(pokemon.abilities),
                    'types': pokemon.types,
                })
        if len(context_generation) == 0:
            return render(request, 'main/generation.html', {'data_len': 'no_data','word':generation_name})
    
    if "sort_generation" in request.GET and "ascdesc_generation" in request.GET:
        context_generation = sort_data(context_generation,"generation",request)

    return render(request, 'main/generation.html', {'context_generation': context_generation,'data_len':len(context_generation),'word':generation_name})

def item_view(request):
    #アイテム入力→英語に変換→アイテム説明、画像、名称表示
    global context_item  # リスト形式に変更
    global context_base
    global context_detail
    global context_generation
    global item_name
    
    context_base,context_detail,context_generation = [],[],[]
    if 'item' in request.GET:
        context_item = []
        item_name = request.GET.get('item', '')
        if item_name:
            #ifの入れ子を避けるために関数を使った
            items = Item.objects.filter(ja_item__icontains=item_name)
            context_item = item_check(items,context_item,item_name)

        if len(context_item) == 0:
            return render(request, 'main/item.html', {'data_len': 'no_data','word':item_name})

    if "sort_item" in request.GET and "ascdesc_item" in request.GET:
        context_item = sort_data(context_item,"item",request)

    return render(request, 'main/item.html', {'context_item': context_item,'data_len':len(context_item),'word':item_name}) 