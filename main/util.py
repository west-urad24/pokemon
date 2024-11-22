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