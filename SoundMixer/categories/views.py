from django.shortcuts import render

from .models import Category, Song

def taglist(request):
    tag_list = Category.objects.all()
    context = {
        'tag_list': tag_list,
    }
    return render(request, 'categories/tags.html', context)

def songlist(request, tag_id):
    tag = Category.objects.get(id=tag_id)
    songquerry = Song.objects.filter(tags=tag)
    context = {
        'song_list': songquerry,
    }
    return render(request, 'categories/list.html', context)

def song(request, song_id):
    song = Song.objects.get(id=song_id)
    context = {
        'song': song,
    }
    return render(request, 'categories/song.html', context)
