from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('base/', views.base_view, name='base'),
  path('detail/', views.detail_view, name='detail'),
  path('item/', views.item_view, name='item'),
]