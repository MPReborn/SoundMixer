from django.urls import path

from . import views

app_name = 'categories'
urlpatterns = [
    path('', views.taglist, name='tag_list'),
    path('tag/<str:tag_name>', views.gettagsongs, name="get_tag_songs"),
    path('song/<int:song_id>', views.song, name="song"),
    path('submit/song', views.submitsong, name="submit_song"),
    path('submit/tag', views.submittag, name="submit_tag"),
    path('search/', views.search, name="search"),
    path('signup/', views.signup.as_view(), name='signup'),
]
