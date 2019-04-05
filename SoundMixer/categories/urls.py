from django.urls import path

from . import views

app_name = 'categories'
urlpatterns = [
    path('', views.taglist, name='tag_list'),
    path('tag/<str:tag_name>', views.gettagsongs, name="get_tag_songs"),
    path('song/<int:song_id>', views.song, name="song"),
    path('submit/', views.submitsong, name="submit_song"),
    path('search/', views.search, name="search"),
]
