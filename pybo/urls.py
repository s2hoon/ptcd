from django.urls import path
from . import now_views
from . import views


app_name = 'pybo'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('kakaomap/', views.kakaomap, name='kakaomap'),
    path('hs/',views.hs, name='hs'),
    path('hs2/', views.hs2, name='hs2'),
    path('weather/', now_views.weather , name='weather'),
    path('sj/',views.sj , name='sj'),
    path('sj2/',views.sj2, name ='sj2'),
    path('pj/',views.pj ,name ='pj')
]