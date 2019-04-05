from django.urls import path

from . import views

app_name = 'categories'
urlpatterns = [
    path('', views.taglist, name='tag_list'),
    path('tag/<int:tag_id>', views.songlist, name="songlist"),
    path('song/<int:song_id>', views.song, name="song"),
    #path('f/<str:tag_name>', views.FractionSortNew, name='fraction_sort_new')
]
