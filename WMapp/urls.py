from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.main, name='main'),
    path('filter/', views.filter_on, name='filter_on'),
    path('map_searched/', views.search, name='search'),   # 검색경로
    path('map_filtered/', views.filter, name='filter'),   # 필터경로
    path('listup', views.listup, name='listup'),
]